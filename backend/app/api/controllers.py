# Flask related methods...
from flask import Blueprint, request, render_template, \
    flash, g, session, redirect, url_for, jsonify, send_from_directory, after_this_request

# importing os module
import os

# Database
from app import db

# System libraries
from datetime import datetime
# Regular expressions libraries
import re

# Trace back libary
import traceback

# SQL Alchemy 
from sqlalchemy.orm import aliased

# Configuration
from app import config_ as config

# Security helpers
from app.utils.utils import is_valid_session, hash_password
from app.utils.utils import get_role
from app.utils.utils import has_permissions

# xls to HTML
from xlsx2html import xlsx2html

# Pandas
import pandas as pd

# Datetime utilities
from datetime import date

# Threading stuff
from time import sleep
import threading

# Logging 
import logging

# OS and representation stuff
import os
from binascii import hexlify

#logging.basicConfig()
#logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

# Database models
# Security
from app.auth.models import Polzovateli
from app.auth.models import Roli
from app.auth.models import Razresheniya

# Balnace models
from app.api.models import Oblasti
from app.api.models import SpravochnikiKategorii
from app.api.models import Spravochniki
from app.api.models import GruppaItogov
from app.api.models import GruppaItogovSopostavlenie
from app.api.models import TipMestorogdeniya
from app.api.models import Mestorogdeniya
from app.api.models import Koordinati
from app.api.models import JDStancii
from app.api.models import NaselenniePunkti
from app.api.models import Expedicii
from app.api.models import Resurs
from app.api.models import ResursInformaciya
from app.api.models import Litsenzii
from app.api.models import Forma5GR
from app.api.models import Forma5GR_Dvijene

# Kadastr models
from app.api.models import KadastrObshayaInformaciya
from app.api.models import KadastrTitul
from app.api.models import KadastrIzuchennost
from app.api.models import KadastrKoordinatu
from app.api.models import KadastrGeoHarakteristiki
from app.api.models import KadastrProsloiPustihPorod
from app.api.models import KadastrVmeshayushiePorodi
from app.api.models import KadastrKachestvennayaHarakteristika
from app.api.models import KadastrFizMehHarakteristika
from app.api.models import KadastrProdukciya
from app.api.models import KadastrGeolograzvedHarakteristika
from app.api.models import KadastrTipiRabot
from app.api.models import KadastrKondicii
from app.api.models import KadastrSvedeniyaOZapasah
from app.api.models import KadastrGornoGeologicheskayaHarakteristika
from app.api.models import KadastrGornotehResheniya
from app.api.models import KadastrOkrujSreda
from app.api.models import KadastrTehnoEkonomPokazateli
from app.api.models import KadastrDopolnitelnieSvedeniya
from app.api.models import KadastrIstochniki
from app.api.models import KadastrRazrez
from app.api.models import KadastrShema

# Temporary files
import tempfile

# Blueprint
mod_api = Blueprint("api", __name__, url_prefix="/api")

@mod_api.teardown_request
def teardown(error=None):
    try:
        
        print("Relasing locks...")
        result = db.session.execute("UNLOCK TABLES")
        print("...........UNLOCK STATUS............")
        #result = db.session.execute("SHOW OPEN TABLES")
        #print("...........SHOW OPEN TABLES............")
        #for r in result:
        #    print(r)
        #db.session.commit()
        db.session.close()

    except Exception as e:
        print(e)




@mod_api.route("/get_deposits/", methods=["POST"])
def get_deposits():
    if not is_valid_session(request, config):
        return jsonify({"auth_fail": True}, 403)
    if not has_permissions(db, get_role(request, config), "/api/get_deposits/"):
        return jsonify({"auth_fail": True, "access_denied": True, "reason": "Доступ запрещен"}, 403)
    data = request.get_json(force=True)
    if not data:
        return jsonify({"auth_fail": False, "result": False}, 400)
    deposit_name = "%" + data.get("deposit_name", "") + "%"
    offset = data.get("offset", 0)
    limit = data.get("limit", 10)
    deposits = db.session.query(Mestorogdeniya.id_mestorojdeniya, \
        Mestorogdeniya.id_uchastka, \
        Mestorogdeniya.id_oblast, \
        Mestorogdeniya.id_rayon, \
        Mestorogdeniya.id_osvoyeniya, \
        Mestorogdeniya.naimenovanie, \
        Mestorogdeniya.opisanie, \
        Mestorogdeniya.tip_id, \
        TipMestorogdeniya.opisanie.label("type")).\
            join(TipMestorogdeniya, Mestorogdeniya.tip_id == TipMestorogdeniya.tip_id).\
                filter(db.and_(Mestorogdeniya.id_mestorojdeniya == Mestorogdeniya.id_uchastka,
                    Mestorogdeniya.naimenovanie.ilike(deposit_name))). \
                        order_by(Mestorogdeniya.naimenovanie.desc()).\
                            offset(offset).limit(limit).\
                                all()
    result = []
    for item in deposits:
        
        result.append({
            "deposit_id": item.id_mestorojdeniya,
            "mine_area_id": item.id_uchastka,
            "area_id": item.id_oblast,
            "district_id": item.id_rayon,
            "dev_id": item.id_osvoyeniya,
            "deposit_name": item.naimenovanie,
            "description": item.opisanie,
            "type_id": item.tip_id,
            "type": item.type
        })
    return jsonify({
        "auth_fail": False,
        "result": result
    }, 200)

@mod_api.route("/get_deposits_and_mine_areas/", methods=["POST"])
def get_deposits_and_mine_areas():
    if not is_valid_session(request, config):
        return jsonify({"auth_fail": True}, 403)
    if not has_permissions(db, get_role(request, config), "/api/get_deposits_and_mine_areas/"):
        return jsonify({"auth_fail": True, "access_denied": True, "reason": "Доступ запрещен"}, 403)

    data = request.get_json(force=True)

    if not data:
        return jsonify({"auth_fail": False, "result": False}, 400)

    deposit_name = "%" + data.get("deposit_name", "") + "%"
    offset = data.get("offset", 0)
    limit = data.get("limit", 10)

    deposit = aliased(Mestorogdeniya)
    mine_area = aliased(Mestorogdeniya)
    
    deposits = db.session.query(deposit.naimenovanie.label("deposit_name"), \
        mine_area.naimenovanie.label("mine_area_name"), \
        mine_area.id_uchastka, \
        mine_area.id_mestorojdeniya, \
        mine_area.id_oblast, \
        mine_area.id_rayon, \
        mine_area.id_osvoyeniya).\
        join(mine_area, db.and_(deposit.id_mestorojdeniya == mine_area.id_mestorojdeniya, deposit.id_mestorojdeniya == deposit.id_uchastka)).\
            filter(db.or_(deposit.naimenovanie.ilike(deposit_name), mine_area.naimenovanie.ilike(deposit_name))). \
                    order_by(deposit.naimenovanie.desc()).\
                        offset(offset).limit(limit).\
                            all();

    result = []
    for item in deposits:
        result.append({
            "deposit_id": item.id_mestorojdeniya,
            "mine_area_id": item.id_uchastka,
            "area_id": item.id_oblast,
            "district_id": item.id_rayon,
            "dev_id": item.id_osvoyeniya,
            "deposit_name": item.deposit_name,
            "mine_area_name": item.mine_area_name
            })
    return jsonify({
        "auth_fail": False,
        "result": result
    }, 200)


@mod_api.route("/get_deposit/", methods=["POST"])
def get_deposit():
    if not is_valid_session(request, config):
        return jsonify({"auth_fail": True}, 403)
    if not has_permissions(db, get_role(request, config), "/api/get_deposit/"):
        return jsonify({"auth_fail": True, "access_denied": True, "reason": "Доступ запрещен"}, 403)
    data = request.get_json(force=True)
    if not data:
        return jsonify({"auth_fail": False, "result": False}, 400)
    deposit_id = data.get("deposit_id", None)
    deposit = db.session.query(Mestorogdeniya).\
        filter(db.and_(Mestorogdeniya.id_mestorojdeniya == Mestorogdeniya.id_uchastka,
                Mestorogdeniya.id_mestorojdeniya == deposit_id)). \
        first()
    deposit = db.session.query(Mestorogdeniya.id_mestorojdeniya, \
        Mestorogdeniya.id_uchastka, \
        Mestorogdeniya.id_oblast, \
        Mestorogdeniya.id_rayon, \
        Mestorogdeniya.id_osvoyeniya, \
        Mestorogdeniya.naimenovanie, \
        Mestorogdeniya.opisanie, \
        Mestorogdeniya.tip_id, \
        TipMestorogdeniya.opisanie.label("type")).\
            join(TipMestorogdeniya, Mestorogdeniya.tip_id == TipMestorogdeniya.tip_id).\
                filter(db.and_(Mestorogdeniya.id_mestorojdeniya == Mestorogdeniya.id_uchastka,
                    Mestorogdeniya.id_mestorojdeniya == deposit_id)).first()
    if deposit:
        result = {
            "deposit_id": deposit.id_mestorojdeniya,
            "mine_area_id": deposit.id_uchastka,
            "area_id": deposit.id_oblast,
            "district_id": deposit.id_rayon,
            "dev_id": deposit.id_osvoyeniya,
            "deposit_name": deposit.naimenovanie,
            "description": deposit.opisanie,
            "type_id": deposit.tip_id,
            "type": deposit.type
        }
        return jsonify({
            "auth_fail": False,
            "result": result
        }, 200)
    else:
        return jsonify({
            "auth_fail": False,
            "result": False
        }, 404)


@mod_api.route("/get_mine_area/", methods=["POST"])
def get_mine_area():
    if not is_valid_session(request, config):
        return jsonify({"auth_fail": True}, 403)
    if not has_permissions(db, get_role(request, config), "/api/get_mine_area/"):
        return jsonify({"auth_fail": True, "access_denied": True, "reason": "Доступ запрещен"}, 403)
    data = request.get_json(force=True)
    if not data:
        return jsonify({"auth_fail": False, "result": False}, 400)
    deposit_id = data.get("deposit_id", None)
    mine_area_id = data.get("mine_area_id", None)

    """mine_area = db.session.query(Mestorogdeniya).\
        filter(db.and_(Mestorogdeniya.id_uchastka == mine_area_id,
                Mestorogdeniya.id_mestorojdeniya == deposit_id)). \
        first()
    """

    deposit = aliased(Mestorogdeniya)
    mine_area = aliased(Mestorogdeniya)
    mine_type = aliased(TipMestorogdeniya)

    mine_area = db.session.query(
        mine_area.id_mestorojdeniya, \
        mine_area.id_uchastka, \
        mine_area.id_oblast, \
        mine_area.id_rayon, \
        mine_area.id_osvoyeniya, \
        mine_area.naimenovanie, \
        mine_area.opisanie, \
        mine_area.tip_id, \
        mine_type.opisanie.label("type")).\
            join(mine_type, mine_area.tip_id == mine_type.tip_id).\
                filter(db.and_(mine_area.id_mestorojdeniya == deposit_id,
                    mine_area.id_uchastka == mine_area_id)).first()

    
    if mine_area:
        result = {
            "deposit_id": mine_area.id_mestorojdeniya,
            "mine_area_id": mine_area.id_uchastka,
            "area_id": mine_area.id_oblast,
            "district_id": mine_area.id_rayon,
            "dev_id": mine_area.id_osvoyeniya,
            "mine_area_name": mine_area.naimenovanie,
            "description": mine_area.opisanie,
            "type_id": mine_area.tip_id,
            "type": mine_area.type
        }

    if not mine_area:
        return jsonify({
            "auth_fail": False,
            "result": False
        }, 200)
    
    return jsonify({
        "auth_fail": False,
        "result": result
    }, 200)


@mod_api.route("/get_mine_areas/", methods=["POST"])
def get_mine_areas():
    if not is_valid_session(request, config):
        return jsonify({"auth_fail": True}, 403)
    if not has_permissions(db, get_role(request, config), "/api/get_mine_areas/"):
        return jsonify({"auth_fail": True, "access_denied": True, "reason": "Доступ запрещен"}, 403)
    data = request.get_json(force=True)
    if not data:
        return jsonify({"auth_fail": False, "result": False}, 400)
    deposit_id = data.get("deposit_id", None)
    if not deposit_id:
        return jsonify({"auth_fail": False, "result": False}, 400)
    mine_area_name = "%" + data.get("mine_area_name", "") + "%"
    offset = data.get("offset", 0)
    limit = data.get("limit", 10)
    deposits = db.session.query(Mestorogdeniya).\
        filter(db.and_(Mestorogdeniya.id_mestorojdeniya == deposit_id,
            Mestorogdeniya.id_mestorojdeniya != Mestorogdeniya.id_uchastka,
                    Mestorogdeniya.naimenovanie.ilike(mine_area_name))). \
            order_by(Mestorogdeniya.opisanie.desc()).\
                offset(offset).limit(limit).\
                    all()
    result = []
    for item in deposits:
        result.append({
            "deposit_id": item.id_mestorojdeniya,
            "mine_area_id": item.id_uchastka,
            "area_id": item.id_oblast,
            "district_id": item.id_rayon,
            "mine_area_name": item.naimenovanie,
            "description": item.opisanie
        })
    return jsonify({
        "auth_fail": False,
        "result": result
    }, 200)

@mod_api.route("/update_mine_area/", methods=["POST"])
def update_mine_area():
    if not is_valid_session(request, config):
        return jsonify({"auth_fail": True}, 403)
    if not has_permissions(db, get_role(request, config), "/api/update_mine_area/"):
        return jsonify({"auth_fail": True, "access_denied": True, "reason": "Доступ запрещен"}, 403)
    data = request.get_json(force=True)
    if not data:
        return jsonify({"auth_fail": False, "result": False}, 400)
    try:
        deposit_id = data.get("deposit_id", None)
        mine_area_id = data.get("mine_area_id", None)
        mine_area_name = data.get("mine_area_name", None)
        dev_id = data.get("dev_id", None)
        description = data.get("description", None)
        area_id = data.get("area_id", None)
        district_id = data.get("district_id", None)

        area = db.session.query(Oblasti). \
            filter(db.and_(Oblasti.id_respubliki == 1,
                           Oblasti.id_oblasti == area_id,
                           Oblasti.id_rayona == 0)).\
            one()
        if not area:
            return jsonify({"auth_fail": False, "result": False}, 400)

        district = db.session.query(Oblasti). \
            filter(db.and_(Oblasti.id_respubliki == 1,
                           Oblasti.id_oblasti == area_id,
                           Oblasti.id_rayona == district_id)).\
            one()
        if not district:
            return jsonify({"auth_fail": False, "result": False}, 400)

        if not deposit_id or not mine_area_id or not mine_area_name or not dev_id:
            return jsonify({"auth_fail": False, "result": False}, 400)
        mine_area = db.session.query(Mestorogdeniya).\
            filter(db.and_(Mestorogdeniya.id_mestorojdeniya == deposit_id,
                           Mestorogdeniya.id_uchastka == mine_area_id)). \
            one()
        if not mine_area:
            return jsonify({"auth_fail": False, "result": False}, 404)
        mine_area_dup_count = db.session.query(Mestorogdeniya).\
            filter(db.and_(Mestorogdeniya.naimenovanie.ilike(mine_area_name),
                           Mestorogdeniya.id_mestorojdeniya == deposit_id,
                           Mestorogdeniya.id_mestorojdeniya != Mestorogdeniya.id_uchastka,
                           Mestorogdeniya.id_uchastka != mine_area_id)). \
            count()
        if mine_area_dup_count > 0:
            return jsonify({"auth_fail": False, "result": False, "reason": "Данный участок уже существует"}, 400)
        mine_area.naimenovanie = mine_area_name
        mine_area.opisanie = description
        mine_area.id_osvoyeniya = dev_id
        mine_area.id_oblast = area.id_oblasti
        mine_area.id_rayon = district.id_rayona
        db.session.commit()
        return jsonify({"auth_fail": False, "result": True}, 200)
    except:
        return jsonify({"auth_fail": False, "result": False}, 404)

@mod_api.route("/get_deposits_incl_mine_areas_count/", methods=["POST"])
def get_deposits_incl_mine_areas_count():
    if not is_valid_session(request, config):
        return jsonify({"auth_fail": True}, 403)
    if not has_permissions(db, get_role(request, config), "/api/get_deposits_incl_mine_areas_count/"):
        return jsonify({"auth_fail": True, "access_denied": True, "reason": "Доступ запрещен"}, 403)
    data = request.get_json(force=True)
    if not data:
        return jsonify({"auth_fail": False, "result": False}, 400)
    deposit_name = "%" + data.get("deposit_name", "") + "%"

    deposit = aliased(Mestorogdeniya)
    mine_area = aliased(Mestorogdeniya)

    count = db.session.query(deposit, mine_area).\
        join(mine_area, db.and_(deposit.id_mestorojdeniya == mine_area.id_mestorojdeniya, deposit.id_mestorojdeniya == deposit.id_uchastka)). \
            filter(db.or_(deposit.naimenovanie.ilike(deposit_name), mine_area.naimenovanie.ilike(deposit_name))). \
                    order_by(deposit.naimenovanie.desc()).\
                            count();

    return jsonify({
        "auth_fail": False,
        "result": count
    }, 200)

@mod_api.route("/get_explorations/", methods=["POST"])
def get_explorations():
    if not is_valid_session(request, config):
        return jsonify({"auth_fail": True}, 403)
    if not has_permissions(db, get_role(request, config), "/api/get_explorations/"):
        return jsonify({"auth_fail": True, "access_denied": True, "reason": "Доступ запрещен"}, 403)
    data = request.get_json(force=True)
    if not data:
        return jsonify({"auth_fail": False, "result": False}, 400)
    deposit_id = data.get("deposit_id", "")
    mine_area_id = data.get("mine_area_id", "")
    component_id = data.get("component_id", "")

    explorations = db.session.query(KadastrIzuchennost).\
        filter(db.and_(KadastrIzuchennost.id_mestorojdeniya == deposit_id, \
            KadastrIzuchennost.id_uchastka == mine_area_id, \
                KadastrIzuchennost.id_poleznogo_iskopaemogo == component_id)). \
                    order_by(KadastrIzuchennost.god.asc()).\
                            all();
    
    result = []
    for e in explorations:
        stage = db.session.query(Spravochniki). \
            filter(db.and_(Spravochniki.id_zapisy == e.id_stadii_izuchennost)). \
                first();
        result.append({
            "deposit_id": deposit_id,
            "mine_area_id": mine_area_id,
            "component_id": component_id,
            "year": e.god,
            "exploration_stage_id": e.id_stadii_izuchennost,
            "exploration_stage": stage.znachenie
        })

    return jsonify({
        "auth_fail": False,
        "result": result
    }, 200)

@mod_api.route("/add_exploration/", methods=["POST"])
def add_exploration():
    if not is_valid_session(request, config):
        return jsonify({"auth_fail": True}, 403)
    if not has_permissions(db, get_role(request, config), "/api/add_exploration/"):
        return jsonify({"auth_fail": True, "access_denied": True, "reason": "Доступ запрещен"}, 403)
    data = request.get_json(force=True)
    if not data:
        return jsonify({"auth_fail": False, "result": False}, 400)
    deposit_id = data.get("deposit_id", "")
    mine_area_id = data.get("mine_area_id", "")
    component_id = data.get("component_id", "")
    year = data.get("year", "")
    exploration_stage_id = data.get("exploration_stage_id", "")

    try:
        exploration = KadastrIzuchennost();
        exploration.id_mestorojdeniya = deposit_id;
        exploration.id_uchastka = mine_area_id;
        exploration.id_poleznogo_iskopaemogo = component_id;
        exploration.god = year;
        exploration.id_stadii_izuchennost = exploration_stage_id;
        db.session.add(exploration);
        db.commit();

        return jsonify({
            "auth_fail": False,
            "result": True
        }, 200)
    except:
        return jsonify({
            "auth_fail": False,
            "result": False
        }, 400)

@mod_api.route("/delete_exploration/", methods=["POST"])
def delete_exploration():
    if not is_valid_session(request, config):
        return jsonify({"auth_fail": True}, 403)
    if not has_permissions(db, get_role(request, config), "/api/delete_exploration/"):
        return jsonify({"auth_fail": True, "access_denied": True, "reason": "Доступ запрещен"}, 403)
    data = request.get_json(force=True)
    if not data:
        return jsonify({"auth_fail": False, "result": False}, 400)
    deposit_id = data.get("deposit_id", "")
    mine_area_id = data.get("mine_area_id", "")
    component_id = data.get("component_id", "")
    year = data.get("year", "")
    exploration_stage_id = data.get("exploration_stage_id", "")

    try:
        exploration = db.session.query(KadastrIzuchennost).\
        filter(db.and_(KadastrIzuchennost.id_mestorojdeniya == deposit_id, \
            KadastrIzuchennost.id_uchastka == mine_area_id, \
                KadastrIzuchennost.id_poleznogo_iskopaemogo == component_id,
                    KadastrIzuchennost.god == year,
                        KadastrIzuchennost.id_stadii_izuchennost == exploration_stage_id)). \
                            first();

        if exploration:
            db.session.delete(exploration);
            db.commit();
            return jsonify({
                "auth_fail": False,
                "result": True
            }, 200)
        else:
            return jsonify({
                "auth_fail": False,
                "result": False
            }, 200)
    except:
        return jsonify({
            "auth_fail": False,
            "result": False
        }, 400)

@mod_api.route("/has_permissions_to_security_settings/", methods=["POST"])
def has_permissions_to_security_settings():
    if not is_valid_session(request, config):
        return jsonify({"auth_fail": True}, 403)
    if not has_permissions(db, get_role(request, config), "/api/has_permissions_to_security_settings/"):
        return jsonify({"auth_fail": True, "access_denied": True, "reason": "Доступ запрещен"}, 403)
    return jsonify({
        "auth_fail": False, 
        "result": True
    }, 200);

@mod_api.route("/get_users_count/", methods=["POST"])
def get_users_count():
    if not is_valid_session(request, config):
        return jsonify({"auth_fail": True}, 403)
    if not has_permissions(db, get_role(request, config), "/api/get_users_count/"):
        return jsonify({"auth_fail": True, "access_denied": True, "reason": "Доступ запрещен"}, 403)
    
    data = request.get_json(force=True)
    username = data.get("username", "")
    limit = data.get("limit", 100)
    offset = data.get("offset", 0)
    username = "%" + username + "%";

    count = db.session.query(Polzovateli).filter(Polzovateli.imya.ilike(username)).offset(offset).limit(limit).count()

    return jsonify({
        "auth_fail": False, 
        "result": count
    }, 200);

@mod_api.route("/get_roles/", methods=["POST"])
def get_roles():
    if not is_valid_session(request, config):
        return jsonify({"auth_fail": True}, 403)
    if not has_permissions(db, get_role(request, config), "/api/get_roles/"):
        return jsonify({"auth_fail": True, "access_denied": True, "reason": "Доступ запрещен"}, 403)
    
    roles = db.session.query(Roli).all();
    result = [];
    for role in roles:
        result.append({
            "role_id": role.id,
            "role": role.rol
        })
    return jsonify({
        "auth_fail": False, 
        "result": result
    }, 200);

@mod_api.route("/add_user/", methods=["POST"])
def add_user():
    if not is_valid_session(request, config):
        return jsonify({"auth_fail": True}, 403)
    if not has_permissions(db, get_role(request, config), "/api/add_user/"):
        return jsonify({"auth_fail": True, "access_denied": True, "reason": "Доступ запрещен"}, 403)
    
    data = request.get_json(force=True)
    role_id = data.get("role_id", None)
    username = data.get("username", "")
    password = data.get("password", "")
    description = data.get("description", None)
    salt = hexlify(os.urandom(32))
    
    role = db.session.query(Roli).filter(Roli.id == role_id).first();
    if not role:
        return jsonify({
            "auth_fail": False, 
            "result": False,
            "reason": "Несуществующая роль"
        }, 400);

    user = db.session.query(Polzovateli).filter(db.and_(Polzovateli.imya == username)).first();
    if user:
        return jsonify({
            "auth_fail": False, 
            "result": False,
            "reason": "Пользователь уже существует"
        }, 400);

    user = Polzovateli()
    user.imya = username;
    user.parol = hash_password(password, salt.decode("UTF-8"))
    user.sol = salt.decode("UTF-8");
    user.opisanie = description;
    user.rol_id = role_id;
    db.session.add(user);
    db.session.commit();

    return jsonify({
        "auth_fail": False, 
        "result": True
    }, 200);

@mod_api.route("/get_users/", methods=["POST"])
def get_users():
    if not is_valid_session(request, config):
        return jsonify({"auth_fail": True}, 403)
    if not has_permissions(db, get_role(request, config), "/api/get_users/"):
        return jsonify({"auth_fail": True, "access_denied": True, "reason": "Доступ запрещен"}, 403)
    
    data = request.get_json(force=True)
    username = data.get("username", "")
    limit = data.get("limit", 100)
    offset = data.get("offset", 0)
    username = "%" + username + "%";

    users = db.session.query(Polzovateli).filter(Polzovateli.imya.ilike(username)).offset(offset).limit(limit).all()

    result = []
    for user in users:
        result.append({
            "user_id": user.id,
            "username": user.imya,
            "description": user.opisanie,
            "role_id": user.rol_id,
            "role": user.rol.rol
        });

    return jsonify({
        "auth_fail": False, 
        "result": result
    }, 200);

@mod_api.route("/get_user/", methods=["POST"])
def get_user():
    if not is_valid_session(request, config):
        return jsonify({"auth_fail": True}, 403)
    if not has_permissions(db, get_role(request, config), "/api/get_user/"):
        return jsonify({"auth_fail": True, "access_denied": True, "reason": "Доступ запрещен"}, 403)
    
    data = request.get_json(force=True)
    user_id = data.get("user_id", "")

    user = db.session.query(Polzovateli).filter(db.and_(Polzovateli.id == user_id)).first();

    if not user:
        return jsonify({
            "auth_fail": False, 
            "result": False
        }, 404);


    result = {
        "user_id": user.id,
        "username": user.imya,
        "description": user.opisanie,
        "role_id": user.rol_id,
        "role": user.rol.rol
    };

    return jsonify({
        "auth_fail": False, 
        "result": result
    }, 200);

@mod_api.route("/update_user/", methods=["POST"])
def update_user():
    if not is_valid_session(request, config):
        return jsonify({"auth_fail": True}, 403)
    if not has_permissions(db, get_role(request, config), "/api/update_user/"):
        return jsonify({"auth_fail": True, "access_denied": True, "reason": "Доступ запрещен"}, 403)
    
    data = request.get_json(force=True)
    user_id = data.get("user_id", "")
    role_id = data.get("role_id", None)
    password = data.get("password", "")
    description = data.get("description", None)
    change_password = data.get("change_password", False)

    print("-------------------------------- Change password --------------------------------")
    print(change_password)
    print("-------------------------------- Change password --------------------------------")

    salt = hexlify(os.urandom(32))
        
    role = db.session.query(Roli).filter(Roli.id == role_id).first();
    if not role:
        return jsonify({
            "auth_fail": False, 
            "result": False,
            "reason": "Несуществующая роль"
        }, 400);

    user = db.session.query(Polzovateli).filter(db.and_(Polzovateli.id == user_id)).first();
    if not user:
        return jsonify({
            "auth_fail": False, 
            "result": False,
            "reason": "Пользователь не существует"
        }, 400);

    if change_password:
        user.parol = hash_password(password, salt.decode("UTF-8"))
        user.sol = salt.decode("UTF-8");
    
    user.opisanie = description;
    user.rol_id = role_id;
    db.session.commit();

    return jsonify({
        "auth_fail": False, 
        "result": True
    }, 200);

@mod_api.route("/delete_user/", methods=["POST"])
def delete_user():
    if not is_valid_session(request, config):
        return jsonify({"auth_fail": True}, 403)
    if not has_permissions(db, get_role(request, config), "/api/delete_user/"):
        return jsonify({"auth_fail": True, "access_denied": True, "reason": "Доступ запрещен"}, 403)
    
    data = request.get_json(force=True)
    user_id = data.get("user_id", "")

    user = db.session.query(Polzovateli).filter(db.and_(Polzovateli.id == user_id)).first();
    if not user:
        return jsonify({
            "auth_fail": False, 
            "result": False,
            "reason": "Пользователь не существует"
        }, 400);
    
    if user.imya == "admin":
        return jsonify({
            "auth_fail": False, 
            "result": False,
            "reason": "Администратора по-умолчанию удалить нельзя"
        }, 400);
    
    db.session.delete(user);
    db.session.commit();

    return jsonify({
        "auth_fail": False, 
        "result": True
    }, 200);

@mod_api.route("/get_areas_count/", methods=["POST"])
def get_areas_count():
    """
    Counts how many areas are there in the database
    """
    if not is_valid_session(request, config):
        return jsonify({"auth_fail": True}, 403)
    if not has_permissions(db, get_role(request, config), "/api/get_areas_count/"):
        return jsonify({"auth_fail": True, "access_denied": True, "reason": "Доступ запрещен"}, 403)
    data = request.get_json(force=True)
    if not data:
        return jsonify({"auth_fail": False, "result": False}, 400)
    republic_id = data.get("republic_id", 1)
    area = "%" + data.get("area_name", "") + "%"
    try:
        total = db.session.query(Oblasti).\
            filter(db.and_(Oblasti.id_respubliki == republic_id,
                           Oblasti.id_oblasti != 0,
                           Oblasti.id_rayona == 0,
                           Oblasti.opisanie.ilike(area))).count()
    except:
        total = 0
    return jsonify({
        "auth_fail": False,
        "result": total
    })


@mod_api.route("/get_areas/", methods=["POST"])
def get_areas():
    """
    Gets the list of areas with offset and limit
    """
    if not is_valid_session(request, config):
        return jsonify({"auth_fail": True}, 403)
    if not has_permissions(db, get_role(request, config), "/api/get_areas/"):
        return jsonify({"auth_fail": True, "access_denied": True, "reason": "Доступ запрещен"}, 403)

    data = request.get_json(force=True)
    if not data:
        return jsonify({"auth_fail": False, "result": False}, 400)
    id_republic = data.get("id_republic", 1)
    area_name = "%" + data.get("area_name", "") + "%"
    offset = data.get("offset", 0)
    limit = data.get("limit", 10)
    areas = db.session.query(Oblasti).\
        filter(db.and_(Oblasti.id_respubliki == id_republic,
                       Oblasti.id_oblasti != 0, Oblasti.id_rayona == 0,
                       Oblasti.opisanie.ilike(area_name))). \
        offset(offset).limit(limit).all()
    result = []
    for item in areas:
        result.append({
            "id_republic": item.id_respubliki,
            "id_area": item.id_oblasti,
            "area_name": item.opisanie
        })
    return jsonify({
        "auth_fail": False,
        "result": result
    }, 200)

@mod_api.route("/get_area/", methods=["POST"])
def get_area():
    """
    Gets the list of areas with offset and limit
    """
    if not is_valid_session(request, config):
        return jsonify({"auth_fail": True}, 403)
    if not has_permissions(db, get_role(request, config), "/api/get_area/"):
        return jsonify({"auth_fail": True, "access_denied": True, "reason": "Доступ запрещен"}, 403)

    data = request.get_json(force=True)
    if not data:
        return jsonify({"auth_fail": False, "result": False}, 400)
    id_republic = data.get("id_republic", 1)
    id_area = data.get("id_area", "")

    area = db.session.query(Oblasti).\
        filter(db.and_(Oblasti.id_respubliki == id_republic,
            Oblasti.id_oblasti == id_area, Oblasti.id_rayona == 0)). \
                first()

    if area:
        return jsonify({
            "auth_fail": False,
            "result": {
                "area_id": area.id_oblasti,
                "area_name": area.opisanie
            }
        }, 200)
    else:
        return jsonify({
            "auth_fail": False,
            "result": False
        }, 200)

@mod_api.route("/get_district/", methods=["POST"])
def get_district():
    """
    Gets the list of areas with offset and limit
    """
    if not is_valid_session(request, config):
        return jsonify({"auth_fail": True}, 403)
    if not has_permissions(db, get_role(request, config), "/api/get_district/"):
        return jsonify({"auth_fail": True, "access_denied": True, "reason": "Доступ запрещен"}, 403)

    data = request.get_json(force=True)
    if not data:
        return jsonify({"auth_fail": False, "result": False}, 400)
    id_republic = data.get("id_republic", 1)
    id_area = data.get("id_area", "")
    id_district = data.get("id_district", "")

    district = db.session.query(Oblasti).\
        filter(db.and_(Oblasti.id_respubliki == id_republic,
            Oblasti.id_oblasti == id_area, Oblasti.id_rayona == id_district)). \
                first()

    if district:
        return jsonify({
            "auth_fail": False,
            "result": {
                "district_id": district.id_oblasti,
                "district_name": district.opisanie
            }
        }, 200)
    else:
        return jsonify({
            "auth_fail": False,
            "result": False
        }, 200)


@mod_api.route("/delete_area/", methods=["POST"])
def delete_area():
    """
    Deletes the given area from the database
    """
    if not is_valid_session(request, config):
        return jsonify({"auth_fail": True}, 403)
    if not has_permissions(db, get_role(request, config), "/api/delete_area/"):
        return jsonify({"auth_fail": True, "access_denied": True, "reason": "Доступ запрещен"}, 403)

    data = request.get_json(force=True)
    if not data:
        return jsonify({"auth_fail": False, "result": False}, 400)
    republic_id = data.get("id_republic", 1)
    area_id = data.get("area_id", None)
    if not area_id:
        return jsonify({"auth_fail": False, "result": False}, 404)
    try:
        area = db.session.query(Oblasti).\
            filter(db.and_(Oblasti.id_respubliki == republic_id,
                        Oblasti.id_oblasti == area_id, Oblasti.id_rayona == 0)).one()
        db.session.delete(area)
        db.session.commit()
        return jsonify({
            "auth_fail": False,
            "result": True
        })
    except:
        return jsonify({
            "auth_fail": False,
            "result": True,
            "reason": "Запись не найдена"
        })


@mod_api.route("/add_area/", methods=["POST"])
def add_area():
    """
    Adds new area into the database
    """
    if not is_valid_session(request, config):
        return jsonify({"auth_fail": True}, 403)
    if not has_permissions(db, get_role(request, config), "/api/add_area/"):
        return jsonify({"auth_fail": True, "access_denied": True, "reason": "Доступ запрещен"}, 403)
    data = request.get_json(force=True)
    if not data:
        return jsonify({"auth_fail": False, "result": False}, 400)
    try:
        db.session.execute("LOCK TABLES Oblasti WRITE")
        area_id = db.session.query(db.func.max(Oblasti.id_oblasti)).\
            filter(db.and_(Oblasti.id_respubliki == 1,
                           Oblasti.id_rayona == 0)).\
            scalar()
        if not area_id:
            area_id = 0
        oblast = Oblasti()
        oblast.id_respubliki = 1
        oblast.id_rayona = 0
        oblast.id_oblasti = area_id + 1
        oblast.opisanie = data["area_name"]
        db.session.execute("UNLOCK TABLES")
        db.session.commit()
        return jsonify({
            "auth_fail": False,
            "result": {
                "area_id": area_id + 1
            }
        }, 200)

    except Exception as e:
        db.session.execute("UNLOCK TABLES")
        return jsonify({
            "auth_fail": False,
            "result": False,
            "reason": "Запись не найдена"
        }, 404)


@mod_api.route("/update_area/", methods=["POST"])
def update_area():
    if not is_valid_session(request, config):
        return jsonify({"auth_fail": True}, 403)
    if not has_permissions(db, get_role(request, config), "/api/update_area/"):
        return jsonify({"auth_fail": True, "access_denied": True, "reason": "Доступ запрещен"}, 403)
    data = request.get_json(force=True)
    if not data:
        return jsonify({"auth_fail": False, "result": False}, 400)
    try:
        area_id = data.get("area_id", None)
        if not area_id:
            return jsonify({"auth_fail": False, "result": False}, 400)
        area = db.session.query(Oblasti).\
            filter(db.and_(Oblasti.id_respubliki == 1,
                           Oblasti.id_oblasti == area_id,
                           Oblasti.id_rayona == 0)).\
            one()
        area.opisanie = data["area_name"]
        db.session.commit()
        return jsonify({"auth_fail": False, "result": True}, 200)
    except:
        return jsonify({"auth_fail": False, "result": False, "reason": "Запись не найдена"}, 404)


@mod_api.route("/get_all_dictionaries/", methods=["GET"])
def get_all_dictionaries():
    if not is_valid_session(request, config):
        return jsonify({"auth_fail": True}, 403)
    if not has_permissions(db, get_role(request, config), "/api/get_all_dictionaries/"):
        return jsonify({"auth_fail": True, "access_denied": True, "reason": "Доступ запрещен"}, 403)
    categories = db.session.query(SpravochnikiKategorii).all()
    result = []
    for category in categories:
        result.append({
            "category": category.kategoriya,
            "description": category.opisanie
        })
    return jsonify({
        "auth_fail": False,
        "result": result
    })


@mod_api.route("/get_dictionary_count/", methods=["POST"])
def get_dictionary_count():
    if not is_valid_session(request, config):
        return jsonify({"auth_fail": True}, 403)
    if not has_permissions(db, get_role(request, config), "/api/get_dictionary_count/"):
        return jsonify({"auth_fail": True, "access_denied": True, "reason": "Доступ запрещен"}, 403)
    data = request.get_json(force=True)
    if not data:
        return jsonify({"auth_fail": False, "result": False}, 400)
    category = data.get("category", "")
    item = "%" + data.get("item", "") + "%"

    try:
        total = db.session.query(Spravochniki).\
            filter(db.and_(Spravochniki.kategoriya == category,
                           Spravochniki.znachenie.ilike(item))).count()
    except:
        total = 0
    return jsonify({
        "auth_fail": False,
        "result": total
    })

@mod_api.route("/get_dictionary_contents/", methods=["POST"])
def get_dictionary_contents():
    if not is_valid_session(request, config):
        return jsonify({"auth_fail": True}, 403)
    if not has_permissions(db, get_role(request, config), "/api/get_dictionary_contents/"):
        return jsonify({"auth_fail": True, "access_denied": True, "reason": "Доступ запрещен"}, 403)
    data = request.get_json(force=True)
    if not data:
        return jsonify({"auth_fail": False, "result": False}, 400)

    category = data.get("category", "")
    offset = data.get("offset", 0)
    limit = data.get("limit", 10)

    item = "%" + data.get("item", "") + "%"
    dictionary = db.session.query(Spravochniki). \
        filter(db.and_(Spravochniki.kategoriya == category,
                       Spravochniki.znachenie.ilike(item))). \
        order_by(Spravochniki.znachenie.desc()).\
        offset(offset).limit(limit).all()

    result = []
    for item in dictionary:
        result.append({
            "id": item.id_zapisy,
            "category": item.kategoriya,
            "description": item.znachenie
        })
    return jsonify({
        "auth_fail": False,
        "result": result
    }, 200)


@mod_api.route("/get_dictionary_item_description/", methods=["POST"])
def get_dictionary_item_description():
    if not is_valid_session(request, config):
        return jsonify({"auth_fail": True}, 403)
    if not has_permissions(db, get_role(request, config), "/api/get_dictionary_item_description/"):
        return jsonify({"auth_fail": True, "access_denied": True, "reason": "Доступ запрещен"}, 403)
    data = request.get_json(force=True)
    if not data:
        return jsonify({"auth_fail": False, "result": False}, 400)
    id = data.get("id", "")
    item = db.session.query(Spravochniki). \
        filter(Spravochniki.id_zapisy == id).first()
    return jsonify({
        "auth_fail": False,
        "result": {
            "id": item.id_zapisy,
            "category": item.kategoriya,
            "description": item.znachenie
        }
    }, 200)


@mod_api.route("/delete_dictionary_contents/", methods=["POST"])
def delete_dictionary_contents():
    if not is_valid_session(request, config):
        return jsonify({"auth_fail": True}, 403)
    if not has_permissions(db, get_role(request, config), "/api/delete_dictionary_contents/"):
        return jsonify({"auth_fail": True, "access_denied": True, "reason": "Доступ запрещен"}, 403)
    data = request.get_json(force=True)
    if not data:
        return jsonify({"auth_fail": False, "result": False}, 400)
    category = data.get("category", None)
    id = data.get("id", None)
    if not category or not id:
        return jsonify({"auth_fail": False, "result": False, "reason": "Некорректные данные"}, 404)

    item = db.session.query(Spravochniki).\
        filter(db.and_(Spravochniki.kategoriya == category,
                       Spravochniki.id_zapisy == id)).one()
    
    if item.kategoriya == "SPR_VED" and item.znachenie == "ГосКомГеологии":
        return jsonify({"auth_fail": False, "result": False, "reason": "Нельзя удалить основное ведомство"}, 400)

    db.session.delete(item)
    db.session.commit()
    return jsonify({
        "auth_fail": False,
        "result": True
    }, 200)


@mod_api.route("/add_dictionary_contents/", methods=["POST"])
def add_dictionary_contents():
    if not is_valid_session(request, config):
        return jsonify({"auth_fail": True}, 403)
    if not has_permissions(db, get_role(request, config), "/api/add_dictionary_contents/"):
        return jsonify({"auth_fail": True, "access_denied": True, "reason": "Доступ запрещен"}, 403)
    data = request.get_json(force=True)
    if not data:
        return jsonify({"auth_fail": False, "result": False}, 400)
    category = data.get("category", None)
    desc = data.get("description", None)
    if not category or not desc:
        return jsonify({"auth_fail": False, "result": False}, 400)
    try:
        item = db.session.query(Spravochniki). \
            filter(db.and_(Spravochniki.kategoriya == category, Spravochniki.znachenie.ilike(desc))). \
            first()
        if item:
            return jsonify({"auth_fail": False, "result": False, "reason": "Экземпляр существует"}, 400)
        item = Spravochniki()
        item.kategoriya = category
        item.znachenie = desc
        db.session.add(item)
        db.session.commit()
        return jsonify({
            "auth_fail": False,
            "result": True
        }, 200)
    except Exception as e:
        print(e)
        return jsonify({
            "auth_fail": False,
            "result": False,
            "reason": "Ошибка сервера"
        }, 400)


@mod_api.route("/update_dictionary_contents/", methods=["POST"])
def update_dictionary_contents():
    if not is_valid_session(request, config):
        return jsonify({"auth_fail": True}, 403)
    if not has_permissions(db, get_role(request, config), "/api/update_dictionary_contents/"):
        return jsonify({"auth_fail": True, "access_denied": True, "reason": "Доступ запрещен"}, 403)
    data = request.get_json(force=True)
    if not data:
        return jsonify({"auth_fail": False, "result": False}, 400)
    id = data.get("id", None)
    category = data.get("category", None)
    desc = data.get("description", None)
    if not category or not desc or not id:
        return jsonify({"auth_fail": False, "result": False}, 400)
    try:
        item = db.session.query(Spravochniki).\
            filter(db.and_(Spravochniki.id_zapisy == id,
                           Spravochniki.kategoriya == category)).\
            one()
        
        if item.kategoriya == "SPR_VED" and item.znachenie == "ГосКомГеологии":
            return jsonify({"auth_fail": False, "result": False, "reason": "Нельзя изменить основное ведомство"}, 400)
        
        item.znachenie = desc
        db.session.commit()
        return jsonify({
            "auth_fail": False,
            "result": True
        }, 200)
    except:
        return jsonify({
            "auth_fail": False,
            "result": False,
            "reason": "Экземпляр не существует"
        }, 400)


@mod_api.route("/get_districts/", methods=["POST"])
def get_districts():
    if not is_valid_session(request, config):
        return jsonify({"auth_fail": True}, 403)
    if not has_permissions(db, get_role(request, config), "/api/get_districts/"):
        return jsonify({"auth_fail": True, "access_denied": True, "reason": "Доступ запрещен"}, 403)
    data = request.get_json(force=True)
    if not data:
        return jsonify({"auth_fail": False, "result": False}, 400)
    
    id_republic = data.get("id_republic", 1)
    id_area = data.get("id_area", None)
    if not id_area:
        return jsonify({"auth_fail": False, "result": False}, 400)
    district_name = "%" + data.get("district_name", "") + "%"
    offset = data.get("offset", 0)
    limit = data.get("limit", 10)
    print("------------------- GETTING DISTRICTS -------------------------")
    print(district_name)

    districts = db.session.query(Oblasti).\
        filter(db.and_(Oblasti.id_respubliki == id_republic,
                       Oblasti.id_oblasti == id_area, Oblasti.id_rayona != 0,
                       Oblasti.opisanie.ilike(district_name))). \
        order_by(Oblasti.opisanie.desc()).\
        offset(offset).limit(limit).\
        all()
    result = []
    for item in districts:
        result.append({
            "id_republic": item.id_respubliki,
            "id_area": item.id_oblasti,
            "id_district": item.id_rayona,
            "district_name": item.opisanie
        })
    return jsonify({
        "auth_fail": False,
        "result": result
    }, 200)


@mod_api.route("/delete_district/", methods=["POST"])
def delete_district():
    if not is_valid_session(request, config):
        return jsonify({"auth_fail": True}, 403)
    if not has_permissions(db, get_role(request, config), "/api/delete_district/"):
        return jsonify({"auth_fail": True, "access_denied": True, "reason": "Доступ запрещен"}, 403)
    data = request.get_json(force=True)
    if not data:
        return jsonify({"auth_fail": False, "result": False}, 400)
    republic_id = data.get("id_republic", 1)
    area_id = data.get("area_id", None)
    district_id = data.get("district_id", None)
    if not area_id or not district_id:
        return jsonify({"auth_fail": False, "result": False}, 404)
    district = db.session.query(Oblasti).\
        filter(db.and_(Oblasti.id_respubliki == republic_id,
                       Oblasti.id_oblasti == area_id,
                       Oblasti.id_rayona == district_id)).one()
    db.session.delete(district)
    db.session.commit()
    return jsonify({
        "auth_fail": False,
        "result": True
    }, 200)


@mod_api.route("/add_district/", methods=["POST"])
def add_district():
    if not is_valid_session(request, config):
        return jsonify({"auth_fail": True}, 403)
    if not has_permissions(db, get_role(request, config), "/api/add_district/"):
        return jsonify({"auth_fail": True, "access_denied": True, "reason": "Доступ запрещен"}, 403)
    data = request.get_json(force=True)
    if not data:
        return jsonify({"auth_fail": False, "result": False}, 400)
    try:
        area_id = data.get("area_id", None)
        if not area_id:
            return jsonify({"auth_fail": False, "result": False}, 400)
        district_name = data.get("district_name", None)
        if not district_name:
            return jsonify({"auth_fail": False, "result": False}, 400)
        db.session.execute("LOCK TABLES Oblasti WRITE")
        district_id = db.session.query(db.func.max(Oblasti.id_rayona)).\
            filter(db.and_(Oblasti.id_respubliki == 1,
                           Oblasti.id_oblasti == area_id)).\
            scalar()
        if not district_id:
            district_id = 0
        district = db.session.query(Oblasti).\
            filter(db.and_(Oblasti.id_respubliki == 1,
                Oblasti.id_oblasti == area_id, Oblasti.id_rayona != 0,
                    Oblasti.opisanie == district_name)). \
                first()
        if district:
            return jsonify({"auth_fail": False, "result": False, "reason": "Запись уже существует"}, 400)
        district = Oblasti()
        district.id_respubliki = 1
        district.id_rayona = district_id + 1
        district.id_oblasti = area_id
        district.opisanie = district_name
        db.session.add(district)
        db.session.commit()
        db.session.execute("UNLOCK TABLES")
        return jsonify({
            "auth_fail": False,
            "result": {
                "area_id": area_id,
                "district_id": district_id + 1
            }
        }, 200)
    except Exception as e:
        db.session.execute("UNLOCK TABLES")
        print(e)
        return jsonify({
            "auth_fail": False,
            "result": False
        }, 404)

@mod_api.route("/update_district/", methods=["POST"])
def update_district():
    if not is_valid_session(request, config):
        return jsonify({"auth_fail": True}, 403)
    if not has_permissions(db, get_role(request, config), "/api/update_district/"):
        return jsonify({"auth_fail": True, "access_denied": True, "reason": "Доступ запрещен"}, 403)
    data = request.get_json(force=True)
    if not data:
        return jsonify({"auth_fail": False, "result": False}, 400)
    try:
        republic_id = data.get("republic_id", 1)
        area_id = data.get("area_id", None)
        district_id = data.get("district_id", None)
        if not area_id or not district_id:
            return jsonify({"auth_fail": False, "result": False}, 400)
        district = db.session.query(Oblasti).\
            filter(db.and_(Oblasti.id_respubliki == republic_id,
                           Oblasti.id_oblasti == area_id,
                           Oblasti.id_rayona == district_id)).\
            one()
        district.opisanie = data.get("distrcit_name", "")
        db.session.commit()
        return jsonify({"auth_fail": False, "result": True}, 200)
    except:
        return jsonify({"auth_fail": False, "result": False}, 404)


@mod_api.route("/get_district_count/", methods=["POST"])
def get_district_count():
    if not is_valid_session(request, config):
        return jsonify({"auth_fail": True}, 403)
    if not has_permissions(db, get_role(request, config), "/api/get_district_count/"):
        return jsonify({"auth_fail": True, "access_denied": True, "reason": "Доступ запрещен"}, 403)
    data = request.get_json(force=True)
    if not data:
        return jsonify({"auth_fail": False, "result": False}, 400)
    republic_id = data.get("republic_id", 1)
    area_id = data.get("area_id", None)
    if not area_id:
        return jsonify({"auth_fail": False, "result": False}, 400)
    district = "%" + data.get("district_name", "") + "%"
    try:
        total = db.session.query(Oblasti).\
            filter(db.and_(Oblasti.id_respubliki == republic_id,
                           Oblasti.id_oblasti == area_id,
                           Oblasti.id_rayona != 0,
                           Oblasti.opisanie.ilike(district))).count()
    except:
        total = 0
    return jsonify({
        "auth_fail": False,
        "result": total
    }, 200)


@mod_api.route("/get_deposits_count/", methods=["POST"])
def get_deposits_count():
    if not is_valid_session(request, config):
        return jsonify({"auth_fail": True}, 403)
    if not has_permissions(db, get_role(request, config), "/api/get_deposits_count/"):
        return jsonify({"auth_fail": True, "access_denied": True, "reason": "Доступ запрещен"}, 403)
    data = request.get_json(force=True)
    if not data:
        return jsonify({"auth_fail": False, "result": False}, 400)
    deposit_name = "%" + data.get("deposit_name", "") + "%"

    try:
        total = db.session.query(Mestorogdeniya). \
            filter(db.and_(Mestorogdeniya.id_mestorojdeniya == Mestorogdeniya.id_uchastka,
                    Mestorogdeniya.naimenovanie.ilike(deposit_name))).count()
    except:
        total = 0
    return jsonify({
        "auth_fail": False,
        "result": total
    }, 200)

@mod_api.route("/get_available_components_for_deposit/", methods=["POST"])
def get_available_components_for_deposit():
    if not is_valid_session(request, config):
        return jsonify({"auth_fail": True}, 403)
    if not has_permissions(db, get_role(request, config), "/api/get_available_components_for_deposit/"):
        return jsonify({"auth_fail": True, "access_denied": True, "reason": "Доступ запрещен"}, 403)
    data = request.get_json(force=True)
    if not data:
        return jsonify({"auth_fail": False, "result": False}, 400)
    deposit_id = data.get("deposit_id", "")
    mine_area_id = data.get("mine_area_id", "")

    try:
        components = db.session.query(KadastrObshayaInformaciya, Spravochniki). \
            join(Spravochniki).\
                filter(db.and_(Mestorogdeniya.id_mestorojdeniya == deposit_id,
                    Mestorogdeniya.id_uchastka == mine_area_id)) \
                        .all()
        result = []
        for c in components:
            result.append({
                "deposit_id": deposit_id,
                "mine_area_id": mine_area_id,
                "component_id": c.id_poleznogo_iskopaemogo,
                "component_name": c.znachenie
            });
        return jsonify({
            "auth_fail": False,
            "result": result
        }, 200)
    except:
        return jsonify({
            "auth_fail": False,
            "result": False
        }, 200)

@mod_api.route("/create_or_ignore_general_info/", methods=["POST"])
def create_or_ignore_general_info():
    """
    This does not work... we should create the record only if all fields are given
    """
    if not is_valid_session(request, config):
        return jsonify({"auth_fail": True}, 403)
    if not has_permissions(db, get_role(request, config), "/api/create_or_ignore_general_info/"):
        return jsonify({"auth_fail": True, "access_denied": True, "reason": "Доступ запрещен"}, 403)
    data = request.get_json(force=True)
    if not data:
        return jsonify({"auth_fail": False, "result": False}, 400)

    deposit_id = data.get("deposit_id", "")
    mine_area_id = data.get("mine_area_id", "")
    component_id = data.get("component_id", "")

    try:
        info = db.session.query(KadastrTitul). \
            filter(db.and_(KadastrTitul.id_mestorojdeniya == deposit_id,
                KadastrTitul.id_uchastka == mine_area_id, \
                    KadastrTitul.id_poleznogo_iskopaemogo == component_id)) \
                        .first()

        if not info:
            info = KadastrTitul();
            info.id_mestorojdeniya = deposit_id
            info.id_uchastka = mine_area_id
            info.id_poleznogo_iskopaemogo = component_id
            db.session.add(info);
            db.session.commit();

        return jsonify({
            "auth_fail": False,
            "result": True
        }, 200)
    except Exception as e:
        print("-------------------------Got exception during save operation for the KadastrTitul --------------------- " + str(e))
        return jsonify({
            "auth_fail": False,
            "result": False
        }, 200)

@mod_api.route("/get_general_info/", methods=["POST"])
def get_general_info():
    if not is_valid_session(request, config):
        return jsonify({"auth_fail": True}, 403)
    if not has_permissions(db, get_role(request, config), "/api/get_general_info/"):
        return jsonify({"auth_fail": True, "access_denied": True, "reason": "Доступ запрещен"}, 403)
    data = request.get_json(force=True)
    if not data:
        return jsonify({"auth_fail": False, "result": False}, 400)
    deposit_id = data.get("deposit_id", "")
    mine_area_id = data.get("mine_area_id", "")
    component_id = data.get("component_id", "")

    try:
        info = db.session.query(KadastrObshayaInformaciya). \
            filter(db.and_(Mestorogdeniya.id_mestorojdeniya == deposit_id,
                Mestorogdeniya.id_uchastka == mine_area_id, \
                    Mestorogdeniya.id_poleznogo_iskopaemogo == component_id)) \
                        .first()
        

        return jsonify({
            "auth_fail": False,
            "result": True
        }, 200)

        
    except:
        return jsonify({
            "auth_fail": False,
            "result": False
        }, 200)

@mod_api.route("/get_geo_characteristics/", methods=["GET"])
def get_geo_characteristics():
    if not is_valid_session(request, config):
        return jsonify({"auth_fail": True}, 403)
    if not has_permissions(db, get_role(request, config), "/api/get_geo_characteristics/"):
        return jsonify({"auth_fail": True, "access_denied": True, "reason": "Доступ запрещен"}, 403)
    data = request.get_json(force=True)
    if not data:
        return jsonify({"auth_fail": False, "result": False}, 400)
    deposit_id = data.get("deposit_id", "")
    mine_area_id = data.get("mine_area_id", "")
    component_id = data.get("component_id", "")
    try:
        characteristic = db.session.query(KadastrGeoHarakteristiki). \
            filter(db.and_(KadastrGeoHarakteristiki.id_mestorojdeniya == deposit_id, \
                KadastrGeoHarakteristiki.id_uchastka == mine_area_id, \
                    KadastrGeoHarakteristiki.id_poleznogo_iskopaemogo == component_id)). \
                        first()
        return jsonify({
            "auth_fail": False,
            "result": {
                "id": characteristic.id,
                "id_mestorojdeniya": characteristic.id_mestorojdeniya,
                "id_uchastka": characteristic.id_uchastka,
                "id_poleznogo_iskopaemogo": characteristic.id_poleznogo_iskopaemogo, 
                "id_gruppi": characteristic.id_gruppi,
                "id_tip_slojnosti": characteristic.id_tip_slojnosti,
                "porodi_slag_pol_iskopaemoe": characteristic.porodi_slag_pol_iskopaemoe,
                "id_forma_tel": characteristic.id_forma_tel,
                "kolichestvo_tel": characteristic.kolichestvo_tel,
                "razmer_tel_dlina_po_protstiraniyu_ot": characteristic.razmer_tel_dlina_po_protstiraniyu_ot,
                "razmer_tel_dlina_po_protstiraniyu_do": characteristic.razmer_tel_dlina_po_protstiraniyu_do,
                "razmer_tel_dlina_po_protstiraniyu_sred": characteristic.razmer_tel_dlina_po_protstiraniyu_sred,
                "moshnost_obshaya_ot": characteristic.moshnost_obshaya_ot,
                "moshnost_obshaya_do": characteristic.moshnost_obshaya_do,
                "moshnost_obshaya_sred": characteristic.moshnost_obshaya_sred,
                "moshnost_vskritaya_ot": characteristic.moshnost_vskritaya_ot,
                "moshnost_vskritaya_do": characteristic.moshnost_vskritaya_do,
                "moshnost_vskritaya_sred": characteristic.moshnost_vskritaya_sred,
                "moshnost_pod_zapasov_ot": characteristic.moshnost_pod_zapasov_ot,
                "moshnost_pod_zapasov_do": characteristic.moshnost_pod_zapasov_do,
                "moshnost_pod_zapasov_sred": characteristic.moshnost_pod_zapasov_sred,
                "moshnost_otdel_sloev_ot": characteristic.moshnost_otdel_sloev_ot,
                "moshnost_otdel_sloev_do": characteristic.moshnost_otdel_sloev_do,
                "moshnost_otdel_sloev_sred": characteristic.moshnost_otdel_sloev_sred,
                "usloviya_zaleganiya_naprav_prostiraniya_ot": characteristic.usloviya_zaleganiya_naprav_prostiraniya_ot,
                "usloviya_zaleganiya_naprav_prostiraniya_do": characteristic.usloviya_zaleganiya_naprav_prostiraniya_do,
                "usloviya_zaleganiya_azimut_padeniya_ot": characteristic.usloviya_zaleganiya_azimut_padeniya_ot,
                "usloviya_zaleganiya_azimut_padeniya_do": characteristic.usloviya_zaleganiya_azimut_padeniya_do,
                "usloviya_zaleganiya_ugol_padeniya_ot": characteristic.usloviya_zaleganiya_ugol_padeniya_ot,
                "usloviya_zaleganiya_ugol_padeniya_do": characteristic.usloviya_zaleganiya_ugol_padeniya_do,
                "usloviya_zaleganiya_ugol_padeniya_sred": characteristic.usloviya_zaleganiya_ugol_padeniya_sred,
                "usloviya_zaleganiya_glubina_zaleganiya_ot": characteristic.usloviya_zaleganiya_glubina_zaleganiya_ot,
                "usloviya_zaleganiya_glubina_zaleganiya_do": characteristic.usloviya_zaleganiya_glubina_zaleganiya_do,
                "usloviya_zaleganiya_glubina_zaleganiya_sred": characteristic.usloviya_zaleganiya_glubina_zaleganiya_sred,
                "moshnost_zoni_vivetrivaniya_ot": characteristic.moshnost_zoni_vivetrivaniya_ot,
                "moshnost_zoni_vivetrivaniya_do": characteristic.moshnost_zoni_vivetrivaniya_do,
                "moshnost_zoni_vivetrivaniya_sred": characteristic.moshnost_zoni_vivetrivaniya_sred,
                "moshnost_zoni_chastichogo_vivetrivaniya_ot": characteristic.moshnost_zoni_chastichogo_vivetrivaniya_ot,
                "moshnost_zoni_chastichogo_vivetrivaniya_do": characteristic.moshnost_zoni_chastichogo_vivetrivaniya_do,
                "moshnost_zoni_chastichogo_vivetrivaniya_sred": characteristic.moshnost_zoni_chastichogo_vivetrivaniya_sred,
                "moshnost_vskrishi_ot": characteristic.moshnost_vskrishi_ot,
                "moshnost_vskrishi_do": characteristic.moshnost_vskrishi_do,
                "moshnost_vskrishi_sred": characteristic.moshnost_vskrishi_sred,
                "moshnost_otlojeniy_ot": characteristic.moshnost_otlojeniy_ot,
                "moshnost_otlojeniy_do": characteristic.moshnost_otlojeniy_do,
                "moshnost_otlojeniy_sred": characteristic.moshnost_otlojeniy_sred,
                "lineynaya_plotnost_treshin": characteristic.lineynaya_plotnost_treshin,
                "zakarstovannost": characteristic.zakarstovannost,
                "zapolnitel_kresta": characteristic.zapolnitel_kresta,
                "kratkoe_opisanie": characteristic.kratkoe_opisanie
            }
        }, 200)
    except:
        return jsonify({
            "auth_fail": False,
            "result": False
        }, 500)


@mod_api.route("/get_deposit_types/", methods=["POST"])
def get_deposit_types():
    if not is_valid_session(request, config):
        return jsonify({"auth_fail": True}, 403)
    if not has_permissions(db, get_role(request, config), "/api/get_deposit_types/"):
        return jsonify({"auth_fail": True, "access_denied": True, "reason": "Доступ запрещен"}, 403)

    types = db.session.query(TipMestorogdeniya).all()
    result = [];
    for t in types:
        result.append({
            "type": t.opisanie,
            "id": t.tip_id
        })
    return jsonify({
        "auth_fail": False,
        "result": result
    }, 200)


@mod_api.route("/update_deposit/", methods=["POST"])
def update_deposit():
    if not is_valid_session(request, config):
        return jsonify({"auth_fail": True}, 403)
    if not has_permissions(db, get_role(request, config), "/api/update_deposit/"):
        return jsonify({"auth_fail": True, "access_denied": True, "reason": "Доступ запрещен"}, 403)
    data = request.get_json(force=True)
    if not data:
        return jsonify({"auth_fail": False, "result": False}, 400)
    try:
        deposit_id = data.get("deposit_id", None)
        deposit_name = data.get("deposit_name", None)
        description = data.get("description", None)
        dev_id = data.get("development_id", None)
        area_id = data.get("area_id", None)
        district_id = data.get("district_id", None)

        area = db.session.query(Oblasti). \
            filter(db.and_(Oblasti.id_respubliki == 1,
                           Oblasti.id_oblasti == area_id,
                           Oblasti.id_rayona == 0)).\
            one()
        if not area:
            return jsonify({"auth_fail": False, "result": False}, 400)

        district = db.session.query(Oblasti). \
            filter(db.and_(Oblasti.id_respubliki == 1,
                           Oblasti.id_oblasti == area_id,
                           Oblasti.id_rayona == district_id)).\
            one()
        if not district:
            return jsonify({"auth_fail": False, "result": False}, 400)
        if not deposit_id or not deposit_name:
            return jsonify({"auth_fail": False, "result": False}, 400)
        deposit_dup_count = db.session.query(Mestorogdeniya).\
            filter(db.and_(Mestorogdeniya.naimenovanie.ilike(deposit_name),
                           Mestorogdeniya.id_mestorojdeniya == Mestorogdeniya.id_uchastka,
                           Mestorogdeniya.id_mestorojdeniya != deposit_id)). \
            count()
        if deposit_dup_count > 0:
            return jsonify({"auth_fail": False, "result": False, "reason": "Данное месторождение уже существует"}, 400)
        deposit = db.session.query(Mestorogdeniya).\
            filter(db.and_(Mestorogdeniya.id_mestorojdeniya == deposit_id,
                           Mestorogdeniya.id_uchastka == deposit_id)). \
            one()
        if not deposit:
            return jsonify({"auth_fail": False, "result": False}, 404)
        deposit.naimenovanie = deposit_name
        deposit.opisanie = description
        deposit.id_osvoyeniya = dev_id
        deposit.id_oblast = area.id_oblasti
        deposit.id_rayon = district.id_rayona
        db.session.commit()
        mine_areas = db.session.query(Mestorogdeniya).\
            filter(db.and_(Mestorogdeniya.id_mestorojdeniya == deposit_id,
                           Mestorogdeniya.id_uchastka != deposit_id)). \
            all()
        for mine_area in mine_areas:
            mine_area.id_oblast = area.id
            mine_area.id_rayon = district_id.id
            db.session.commit()
        return jsonify({"auth_fail": False, "result": True}, 200)
    except Exception as e:
        return jsonify({"auth_fail": False, "result": False}, 404)

@mod_api.route("/has_mine_areas/", methods=["POST"])
def has_mine_areas():
    if not is_valid_session(request, config):
        return jsonify({"auth_fail": True}, 403)
    if not has_permissions(db, get_role(request, config), "/api/has_mine_areas/"):
        return jsonify({"auth_fail": True, "access_denied": True, "reason": "Доступ запрещен"}, 403)
    data = request.get_json(force=True)
    if not data:
        return jsonify({"auth_fail": False, "result": False}, 400)
    deposit_id = data.get("deposit_id", None)
    try:
        total = db.session.query(Mestorogdeniya). \
            filter(db.and_(Mestorogdeniya.id_mestorojdeniya != Mestorogdeniya.id_uchastka,
                    Mestorogdeniya.id_mestorojdeniya == deposit_id)).count()
    except:
        total = 0
    return jsonify({
        "auth_fail": False,
        "result": total > 0
    }, 200)

@mod_api.route("/delete_deposit/", methods=["POST"])
def delete_deposit():
    if not is_valid_session(request, config):
        return jsonify({"auth_fail": True}, 403)
    if not has_permissions(db, get_role(request, config), "/api/delete_deposit/"):
        return jsonify({"auth_fail": True, "access_denied": True, "reason": "Доступ запрещен"}, 403)
    data = request.get_json(force=True)
    if not data:
        return jsonify({"auth_fail": False, "result": False}, 400)
    deposit_id = data.get("deposit_id", None)
    if not deposit_id:
        return jsonify({"auth_fail": False, "result": False}, 400)
    try:

        mine_areas = db.session.query(Mestorogdeniya). \
            filter(db.and_(Mestorogdeniya.id_mestorojdeniya == deposit_id,
                Mestorogdeniya.id_uchastka != deposit_id)). \
            all()
        for mine_area in mine_areas:
            print("DROPING MINE AREA " + mine_area.naimenovanie)
            db.session.delete(mine_area)
            db.session.commit()
        
        deposit = db.session.query(Mestorogdeniya). \
            filter(db.and_(Mestorogdeniya.id_mestorojdeniya == deposit_id)). \
            first()
        db.session.delete(deposit)
        db.session.commit()
        return jsonify({
            "auth_fail": False,
            "result": True
        }, 200)
    except Exception as a:
        print(a);
        return jsonify({
            "auth_fail": False,
            "result": False
        }, 500)


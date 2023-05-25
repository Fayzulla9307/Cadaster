from app import db

class Oblasti(db.Model):
	"""
	Areas and districts reference table
	"""
	__tablename__ = "Oblasti";

	id_respubliki      = db.Column(db.Integer,  nullable=False, primary_key=True, default=1)
	id_oblasti         = db.Column(db.Integer,  nullable=False, primary_key=True, default=0)
	id_rayona          = db.Column(db.Integer,      nullable=False, primary_key=True, default=0)
	opisanie           = db.Column(db.String(100),  nullable=False, default="Узбекистан")

class SpravochnikiKategorii(db.Model):
	"""
	Types of categories
	"""
	__tablename__      = "SpravochnikiKategorii"
	kategoriya         = db.Column(db.String(100), nullable = False, primary_key = True)
	opisanie           = db.Column(db.String(1000), nullable = False)

class Spravochniki(db.Model):
	"""
	General reference table
	"""
	__tablename__      = "Spravochniki";
	id_zapisy          = db.Column(db.Integer, primary_key = True, autoincrement=True)
	kategoriya         = db.Column(db.String(100), db.ForeignKey("SpravochnikiKategorii.kategoriya"), nullable = False)
	znachenie          = db.Column(db.String(1000), nullable = False, default = "")
	kod                = db.Column(db.String(100), nullable = True, default = "")

class GruppaItogov(db.Model):
	"""
	Resource group table
	"""
	__tablename__            = "GruppaItogov";

	id                       = db.Column(db.Integer, primary_key = True, autoincrement=True)
	nazvanie_gruppi          = db.Column(db.String(100), nullable = False)
	kod                      = db.Column(db.String(100), nullable = True, default = None)

class GruppaItogovSopostavlenie(db.Model):
	"""
	Resource group mapping table
	"""
	__tablename__            = "GruppaItogovSopostavlenie";

	id                       = db.Column(db.Integer, primary_key = True, autoincrement=True)
	
	id_poleznogo_iskopaemogo = db.Column(db.Integer, db.ForeignKey("Spravochniki.id_zapisy"), nullable = False)
	id_primeneniya           = db.Column(db.Integer, db.ForeignKey("Spravochniki.id_zapisy"), nullable = False)
	id_gruppi                = db.Column(db.Integer, db.ForeignKey("GruppaItogov.id"), nullable = False)

	poleznoe_iskoaemoe = db.relationship("Spravochniki", foreign_keys=[id_poleznogo_iskopaemogo])
	oblast_primeneniya = db.relationship("Spravochniki", foreign_keys=[id_primeneniya])
	gruppa_itogov      = db.relationship("GruppaItogov", foreign_keys=[id_gruppi])

class TipMestorogdeniya(db.Model):
	"""
	Deposits table
	"""
	__tablename__      = "TipMestorogdeniya";

	opisanie           = db.Column(db.String(1000), nullable = False, primary_key = False)
	tip_id             = db.Column(db.String(100), nullable = False, primary_key = True)

class Mestorogdeniya(db.Model):
	"""
	Deposits table
	"""
	__tablename__      = "Mestorogdeniya";

	id_mestorojdeniya  = db.Column(db.Integer, nullable = False, primary_key = True)
	id_uchastka        = db.Column(db.Integer, nullable = False, primary_key = True)
	id_oblast          = db.Column(db.Integer, db.ForeignKey("Oblasti.id_oblasti"), nullable = False)
	id_rayon           = db.Column(db.Integer, db.ForeignKey("Oblasti.id_rayona"), nullable = False)
	id_osvoyeniya      = db.Column(db.Integer, db.ForeignKey("Spravochniki.id_zapisy"), nullable = False)
	naimenovanie       = db.Column(db.String(400), nullable = False)
	opisanie           = db.Column(db.String(1000), nullable = True)
	tip_id             = db.Column(db.String(100), db.ForeignKey("TipMestorogdeniya.tip_id"), nullable = False, default = 1)

class Koordinati(db.Model):
	"""
	Deposit coordinates
	"""

	__tablename__      = "Koordinati"

	id_mestorojdeniya  = db.Column(db.Integer, nullable = False, primary_key = True)
	id_uchastka        = db.Column(db.Integer, nullable = False, primary_key = True)
	dolgota            = db.Column(db.Float, nullable = False, default = 0.0)
	shirota            = db.Column(db.Float, nullable = False, default = 0.0)

	__table_args__ = (db.ForeignKeyConstraint([id_mestorojdeniya, id_uchastka],
                                           [Mestorogdeniya.id_mestorojdeniya, Mestorogdeniya.id_uchastka]),
                      {})

class JDStancii(db.Model):
	"""
	Closest inhabited areas
	"""

	__tablename__      = "JDStancii"
	
	id_mestorojdeniya  = db.Column(db.Integer, nullable = False, primary_key = True)
	id_uchastka        = db.Column(db.Integer, nullable = False, primary_key = True)
	naimenovanie       = db.Column(db.String(100), nullable = False)
	rasstoyanie        = db.Column(db.String(100), nullable = False)

	__table_args__ = (db.ForeignKeyConstraint([id_mestorojdeniya, id_uchastka],
                                           [Mestorogdeniya.id_mestorojdeniya, Mestorogdeniya.id_uchastka]),
                      {})

class NaselenniePunkti(db.Model):
	"""
	Closest inhabited areas
	"""

	__tablename__      = "NaselenniePunkti"
	
	id_mestorojdeniya  = db.Column(db.Integer, nullable = False, primary_key = True)
	id_uchastka        = db.Column(db.Integer, nullable = False, primary_key = True)
	naimenovanie       = db.Column(db.String(100), nullable = False)
	napravlenie        = db.Column(db.String(100), nullable = False)
	rasstoyanie        = db.Column(db.String(100), nullable = False)

	__table_args__ = (db.ForeignKeyConstraint([id_mestorojdeniya, id_uchastka],
                                           [Mestorogdeniya.id_mestorojdeniya, Mestorogdeniya.id_uchastka]),
                      {})


class Expedicii(db.Model):
	"""
	Expeditions table
	"""
	__tablename__      = "Expedicii";

	id_mestorojdeniya  = db.Column(db.Integer, nullable = False, primary_key = True)
	id_uchastka        = db.Column(db.Integer, nullable = False, primary_key = True)
	id_vedomstva       = db.Column(db.Integer, nullable = False, primary_key = True)

	data_ot            = db.Column(db.Date, nullable = False)
	data_do            = db.Column(db.Date, nullable = False)
	
	opisanie           = db.Column(db.String(1000))

	__table_args__ = (db.ForeignKeyConstraint([id_mestorojdeniya, id_uchastka],
                                           [Mestorogdeniya.id_mestorojdeniya, Mestorogdeniya.id_uchastka]),
                      {})

class Resurs(db.Model):
	"""
	Reserves table
	"""
	__tablename__      = "Resurs";

	id_resursa         = db.Column(db.Integer, nullable = False, autoincrement=True, primary_key = True)
	id_mestorojdeniya   = db.Column(db.Integer, nullable = False)
	id_uchastka        = db.Column(db.Integer, nullable = False)
	id_poleznogo_iskopaemogo = db.Column(db.Integer, db.ForeignKey("Spravochniki.id_zapisy"), nullable = False)
	id_primeneniya     = db.Column(db.Integer, db.ForeignKey("Spravochniki.id_zapisy"), nullable = False)
	id_ed_izmereniya_rudi = db.Column(db.Integer, db.ForeignKey("Spravochniki.id_zapisy"), nullable = False)
	A                  = db.Column(db.Float, nullable = False, default = 0.0)
	B                  = db.Column(db.Float, nullable = False, default = 0.0)
	C1                 = db.Column(db.Float, nullable = False, default = 0.0)
	C2                 = db.Column(db.Float, nullable = False, default = 0.0)
	zabalans           = db.Column(db.Float, nullable = False, default = 0.0)
	zapasi_dlya_pol_iskopaemogo = db.Column(db.Boolean, nullable = False, default = True)
	id_ed_izmereniya_poleznogo_iskopayemogo = db.Column(db.Integer, db.ForeignKey("Spravochniki.id_zapisy"), nullable = True)
	PI_A               = db.Column(db.Float, nullable = True, default = 0.0)
	PI_B               = db.Column(db.Float, nullable = True, default = 0.0)
	PI_C1              = db.Column(db.Float, nullable = True, default = 0.0)
	PI_C2              = db.Column(db.Float, nullable = True, default = 0.0)
	PI_zabalans        = db.Column(db.Float, nullable = True, default = 0.0)
	id_himicheskogo_komponenta = db.Column(db.Integer, db.ForeignKey("Spravochniki.id_zapisy"), nullable = True)
	id_himicheskoy_formuli = db.Column(db.Integer, db.ForeignKey("Spravochniki.id_zapisy"), nullable = True)
	id_gosta           = db.Column(db.Integer, db.ForeignKey("Spravochniki.id_zapisy"), nullable = True)
	data_utverjdeniya  = db.Column(db.Date, nullable = True)
	god_utverjdeniya   = db.Column(db.String(4), nullable = True)
	nomer_protocola    = db.Column(db.String(100), nullable = True)
	organizaciya_utverdivshaya = db.Column(db.String(1000), nullable = True)
	id_gruppi          = db.Column(db.Integer, db.ForeignKey("GruppaItogov.id"), nullable = False)
	#opisanie           = db.Column(db.String(1000), nullable = True)

	poleznoe_iskoaemoe = db.relationship("Spravochniki", foreign_keys=[id_poleznogo_iskopaemogo])
	oblast_primeneniya = db.relationship("Spravochniki", foreign_keys=[id_primeneniya])
	mestorogdenie = db.relationship("Mestorogdeniya", foreign_keys=[id_mestorojdeniya, id_uchastka])
	
	__table_args__ = (db.ForeignKeyConstraint([id_mestorojdeniya, id_uchastka],
                                           [Mestorogdeniya.id_mestorojdeniya, Mestorogdeniya.id_uchastka]),
                      {})

class ResursInformaciya(db.Model):
	"""
	Reserve information table
	"""

	__tablename__      = "ResursInformaciya"

	id_resursa         = db.Column(db.Integer, nullable = False, autoincrement=True, primary_key = True)
	id_mestorojdeniya   = db.Column(db.Integer, nullable = False, primary_key = True)
	id_uchastka        = db.Column(db.Integer, nullable = False, primary_key = True)
	id_poleznogo_iskopaemogo = db.Column(db.Integer, db.ForeignKey("Spravochniki.id_zapisy"), nullable = False, primary_key = True)
	id_primeneniya     = db.Column(db.Integer, db.ForeignKey("Spravochniki.id_zapisy"), nullable = False, primary_key = True)
	
	srednee_soderjanie = db.Column(db.String(100), nullable = True)
	proizvodetelnost   = db.Column(db.String(100), nullable = True)
	glubina            = db.Column(db.String(100), nullable = True)

	__table_args__ = (db.ForeignKeyConstraint([id_resursa, id_mestorojdeniya, id_uchastka, id_poleznogo_iskopaemogo, id_primeneniya],
                                           [Resurs.id_resursa, Resurs.id_mestorojdeniya, Resurs.id_uchastka, Resurs.id_poleznogo_iskopaemogo, Resurs.id_primeneniya]),
                      {})

class Litsenzii(db.Model):
	"""
	Licenses table
	"""
	__tablename__      = "Litsenzii"

	id_mestorojdeniya  = db.Column(db.Integer, nullable = False)
	id_uchastka        = db.Column(db.Integer, nullable = False)
	id_litsenzii       = db.Column(db.Integer, nullable = False, primary_key = True, autoincrement = True)

	A                  = db.Column(db.Float, nullable = False, default = 0.0)
	B                  = db.Column(db.Float, nullable = False, default = 0.0)
	C1                 = db.Column(db.Float, nullable = False, default = 0.0)
	C2                 = db.Column(db.Float, nullable = False, default = 0.0)
	zabalans           = db.Column(db.Float, nullable = False, default = 0.0)

	PI_A               = db.Column(db.Float, nullable = False, default = 0.0)
	PI_B               = db.Column(db.Float, nullable = False, default = 0.0)
	PI_C1              = db.Column(db.Float, nullable = False, default = 0.0)
	PI_C2              = db.Column(db.Float, nullable = False, default = 0.0)
	PI_zabalans        = db.Column(db.Float, nullable = False, default = 0.0)

	nomer_litsenzii    = db.Column(db.String(100), nullable = False)
	id_resursa         = db.Column(db.Integer, nullable = False)
	id_vedomstva       = db.Column(db.Integer, db.ForeignKey("Spravochniki.id_zapisy"), nullable = False)
	opisanie           = db.Column(db.Text)

	data_ot            = db.Column(db.Date, nullable = True)
	data_do            = db.Column(db.Date, nullable = True)

	na_balanse_gkg     = db.Column(db.Boolean, nullable = False, default = False)

	__table_args__ = (db.ForeignKeyConstraint([id_mestorojdeniya, id_uchastka],
                                           [Mestorogdeniya.id_mestorojdeniya, Mestorogdeniya.id_uchastka]),
					db.ForeignKeyConstraint([id_resursa],
                                           [Resurs.id_resursa]),
                      {})
	mestorogdenie = db.relationship("Mestorogdeniya", foreign_keys=[id_mestorojdeniya, id_mestorojdeniya])
	uchastok = db.relationship("Mestorogdeniya", foreign_keys=[id_mestorojdeniya, id_uchastka])
	reserve = db.relationship("Resurs", foreign_keys=[id_resursa]);

class Forma5GR(db.Model):
	"""
	Reserves movement table one record per one year
	"""
	__tablename__      = "5GR"

	id_mestorojdeniya  = db.Column(db.Integer, nullable = False, primary_key = True)
	id_uchastka        = db.Column(db.Integer, nullable = False, primary_key = True)
	id_litsenzii       = db.Column(db.Integer, nullable = False, primary_key = True)
	god                = db.Column(db.Integer, nullable = False, primary_key = True)
	opisaniye          = db.Column(db.Text)

	__table_args__ = (db.ForeignKeyConstraint([id_mestorojdeniya, id_uchastka, id_litsenzii],
                                           [Litsenzii.id_mestorojdeniya, Litsenzii.id_uchastka, Litsenzii.id_litsenzii]),
                      {})

class Forma5GR_Dvijene(db.Model):
	__tablename__      = "5GR_Dvijene"

	id_mestorojdeniya  = db.Column(db.Integer, nullable = False, primary_key = True)
	id_uchastka        = db.Column(db.Integer, nullable = False, primary_key = True)
	id_litsenzii       = db.Column(db.Integer, nullable = False, primary_key = True)
	god                = db.Column(db.Integer, nullable = False, primary_key = True)
	kategoriya_zapasov = db.Column(db.String(100), nullable = False, primary_key = True)
	ruda               = db.Column(db.Boolean, default = False, nullable = False)
	data               = db.Column(db.Date, nullable = True)
	dobicha            = db.Column(db.Float, default = 0.0)
	poteri             = db.Column(db.Float, default = 0.0)
	razvedka           = db.Column(db.Float, default = 0.0)
	izmenenie          = db.Column(db.Float, default = 0.0)
	spisano            = db.Column(db.Float, default = 0.0)
	drugoe             = db.Column(db.Float, default = 0.0)
	ostatok_na_konec_goda = db.Column(db.Float, default = 0.0)
	ostatok_na_nachalo_goda = db.Column(db.Float, default = 0.0)

	__table_args__ = (db.ForeignKeyConstraint([id_mestorojdeniya, id_uchastka, id_litsenzii, god],
                                           [Forma5GR.id_mestorojdeniya, Forma5GR.id_uchastka, Forma5GR.id_litsenzii, Forma5GR.god]),
                      {})

class KadastrTitul(db.Model):
	__tablename__                = "KadastrTitul";

	id_mestorojdeniya            = db.Column(db.Integer, nullable = False, primary_key = True)
	id_uchastka                  = db.Column(db.Integer, nullable = False, primary_key = True)
	id_poleznogo_iskopaemogo     = db.Column(db.Integer, nullable = False, primary_key = True)

	razdel                       = db.Column(db.String(100), default = "", nullable = True)
	gos_balans                   = db.Column(db.String(5), default = "", nullable = True)
	sostavil_fio                 = db.Column(db.String(150), default = "", nullable = True)
	data_sostavleniya            = db.Column(db.Date, nullable = True)
	utverdil_fio                 = db.Column(db.String(100), default = "", nullable = True)
	god                          = db.Column(db.Integer, nullable = True)
	data                         = db.Column(db.Date, nullable = True)

class KadastrObshayaInformaciya(db.Model):
	__tablename__                = "KadastrObshayaInformaciya"

	id                           = db.Column(db.Integer, nullable = False, autoincrement=True, primary_key = True)
	id_mestorojdeniya            = db.Column(db.Integer, nullable = False)
	id_uchastka                  = db.Column(db.Integer, nullable = False)
	id_poleznogo_iskopaemogo     = db.Column(db.Integer, nullable = False)
	nomenklatura                 = db.Column(db.String(100), nullable = False, default = "")
	id_vedomstva                 = db.Column(db.Integer, db.ForeignKey("Spravochniki.id_zapisy"), nullable = True)
	pityevaya_voda_nazvanie      = db.Column(db.String(1000), nullable = False, default = "")
	pityevaya_voda_rast          = db.Column(db.String(1000), nullable = False, default = "")
	tehnicheskaya_voda_nazvanie  = db.Column(db.String(1000), nullable = False, default = "")
	tehnicheskaya_voda_rast      = db.Column(db.String(1000), nullable = False, default = "")
	elektrichestvo_nazvanie      = db.Column(db.String(1000), nullable = False, default = "")
	elektrichestvo_rast          = db.Column(db.String(1000), nullable = False, default = "")
	absolyutnaya_otmetka_min     = db.Column(db.Float, default = 0.0)
	absolyutnaya_otmetka_max     = db.Column(db.Float, default = 0.0)
	id_tip_relyefa               = db.Column(db.Integer,db.ForeignKey("Spravochniki.id_zapisy"), nullable = True)
	seysmichnost                 = db.Column(db.Float, default = 0.0)
	id_seleopasnost              = db.Column(db.Integer,db.ForeignKey("Spravochniki.id_zapisy"), nullable = True)
	id_opolzneopasnost           = db.Column(db.Integer,db.ForeignKey("Spravochniki.id_zapisy"), nullable = True)
	prinadlejnost_zemel          = db.Column(db.Text)
	id_tip_zemel                 = db.Column(db.Integer, db.ForeignKey("Spravochniki.id_zapisy"), nullable = True)
	razmer_dlina                 = db.Column(db.Float, default = 0.0)
	razmer_shirina               = db.Column(db.Float, default = 0.0)
	ploshad                      = db.Column(db.Float, default = 0.0)
	ploshad_utverjdennih_zapasov = db.Column(db.Float, default = 0.0)

	__table_args__ = (db.ForeignKeyConstraint([id_mestorojdeniya, id_uchastka, id_poleznogo_iskopaemogo],
                                           [KadastrTitul.id_mestorojdeniya, KadastrTitul.id_uchastka, KadastrTitul.id_poleznogo_iskopaemogo]),
                      {})

	

class KadastrIzuchennost(db.Model):
	__tablename__                = "KadastrIzuchennost";

	id                           = db.Column(db.Integer, nullable = False, autoincrement=True, primary_key = True)
	id_mestorojdeniya            = db.Column(db.Integer, nullable = False)
	id_uchastka                  = db.Column(db.Integer, nullable = False)
	id_poleznogo_iskopaemogo     = db.Column(db.Integer, nullable = False)
	god                          = db.Column(db.Integer, nullable = False)
	id_stadii_izuchennost        = db.Column(db.Integer, db.ForeignKey("Spravochniki.id_zapisy"), nullable = True)

	__table_args__ = (db.ForeignKeyConstraint([id_mestorojdeniya, id_uchastka, id_poleznogo_iskopaemogo],
                                           [KadastrTitul.id_mestorojdeniya, KadastrTitul.id_uchastka, KadastrTitul.id_poleznogo_iskopaemogo]),
                      {})

class KadastrKoordinatu(db.Model):
	__tablename__                = "KadastrKoordinatu";

	id                           = db.Column(db.Integer, nullable = False, autoincrement=True, primary_key = True)
	id_mestorojdeniya            = db.Column(db.Integer, nullable = False)
	id_uchastka                  = db.Column(db.Integer, nullable = False)
	id_poleznogo_iskopaemogo     = db.Column(db.Integer, nullable = False)

	dolgota                      = db.Column(db.Float, default = 0.0)
	shirota                      = db.Column(db.Float, default = 0.0)

	__table_args__ = (db.ForeignKeyConstraint([id_mestorojdeniya, id_uchastka, id_poleznogo_iskopaemogo],
                                           [KadastrTitul.id_mestorojdeniya, KadastrTitul.id_uchastka, KadastrTitul.id_poleznogo_iskopaemogo]),
                      {})

class KadastrGeoHarakteristiki(db.Model):
	__tablename__                = "KadastrGeoHarakteristiki";

	id                           = db.Column(db.Integer, nullable = False, autoincrement=True, primary_key = True)
	id_mestorojdeniya            = db.Column(db.Integer, nullable = False)
	id_uchastka                  = db.Column(db.Integer, nullable = False)
	id_poleznogo_iskopaemogo     = db.Column(db.Integer, nullable = False)
	id_gruppi                    = db.Column(db.Integer, db.ForeignKey("Spravochniki.id_zapisy"), nullable = True)
	id_tip_slojnosti             = db.Column(db.Integer, db.ForeignKey("Spravochniki.id_zapisy"), nullable = True)
	porodi_slag_pol_iskopaemoe   = db.Column(db.String(1000), default = "")
	id_forma_tel                 = db.Column(db.Integer, db.ForeignKey("Spravochniki.id_zapisy"), nullable = True)
	kolichestvo_tel              = db.Column(db.Integer, nullable = False, default = 0)

	razmer_tel_dlina_po_protstiraniyu_ot         = db.Column(db.Float, nullable = False, default = 0)
	razmer_tel_dlina_po_protstiraniyu_do         = db.Column(db.Float, nullable = False, default = 0)
	razmer_tel_dlina_po_protstiraniyu_sred       = db.Column(db.Float, nullable = False, default = 0)
	moshnost_obshaya_ot                          = db.Column(db.Float, nullable = False, default = 0)
	moshnost_obshaya_do                          = db.Column(db.Float, nullable = False, default = 0)
	moshnost_obshaya_sred                        = db.Column(db.Float, nullable = False, default = 0)
	moshnost_vskritaya_ot                        = db.Column(db.Float, nullable = False, default = 0)
	moshnost_vskritaya_do                        = db.Column(db.Float, nullable = False, default = 0)
	moshnost_vskritaya_sred                      = db.Column(db.Float, nullable = False, default = 0)
	moshnost_pod_zapasov_ot                      = db.Column(db.Float, nullable = False, default = 0)
	moshnost_pod_zapasov_do                      = db.Column(db.Float, nullable = False, default = 0)
	moshnost_pod_zapasov_sred                    = db.Column(db.Float, nullable = False, default = 0)
	moshnost_otdel_sloev_ot                      = db.Column(db.Float, nullable = False, default = 0)
	moshnost_otdel_sloev_do                      = db.Column(db.Float, nullable = False, default = 0)
	moshnost_otdel_sloev_sred                    = db.Column(db.Float, nullable = False, default = 0)
	usloviya_zaleganiya_naprav_prostiraniya_ot   = db.Column(db.Float, nullable = False, default = 0)
	usloviya_zaleganiya_naprav_prostiraniya_do   = db.Column(db.Float, nullable = False, default = 0)
	usloviya_zaleganiya_azimut_padeniya_ot       = db.Column(db.Float, nullable = False, default = 0)
	usloviya_zaleganiya_azimut_padeniya_do       = db.Column(db.Float, nullable = False, default = 0)
	usloviya_zaleganiya_ugol_padeniya_ot         = db.Column(db.Float, nullable = False, default = 0)
	usloviya_zaleganiya_ugol_padeniya_do         = db.Column(db.Float, nullable = False, default = 0)
	usloviya_zaleganiya_ugol_padeniya_sred       = db.Column(db.Float, nullable = False, default = 0)
	usloviya_zaleganiya_glubina_zaleganiya_ot    = db.Column(db.Float, nullable = False, default = 0)
	usloviya_zaleganiya_glubina_zaleganiya_do    = db.Column(db.Float, nullable = False, default = 0)
	usloviya_zaleganiya_glubina_zaleganiya_sred  = db.Column(db.Float, nullable = False, default = 0)
	moshnost_zoni_vivetrivaniya_ot               = db.Column(db.Float, nullable = False, default = 0)
	moshnost_zoni_vivetrivaniya_do               = db.Column(db.Float, nullable = False, default = 0)
	moshnost_zoni_vivetrivaniya_sred             = db.Column(db.Float, nullable = False, default = 0)
	moshnost_zoni_chastichogo_vivetrivaniya_ot   = db.Column(db.Float, nullable = False, default = 0)
	moshnost_zoni_chastichogo_vivetrivaniya_do   = db.Column(db.Float, nullable = False, default = 0)
	moshnost_zoni_chastichogo_vivetrivaniya_sred = db.Column(db.Float, nullable = False, default = 0)
	moshnost_vskrishi_ot                         = db.Column(db.Float, nullable = False, default = 0)
	moshnost_vskrishi_do                         = db.Column(db.Float, nullable = False, default = 0)
	moshnost_vskrishi_sred                       = db.Column(db.Float, nullable = False, default = 0)
	moshnost_otlojeniy_ot                        = db.Column(db.Float, nullable = False, default = 0)
	moshnost_otlojeniy_do                        = db.Column(db.Float, nullable = False, default = 0),
	moshnost_otlojeniy_sred                      = db.Column(db.Float, nullable = False, default = 0)
	lineynaya_plotnost_treshin                   = db.Column(db.Float, nullable = False, default = 0)
	zakarstovannost                              = db.Column(db.Float, nullable = False, default = 0)
	zapolnitel_kresta                            = db.Column(db.Float, nullable = False, default = 0)
	kratkoe_opisanie                             = db.Column(db.Text, nullable = True)

	__table_args__ = (db.ForeignKeyConstraint([id_mestorojdeniya, id_uchastka, id_poleznogo_iskopaemogo],
                                           [KadastrTitul.id_mestorojdeniya, KadastrTitul.id_uchastka, KadastrTitul.id_poleznogo_iskopaemogo]),
                      {})
	
class KadastrProsloiPustihPorod(db.Model):
	__tablename__                = "KadastrProsloiPustihPorod";

	id                           = db.Column(db.Integer, nullable = False, autoincrement=True, primary_key = True)
	id_geo_harakteristiki        = db.Column(db.Integer, db.ForeignKey("KadastrGeoHarakteristiki.id"), nullable = False)
	nazvanie                     = db.Column(db.String(10000), default = "")
	moshnost_ot                  = db.Column(db.Float, nullable = False, default = 0)
	moshnost_do                  = db.Column(db.Float, nullable = False, default = 0)
	moshnost_sred                = db.Column(db.Float, nullable = False, default = 0)

class KadastrVmeshayushiePorodi(db.Model):
	__tablename__                = "KadastrVmeshayushiePorodi";

	id                           = db.Column(db.Integer, nullable = False, autoincrement=True, primary_key = True)
	id_geo_harakteristiki        = db.Column(db.Integer, db.ForeignKey("KadastrGeoHarakteristiki.id"), nullable = False)
	polojenie                    = db.Column(db.String(1000), default = "")
	raznosti_poro                = db.Column(db.String(1000), default = "")
	geologicheskiy_vozrast       = db.Column(db.String(1000), default = "")

class KadastrKachestvennayaHarakteristika(db.Model):
	__tablename__                = "KadastrKachestvennayaHarakteristika";

	id                           = db.Column(db.Integer, nullable = False, autoincrement=True, primary_key = True)
	id_mestorojdeniya            = db.Column(db.Integer, nullable = False)
	id_uchastka                  = db.Column(db.Integer, nullable = False)
	id_poleznogo_iskopaemogo     = db.Column(db.Integer, nullable = False)

	pokazatel                    = db.Column(db.String(1000), default = "")
	id_ed_izm                    = db.Column(db.Integer, db.ForeignKey("Spravochniki.id_zapisy"), nullable = True)
	znachenie_ot                 = db.Column(db.Float, nullable = False, default = 0)
	znachenie_do                 = db.Column(db.Float, nullable = False, default = 0)
	znachenie_sred               = db.Column(db.Float, nullable = False, default = 0)

	__table_args__ = (db.ForeignKeyConstraint([id_mestorojdeniya, id_uchastka, id_poleznogo_iskopaemogo],
                                           [KadastrTitul.id_mestorojdeniya, KadastrTitul.id_uchastka, KadastrTitul.id_poleznogo_iskopaemogo]),
                      {})

class KadastrFizMehHarakteristika(db.Model):
	__tablename__                = "KadastrFizMehHarakteristika";

	id                           = db.Column(db.Integer, nullable = False, autoincrement=True, primary_key = True)
	id_mestorojdeniya            = db.Column(db.Integer, nullable = False)
	id_uchastka                  = db.Column(db.Integer, nullable = False)
	id_poleznogo_iskopaemogo     = db.Column(db.Integer, nullable = False)

	svoystva                     = db.Column(db.String(1000), default = "")
	id_ed_izm                    = db.Column(db.Integer, db.ForeignKey("Spravochniki.id_zapisy"), nullable = True)
	velichina_ot                 = db.Column(db.Float, nullable = False, default = 0)
	velichina_do                 = db.Column(db.Float, nullable = False, default = 0)
	velichina_sred               = db.Column(db.Float, nullable = False, default = 0)

	__table_args__ = (db.ForeignKeyConstraint([id_mestorojdeniya, id_uchastka, id_poleznogo_iskopaemogo],
                                           [KadastrTitul.id_mestorojdeniya, KadastrTitul.id_uchastka, KadastrTitul.id_poleznogo_iskopaemogo]),
                      {})

class KadastrProdukciya(db.Model):
	__tablename__                = "KadastrProdukciya";

	id                           = db.Column(db.Integer, nullable = False, autoincrement=True, primary_key = True)
	id_mestorojdeniya            = db.Column(db.Integer, nullable = False)
	id_uchastka                  = db.Column(db.Integer, nullable = False)
	id_poleznogo_iskopaemogo     = db.Column(db.Integer, nullable = False)

	proch_svoysva                = db.Column(db.Text)
	rezultati_ispitaniya         = db.Column(db.Text)
	vid_produkzii                = db.Column(db.String(1000), nullable = True, default = "")
	sort_produkzii               = db.Column(db.String(1000), nullable = True, default = "")
	sootvetstvie                 = db.Column(db.Text)

	__table_args__ = (db.ForeignKeyConstraint([id_mestorojdeniya, id_uchastka, id_poleznogo_iskopaemogo],
                                           [KadastrTitul.id_mestorojdeniya, KadastrTitul.id_uchastka, KadastrTitul.id_poleznogo_iskopaemogo]),
                      {})

class KadastrGeolograzvedHarakteristika(db.Model):
	__tablename__                = "KadastrGeolograzvedHarakteristika";

	id                           = db.Column(db.Integer, nullable = False, autoincrement=True, primary_key = True)
	id_mestorojdeniya            = db.Column(db.Integer, nullable = False)
	id_uchastka                  = db.Column(db.Integer, nullable = False)
	id_poleznogo_iskopaemogo     = db.Column(db.Integer, nullable = False)

	id_sistema_geologoraz_rabot  = db.Column(db.Integer, db.ForeignKey("Spravochniki.id_zapisy"), nullable = True)
	gustota_razver_seti_A        = db.Column(db.Float, nullable = False, default = 0)
	gustota_razver_seti_B        = db.Column(db.Float, nullable = False, default = 0)
	gustota_razver_seti_C1       = db.Column(db.Float, nullable = False, default = 0)
	gustota_razver_seti_C2       = db.Column(db.Float, nullable = False, default = 0)
	glubina_razvedki             = db.Column(db.Float, nullable = False, default = 0)
	vihod_kerna                  = db.Column(db.Float, nullable = False, default = 0)

	__table_args__ = (db.ForeignKeyConstraint([id_mestorojdeniya, id_uchastka, id_poleznogo_iskopaemogo],
                                           [KadastrTitul.id_mestorojdeniya, KadastrTitul.id_uchastka, KadastrTitul.id_poleznogo_iskopaemogo]),
                      {})

class KadastrTipiRabot(db.Model):
	__tablename__                = "KadastrTipiRabot";

	id                           = db.Column(db.Integer, nullable = False, autoincrement=True, primary_key = True)
	id_mestorojdeniya            = db.Column(db.Integer, nullable = False)
	id_uchastka                  = db.Column(db.Integer, nullable = False)
	id_poleznogo_iskopaemogo     = db.Column(db.Integer, nullable = False)

	tip                          = db.Column(db.String(1000), default = "")
	znachenie                    = db.Column(db.String(1000), default = "")

	__table_args__ = (db.ForeignKeyConstraint([id_mestorojdeniya, id_uchastka, id_poleznogo_iskopaemogo],
                                           [KadastrTitul.id_mestorojdeniya, KadastrTitul.id_uchastka, KadastrTitul.id_poleznogo_iskopaemogo]),
                      {})

class KadastrKondicii(db.Model):
	__tablename__                = "KadastrKondicii";

	id                           = db.Column(db.Integer, nullable = False, autoincrement=True, primary_key = True)
	id_mestorojdeniya            = db.Column(db.Integer, nullable = False)
	id_uchastka                  = db.Column(db.Integer, nullable = False)
	id_poleznogo_iskopaemogo     = db.Column(db.Integer, nullable = False)

	vid                          = db.Column(db.String(1000), default = "")
	kem_razrabotan               = db.Column(db.String(1000), default = "")
	nomer_protokola              = db.Column(db.String(1000), default = "")
	sostav                       = db.Column(db.Text)

	__table_args__ = (db.ForeignKeyConstraint([id_mestorojdeniya, id_uchastka, id_poleznogo_iskopaemogo],
                                           [KadastrTitul.id_mestorojdeniya, KadastrTitul.id_uchastka, KadastrTitul.id_poleznogo_iskopaemogo]),
                      {})

class KadastrSvedeniyaOZapasah(db.Model):
	__tablename__                = "KadastrSvedeniyaOZapasah";

	id                           = db.Column(db.Integer, nullable = False, autoincrement=True, primary_key = True)
	id_mestorojdeniya            = db.Column(db.Integer, nullable = False)
	id_uchastka                  = db.Column(db.Integer, nullable = False)
	id_poleznogo_iskopaemogo     = db.Column(db.Integer, nullable = False)

	id_vedomstva                 = db.Column(db.Integer, db.ForeignKey("Spravochniki.id_zapisy"), nullable = True)
	metod_podscheta              = db.Column(db.String(1000), default = "")
	glubina                      = db.Column(db.String(1000), default = "")

	__table_args__ = (db.ForeignKeyConstraint([id_mestorojdeniya, id_uchastka, id_poleznogo_iskopaemogo],
                                           [KadastrTitul.id_mestorojdeniya, KadastrTitul.id_uchastka, KadastrTitul.id_poleznogo_iskopaemogo]),
                      {})

class KadastrGornoGeologicheskayaHarakteristika(db.Model):
	__tablename__                = "KadastrGornoGeologicheskayaHarakteristika";

	id                           = db.Column(db.Integer, nullable = False, autoincrement=True, primary_key = True)
	id_mestorojdeniya            = db.Column(db.Integer, nullable = False)
	id_uchastka                  = db.Column(db.Integer, nullable = False)
	id_poleznogo_iskopaemogo     = db.Column(db.Integer, nullable = False)

	id_radiozionnaya_harakteristika_poroda      = db.Column(db.Integer, db.ForeignKey("Spravochniki.id_zapisy"), nullable = True)
	radiozionnaya_harakteristika_radioaktivnost = db.Column(db.Float, default = 0)
	radiozionnaya_harakteristika_klass          = db.Column(db.Integer, db.ForeignKey("Spravochniki.id_zapisy"), nullable = True)
	koef_krep_pol_iskopaemogo                   = db.Column(db.Float, default = 0)
	koef_krep_pustih_porod                      = db.Column(db.Float, default = 0)
	koef_razrihl_pol_iskopaemogo                = db.Column(db.Float, default = 0)
	koef_razrihl_pustih_porod                   = db.Column(db.Float, default = 0)
	koef_razrihl_vmeshayushih_porod             = db.Column(db.Float, default = 0)
	vodonosnie_gorizonti_glubina                = db.Column(db.String(1000), default = "")
	ojidayemiy_vodopotok                        = db.Column(db.Float, default = 0)
	him_sostav                                  = db.Column(db.String(1000), default = "")
	mineralizaciya                              = db.Column(db.Float, default = 0)

	__table_args__ = (db.ForeignKeyConstraint([id_mestorojdeniya, id_uchastka, id_poleznogo_iskopaemogo],
                                           [KadastrTitul.id_mestorojdeniya, KadastrTitul.id_uchastka, KadastrTitul.id_poleznogo_iskopaemogo]),
                      {})

class KadastrGornotehResheniya(db.Model):
	__tablename__                = "KadastrGornotehResheniya";

	id                           = db.Column(db.Integer, nullable = False, autoincrement=True, primary_key = True)
	id_mestorojdeniya            = db.Column(db.Integer, nullable = False)
	id_uchastka                  = db.Column(db.Integer, nullable = False)
	id_poleznogo_iskopaemogo     = db.Column(db.Integer, nullable = False)
	opisanie                     = db.Column(db.Text)
	__table_args__ = (db.ForeignKeyConstraint([id_mestorojdeniya, id_uchastka, id_poleznogo_iskopaemogo],
                                           [KadastrTitul.id_mestorojdeniya, KadastrTitul.id_uchastka, KadastrTitul.id_poleznogo_iskopaemogo]),
                      {})

class KadastrOkrujSreda(db.Model):
	__tablename__                = "KadastrOkrujSreda";

	id                           = db.Column(db.Integer, nullable = False, autoincrement=True, primary_key = True)
	id_mestorojdeniya            = db.Column(db.Integer, nullable = False)
	id_uchastka                  = db.Column(db.Integer, nullable = False)
	id_poleznogo_iskopaemogo     = db.Column(db.Integer, nullable = False)
	opisanie                     = db.Column(db.Text)
	__table_args__ = (db.ForeignKeyConstraint([id_mestorojdeniya, id_uchastka, id_poleznogo_iskopaemogo],
                                           [KadastrTitul.id_mestorojdeniya, KadastrTitul.id_uchastka, KadastrTitul.id_poleznogo_iskopaemogo]),
                      {})

class KadastrTehnoEkonomPokazateli(db.Model):
	__tablename__                = "KadastrTehnoEkonomPokazateli";

	id                           = db.Column(db.Integer, nullable = False, autoincrement=True, primary_key = True)
	id_mestorojdeniya            = db.Column(db.Integer, nullable = False)
	id_uchastka                  = db.Column(db.Integer, nullable = False)
	id_poleznogo_iskopaemogo     = db.Column(db.Integer, nullable = False)
	opisanie                     = db.Column(db.Text)
	zena                         = db.Column(db.String(1000), default = "")

	__table_args__ = (db.ForeignKeyConstraint([id_mestorojdeniya, id_uchastka, id_poleznogo_iskopaemogo],
                                           [KadastrTitul.id_mestorojdeniya, KadastrTitul.id_uchastka, KadastrTitul.id_poleznogo_iskopaemogo]),
                      {})


class KadastrDopolnitelnieSvedeniya(db.Model):
	__tablename__                = "KadastrDopolnitelnieSvedeniya";

	id                           = db.Column(db.Integer, nullable = False, autoincrement=True, primary_key = True)
	id_mestorojdeniya            = db.Column(db.Integer, nullable = False)
	id_uchastka                  = db.Column(db.Integer, nullable = False)
	id_poleznogo_iskopaemogo     = db.Column(db.Integer, nullable = False)
	opisanie                     = db.Column(db.Text)

	__table_args__ = (db.ForeignKeyConstraint([id_mestorojdeniya, id_uchastka, id_poleznogo_iskopaemogo],
                                           [KadastrTitul.id_mestorojdeniya, KadastrTitul.id_uchastka, KadastrTitul.id_poleznogo_iskopaemogo]),
                      {})


class KadastrIstochniki(db.Model):
	__tablename__                = "KadastrIstochniki";

	id                           = db.Column(db.Integer, nullable = False, autoincrement=True, primary_key = True)
	id_mestorojdeniya            = db.Column(db.Integer, nullable = False)
	id_uchastka                  = db.Column(db.Integer, nullable = False)
	id_poleznogo_iskopaemogo     = db.Column(db.Integer, nullable = False)
	inv_nomer                    = db.Column(db.String(1000), default = "")
	avtor                        = db.Column(db.String(100), default = "")
	naimenovanie_raboti          = db.Column(db.String(1000), default ="")

	__table_args__ = (db.ForeignKeyConstraint([id_mestorojdeniya, id_uchastka, id_poleznogo_iskopaemogo],
                                           [KadastrTitul.id_mestorojdeniya, KadastrTitul.id_uchastka, KadastrTitul.id_poleznogo_iskopaemogo]),
                      {})
	
class KadastrRazrez(db.Model):
	__tablename__                = "KadastrRazrez";

	id                           = db.Column(db.Integer, nullable = False, autoincrement=True, primary_key = True)
	id_mestorojdeniya            = db.Column(db.Integer, nullable = False)
	id_uchastka                  = db.Column(db.Integer, nullable = False)
	id_poleznogo_iskopaemogo     = db.Column(db.Integer, nullable = False)
	razrez                       = db.Column(db.BLOB)

	__table_args__ = (db.ForeignKeyConstraint([id_mestorojdeniya, id_uchastka, id_poleznogo_iskopaemogo],
                                           [KadastrTitul.id_mestorojdeniya, KadastrTitul.id_uchastka, KadastrTitul.id_poleznogo_iskopaemogo]),
                      {})

class KadastrShema(db.Model):
	__tablename__                = "KadastrShema";

	id                           = db.Column(db.Integer, nullable = False, autoincrement=True, primary_key = True)
	id_mestorojdeniya            = db.Column(db.Integer, nullable = False)
	id_uchastka                  = db.Column(db.Integer, nullable = False)
	id_poleznogo_iskopaemogo     = db.Column(db.Integer, nullable = False)
	shema                        = db.Column(db.BLOB)

	__table_args__ = (db.ForeignKeyConstraint([id_mestorojdeniya, id_uchastka, id_poleznogo_iskopaemogo],
                                           [KadastrTitul.id_mestorojdeniya, KadastrTitul.id_uchastka, KadastrTitul.id_poleznogo_iskopaemogo]),
                      {})


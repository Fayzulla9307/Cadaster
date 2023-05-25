DROP DATABASE IF EXISTS balans;

CREATE DATABASE balans;

USE balans;

CREATE TABLE IF NOT EXISTS Roli (
	id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
	rol VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS Polzovateli (
	id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
	imya VARCHAR(100) NOT NULL,
	parol VARCHAR(192) NOT NULL,
	sol VARCHAR(100) NOT NULL,
	opisanie VARCHAR(1000),
	rol_id INT NOT NULL,
	CONSTRAINT fk_p_rol FOREIGN KEY (rol_id)
		REFERENCES Roli(id)
		ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Razresheniya (
	id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
	id_roli INT NOT NULL,
	resurs VARCHAR(1000) NOT NULL,
	CONSTRAINT fk_raz_rol FOREIGN KEY (id_roli)
		REFERENCES Roli(id)
		ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Nastroyki (
	id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
	id_polzovatelya INT NOT NULL,
	klyuch VARCHAR(100) NOT NULL,
	znachenie VARCHAR(1000) NOT NULL,
	CONSTRAINT fk_n_p FOREIGN KEY (id_polzovatelya)
		REFERENCES Polzovateli(id)
		ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Oblasti (
	id_respubliki INT NOT NULL,
	id_oblasti INT NOT NULL,
	id_rayona INT NOT NULL,
	opisanie VARCHAR(100) NOT NULL,
	UNIQUE KEY id(id_oblasti, id_rayona)
);

CREATE TABLE IF NOT EXISTS SpravochnikiKategorii
(
	kategoriya VARCHAR(100) NOT NULL PRIMARY KEY,
	opisanie VARCHAR(1000) NOT NULL,
	tolko_dlya_balansa BOOLEAN DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS Spravochniki
(
	id_zapisy int PRIMARY KEY AUTO_INCREMENT,
	kategoriya VARCHAR(100) NOT NULL,
	znachenie VARCHAR(1000),
	kod VARCHAR(100),
	kod_gruppi VARCHAR(100),
	CONSTRAINT fk_s_sk FOREIGN KEY (kategoriya)
		REFERENCES SpravochnikiKategorii(kategoriya)
		ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS GruppaItogov (
	id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
	nazvanie_gruppi VARCHAR(100) NOT NULL,
	kod VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS GruppaItogovSopostavlenie (
	id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
	id_poleznogo_iskopaemogo INT NOT NULL,
	id_primeneniya INT NOT NULL,
	id_gruppi INT NOT NULL,
	CONSTRAINT fk_pol_sp FOREIGN KEY (id_poleznogo_iskopaemogo)
		REFERENCES Spravochniki(id_zapisy)
		ON DELETE CASCADE,
	CONSTRAINT fk_prim_sp FOREIGN KEY (id_primeneniya)
		REFERENCES Spravochniki(id_zapisy)
		ON DELETE CASCADE,
	CONSTRAINT fk_gis_g FOREIGN KEY (id_gruppi)
		REFERENCES GruppaItogov(id)
		ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS TipMestorogdeniya
(
	tip_id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
	opisanie VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS Mestorogdeniya 
(
	id_mestorojdeniya INT NOT NULL,
	id_uchastka INT NOT NULL,
	id_oblast INT NOT NULL,
	id_rayon INT NOT NULL,
	id_osvoyeniya INT NOT NULL,
	naimenovanie VARCHAR(400) NOT NULL,
	opisanie TEXT,
	tip_id INT NOT NULL DEFAULT 1,
	UNIQUE KEY id (id_mestorojdeniya, id_uchastka),
	CONSTRAINT fk_m_rayon FOREIGN KEY (id_oblast, id_rayon)
		REFERENCES Oblasti(id_oblasti, id_rayona)
		ON DELETE CASCADE,
	CONSTRAINT fk_m_type FOREIGN KEY (tip_id)
		REFERENCES TipMestorogdeniya(tip_id)
		ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Koordinati
(
	id_mestorojdeniya INT NOT NULL,
	id_uchastka INT NOT NULL,
	dolgota FLOAT NOT NULL DEFAULT 0.0,
	shirota FLOAT NOT NULL DEFAULT 0.0,
	UNIQUE KEY id (id_mestorojdeniya, id_uchastka),
	CONSTRAINT fk_k_m FOREIGN KEY (id_mestorojdeniya, id_uchastka)
		REFERENCES Mestorogdeniya(id_mestorojdeniya, id_uchastka)
		ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS JDStancii
(
	id_mestorojdeniya INT NOT NULL,
	id_uchastka INT NOT NULL,
	naimenovanie VARCHAR(100) NOT NULL DEFAULT "",
	rasstoyanie VARCHAR(100) NOT NULL DEFAULT "",
	napravlenie VARCHAR(100) NOT NULL DEFAULT "",
	put_soobsheniya VARCHAR(100) NOT NULL DEFAULT "",
	UNIQUE KEY id (id_mestorojdeniya, id_uchastka),
	CONSTRAINT fk_jd_m FOREIGN KEY (id_mestorojdeniya, id_uchastka)
		REFERENCES Mestorogdeniya(id_mestorojdeniya, id_uchastka)
		ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS NaselenniePunkti
(
	id_mestorojdeniya INT NOT NULL,
	id_uchastka INT NOT NULL,
	naimenovanie VARCHAR(100) NOT NULL DEFAULT "",
	napravlenie VARCHAR(100) NOT NULL DEFAULT "",
	rasstoyanie VARCHAR(100) NOT NULL DEFAULT "",
	put_soobsheniya VARCHAR(100) NOT NULL,
	UNIQUE KEY id (id_mestorojdeniya, id_uchastka),
	CONSTRAINT fk_np_m FOREIGN KEY (id_mestorojdeniya, id_uchastka)
		REFERENCES Mestorogdeniya(id_mestorojdeniya, id_uchastka)
		ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Expedicii
(
	id_mestorojdeniya INT NOT NULL,
	id_uchastka INT NOT NULL,
	id_vedomstva INT NOT NULL,
	data_ot DATE,
	data_do DATE,
	opisanie VARCHAR(1000),
	UNIQUE KEY id (id_mestorojdeniya, id_uchastka, id_vedomstva),
	CONSTRAINT fk_ex_m FOREIGN KEY (id_mestorojdeniya, id_uchastka)
		REFERENCES Mestorogdeniya(id_mestorojdeniya, id_uchastka)
		ON DELETE CASCADE,
	CONSTRAINT fk_ex_v FOREIGN KEY (id_vedomstva)
		REFERENCES Spravochniki(id_zapisy)
		ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Resurs
(
	id_resursa INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
	id_mestorojdeniya INT NOT NULL,
	id_uchastka INT NOT NULL,
	id_poleznogo_iskopaemogo INT NOT NULL,
	id_primeneniya INT NOT NULL,
	id_ed_izmereniya_rudi INT NOT NULL,
	A DECIMAL(30, 10),
	B DECIMAL(30, 10),
	C1 DECIMAL(30, 10),
	C2 DECIMAL(30, 10),
	zabalans DECIMAL(30, 10),
	zapasi_dlya_pol_iskopaemogo BOOLEAN DEFAULT FALSE,
	id_ed_izmereniya_poleznogo_iskopayemogo INT,
	PI_A DECIMAL(30, 10),
	PI_B DECIMAL(30, 10),
	PI_C1 DECIMAL(30, 10),
	PI_C2 DECIMAL(30, 10),
	PI_zabalans DECIMAL(30, 10),
	id_himicheskogo_komponenta INT,
	id_himicheskoy_formuli INT,
	id_gosta INT,
	data_utverjdeniya DATE,
	god_utverjdeniya VARCHAR(4),
	nomer_protocola VARCHAR(100),
	organizaciya_utverdivshaya VARCHAR(1000),
	id_gruppi INT NOT NULL,
	opisanie VARCHAR(1000),
	UNIQUE KEY id (id_resursa, id_mestorojdeniya, id_uchastka, id_poleznogo_iskopaemogo, id_primeneniya),
	CONSTRAINT fk_r_m FOREIGN KEY (id_mestorojdeniya, id_uchastka)
		REFERENCES Mestorogdeniya(id_mestorojdeniya, id_uchastka)
		ON DELETE CASCADE,
	CONSTRAINT fk_r_pi FOREIGN KEY (id_poleznogo_iskopaemogo)
		REFERENCES Spravochniki(id_zapisy)
		ON DELETE CASCADE,
	CONSTRAINT fk_r_osv FOREIGN KEY (id_primeneniya)
		REFERENCES Spravochniki(id_zapisy)
		ON DELETE CASCADE,
	CONSTRAINT fk_r_eir FOREIGN KEY (id_ed_izmereniya_rudi)
		REFERENCES Spravochniki(id_zapisy)
		ON DELETE CASCADE,
	CONSTRAINT fk_r_eipi FOREIGN KEY (id_ed_izmereniya_poleznogo_iskopayemogo)
		REFERENCES Spravochniki(id_zapisy)
		ON DELETE CASCADE,
	CONSTRAINT fk_r_hk FOREIGN KEY (id_himicheskogo_komponenta)
		REFERENCES Spravochniki(id_zapisy)
		ON DELETE CASCADE,
	CONSTRAINT fk_r_hf FOREIGN KEY (id_himicheskoy_formuli)
		REFERENCES Spravochniki(id_zapisy)
		ON DELETE CASCADE,
	CONSTRAINT fk_r_g FOREIGN KEY (id_gosta)
		REFERENCES Spravochniki(id_zapisy)
		ON DELETE CASCADE,
	CONSTRAINT fk_r_gi FOREIGN KEY (id_gruppi)
		REFERENCES GruppaItogov(id)
		ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS ResursInformaciya
(
	id_resursa INT NOT NULL,
	id_mestorojdeniya INT NOT NULL,
	id_uchastka INT NOT NULL,
	id_poleznogo_iskopaemogo INT NOT NULL,
	id_primeneniya INT NOT NULL,
	srednee_soderjanie VARCHAR(100),
	proizvodetelnost VARCHAR(100),
	glubina VARCHAR(100),
	UNIQUE KEY id (id_resursa, id_mestorojdeniya, id_uchastka, id_poleznogo_iskopaemogo, id_primeneniya),
	CONSTRAINT fk_i_r FOREIGN KEY (id_resursa, id_mestorojdeniya, id_uchastka, id_poleznogo_iskopaemogo, id_primeneniya)
		REFERENCES Resurs(id_resursa, id_mestorojdeniya, id_uchastka, id_poleznogo_iskopaemogo, id_primeneniya)
		ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Litsenzii
(
	id_mestorojdeniya INT NOT NULL,
	id_uchastka INT NOT NULL,
	id_litsenzii INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
	A DECIMAL(30, 10),
	B DECIMAL(30, 10),
	C1 DECIMAL(30, 10),
	C2 DECIMAL(30, 10),
	zabalans DECIMAL(30, 10),
	PI_A DECIMAL(30, 10),
	PI_B DECIMAL(30, 10),
	PI_C1 DECIMAL(30, 10),
	PI_C2 DECIMAL(30, 10),
	PI_zabalans DECIMAL(30, 10),
	nomer_litsenzii VARCHAR(100),
	id_resursa INT NOT NULL,
	id_vedomstva INT NOT NULL,
	na_balanse_gkg INT NOT NULL DEFAULT FALSE,
	opisanie TEXT,
	data_ot DATE,
	data_do DATE,
	CONSTRAINT fk_l_m FOREIGN KEY (id_mestorojdeniya, id_uchastka)
		REFERENCES Mestorogdeniya(id_mestorojdeniya, id_uchastka)
		ON DELETE CASCADE,
	CONSTRAINT fk_l_r FOREIGN KEY (id_resursa)
		REFERENCES Resurs(id_resursa)
		ON DELETE CASCADE,
	CONSTRAINT fk_l_v FOREIGN KEY (id_vedomstva)
		REFERENCES Spravochniki(id_zapisy)
		ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS 5GR
(
	id_mestorojdeniya INT NOT NULL,
	id_uchastka INT NOT NULL,
	id_litsenzii INT NOT NULL,
	god INT NOT NULL,
	opisaniye TEXT,
	UNIQUE KEY id (id_mestorojdeniya, id_uchastka, id_litsenzii, god),
	CONSTRAINT fk_5gr_l FOREIGN KEY (id_litsenzii)
		REFERENCES Litsenzii(id_litsenzii)
		ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS 5GR_Dvijene
(
	id_mestorojdeniya INT NOT NULL,
	id_uchastka INT NOT NULL,
	id_litsenzii INT NOT NULL,
	god INT NOT NULL,
	kategoriya_zapasov VARCHAR(100),
	ruda BOOLEAN,
	data DATE,
	dobicha DECIMAL(30, 10),
	poteri DECIMAL(30, 10),
	razvedka DECIMAL(30, 10),
	izmenenie DECIMAL(30, 10),
	spisano DECIMAL(30, 10),
	drugoe DECIMAL(30, 10),
	ostatok_na_konec_goda DECIMAL(30, 10),
	ostatok_na_nachalo_goda DECIMAL(30, 10),
	UNIQUE KEY id (id_mestorojdeniya, id_uchastka, id_litsenzii, god, kategoriya_zapasov),
	CONSTRAINT fk_5gr_5grd FOREIGN KEY (id_mestorojdeniya, id_uchastka, id_litsenzii, god)
		REFERENCES 5GR(id_mestorojdeniya, id_uchastka, id_litsenzii, god)
		ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS KadastrObshayaInformaciya
(
	id_mestorojdeniya INT NOT NULL,
	id_uchastka INT NOT NULL,
	id_poleznogo_iskopaemogo INT NOT NULL,
	nomenklatura VARCHAR(100) NOT NULL DEFAULT "",
	id_vedomstva INT,
	pityevaya_voda_nazvanie VARCHAR(1000) DEFAULT "",
	pityevaya_voda_rast VARCHAR(1000) DEFAULT "",
	tehnicheskaya_voda_nazvanie VARCHAR(1000) DEFAULT "",
	tehnicheskaya_voda_rast VARCHAR(1000) DEFAULT "",
	elektrichestvo_nazvanie VARCHAR(1000) DEFAULT "",
	elektrichestvo_rast VARCHAR(1000) DEFAULT "",
	absolyutnaya_otmetka_min DECIMAL(30, 10) DEFAULT 0.0,
	absolyutnaya_otmetka_max DECIMAL(30, 10) DEFAULT 0.0,
	id_tip_relyefa INT,
	seysmichnost DECIMAL(30, 10) DEFAULT 0.0,
	id_seleopasnost INT,
	id_opolzneopasnost INT,
	prinadlejnost_zemel TEXT,
	id_tip_zemel INT,
	razmer_dlina DECIMAL(30, 10) DEFAULT 0.0,
	razmer_shirina DECIMAL(30, 10) DEFAULT 0.0,
	ploshad DECIMAL(30, 10) DEFAULT 0.0,
	ploshad_utverjdennih_zapasov DECIMAL(30, 10) DEFAULT 0.0,
	UNIQUE KEY id (id_mestorojdeniya, id_uchastka, id_poleznogo_iskopaemogo),
	CONSTRAINT fk_inf_v FOREIGN KEY (id_vedomstva)
		REFERENCES Spravochniki(id_zapisy)
		ON DELETE CASCADE,
	CONSTRAINT fk_inf_m FOREIGN KEY (id_mestorojdeniya, id_uchastka)
		REFERENCES Mestorogdeniya(id_mestorojdeniya, id_uchastka)
		ON DELETE CASCADE,
	CONSTRAINT fk_inf_pi FOREIGN KEY (id_poleznogo_iskopaemogo)
		REFERENCES Spravochniki(id_zapisy)
		ON DELETE CASCADE,
	CONSTRAINT fk_inf_rel FOREIGN KEY (id_tip_relyefa)
		REFERENCES Spravochniki(id_zapisy)
		ON DELETE CASCADE,
	CONSTRAINT fk_inf_sel FOREIGN KEY (id_seleopasnost)
		REFERENCES Spravochniki(id_zapisy)
		ON DELETE CASCADE,
	CONSTRAINT fk_inf_op FOREIGN KEY (id_opolzneopasnost)
		REFERENCES Spravochniki(id_zapisy)
		ON DELETE CASCADE,
	CONSTRAINT fk_inf_zem FOREIGN KEY (id_tip_zemel)
		REFERENCES Spravochniki(id_zapisy)
		ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS KadastrTitul (
	id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
	id_mestorojdeniya INT NOT NULL,
	id_uchastka INT NOT NULL,
	id_poleznogo_iskopaemogo INT NOT NULL,
	razdel VARCHAR(100) NULL DEFAULT "",
	gos_balans VARCHAR(5) NULL DEFAULT "",
	sostavil_fio VARCHAR(150) NULL DEFAULT "",
	data_sostavleniya DATE NULL,
	utverdil_fio VARCHAR(100) NULL,
	data_utverjdeniya DATE NULL,
	god INT NULL,
	data DATE NULL,
	UNIQUE KEY id (id_mestorojdeniya, id_uchastka, id_poleznogo_iskopaemogo),
	CONSTRAINT fk_titul_m FOREIGN KEY (id_mestorojdeniya, id_uchastka, id_poleznogo_iskopaemogo)
		REFERENCES KadastrObshayaInformaciya(id_mestorojdeniya, id_uchastka, id_poleznogo_iskopaemogo)
		ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS KadastrIzuchennost
(
	id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
	id_mestorojdeniya INT NOT NULL,
	id_uchastka INT NOT NULL,
	id_poleznogo_iskopaemogo INT NOT NULL,
	god INT NOT NULL,
	id_stadii_izuchennost INT NOT NULL,
	CONSTRAINT fk_izu_m FOREIGN KEY (id_mestorojdeniya, id_uchastka, id_poleznogo_iskopaemogo)
		REFERENCES KadastrObshayaInformaciya(id_mestorojdeniya, id_uchastka, id_poleznogo_iskopaemogo)
		ON DELETE CASCADE,
	CONSTRAINT fk_sp_izu FOREIGN KEY (id_stadii_izuchennost)
		REFERENCES Spravochniki(id_zapisy)
		ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS KadastrKoordinatu
(
	id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
	id_mestorojdeniya INT NOT NULL,
	id_uchastka INT NOT NULL,
	id_poleznogo_iskopaemogo INT NOT NULL,
	dolgota FLOAT NOT NULL DEFAULT 0.0,
	shirota FLOAT NOT NULL DEFAULT 0.0,
	CONSTRAINT fk_koord_m FOREIGN KEY (id_mestorojdeniya, id_uchastka, id_poleznogo_iskopaemogo)
		REFERENCES KadastrObshayaInformaciya(id_mestorojdeniya, id_uchastka, id_poleznogo_iskopaemogo)
		ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS KadastrGeoHarakteristiki 
(
	id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
	id_mestorojdeniya INT NOT NULL,
	id_uchastka INT NOT NULL,
	id_poleznogo_iskopaemogo INT NOT NULL,
	id_gruppi_slojnosti INT,
	id_tip_slojnosti INT,
	porodi_slag_pol_iskopaemoe VARCHAR(1000),
	id_forma_tel INT,
	kolichestvo_tel INT NOT NULL DEFAULT 0,
	razmer_tel_dlina_po_protstiraniyu_ot DECIMAL(30, 10) DEFAULT 0.0,
	razmer_tel_dlina_po_protstiraniyu_do DECIMAL(30, 10) DEFAULT 0.0,
	razmer_tel_dlina_po_protstiraniyu_sred DECIMAL(30, 10) DEFAULT 0.0,
	moshnost_obshaya_ot DECIMAL(30, 10) DEFAULT 0.0,
	moshnost_obshaya_do DECIMAL(30, 10) DEFAULT 0.0,
	moshnost_obshaya_sred DECIMAL(30, 10) DEFAULT 0.0,
	moshnost_vskritaya_ot DECIMAL(30, 10) DEFAULT 0.0,
	moshnost_vskritaya_do DECIMAL(30, 10) DEFAULT 0.0,
	moshnost_vskritaya_sred DECIMAL(30, 10) DEFAULT 0.0,
	moshnost_pod_zapasov_ot DECIMAL(30, 10) DEFAULT 0.0,
	moshnost_pod_zapasov_do DECIMAL(30, 10) DEFAULT 0.0,
	moshnost_pod_zapasov_sred DECIMAL(30, 10) DEFAULT 0.0,
	moshnost_otdel_sloev_ot DECIMAL(30, 10) DEFAULT 0.0,
	moshnost_otdel_sloev_do DECIMAL(30, 10) DEFAULT 0.0,
	moshnost_otdel_sloev_sred DECIMAL(30, 10) DEFAULT 0.0,
	usloviya_zaleganiya_naprav_prostiraniya_ot DECIMAL(30, 10) DEFAULT 0.0,
	usloviya_zaleganiya_naprav_prostiraniya_do DECIMAL(30, 10) DEFAULT 0.0,
	usloviya_zaleganiya_azimut_padeniya_ot DECIMAL(30, 10) DEFAULT 0.0,
	usloviya_zaleganiya_azimut_padeniya_do DECIMAL(30, 10) DEFAULT 0.0,
	usloviya_zaleganiya_ugol_padeniya_ot DECIMAL(30, 10) DEFAULT 0.0,
	usloviya_zaleganiya_ugol_padeniya_do DECIMAL(30, 10) DEFAULT 0.0,
	usloviya_zaleganiya_ugol_padeniya_sred DECIMAL(30, 10) DEFAULT 0.0,
	usloviya_zaleganiya_glubina_zaleganiya_ot DECIMAL(30, 10) DEFAULT 0.0,
	usloviya_zaleganiya_glubina_zaleganiya_do DECIMAL(30, 10) DEFAULT 0.0,
	usloviya_zaleganiya_glubina_zaleganiya_sred DECIMAL(30, 10) DEFAULT 0.0,
	moshnost_zoni_vivetrivaniya_ot DECIMAL(30, 10) DEFAULT 0.0,
	moshnost_zoni_vivetrivaniya_do DECIMAL(30, 10) DEFAULT 0.0,
	moshnost_zoni_vivetrivaniya_sred DECIMAL(30, 10) DEFAULT 0.0,
	moshnost_zoni_chastichogo_vivetrivaniya_ot DECIMAL(30, 10) DEFAULT 0.0,
	moshnost_zoni_chastichogo_vivetrivaniya_do DECIMAL(30, 10) DEFAULT 0.0,
	moshnost_zoni_chastichogo_vivetrivaniya_sred DECIMAL(30, 10) DEFAULT 0.0,
	moshnost_vskrishi_ot DECIMAL(30, 10) DEFAULT 0.0,
	moshnost_vskrishi_do DECIMAL(30, 10) DEFAULT 0.0,
	moshnost_vskrishi_sred DECIMAL(30, 10) DEFAULT 0.0,
	moshnost_otlojeniy_ot DECIMAL(30, 10) DEFAULT 0.0,
	moshnost_otlojeniy_do DECIMAL(30, 10) DEFAULT 0.0,
	moshnost_otlojeniy_sred DECIMAL(30, 10) DEFAULT 0.0,
	lineynaya_plotnost_treshin DECIMAL(30, 10) DEFAULT 0.0,
	zakarstovannost DECIMAL(30, 10) DEFAULT 0.0,
	zapolnitel_kresta DECIMAL(30, 10) DEFAULT 0.0,
	kratkoe_opisanie TEXT,
	CONSTRAINT fk_geo_harakteristiki_m FOREIGN KEY (id_mestorojdeniya, id_uchastka, id_poleznogo_iskopaemogo)
		REFERENCES KadastrObshayaInformaciya(id_mestorojdeniya, id_uchastka, id_poleznogo_iskopaemogo)
		ON DELETE CASCADE,
	CONSTRAINT fk_sp_gr_sloj FOREIGN KEY (id_gruppi_slojnosti)
		REFERENCES Spravochniki(id_zapisy)
		ON DELETE CASCADE,
	CONSTRAINT fk_sp_tip_sloj FOREIGN KEY (id_tip_slojnosti)
		REFERENCES Spravochniki(id_zapisy)
		ON DELETE CASCADE,
	CONSTRAINT fk_sp_forma_tel FOREIGN KEY (id_forma_tel)
		REFERENCES Spravochniki(id_zapisy)
		ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS KadastrProsloiPustihPorod
(
	id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
	id_geo_harakteristiki INT NOT NULL,
	nazvanie VARCHAR(10000) NOT NULL DEFAULT "",
	moshnost_ot DECIMAL(30, 10) NOT NULL DEFAULT 0.0,
	moshnost_do DECIMAL(30, 10) NOT NULL DEFAULT 0.0,
	moshnost_sred DECIMAL(30, 10) NOT NULL DEFAULT 0.0,
	CONSTRAINT fk_prosloi_geo_harakteristiki FOREIGN KEY (id_geo_harakteristiki)
		REFERENCES KadastrGeoHarakteristiki(id)
		ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS KadastrVmeshayushiePorodi
(
	id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
	id_geo_harakteristiki INT NOT NULL,
	polojenie VARCHAR(1000) NOT NULL DEFAULT "",
	raznosti_porod VARCHAR(1000) NOT NULL DEFAULT "",
	geologicheskiy_vozrast VARCHAR(1000) NOT NULL DEFAULT "",
	CONSTRAINT fk_vmesh_porodi_harakteristiki FOREIGN KEY (id_geo_harakteristiki)
		REFERENCES KadastrGeoHarakteristiki(id)
		ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS KadastrKachestvennayaHarakteristika
(
	id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
	id_mestorojdeniya INT NOT NULL,
	id_uchastka INT NOT NULL,
	id_poleznogo_iskopaemogo INT NOT NULL,
	pokazatel VARCHAR(1000) NOT NULL,
	id_ed_izm INT NOT NULL,
	znachenie_ot DECIMAL(30, 10) DEFAULT 0.0,
	znachenie_do DECIMAL(30, 10) DEFAULT 0.0,
	znachenie_sred DECIMAL(30, 10) DEFAULT 0.0,
	CONSTRAINT fk_kach_harakteristiki_m FOREIGN KEY (id_mestorojdeniya, id_uchastka, id_poleznogo_iskopaemogo)
		REFERENCES KadastrObshayaInformaciya(id_mestorojdeniya, id_uchastka, id_poleznogo_iskopaemogo)
		ON DELETE CASCADE,
	CONSTRAINT fk_kach_harakteristiki_ed_izm FOREIGN KEY (id_ed_izm)
		REFERENCES Spravochniki(id_zapisy)
		ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS KadastrFizMehHarakteristika
(
	id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
	id_mestorojdeniya INT NOT NULL,
	id_uchastka INT NOT NULL,
	id_poleznogo_iskopaemogo INT NOT NULL,
	svoystva VARCHAR(1000) NOT NULL,
	id_ed_izm INT NOT NULL,
	velichina_ot DECIMAL(30, 10) DEFAULT 0.0,
	velichina_do DECIMAL(30, 10) DEFAULT 0.0,
	velichina_sred DECIMAL(30, 10) DEFAULT 0.0,
	CONSTRAINT fk_fiz_harakteristiki_m FOREIGN KEY (id_mestorojdeniya, id_uchastka, id_poleznogo_iskopaemogo)
		REFERENCES KadastrObshayaInformaciya(id_mestorojdeniya, id_uchastka, id_poleznogo_iskopaemogo)
		ON DELETE CASCADE,
	CONSTRAINT fk_fiz_harakteristiki_ed_izm_m FOREIGN KEY (id_ed_izm)
		REFERENCES Spravochniki(id_zapisy)
		ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS KadastrProdukciya
(
	id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
	id_mestorojdeniya INT NOT NULL,
	id_uchastka INT NOT NULL,
	id_poleznogo_iskopaemogo INT NOT NULL,
	proch_svoysva TEXT NOT NULL,
	rezultati_ispitaniya TEXT NOT NULL,
	vid_produkzii VARCHAR(1000) NOT NULL DEFAULT "",
	sort_produkzii VARCHAR(1000) NOT NULL DEFAULT "",
	sootvetstvie TEXT,
	CONSTRAINT fk_produkciya_m FOREIGN KEY (id_mestorojdeniya, id_uchastka, id_poleznogo_iskopaemogo)
		REFERENCES KadastrObshayaInformaciya(id_mestorojdeniya, id_uchastka, id_poleznogo_iskopaemogo)
		ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS KadastrGeolograzvedHarakteristika
(
	id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
	id_mestorojdeniya INT NOT NULL,
	id_uchastka INT NOT NULL,
	id_poleznogo_iskopaemogo INT NOT NULL,
	id_sistema_geologoraz_rabot INT NOT NULL,
	gustota_razver_seti_A DECIMAL(30, 10),
	gustota_razver_seti_B DECIMAL(30, 10),
	gustota_razver_seti_C1 DECIMAL(30, 10),
	gustota_razver_seti_C2 DECIMAL(30, 10),
	glubina_razvedki DECIMAL(30, 10),
	vihod_kerna DECIMAL(30, 10),
	CONSTRAINT fk_razvedka_harakteristiki_m FOREIGN KEY (id_mestorojdeniya, id_uchastka, id_poleznogo_iskopaemogo)
		REFERENCES KadastrObshayaInformaciya(id_mestorojdeniya, id_uchastka, id_poleznogo_iskopaemogo)
		ON DELETE CASCADE,
	CONSTRAINT fk_sistema_geologoraz_sp FOREIGN KEY (id_sistema_geologoraz_rabot)
		REFERENCES Spravochniki(id_zapisy)
		ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS KadastrTipiRabot
(
	id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
	id_mestorojdeniya INT NOT NULL,
	id_uchastka INT NOT NULL,
	id_poleznogo_iskopaemogo INT NOT NULL,
	tip VARCHAR(1000) DEFAULT "",
	znachenie VARCHAR(1000) DEFAULT "",
	CONSTRAINT fk_tip_rabot_m FOREIGN KEY (id_mestorojdeniya, id_uchastka, id_poleznogo_iskopaemogo)
		REFERENCES KadastrObshayaInformaciya(id_mestorojdeniya, id_uchastka, id_poleznogo_iskopaemogo)
		ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS KadastrKondicii
(
	id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
	id_mestorojdeniya INT NOT NULL,
	id_uchastka INT NOT NULL,
	id_poleznogo_iskopaemogo INT NOT NULL,
	vid VARCHAR(1000) DEFAULT "",
	kem_razrabotan VARCHAR(1000) DEFAULT "",
	kem_utverjden VARCHAR(1000) DEFAULT "",
	nomer_protokola VARCHAR(1000) DEFAULT "",
	sostav TEXT,
	CONSTRAINT fk_kondicii_m FOREIGN KEY (id_mestorojdeniya, id_uchastka, id_poleznogo_iskopaemogo)
		REFERENCES KadastrObshayaInformaciya(id_mestorojdeniya, id_uchastka, id_poleznogo_iskopaemogo)
		ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS KadastrSvedeniyaOZapasah
(
	id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
	id_mestorojdeniya INT NOT NULL,
	id_uchastka INT NOT NULL,
	id_poleznogo_iskopaemogo INT NOT NULL,
	id_vedomstva INT NOT NULL,
	metod_podscheta VARCHAR(1000) DEFAULT "",
	glubina DECIMAL(30, 10) DEFAULT 0.0,
	CONSTRAINT fk_ved_sp FOREIGN KEY (id_vedomstva)
		REFERENCES Spravochniki(id_zapisy)
		ON DELETE CASCADE,
	CONSTRAINT fk_zapasi_m FOREIGN KEY (id_mestorojdeniya, id_uchastka, id_poleznogo_iskopaemogo)
		REFERENCES KadastrObshayaInformaciya(id_mestorojdeniya, id_uchastka, id_poleznogo_iskopaemogo)
		ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS KadastrGornoGeologicheskayaHarakteristika
(
	id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
	id_mestorojdeniya INT NOT NULL,
	id_uchastka INT NOT NULL,
	id_poleznogo_iskopaemogo INT NOT NULL,
	id_radiozionnaya_harakteristika_poroda INT NOT NULL,
	radiozionnaya_harakteristika_radioaktivnost DECIMAL(30, 10) DEFAULT 0.0,
	radiozionnaya_harakteristika_klass INT NOT NULL,
	koef_krep_pol_iskopaemogo DECIMAL(30, 10) DEFAULT 0.0,
	koef_krep_pustih_porod DECIMAL(30, 10) DEFAULT 0.0,
	koef_krep_vmeshayushih_porod DECIMAL(30, 10) DEFAULT 0.0,
	koef_razrihl_pol_iskopaemogo DECIMAL(30, 10) DEFAULT 0.0,
	koef_razrihl_pustih_porod DECIMAL(30, 10) DEFAULT 0.0,
	koef_razrihl_vmeshayushih_porod DECIMAL(30, 10) DEFAULT 0.0,
	vodonosnie_gorizonti_glubina VARCHAR(1000) DEFAULT "",
	ojidayemiy_vodopotok DECIMAL DEFAULT 0.0,
	him_sostav VARCHAR(1000) DEFAULT "",
	mineralizaciya DECIMAL(30, 10) DEFAULT 0.0,
	CONSTRAINT fk_poroda_sp FOREIGN KEY (id_radiozionnaya_harakteristika_poroda)
		REFERENCES Spravochniki(id_zapisy)
		ON DELETE CASCADE,
	CONSTRAINT fk_klass_sp FOREIGN KEY(radiozionnaya_harakteristika_klass)
		REFERENCES Spravochniki(id_zapisy)
		ON DELETE CASCADE,
	CONSTRAINT fk_gorno_geo_harakteristiki_m FOREIGN KEY (id_mestorojdeniya, id_uchastka, id_poleznogo_iskopaemogo)
		REFERENCES KadastrObshayaInformaciya(id_mestorojdeniya, id_uchastka, id_poleznogo_iskopaemogo)
		ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS KadastrGornotehResheniya
(
	id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
	id_mestorojdeniya INT NOT NULL,
	id_uchastka INT NOT NULL,
	id_poleznogo_iskopaemogo INT NOT NULL,
	opisanie TEXT,
	CONSTRAINT fk_gor_teh_m FOREIGN KEY (id_mestorojdeniya, id_uchastka, id_poleznogo_iskopaemogo)
		REFERENCES KadastrObshayaInformaciya(id_mestorojdeniya, id_uchastka, id_poleznogo_iskopaemogo)
		ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS KadastrOkrujSreda
(
	id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
	id_mestorojdeniya INT NOT NULL,
	id_uchastka INT NOT NULL,
	id_poleznogo_iskopaemogo INT NOT NULL,
	opisanie TEXT,
	CONSTRAINT fk_sreda_m FOREIGN KEY (id_mestorojdeniya, id_uchastka, id_poleznogo_iskopaemogo)
		REFERENCES KadastrObshayaInformaciya(id_mestorojdeniya, id_uchastka, id_poleznogo_iskopaemogo)
		ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS KadastrTehnoEkonomPokazateli
(
	id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
	id_mestorojdeniya INT NOT NULL,
	id_uchastka INT NOT NULL,
	id_poleznogo_iskopaemogo INT NOT NULL,
	opisanie TEXT,
	zena VARCHAR(1000) DEFAULT "",
	CONSTRAINT fk_ekonom_m FOREIGN KEY (id_mestorojdeniya, id_uchastka, id_poleznogo_iskopaemogo)
		REFERENCES KadastrObshayaInformaciya(id_mestorojdeniya, id_uchastka, id_poleznogo_iskopaemogo)
		ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS KadastrDopolnitelnieSvedeniya
(
	id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
	id_mestorojdeniya INT NOT NULL,
	id_uchastka INT NOT NULL,
	id_poleznogo_iskopaemogo INT NOT NULL,
	opisanie TEXT,
	CONSTRAINT fk_dop_m FOREIGN KEY (id_mestorojdeniya, id_uchastka, id_poleznogo_iskopaemogo)
		REFERENCES KadastrObshayaInformaciya(id_mestorojdeniya, id_uchastka, id_poleznogo_iskopaemogo)
		ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS KadastrIstochniki
(
	id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
	id_mestorojdeniya INT NOT NULL,
	id_uchastka INT NOT NULL,
	id_poleznogo_iskopaemogo INT NOT NULL,
	inv_nomer VARCHAR(100) DEFAULT "",
	avtor VARCHAR(100) DEFAULT "",
	naimenovanie_raboti VARCHAR(1000) DEFAULT "",
	CONSTRAINT fk_ist_m FOREIGN KEY (id_mestorojdeniya, id_uchastka, id_poleznogo_iskopaemogo)
		REFERENCES KadastrObshayaInformaciya(id_mestorojdeniya, id_uchastka, id_poleznogo_iskopaemogo)
		ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS KadastrRazrez
(
	id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
	id_mestorojdeniya INT NOT NULL,
	id_uchastka INT NOT NULL,
	id_poleznogo_iskopaemogo INT NOT NULL,
	razrez BLOB,
	CONSTRAINT fk_razrez_m FOREIGN KEY (id_mestorojdeniya, id_uchastka, id_poleznogo_iskopaemogo)
		REFERENCES KadastrObshayaInformaciya(id_mestorojdeniya, id_uchastka, id_poleznogo_iskopaemogo)
		ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS KadastrShema
(
	id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
	id_mestorojdeniya INT NOT NULL,
	id_uchastka INT NOT NULL,
	id_poleznogo_iskopaemogo INT NOT NULL,
	shema BLOB,
	CONSTRAINT fk_shema_m FOREIGN KEY (id_mestorojdeniya, id_uchastka, id_poleznogo_iskopaemogo)
		REFERENCES KadastrObshayaInformaciya(id_mestorojdeniya, id_uchastka, id_poleznogo_iskopaemogo)
		ON DELETE CASCADE
);


INSERT INTO Oblasti(id_respubliki, id_oblasti, id_rayona, opisanie) VALUES(1, 0, 0, "Узбекистан");

INSERT INTO Oblasti(id_respubliki, id_oblasti, id_rayona, opisanie) VALUES(1, 1, 0, "Ташкентская область");
INSERT INTO Oblasti(id_respubliki, id_oblasti, id_rayona, opisanie) VALUES(1, 2, 0, "Ферганская область");
INSERT INTO Oblasti(id_respubliki, id_oblasti, id_rayona, opisanie) VALUES(1, 3, 0, "Навоийская область");
INSERT INTO Oblasti(id_respubliki, id_oblasti, id_rayona, opisanie) VALUES(1, 4, 0, "Бухарская область");
INSERT INTO Oblasti(id_respubliki, id_oblasti, id_rayona, opisanie) VALUES(1, 5, 0, "Наманганская область");
INSERT INTO Oblasti(id_respubliki, id_oblasti, id_rayona, opisanie) VALUES(1, 6, 0, "Кашкадарьинская область");
INSERT INTO Oblasti(id_respubliki, id_oblasti, id_rayona, opisanie) VALUES(1, 7, 0, "Андижанская область");
INSERT INTO Oblasti(id_respubliki, id_oblasti, id_rayona, opisanie) VALUES(1, 8, 0, "Pеспублика Каракалпакстан");
INSERT INTO Oblasti(id_respubliki, id_oblasti, id_rayona, opisanie) VALUES(1, 9, 0, "Хорезмская область");
INSERT INTO Oblasti(id_respubliki, id_oblasti, id_rayona, opisanie) VALUES(1, 10, 0, "Сырдарьинская область");
INSERT INTO Oblasti(id_respubliki, id_oblasti, id_rayona, opisanie) VALUES(1, 11, 0, "Самаркандская область");
INSERT INTO Oblasti(id_respubliki, id_oblasti, id_rayona, opisanie) VALUES(1, 12, 0, "Джизакская область");
INSERT INTO Oblasti(id_respubliki, id_oblasti, id_rayona, opisanie) VALUES(1, 13, 0, "Сурхандарьинская область");

INSERT INTO SpravochnikiKategorii(kategoriya, opisanie) VALUES('SPR_ED_IZM', 'Единицы измерения');
INSERT INTO SpravochnikiKategorii(kategoriya, opisanie) VALUES('SPR_GOST', 'Государственные стандарты');
INSERT INTO SpravochnikiKategorii(kategoriya, opisanie) VALUES('SPR_VED', 'Ведомства');
INSERT INTO SpravochnikiKategorii(kategoriya, opisanie) VALUES('SPR_OSV', 'Степень освоения');
INSERT INTO SpravochnikiKategorii(kategoriya, opisanie) VALUES('SPR_PRIM', 'Направление применения');
INSERT INTO SpravochnikiKategorii(kategoriya, opisanie) VALUES('SPR_POL', 'Полезные ископаемые');
INSERT INTO SpravochnikiKategorii(kategoriya, opisanie) VALUES('SPR_HIM_KOMP', 'Химические компоненты');
INSERT INTO SpravochnikiKategorii(kategoriya, opisanie) VALUES('SPR_HIM_FORMULA', 'Химические формулы');

INSERT INTO SpravochnikiKategorii(kategoriya, opisanie, tolko_dlya_balansa) VALUES('SPR_TIP_RELEFA', 'Тип рельефа', FALSE);
INSERT INTO SpravochnikiKategorii(kategoriya, opisanie, tolko_dlya_balansa) VALUES('SPR_SELEOPASNOST', 'Селеопасность', FALSE);
INSERT INTO SpravochnikiKategorii(kategoriya, opisanie, tolko_dlya_balansa) VALUES('SPR_OPOLZNEOPASNOST', 'Оползнеопасность', FALSE);
INSERT INTO SpravochnikiKategorii(kategoriya, opisanie, tolko_dlya_balansa) VALUES('SPR_TIP_ZEMEL', 'Тип земель', FALSE);
INSERT INTO SpravochnikiKategorii(kategoriya, opisanie, tolko_dlya_balansa) VALUES('SPR_STADII_IZUCHENNOSTI', 'Стадии изученности', FALSE);
INSERT INTO SpravochnikiKategorii(kategoriya, opisanie, tolko_dlya_balansa) VALUES('SPR_GRUPPI_SLOJNOSTI', 'Группы сложности', FALSE);
INSERT INTO SpravochnikiKategorii(kategoriya, opisanie, tolko_dlya_balansa) VALUES('SPR_TIP_SLOJNOSTI', 'Тип сложности', FALSE);
INSERT INTO SpravochnikiKategorii(kategoriya, opisanie, tolko_dlya_balansa) VALUES('SPR_FORMA_TEL', 'Форма тел', FALSE);
INSERT INTO SpravochnikiKategorii(kategoriya, opisanie, tolko_dlya_balansa) VALUES('SPR_SISTEM_GEORAZ', 'Система геологоразведочных работ', FALSE);

INSERT INTO Spravochniki(kategoriya, znachenie) VALUES('SPR_ED_IZM', 'тыс. т');
INSERT INTO Spravochniki(kategoriya, znachenie) VALUES('SPR_ED_IZM', 'т');
INSERT INTO Spravochniki(kategoriya, znachenie) VALUES('SPR_ED_IZM', 'кг');
INSERT INTO Spravochniki(kategoriya, znachenie) VALUES('SPR_ED_IZM', 'г');
INSERT INTO Spravochniki(kategoriya, znachenie) VALUES('SPR_ED_IZM', 'г/т');
INSERT INTO Spravochniki(kategoriya, znachenie) VALUES('SPR_ED_IZM', '%');

INSERT INTO Spravochniki(kategoriya, znachenie) VALUES('SPR_VED', 'ГосКомГеологии');

INSERT INTO TipMestorogdeniya(tip_id, opisanie) VALUES(1, 'На балансе');
INSERT INTO TipMestorogdeniya(tip_id, opisanie) VALUES(2, 'Перспективные площади');
INSERT INTO TipMestorogdeniya(tip_id, opisanie) VALUES(3, 'Рудные проявления');

INSERT INTO Roli(rol) VALUES('administrator');
INSERT INTO Roli(rol) VALUES('operator');
INSERT INTO Roli(rol) VALUES('viewer');

INSERT INTO Polzovateli(imya, parol, sol, opisanie, rol_id) VALUES("admin", SHA2(CONCAT("ac4OfWinup", "DanWocsAtAv8"), 256), "DanWocsAtAv8", "Учетная запись администратора баланса", (SELECT id FROM Roli WHERE rol="administrator"));

INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'administrator'), '/api/get_areas_count/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'administrator'), '/api/get_areas/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'administrator'), '/api/delete_area/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'administrator'), '/api/add_area/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'administrator'), '/api/update_area/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'administrator'), '/api/get_all_dictionaries/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'administrator'), '/api/get_dictionary_count/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'administrator'), '/api/get_dictionary_contents/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'administrator'), '/api/get_dictionary_item_description/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'administrator'), '/api/delete_dictionary_contents/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'administrator'), '/api/add_dictionary_contents/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'administrator'), '/api/update_dictionary_contents/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'administrator'), '/api/get_districts/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'administrator'), '/api/delete_district/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'administrator'), '/api/add_district/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'administrator'), '/api/update_district/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'administrator'), '/api/get_district_count/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'administrator'), '/api/get_deposits_count/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'administrator'), '/api/get_deposits/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'administrator'), '/api/get_deposit/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'administrator'), '/api/get_mine_area/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'administrator'), '/api/delete_deposit/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'administrator'), '/api/save_or_update_coordinates/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'administrator'), '/api/get_coordinates/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'administrator'), '/api/save_or_update_train_stations/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'administrator'), '/api/get_train_station/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'administrator'), '/api/save_or_update_inhabited_areas/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'administrator'), '/api/get_inhab_area/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'administrator'), '/api/save_or_update_expedition/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'administrator'), '/api/get_expedition/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'administrator'), '/api/update_deposit/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'administrator'), '/api/add_deposit/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'administrator'), '/api/get_mine_area_count/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'administrator'), '/api/get_mine_areas/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'administrator'), '/api/delete_mine_area/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'administrator'), '/api/update_mine_area/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'administrator'), '/api/add_mine_area/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'administrator'), '/api/get_reserves_for_deposit/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'administrator'), '/api/get_reserves_for_mine_area/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'administrator'), '/api/get_reserve_for_deposit/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'administrator'), '/api/delete_reserve/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'administrator'), '/api/get_reserves_description/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'administrator'), '/api/add_or_update_reserves_description/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'administrator'), '/api/add_reserves_for_deposit/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'administrator'), '/api/update_reserves_for_deposit/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'administrator'), '/api/add_reserves_for_mine_area/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'administrator'), '/api/update_reserves_for_mine_area/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'administrator'), '/api/get_license_count/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'administrator'), '/api/get_licenses/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'administrator'), '/api/get_license_description/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'administrator'), '/api/get_license/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'administrator'), '/api/delete_license/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'administrator'), '/api/add_license/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'administrator'), '/api/update_license/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'administrator'), '/api/get_movement/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'administrator'), '/api/update_movement/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'administrator'), '/api/select_possible_components/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'administrator'), '/api/balans_report_xlsx/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'administrator'), '/api/balans_report_xlsx_with_area/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'administrator'), '/api/balans_report_with_group_xlsx/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'administrator'), '/api/download_xlsx_report/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'administrator'), '/api/balans_report_html/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'administrator'), '/api/has_permissions_to_security_settings/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'administrator'), '/api/get_roles/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'administrator'), '/api/get_users/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'administrator'), '/api/add_user/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'administrator'), '/api/update_user/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'administrator'), '/api/delete_user/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'administrator'), '/api/get_users_count/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'administrator'), '/api/get_user/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'administrator'), '/api/get_deposit_by_name/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'administrator'), '/api/get_mine_area_by_name/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'administrator'), '/api/get_deposits_and_mine_areas/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'administrator'), '/api/get_deposits_and_mine_areas/');


INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'administrator'), '/api/get_groups/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'administrator'), '/api/get_group/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'administrator'), '/api/add_group/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'administrator'), '/api/update_group/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'administrator'), '/api/delete_group/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'administrator'), '/api/get_groups_count/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'administrator'), '/api/get_group_mappings_count/');

INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'administrator'), '/api/get_group_mappings/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'administrator'), '/api/get_group_mapping/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'administrator'), '/api/add_group_mapping/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'administrator'), '/api/delete_group_mapping/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'administrator'), '/api/get_groups_with_usage/');


INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'operator'), '/api/get_areas_count/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'operator'), '/api/get_areas/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'operator'), '/api/add_area/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'operator'), '/api/update_area/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'operator'), '/api/get_all_dictionaries/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'operator'), '/api/get_dictionary_count/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'operator'), '/api/get_dictionary_contents/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'operator'), '/api/get_dictionary_item_description/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'operator'), '/api/add_dictionary_contents/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'operator'), '/api/update_dictionary_contents/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'operator'), '/api/get_districts/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'operator'), '/api/add_district/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'operator'), '/api/update_district/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'operator'), '/api/get_district_count/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'operator'), '/api/get_deposits_count/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'operator'), '/api/get_deposits/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'operator'), '/api/get_deposit/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'operator'), '/api/get_mine_area/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'operator'), '/api/save_or_update_coordinates/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'operator'), '/api/get_coordinates/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'operator'), '/api/save_or_update_train_stations/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'operator'), '/api/get_train_station/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'operator'), '/api/save_or_update_inhabited_areas/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'operator'), '/api/get_inhab_area/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'operator'), '/api/save_or_update_expedition/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'operator'), '/api/get_expedition/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'operator'), '/api/update_deposit/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'operator'), '/api/add_deposit/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'operator'), '/api/get_mine_area_count/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'operator'), '/api/get_mine_areas/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'operator'), '/api/update_mine_area/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'operator'), '/api/add_mine_area/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'operator'), '/api/get_reserves_for_deposit/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'operator'), '/api/get_reserves_for_mine_area/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'operator'), '/api/get_reserve_for_deposit/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'operator'), '/api/get_reserves_description/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'operator'), '/api/add_or_update_reserves_description/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'operator'), '/api/add_reserves_for_deposit/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'operator'), '/api/update_reserves_for_deposit/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'operator'), '/api/add_reserves_for_mine_area/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'operator'), '/api/update_reserves_for_mine_area/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'operator'), '/api/get_license_count/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'operator'), '/api/get_licenses/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'operator'), '/api/get_license_description/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'operator'), '/api/get_license/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'operator'), '/api/add_license/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'operator'), '/api/update_license/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'operator'), '/api/get_movement/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'operator'), '/api/update_movement/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'operator'), '/api/select_possible_components/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'operator'), '/api/balans_report_xlsx/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'operator'), '/api/balans_report_xlsx_with_area/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'operator'), '/api/balans_report_with_group_xlsx/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'operator'), '/api/download_xlsx_report/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'operator'), '/api/balans_report_html/');

INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'operator'), '/api/get_groups/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'operator'), '/api/get_group/');

INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'operator'), '/api/get_group_mappings/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'operator'), '/api/get_group_mapping/');

INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'operator'), '/api/get_groups_count/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'operator'), '/api/get_group_mappings_count/');

INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'operator'), '/api/get_groups_with_usage/');

INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'viewer'), '/api/get_areas_count/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'viewer'), '/api/get_areas/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'viewer'), '/api/add_area/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'viewer'), '/api/get_all_dictionaries/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'viewer'), '/api/get_dictionary_count/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'viewer'), '/api/get_dictionary_contents/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'viewer'), '/api/get_dictionary_item_description/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'viewer'), '/api/get_districts/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'viewer'), '/api/get_district_count/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'viewer'), '/api/get_deposits_count/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'viewer'), '/api/get_deposits/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'viewer'), '/api/get_deposit/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'viewer'), '/api/get_mine_area/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'viewer'), '/api/get_coordinates/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'viewer'), '/api/get_train_station/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'viewer'), '/api/get_inhab_area/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'viewer'), '/api/get_expedition/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'viewer'), '/api/get_mine_area_count/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'viewer'), '/api/get_mine_areas/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'viewer'), '/api/get_reserves_for_deposit/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'viewer'), '/api/get_reserves_for_mine_area/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'viewer'), '/api/get_reserve_for_deposit/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'viewer'), '/api/get_reserves_description/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'viewer'), '/api/get_license_count/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'viewer'), '/api/get_licenses/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'viewer'), '/api/get_license_description/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'viewer'), '/api/get_license/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'viewer'), '/api/get_movement/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'viewer'), '/api/select_possible_components/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'viewer'), '/api/balans_report_xlsx/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'viewer'), '/api/balans_report_xlsx_with_area/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'viewer'), '/api/balans_report_with_group_xlsx/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'viewer'), '/api/download_xlsx_report/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'viewer'), '/api/balans_report_html/');

INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'viewer'), '/api/get_groups/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'viewer'), '/api/get_group/');

INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'viewer'), '/api/get_group_mappings/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'viewer'), '/api/get_group_mapping/');

INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'viewer'), '/api/get_groups_count/');
INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'viewer'), '/api/get_group_mappings_count/');

INSERT INTO Razresheniya(id_roli, resurs) VALUES((SELECT id FROM Roli WHERE Rol = 'viewer'), '/api/get_groups_with_usage/');
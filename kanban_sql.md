# Kanban SQL

## Tables:
 - kunden
 - produktauslieferungen
 - produktionslinie
 - produktionslinien
 - umsatz

## Kunden:
 - kundenid int(11) NO PRI None auto_increment
 - KU_ID int(11) YES  None 
 - KG_ID int(11) YES  None 
 - KU_NR int(11) YES MUL None 
 - KU_DEBITOR int(11) YES  None 
 - Firma varchar(60) YES  None 
 - Firma2 varchar(60) YES  None 
 - Strasse varchar(100) YES  None 
 - Plz varchar(10) YES  None 
 - Ort varchar(100) YES  None 
 - Land varchar(20) YES  None 
 - Telefon varchar(20) YES  None 
 - Fax varchar(20) YES  None 
 - Email varchar(50) YES  None 
 - Homepage varchar(50) YES  None 
 - Kreditinstitut varchar(100) YES  None 
 - Bankleitzahl varchar(50) YES  None 
 - Kontonummer varchar(50) YES  None 
 - Erstkontaktdatum date YES  None 
 - Steuernummer varchar(20) YES  None 
 - Notizen text YES  None 
 - Lieferbedingungen varchar(50) YES  None 
 - KU_ZNETTOTAGE int(11) YES  None 
 - KU_ZSKONTO int(11) YES  None 
 - KU_ZSKONTOTAGE int(11) YES  None 
 - KU_UMSATZ decimal(10,2) YES  None 
 - KU_UMSATZ_LETZTESJAHR decimal(10,2) YES  None 
 - KU_GESUMSATZ decimal(10,2) YES  None 
 - Sperrung tinyint(1) YES  None 
 - Freigabe tinyint(1) YES  None 
 - Typ varchar(50) YES  None 
 - Status varchar(50) YES  None 
 - zeitpunkt timestamp YES  None 
 - readout tinyint(1) YES  None 
 - readout_umsatz tinyint(1) YES  None

## Produktauslieferungen:
 - id int(11) NO PRI None auto_increment
 - vpid int(11) YES  None 
 - artikelnummer varchar(50) YES  None 
 - bezeichnung varchar(100) YES  None 
 - seriennummer varchar(80) YES  None 
 - lieferscheindatum date YES  None 
 - lieferscheindateipfad varchar(500) YES  None 
 - lieferscheindaten blob YES  None 
 - readout tinyint(4) YES  None 
 - geloescht tinyint(1) YES  0  

## Produktionslinie:
 - id int(11) NO PRI None auto_increment
 - vp_id int(11) NO  None 
 - vo_id int(11) NO  None 
 - vo_nummer varchar(30) NO  None 
 - vo_datum date NO  None 
 - ku_nr int(11) NO  None 
 - ar_nr varchar(25) NO  None 
 - ar_match varchar(80) NO  None 
 - vp_menge double NO  None 
 - vp_erlmenge double NO  None 
 - me_text varchar(30) NO  None 
 - produktionslinie varchar(80) NO  None 
 - vp_liefer_kw int(11) NO  None 
 - vp_liefer_kwj int(11) NO  None 
 - vp_lieferdatum date NO  None 
 - ku_anschrift varchar(1000) NO  None 
 - vp_delete int(11) NO  None 
 - vo_status int(11) NO  None 
 - vo_art int(11) NO  None 
 - zeitpunkt timestamp NO  CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP
 - readout int(11) NO  None 
 - beschreibung_kurz varchar(255) YES  None 
 - beschreibung varchar(255) YES  None 
 - vorgang_text varchar(255) YES  None 
 - prodlinie_optima_id tinyint(4) YES  None 

### Example:
Produktionslinie:
id: 1
vp_id: 3146213
vo_id: 550656
vo_nummer: AU-201905/133687
vo_datum: 2019-05-21
ku_nr: 30076
ar_nr: 166
ar_match: Heidelberger Liegebär 'Lasse' Gr. 2
vp_menge: 1.0
vp_erlmenge: 1.0
me_text: Stück
produktionslinie: Rückenliegebrett (Lasse/DaVinci)
vp_liefer_kw: 24
vp_liefer_kwj: 2019
vp_lieferdatum: 2019-06-10
ku_anschrift: ORATHO GmbH
z.Hd. Herr  Metzger
Berliner Str. 312

63067 Offenbach
Deutschland

vp_delete: 0
vo_status: 0
vo_art: 0
zeitpunkt: 2019-06-11 00:00:00
readout: 0
beschreibung_kurz: None
beschreibung: None
vorgang_text: None
prodlinie_optima_id: None

## Produktionslinien:
 - prodlinie_optima_id tinyint(4) NO PRI None 
 - prodlinie_optima_bezeichnung varchar(500) NO  None 

## Umsatz:
 - umsatzid int(11) NO PRI None auto_increment
 - umsatzjahr varchar(4) YES  None 
 - kundenid int(11) YES  None 
 - warengruppeid int(11) YES  None 
 - warengruppe varchar(100) YES  None 
 - umsatz decimal(10,2) YES  None 
 - zeitpunkt timestamp YES  None 
 - readout tinyint(1) YES  None 

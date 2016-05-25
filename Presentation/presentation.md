# Us avançat de journalctl i la seva sortida en format JSON

**Autor:** Sergi Ruiz Carrasco

**Data:** 25/05/2016

**Curs:** ASIX2

----------------

# Syslog

Les principals limitacions són:

1. Les dades no estan ni verificades ni autenticades.

2. Els logs tenen un format lliure, per tant dificulta la seva interpretació, tant per identificar el tipus de missatge com per a parsejar els seus paràmetres.

3. Els timestamps (data i hora) generalment no tenen informació sobre la zona horària.

4. Syslog és només una de les moltes aplicacions per a logs. El que provoca que es trobin logs en diferents sistemes.

----------------

# Syslog

5. Llegir els logs és ineficient, ja que la indexació generalment no està disponible.

6. El funcionament del syslog és simple pero molt limitat, només soporta el model de *push transfer* 
 i no utilitza un sistema de *store-and-forward* o de pèrdua de paquets.
 
7. Els archius de log són facilment manipulables per atacants, de manera que és fàcil amagar informació d'atacs del administrador.

8. El control d'accés és inexistent. A menys que es programi per l'administrador, un usuari tindrà accés total o nul.

----------------

# Syslog


9. La metadata enmagatzemada està limitada i falta informació clau com el nom de servei, el timestamp monòton...

10. La rotació automàtica dels fitxers de log està disponible, però en la majoria de les implementacións no és ideal.
En comptes de fixarse en l'utilització de disc de forma contínua, només ho fa en intervals de temps fixe, el que provoca una vulnerabilitat contra atacs de DDOS.

11. El *rate limiting* està disponible en algunes implementacions, però generalment no té en compte l'utilització de disc o l'assignació de serveis.

----------------

# Syslog

12. La compressió  de l'estructura de logs normalment està disponible però només com un efecte de la rotació i té efectes negatius en comportament de moltes operacions amb els logs.

13. El syslog més clàssic no suporta el log dels primers moments del boot o els últims moments del shutdown, encara que les noves implementacions si que ho fan.

14. No es pot fer log de dades en binari, que en alguns casos és esencial.

----------------

# Journal

Els principals objectius en la creació del Journal són:

1. **Simplicitat:** Poc codi

2. **Manteniment Zero**

3. **Robustesa:** Els fitxers de journal es poden copiar a diferents hosts amb eines com *scp* o *rsync*.

4. **Portable:** Els fitxers són utilitzables en tots els tipus de sistemes Linux.

5. **Rendiment:** Les operacions per afegir o buscar al journal són rapides en termes de complexitat.

6. **Integració:** Està completament integrat en la resta del sistema.

----------------

# Journal

7. **Mínim rastre:** Els fitxers són petits en tamany de disc.

8. **Emmagatzematge de qualsevol esdeveniment:** És capaç d'inserir qualsevol tipus d'entrada.

9. **Unificació:** Uneix els diferents tipus de tecnologies de logs.

10. **Base per a eines d'alt nivell**

11. **Escalabilitat:** Serveix tant per màquines petites com per a superordinadors.

12. **Universalitat:** S'adapta a les necesitats de totes les aplicacions.

----------------

# Journal

13. **Clusterització i xarxa:** Accepta instalacions en multi-host.

14. **Seguretat:** Els fitxers de log estan autenticats de manera que fan imposible la manipulació sense detectar.

----------------

# Per què utilizar JSON?

JSON s'utilitza principalment com a format per a intercanviar dades.

Un altre llenguatge utilitzat per al mateix motiu és el conegut XML.

----------------

## Extensible Markup Language

XML és l'abrebiatura per a Extensible Markup Language. 

El XML és fàcil i extremadament flexible.

El XML utilitza tags definits per l'usuari i utilitza elements i atributs per tal de descriure les dades.

El format XML pot ser parsejat utilitzant un parsejador de XML.

----------------

Per exemple:

		<?xml version=“1.0” encoding=“UTF-8”?>
		<Addresses>
			<Address>
				<name>Lakshmi</name>
				<street>John Street</street>
				<city>Vizag</city>
				<state>Andhra Pradesh</state>
			</Address>
			<Address>
				<name>Karuna</name>
				<street>Roy Street</street>
				<city>Kolkata</city>
				<state>West Bengal</state>
			</Address>
		</Addresses>

----------------

## JavaScript Object Nation

JSON és un acrònim per a JavaScript Object Nation. 

L'objectiu amb el qual es va desenvolupar el JSON era que fos 
un llenguatge d'intercanvi de dades fàcil de llegir per a humans i simple d'utilitzar i parsejar per ordinadors.

JSON és auto-descriptiu i simple d'entendre.

El format JSON està basat en text i la seva sintaxis un subconjunt de la sintaxis de JavaScript.

En comptes d'utilitzar un pasejador, una funció standard de
JavaScript pot ser utilitzada per a parsejar dades en JSON.

----------------

## JavaScript Object Nation

JSON utilitza arrays i objectes.

* Un array conté un conjunt ordenat de valors. En JSON els arrays començen amb '\[' i
acaben amb '\]' i els valors estan separats per comes.

* En JSON un objecte és un conjunt desordenat de parelles de nom/valor.
Comencen per '{' i acaben per '}'. El nom i el valor estan separats per ':' i les parelles que formen l'objecte estan separades
per comes.

Els objectes i els arrays poden ser niats.

----------------

# JSON -----> Python

* object --------------> dict

* array ---------------> list

* string --------------> unicode

* number (int) ------> int, long

* number (real) -----> float

* true ----------------> True

* false ---------------> False

* null ----------------> None

----------------

Per exemple:

	{“Addresses”:
		{“Address”:
		[{
				“name”:“Lakshmi”,
				“street”:“John Street”,
				“city”:“Vizag”,
				”state”: “Andhra Pradesh”
			},
			{
				“name”: “Karuna”,
				“street”: “Roy Street”,
				“city”: “Kolkata”,
				“state”: “West Bengal”
			}]  
		}
	}

----------------

# XML

1. Conté Tags. A vegades sufreix a cause d'utilitzarlos massa freqüentment.

2. XML és més dificil que el JSON.

3. Parsejar i formatar dades en XML és poc eficient.

4. Parsejar dades en XML requereix més temps.

5. Parsejar dades en XML requereix més memòria.

6. XML no pot utilitzar arrys.

7. XML és extremadament flexible.

----------------

# JSON

1. No conté Tags.

2. JSON és més concís que el XML.

3. Comparat amb el XML, JSON es pot parsejar eficientment.

4. Parsejar dades en JSON utilitza ments temps que pasejar XML.

5. Comparat amb el XML, parsejar JSON requereix menys memòria.

6. JSON pot utilitzar arrays.

7. JSON és bastant flexibgle i molt més efectiu que el XML.

----------------

# Journalctl

Com el systemctl, el journalctl és també una utilitat del systemd.

S'utilitza per a consultar i mostrar misatges del journal.

Com que el journal esta format per un o més archius binaris, el journalctl és la manera estandard de llegir-lo.

Si s'utiliza sense paràmetres, el següent paràmetre mostrarà totes les entrades del journal (que poden ser moltes).

		journalctl

----------------

# Journalctl

**-n** o **--lines=**

> Mostra el numero d'entrades especificat.

**-r** o **--reverse**

> Mostra les entrades en ordre cronològic invers.


----------------

## Missatges d'arrencada

**-b** o **--boot**

> Missatges relacionats amb el boot actual.

		journalctl --boot -1

> > Missatges relacionats amb el boot anterior.

**--list-boots**

> Llista les arrencades del sistema.

----------------

## Rangs de temps

**--since=** i **--until=**

> Serveixen per especificar una finestra de temps.

## Per Unit

**-u** o **--unit=**

> Serveix per a mostrar els logs d'un servei en concret.

----------------

## Follow

**-f** o **--follow**

> Mostra continuament cada entrada que s'afegeix al journal.

## Per usuari

> Es poden filtrar les entrades relacionades amb qualsevol usuari mitjançant el seu UID:

		journalctl \_UID=nºUID

----------------

## Formats de sortida

**-o** o **--output=**

Alguns valors que pot pendre són:

* **cat:** mostra nomes el camp de missatge.

* **json:** formateja les entrades com a estructures de dades JSON, un per línia.

* **json-pretty:** formateja les entrades com a estructures de dades JSON però en múltiples línies per tal de fer-ho més llegible per a humans.

* **short:** és el format per defecte.

* **verbose:** mostra l'estructura sencera d'elements amb tots els camps.

----------------

## Per prioritat

**-p** o **--priority=**

Els nivells de prioritat són els següents:

* 0: emerg
* 1: alert
* 2: crit
* 3: err
* 4: warning
* 5: notice
* 6: info
* 7: debug

----------------

# Camps del Journal

## Camps d'usuari

Els camps d'usuari són camps que provenen directament del client i són emmagatzemats al journal.

MESSAGE=, MESSAGE\_ID=, PRIORITY=, CODE\_FILE=, CODE\_LINE=, CODE\_FUNC=, ERRNO=, SYSLOG\_FACILITY=, SYSLOG\_IDENTIFIER=, SYSLOG\_PID=

----------------

## Camps segurs

Els camps precedits per '\_' són camps segurs. 

Són camps afegits pel journal i no poden ser modificats per un usuari.

\_PID=, \_UID=, \_GID=, \_COMM=, \_EXE=, \_CMDLINE=, \_CAP\_EFFECTIVE=, \_AUDIT\_SESSION=, \_AUDIT\_LOGINUID=, 
\_SYSTEMD\_CGROUP=, \_SYSTEMD\_SESSION=, \_SYSTEMD\_UNIT=, \_SYSTEMD\_USER\_UNIT=, \_SYSTEMD\_OWNER\_UID=, \_SYSTEMD\_SLICE=, 
\_SELINUX_CONTENT=, \_SOURCE\_REALTIME\_TIMESTAMP=, \_BOOT\_ID=, \_MACHINE\_ID=, \_HOSTNAME=, \_TRANSPORT=

----------------

## Camps de kernel

Són camps utilitzats pels missatges generats en el kernel.

\_KERNEL\_DEVICE=, \_KERNEL\_SUBSYSTEM=, \_UDEV\_SYSNAME=, \_UDEV\_DEVNODE=, \_UDEV\_DEVLINK=

## Camps d'adreça

\_\_CURSOR=, \_\_REALTIME\_TIMESTAMP=, \_\_MONOTONIC\_TIMESTAMP=

----------------

## Camps per a fer log a favor d'un altre programa

Camps utilitzats per programes per especificar que estar fent logging a favor d'un altre programa o unitat.

COREDUMP\_UNIT=, COREDUMP\_USER\_UNIT=, OBJECT\_PID=, OBJECT\_UID=, OBJECT\_GID=, OBJECT\_COMM=, OBJECT\_EXE=, 
OBJECT\_CMDLINE=, OBJECT\_AUDIT\_SESSION=, OBJECT\_AUDIT\_LOGINUID=, OBJECT\_SYSTEMD\_CGROUP=, OBJECT\_SYSTEMD\_SESSION=, 
OBJECT\_SYSTEMD\_OWNER\_UID=, OBJECT\_SYSTEMD\_UNIT=, OBJECT\_SYSTEMD\_USER\_UNIT=

----------------

# Journal2mysql

Programa que exporta els logs del journalctl en format JSON per a insertar-los en una base de dades mysql.

Utilització:

> journalctl --output=json | journal2mysql.py \[--user\] \[--password\] \[--database\] \[--table\] \[--new\] \[--truncate\]

----------------

## Paràmetres:

* -u *username*, --user *username*

* -p *password*, --password *password*

* -d *dbname*, --database *dbname*

* -t *tablename*, --table *tablename*

* -n, --new

* -T, --truncate

----------------

# GRÀCIES

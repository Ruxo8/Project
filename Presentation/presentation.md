# Us avançat de journalctl

**Autor:** Sergi Ruiz Carrasco

**Data:** 25/05/2016

**Curs:** ASIX2

----------------

# Syslog

Les principals limitacions són:

1. Dades no verificades ni autenticades.

2. Els logs tenen un format lliure.

3. Timestamps sense zona horària.

4. Logs de moltes aplicacions diferents.

----------------

# Syslog

5. Logs sense indexació: **Ineficient**.

6. Funcionament simple però molt limitat.
 
7. Fàcilment manipulable per atacants.

8. Control d'accés inexistent.

----------------

# Syslog


9. Metadades emmagatzemades limitades.

10. Rotació automàtica no disponible o vulnerable a atacs de DDOS.

11. *Rate limiting* només disponible en algunes implementacions, però generalment no té en compte la utilització de disc o l'assignació de serveis.

----------------

# Syslog

12. Mala compressió  de l'estructura de logs.

13. No suporta el early boot o late shutdown.

14. No es pot fer log de dades en binari.

----------------

# Journal

Els principals objectius en la creació del Journal són:

1. **Simplicitat:** Poc codi

2. **Manteniment Zero**

3. **Robustesa:** Fitxers copiables a diferents hosts.

4. **Portable:** Fitxers utilitzables en tots els tipus de sistemes Linux.

5. **Rendiment:** Operacions ràpides en termes de complexitat.

6. **Integració:** Completament integrat en el sistema.

----------------

# Journal

7. **Mínim rastre:** Fitxers petits.

8. **Emmagatzematge de qualsevol esdeveniment**

9. **Unificació:** Unió de diferents tecnologies de logs.

10. **Base per a eines d'alt nivell**

11. **Escalabilitat:** Tant per a màquines petites com per a superordinadors.

12. **Universalitat:** S'adapta a les necessitats de totes les aplicacions.

----------------

# Journal

13. **Clusterització i xarxa:** Accepta instal·lacions en multi-host.

14. **Seguretat:** Fitxers de log autenticats.

----------------

# Journalctl

Com el systemctl, el journalctl és també una utilitat del systemd.

S'utilitza per a consultar i mostrar missatges del journal.

Com que el journal està format per un o més arxius binaris, el journalctl és la manera estandard de llegir-ho.

Si s'utiliza sense paràmetres, la següent ordre mostrarà totes les entrades del journal (que poden ser moltes).

		journalctl

----------------

# Journalctl

**-n** o **--lines=**

> Mostra el número d'entrades especificat.

**-r** o **--reverse**

> Mostra les entrades en ordre cronològic invers.

----------------

## Missatges d'arrencada

Per habilitar l'emmagatzematge persistent:

*/etc/systemd/journald.conf*

		...
		[Journal]
		Storage=persistent

		sudo mkdir -p /var/log/journal

		systemctl restart systemd-journald

----------------

## Missatges d'arrencada

**-b** o **--boot=**

> Missatges relacionats amb el boot actual.

		journalctl --boot=-1

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

		journalctl --unit=nom\_servei1 
		--unit=nom\_servei2 --since=today

> > Logs d'un o més serveis en una finestra de temps.

----------------

## Per camp

Per PID:

		journalctl \_PID=6000

Per UID:

		journalctl \_UID="num UID"

Per GID:

		journalctl \_GID="num GID"

----------------

## Per camp

Per filtrar per qualsevol camp:

		journalctl "nomcamp"="valorcamp"

Per filtrar per més d'un camp a la vegada (AND):

		journalctl "nomcamp1"="valorcamp1" 
		"nomcamp2"="valorcamp2"

Per filtrar per un camp o un altre (OR):

		journalctl "nomcamp1"="valorcamp1" 
		+ "nomcamp2"="valorcamp2"

----------------

## Per camp


"nomcamp1"="valorcamp1" **AND** **(**"nomcamp2"="valorcamp2" **OR** "nomcamp2"="valorcamp3"**)**

		journalctl "nomcamp1"="valorcamp1" 
		"nomcamp2"="valorcamp2" 
		"nomcamp2"="valorcamp3"

Per trobar tots els valor que conté el journal per a un camp:

		journalctl --field="nomcamp"

----------------

## Per ruta

Si la ruta té un executable, mostrarà totes les entrades relacionades.

Per buscar entrades relacionades amb el bash:

		journalctl /usr/bin/bash

----------------

## Entrades del kernel

**-k** o **--dmesg**

> Per mostrar entrades relacionades amb el kernel:

Implica el **--boot** i filtra per "\_TRANSPORT=kernel"

----------------

## Follow

**-f** o **--follow**

> Mostra contínuament cada entrada que s'afegeix al journal.

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

## Sortida

**--all**

> Mostra tota la informació, encara que tingui caràcters no imprimibles.

**--no-pager**

> Mostra la sortida per sortida estàndard.

----------------

## Formats de sortida

**-o** o **--output=**

Alguns valors que pot prendre són:

* **cat:** mostra només el camp del missatge.

* **export:** format binari per a transferir o realitzar backups.

* **json:** formateja les entrades com a estructures de dades JSON, una per línia.

* **short:** és el format per defecte.

* **verbose:** mostra l'estructura sencera d'elements amb tots els camps.

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
\_SELINUX\_CONTENT=, \_SOURCE\_REALTIME\_TIMESTAMP=, \_BOOT\_ID=, \_MACHINE\_ID=, \_HOSTNAME=, \_TRANSPORT=

----------------

## Camps de kernel

Són camps utilitzats pels missatges generats en el kernel.

\_KERNEL\_DEVICE=, \_KERNEL\_SUBSYSTEM=, \_UDEV\_SYSNAME=, \_UDEV\_DEVNODE=, \_UDEV\_DEVLINK=

## Camps d'adreça

\_\_CURSOR=, \_\_REALTIME\_TIMESTAMP=, \_\_MONOTONIC\_TIMESTAMP=

----------------

## Camps per a fer log a favor d'un altre programa

Camps utilitzats per programes per especificar que està fent logging a favor d'un altre programa o unitat.

COREDUMP\_UNIT=, COREDUMP\_USER\_UNIT=, OBJECT\_PID=, OBJECT\_UID=, OBJECT\_GID=, OBJECT\_COMM=, OBJECT\_EXE=, 
OBJECT\_CMDLINE=, OBJECT\_AUDIT\_SESSION=, OBJECT\_AUDIT\_LOGINUID=, OBJECT\_SYSTEMD\_CGROUP=, OBJECT\_SYSTEMD\_SESSION=, 
OBJECT\_SYSTEMD\_OWNER\_UID=, OBJECT\_SYSTEMD\_UNIT=, OBJECT\_SYSTEMD\_USER\_UNIT=

----------------

# Ús avançat del Journalctl

Control d'accés:

		usermod --append --groups=adm username

Veure utilització de disc:

		journalctl --disk-usage

----------------

## Esborrar logs antics

Per tamany:

		journalctl --vacuum-size=1G

Per temps:

		journalctl --vacum-time=1years

----------------

## Limitar el tamany del Journal

*/etc/systemd/journald.conf*

* SystemMaxUse=

* SystemKeepFree=

* SystemMaxFileSize=

* RuntimeMaxUse=

* RuntimeKeepFree=

* RuntimeMaxFileSize=

----------------

## Consultar logs d'es de l'entorn gràfic

Instal·lació:

		yum install gnome-system-log

Execució:

		gnome-system-log

----------------

# Conclusió

El journal és una eina molt potent per a recollir i administrar els logs tant del sistema com d'aplicacions.

Té una gran flexibilitat a causa, principalment, de totes les metadades que recull i del seu sistema centralitzat.

L'ordre *journalctl* facilita molt la utilització del journal i és molt útil per a realitzar anàlisi 
i trobar errors en diferents aplicacions o processos del sistema.

----------------

# GRÀCIES

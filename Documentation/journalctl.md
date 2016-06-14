# Journalctl

Com el systemctl, el journalctl és també una utilitat del systemd.
S'utilitza per a consultar i mostrar missatges del journal.
Com que el journal està format per un o més arxius binaris, el journalctl és la manera estandard de llegir-ho.

Abans de començar a utilitzar el journal, és necessàri asegurar-se de que el temps del sistema és correcte.
Per això primer mostrarem les zones horàries disponibles:

		timedatectl list-timezones

Com surten moltes possibilitats, serà millor acotar la búsqueda:

		timedatectl list-timezones | grep "Europe"

Finalment, establim la zona horària adecuada:

		sudo timedatectl set-timezone "zone"

En el nostre cas:

		sudo timedatectl set-timezone Europe/Madrid

Per a comprobar-ho:

		timedatectl status

		      Local time: Tue 2016-06-07 09:29:20 CEST
		  Universal time: Tue 2016-06-07 07:29:20 UTC
		        RTC time: Tue 2016-06-07 09:29:20
		       Time zone: Europe/Madrid (CEST, +0200)
		 Network time on: yes
		NTP synchronized: yes
		 RTC in local TZ: yes

Ens hauríem de fixar en la primera línia i comprovar que és correcte.

##Ús bàsic del journalctl

La majoria de paràmetres de la ordre s'utilitzen per a limitar l'abast de la consulta.

Si s'utiliza sense paràmetres, la següent ordre mostrarà totes les entrades del journal (que poden ser moltes).

		journalctl

A l'executar journalctl la primera línia serà semblant a:

		-- Logs begin at Sat 2015-12-19 15:56:22 CET, end at Tue 2016-05-24 22:45:42 CEST. --

Informant sobre les dates que cobreixen les entrades.

A continuació el journal mostrarà les entrades com si les llegissim amb un *less*

Podem limitar el nombre d'entrades a mostrar i mostrarà les 'n' entrades més recents amb *-n* o *--lines=*

		journalctl --lines 20

El paràmetre *-r* o *--reverse* mostrarà les entrades en ordre cronològic invers, per tant, mostrarà primer les més recents.

		journalctl -r

## Missatges d'arrencada

Per veure els missatges relacionats amb l'arrencada actual, s'ha d'utilitzar el paràmetre *-b* o *--boot*

		journalctl --boot

### Boots anteriors

Normalment, voldrem consultar informació sobre l'arrencada actual, però, a vegades, la informació d'arrencades anteriors també ens serà útil.
Algunes distribucions habiliten l'enmagatzemament d'informació d'anteriors arrencades per defecte, per d'altres no.
Per a habilitar-ho, podem canviar la configuració en el fitxer: */etc/systemd/journald.conf*
A sota de *[ Journal ]* establir l'opció *Storage=* com a "persistent":

		. . .
		[Journal]
		Storage=persistent

També haurem de crear el directori on es guardaran els fitxers de log (*/var/log/journal*):

		sudo mkdir -p /var/log/journal

I reiniciar el journald per aplicar els canvis:

		systemctl restart systemd-journald

Per a veure les entrades relacionades amb l'anterior arrencada s'utilitza el modificador *-1*, per l'anterior: *-2*; i així succesivament.

		journalctl --boot=-1

Per a llistar les arrencades del sistema s'utilitza el paràmetre *--list-boots*:

		journalctl --list-boots

En cas de que no estiguem utilitzant aquesta opció, el journalctl insertarà una línia cada vegada que el sistema s'ha apagat.

		-- Reboot --

## Rangs de temps

Per a mostrar les entrades en una finestra de temps específica, podem utilitzar els paràmetres *--since=* i *--until=*.

Per a mostrar els logs de l'última hora:

		journalctl --since="1 hour ago"

Per a mostrar els logs entre 2 dates i hores:

		journalctl --since="2016-05-23 12:00:00" --until="2016-05-24 12:00:00"

## Per unit

Per mostrar entrades d'un servei del sistema, s'utilitza el paràmetre *-u* o *--unit=*.

		journalctl --unit=nom-servei

Es poden mostrar entrades de múltiples serveis:

		journalctl --unit=nom_servei1 --unit=nom_servei2

Per mostrar, per exemple, els missatges relacionats amb un o més serveis executats avui:

		journalctl --unit=nom_servei1 --unit=nom_servei2 --since=today

## Per camp

A vegades, ens pot interessar filtrar els missatges per el número de PID.
Per exemple: si estiguéssim interessats en el procés que té el PID 6000, hauríem de seleccionar els missatges on el camp
_PID fos 600. Per a aconseguir això faríem:

		journalctl _PID=6000

Per filtrar per el UID:

		journalctl _UID="num UID"

I per filtrar per el GID:

		journalctl _GID="num GID"

Aquests són exemples de camps que es poden utilitzar per filtrar. 
Hi han camps que s'especifiquen pel servei que escriu el log, i d'altres que els escriu el journal en el moment que es realitza el log
agafant les dades del sistema.
El "_" de davant d'un camp, ens indica que és el journal el que ha escrit aquest camp.

Per tant, si volguéssim filtrar per qualsevol camp:

		journalctl "nomcamp"="valorcamp"

També es pot filtrar per més d'un camp a la vegada (**AND**):

		journalctl "nomcamp1"="valorcamp1" "nomcamp2"="valorcamp2"

Per l'exemple anterior, si volguéssim que es complís només una de les dues condicions (**OR**):

		journalctl "nomcamp1"="valorcamp1" + "nomcamp2"="valorcamp2"

De totes formes, si posem més d'una condició per a un mateix camp, el journalctl ja ho entendrà com un OR.
Per tant, aquesta ordre:

		journalctl "nomcamp1"="valorcamp1" "nomcamp2"="valorcamp2" "nomcamp2"="valorcamp3"

Seria com fer: *("nomcamp1"="valorcamp1" AND ("nomcamp2"="valorcamp2" OR "nomcamp2"="valorcamp3"))*

A l'hora de filtrar, el camp *-F* o *--field=* ens serveix per mostrar els possibles valors dels quals el journal té entrades.
Per exemple, si volguéssim veure els valors de GID dels qual el journal té entrades:

		journalctl --field=_GID

Per tant, si volguéssim mostrar tots els valors que té el journal per un camp:

		journalctl --field="nomcamp"

Per a veure informació sobre els camps del journal:

		man systemd.journal-fields

## Per ruta

També es pot filtrar per la ruta de l'executable (si és que existeix).

Si la ruta conté un executable, journalctl mostrarà totes les entrades que tinguin relació amb aquell executable.

Per exemple, si volguéssim trobar totes les entrades relacionades amb el *bash*:

		journalctl /usr/bin/bash

## Mostrar missatges del kernel

Per mostrar missatges relacionats amb el kernel, hem d'utilitzar *-k* o *--dmesg*

		journalctl --dmesg

Aquest argument implica el *-b* o *--boot* i filtra per *"_TRANSPORT=kernel"*

Si volguéssim mostrar missatges de boots anteriors, podríem filtrar-los amb *--boot=nºboot*

## Follow

Per a mostrar continuament els missatges de log que s'afegeixen, s'utilitza *-f* o *--follow*.

## Per prioritat

El paràmetre *-p* o *--priority=* ens permet filtrar les entrades segons el nivell de prioritat.

		journalctl --priority=0

Els nivells de prioritat són els següents:

* 0: emerg
* 1: alert
* 2: crit
* 3: err
* 4: warning
* 5: notice
* 6: info
* 7: debug

Amb *-p* o *--priority* es pot utilitzar tant el número de prioritat com el nom de la prioritat.

Quan seleccionem una prioritat, el journalctl mostrarà tots els logs d'aquella priotitat i els que estan per sobre.
És a dir, si seleccionem prioritat 2, mostrarà les entrades de prioritat 2, 1 i 0.

# Modificar l'aparença del journal

## Tota la informació

Amb *-a* o *--all* el journalctl mostrarà tota la informació encara que contingui caràcters no imprimibles.

		journalctl --all

## Sortida

Per defecte el journalctl mostra la sortida en un paginador tipus *less*, pero si volem processar la sortida,
serà millor que mostri la sortida per sortida estàndard.

Això es pot especificar amb *--no-pager*:

		journalctl --no-pager

## Formats de sortida

El paràmetre *-o* o *--output=* ens permetrà seleccionar el format amb el que volem que el journalctl ens mostri les entrades.

Els valors que pot prendre són:

* **cat:** mostra només el camp de missatge.

* **export:** un format binari pensat per transferir o fer un back up.

* **json:** formateja les entrades com a estructures de dades JSON, una per línia.

* **json-pretty:** formateja les entrades com a estructures de dades JSON però en múltiples línies per tal de fer-ho més llegible per a humans.

* **json-sse:** formateja les entrades com a estructures de dades de JSON embolcallades per a que sigui compatible amb server-sent event.

* **short:** és el format per defecte.

* **short-iso:** és el format per defecte modificat per tal que mostri els timestamps en format ISO 8601.

* **short-monotonic:** el mateix que el format *short* però mostra els timestamps en format monòton.

* **short-precise:** el mateix que el format *short* però amb precisió de microsegons.

* **verbose:** mostra l'estructura sencera d'elements amb tots els camps.

# Camps del Journal

## Camps d'usuari

Els camps d'usuari són camps que provenen directament del client i són emmagatzemats al journal.

* MESSAGE=
> El missatge en format llegible per a humans. És el text principal que es mostra a l'usuari, normalment no està traduït i no
està pensat per ser parsejat per a metadades.

* MESSAGE\_ID=
> Un identificador de 128 bits del missatge. Es recomana que sigui compatible amb UUID. 
Els desenvolupadors poden generar un de nou amb *journalctl --new-id*.

* PRIORITY=
> Un valor de prioritat enre 0 i 7.

* CODE\_FILE=, CODE\_LINE=, CODE\_FUNC=
> Localització del codi que genera el missatge. Conté el nom del fitxer, el número de la línia i el nom de la funció.

* ERRNO=
> El número d'error UNIX de baix nivell.

* SYSLOG\_FACILITY=, SYSLOG\_IDENTIFIER=, SYSLOG\_PID=
> Camps compatibles amb el syslog. Contenen la facility, l'identificador i el PID.

## Camps segurs

Els camps precedits per '\_' són camps segurs. Són camps afegits pel journal i no poden ser modificats per un usuari.

* \_PID=, \_UID=, \_GID=
> La ID de procés, d'usuari i de grup del procés que origina l'entrada.

* \_COMM=, \_EXE=, \_CMDLINE=
> El nom, la ruta de l'executable i la línia de comandes del procés que origina l'entrada.

* \_CAP\_EFFECTIVE=
> Les capacitats efectives del procés.

* \_AUDIT\_SESSION=, \_AUDIT\_LOGINUID=
> La sessió i el UID de login del procés.

* \_SYSTEMD\_CGROUP=, \_SYSTEMD\_SESSION=, \_SYSTEMD\_UNIT=, \_SYSTEMD\_USER\_UNIT=, \_SYSTEMD\_OWNER\_UID=, \_SYSTEMD\_SLICE=
> La ruta del grup de control, la ID de la sessió de systemd, el nom de la unitat del systemd, el nom d'usuari de la sessió del systemd, 
el UID del propietari de la sessió i la part de la unitat del systemd del procés.

* \_SELINUX_CONTENT=
> El context de seguretat del SELinux.

* \_SOURCE\_REALTIME\_TIMESTAMP=
> El primer camp segur de data i hora. Està en microsegons.

* \_BOOT\_ID=
> La ID de boot del kernel en el boot en que s'origina la entrada.

* \_MACHINE\_ID=
> La ID de la màquina.

* \_HOSTNAME=
> El nom del host.

* \_TRANSPORT=
> Com ha rebut el journal l'entrada. Els valors vàlids són:

> * audit
> > llegit del kernel audit subsystem.

> * driver
> > per a missatges generats internament.

> * syslog
> > per a missatges rebuts a través del socket local de syslog amb el protocol de syslog.

> * journal
> > per a missatges rebuts a través del protocol natiu del journalctl.

> * stdout
> > per a missatges llegits de la sortida estandard del servei o de la sortida d'error.

> * kernel
> > per a missatges llegits del kernel.

## Camps de kernel

Són camps utilitzats pels missatges generats en el kernel.

* \_KERNEL\_DEVICE=
> El nom de dispositiu del kernel.

* \_KERNEL\_SUBSYSTEM=
> El nom del subsistema del kernel.

* \_UDEV\_SYSNAME=
> El nom del dispositiu del kernel tal i com es mostra en l'arbre de dispositius sota /sys.

* \_UDEV\_DEVNODE=
> La ruta al node de dispositiu del dispositiu a /dev.

* \_UDEV\_DEVLINK=
> Nom adicional d'enllaç simbòlic que apunta al node de dispositiu a /dev.

## Camps per a fer log a favor d'un altre programa

Camps utilitzats per programes per especificar que està fent logging a favor d'un altre programa o unitat.

Camps utilitzats pel *systemd-coredump*:

* COREDUMP\_UNIT=, COREDUMP\_USER\_UNIT=
> Utilitzats per a escriure missatges que contenen coredumps del sistema i sessions d'unitats.

* OBJECT\_PID=
> PID del programa al que pertany el missatge.

* OBJECT\_UID=, OBJECT\_GID=, OBJECT\_COMM=, OBJECT\_EXE=, OBJECT\_CMDLINE=, OBJECT\_AUDIT\_SESSION=, OBJECT\_AUDIT\_LOGINUID=, 
OBJECT\_SYSTEMD\_CGROUP=, OBJECT\_SYSTEMD\_SESSION=, OBJECT\_SYSTEMD\_OWNER\_UID=, OBJECT\_SYSTEMD\_UNIT=, OBJECT\_SYSTEMD\_USER\_UNIT=
> Aquests són camps afegits automàticament pel journal. El seu significat és el mateix que:
\_UID=, \_GID=, \_COMM=, \_EXE=, \_CMDLINE=, \_AUDIT\_SESSION=, \_AUDIT\_LOGINUID=, 
\_SYSTEMD\_CGROUP=, \_SYSTEMD\_SESSION=, \_SYSTEMD\_UNIT=, \_SYSTEMD\_USER\_UNIT=, and \_SYSTEMD\_OWNER\_UID=
però fan referència al procés que especifica el PID, en comptes del procés que ha enviat l'entrada.

## Camps d'adreça

* \_\_CURSOR=
> El cursor per a la entrada. Únicament descriu la posició d'una entrada en el journal i és portable entre màquines, 
plataformes i arxius de journal.

* \_\_REALTIME\_TIMESTAMP=
> El timestamp en que el journal ha rebut l'entrada en microsegons.

* \_\_MONOTONIC\_TIMESTAMP=
> El timestamp monòton del moment en que el journal ha rebut l'entrada en microsegons. Per a ser útil com a adreça per a la
entrada, hauria de ser combinat amb la ID de boot ("\_BOOT\_ID=").

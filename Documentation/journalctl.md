# Journalctl

Com el systemctl, el journalctl és també una utilitat del systemd.
S'utilitza per a consultar i mostrar misatges del journal.
Com que el journal esta format per un o més archius binaris, el journalctl és la manera estandard de llegir-lo.

La majoria de paràmetres de la ordre s'utilitzen per a limitar l'abast de la consulta.

Si s'utiliza sense paràmetres, el següent paràmetre mostrarà totes les entrades del journal (que poden ser bastantes).

		journalctl

Al executar journalctl la primera línia sera semblant a:

		-- Logs begin at Sat 2015-12-19 15:56:22 CET, end at Tue 2016-05-24 22:45:42 CEST. --

Informant sobre les dates que cobreixen les entrades mostrades.

A continuació el journal mostrarà les entrades com si les llegisim amb un *less*

Podem limitar el nombre d'entrades a mostrar i mostrarà les 'n' entrades més recents amb *-n* o *--lines=*

		journalctl --lines 20

El paràmetre *-r* o *--reverse* mostrarà les entrades en ordre cronològic invers, per tant mostrarà primer les més recents.

		journalctl -r

## Missatges d'arrencada

Per veure els missatges relacionats amb l'arrencada actual, s'ha d'utilitzar el paràmetre *-b* o *--boot*

		journalctl --boot

Per a veure les entrades relacionades amb l'anterior arrencada s'utilitza el modificador *-1*, per l'anterior: *-2*; i així succesivament.

		journalctl --boot -1

Per a llistar les arrencades del sistema s'utilitza el paràmetre *--list-boots*:

		journalctl --list-boots

## Rangs de temps

Per a mostrar les entrades en una finestra de temps específica, podem utilitzar els paràmetres *--since=* i *--until=*.

Per a mostrar els logs de la última hora:

		journalctl --since="1 hour ago"

Per a mostrar els logs entre 2 dates i hores:

		journalctl --since="2016-05-23 12:00:00" --until="2016-05-24 12:00:00"

## Per Unit

Per mostrar entrades d'un servei del sistema, s'utilitza el paràmetre *-u* o *--unit=*.

		journalctl --unit nom-servei

Es poden mostrar entrades de multiples serveis:

		journalctl --unit nom_servei1 --unit nom_servei2

## Follow

Per a mostrar continuament els missatges de log que s'afegeixen, s'utilitza *-f* o *--follow*.

## Formats de sortida

El paràmetre *-o* o *--output=** ens permetrà seleccionar el format amb el que volem que el journalctl ens mostri les entrades.

Els valors que pot pendre són:

* **cat:** mostra nomes el camp de missatge.

* **export:** un format binari pensat per transferir o fer un back up.

* **json:** formateja les entrades com a estructures de dades JSON, un per línia.

* **json-pretty:** formateja les entrades com a estructures de dades JSON però en múltiples línies per tal de fer-ho més llegible per a humans.

* **json-sse:** formateja les entrades com a estructures de dades de JSON embolcallades per que sigui compatible amb server-sent event.

* **short:** és el format per defecte.

* **short-iso:** és el format per defecte modificat per tal que mostri els timestamps en format ISO 8601.

* **short-monotonic:** el mateix que el format *short* però mostra els timestamps en format monòton.

* **short-precise:** el mateix que el format *short* però amb precisió de microsegons.

* **verbose:** mostra l'estructura sencera d'elements amb tots els camps.

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

Quan seleccionem una prioritat, el journalctl mostrarà tots els d'aquella priotitat i els que estan per sobre.
És a dir, si seleccionem prioritat 2, mostrarà les entrades de prioritat 2, 1 i 0.

## Per usuari

Es poden filtrar les entrades relacionades amb qualsevol usuari mitjançant el seu UID:

		journalctl \_UID=1000

# Camps del Journal

## Camps d'usuari

Els camps d'usuari són camps que provenen directament del client i són emmagatzemats al journal.

* MESSAGE=
> El missatge en format llegible per a humans. Es el text principal que es mostra a l'usuari, normalment no està traduit i no
està pensat per ser parsejat per a metadades.

* MESSAGE\_ID=
> Un identificador de 128 bits del missatge. Es recomana que sigui compatible amb UUID. 
Els desenvolupadors poden generar un de nou amb *journalctl --new-id*.

* PRIORITY=
> Un valor de prioritat enre 0 i 7.

* CODE\_FILE=, CODE\_LINE=, CODE\_FUNC=
> La localització del codi que genera el missatge. Conté el nom de fitxer, el número de linia i el nom de la funció.

* ERRNO=
> El numero d'error UNIX de baix nivell.

* SYSLOG\_FACILITY=, SYSLOG\_IDENTIFIER=, SYSLOG\_PID=
> Camps compatibles amb el syslog. Contenen la facility, l'identificador i el PID.

## Camps segurs

Els camps precedits per '\_' són camps segur, són camps afegits pel journal i no poden ser modificat per un usuari.

* \_PID=, \_UID=, \_GID=
> La ID de procés, usuari, grup del procés que origina l'entrada.

* \_COMM=, \_EXE=, \_CMDLINE=
> El nom, la ruta de l'executable i la línia de comandes del procés que origina l'entrada.

* \_CAP\_EFFECTIVE=
> Les capacitats efectives del procés.

* \_AUDIT\_SESSION=, \_AUDIT\_LOGINUID=
> La sessió i el UID de login del procés.

* \_SYSTEMD\_CGROUP=, \_SYSTEMD\_SESSION=, \_SYSTEMD\_UNIT=, \_SYSTEMD\_USER\_UNIT=, \_SYSTEMD\_OWNER\_UID=, \_SYSTEMD\_SLICE=
> La ruta del grup de control, la ID de la sessió de systemd, el nom de unitat del systemd, el nom d'usuari de la sessió del systemd, 
el UID del propietari de la sessió i la part de la unitat del systemd del procés.

* \_SELINUX_CONTENT=
> El context de seguretat del SELinux.

* \_SOURCE\_REALTIME\_TIMESTAMP=
> El primer camp segur de data i hora. Esta en microsegons.

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
> El nom del sipositiu del kernel tal i com es mostra en el arbre de dispositius sota /sys.

* \_UDEV\_DEVNODE=
> La ruta al node de dispositiu del dispositiu a /dev.

* \_UDEV\_DEVLINK=
> Nom adicional d'enllaç simbòlics que apunten al node de dispositiu a /dev.

## Camps per a fer log a favor d'un altre programa

Camps utilitzats per programes per especificar que estar fent logging a favor d'un altre programa o unitat.

Camps utilitzats pel *systemd-coredump*:

* COREDUMP\_UNIT=, COREDUMP\_USER\_UNIT=
> Utilitzats per a escriure missatges que contenen coredumps del sistema i sessions d'unitats.

* OBJECT\_PID=
> PID del programa al que pertany el missatge.

* OBJECT\_UID=, OBJECT\_GID=, OBJECT\_COMM=, OBJECT\_EXE=, OBJECT\_CMDLINE=, OBJECT\_AUDIT\_SESSION=, OBJECT\_AUDIT\_LOGINUID=, 
OBJECT\_SYSTEMD\_CGROUP=, OBJECT\_SYSTEMD\_SESSION=, OBJECT\_SYSTEMD\_OWNER\_UID=, OBJECT\_SYSTEMD\_UNIT=, OBJECT\_SYSTEMD\_USER\_UNIT=
> Aquests són camps afegits automaticament per journal. El seu significat és el mateix que:
\_UID=, \_GID=, \_COMM=, \_EXE=, \_CMDLINE=, \_AUDIT\_SESSION=, \_AUDIT\_LOGINUID=, 
\_SYSTEMD\_CGROUP=, \_SYSTEMD\_SESSION=, \_SYSTEMD\_UNIT=, \_SYSTEMD\_USER\_UNIT=, and \_SYSTEMD\_OWNER\_UID=
però fan referencia al procés que especifica el PID, en comptes del procés que ha enviat l'entrada.

## Camps d'adreça

* \_\_CURSOR=
> El cursor per a la entrada. Unicament descriu la posició d'una entrada en el journal i es portable entra màquines, 
plataformes i archius de journal.

* \_\_REALTIME\_TIMESTAMP=
> El timestamp en que el journal ha rebut la entrada en microsegons.

* \_\_MONOTONIC\_TIMESTAMP=
> El timestamp monòton del moment en que el journal ha rebut l'entrada en microsegons. Per a ser útil com a adreça per a la
entrada, hauria de ser combinat amb la ID de boot ("\_BOOT\_ID=").



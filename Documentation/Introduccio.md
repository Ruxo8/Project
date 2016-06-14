# Introducció al Journal

Durant anys, el sistema de log que s'ha utilitzat ha sigut el syslog.

## Syslog

El propòsit del syslog és ser un sistema de logging (com el seu nom suggereix). 
Rep els missatges en un format relativament lliure de les aplicacions i els guarda en el disc.
Normalment, les úniques meta-dades lligades al missatge són el valor de prioritat, el timestamp (data i hora), el nom de process (tag), i el PID.
Aquestes dades es passen al client i són guardades sense cap tipus de verificació.
Molts d'aquests camps són opcionals i la sintaxis varia bastant entre les diferents implementacions del syslog, encara que es va intentar formalitzar mitjançant un RFC.

Les principals limitacions són:

1. Les dades no estan ni verificades ni autenticades.

2. Els logs tenen un format lliure que dificulta la seva interpretació, tant per identificar el tipus de missatge com per a parsejar els seus paràmetres.

3. Els timestamps (data i hora) generalment no tenen informació sobre la zona horària.

4. Syslog és només una de les moltes aplicacions per a logs, això provoca que es trobin logs en diferents sistemes.

5. Llegir els logs és ineficient, ja que la indexació, generalment, no està disponible.

6. El funcionament del syslog és simple però molt limitat, només soporta el model de *push transfer* (l'emisor és el que comença la transferència)
 i no utilitza un sistema de *store-and-forward* (les dades s'envien a un node intermedi que les guarda fins que el client les pot rebre),
 el que provoca que hi hagin problemes de pèrdua de paquets o de *Thundering Herd* (molts procesos es "desperten" a la vegada per realitzar el log,
 pero només pot un, que s'escolleix aleatòriament, cada vegada i els altres es posen a "dormir"; en quan aquest acaba, es tornen a despertar tots i així repetitivament. Per tant, és molt ineficient).
 
7. Els arxius de log són fàcilment manipulables per atacants, de manera que és fàcil amagar informació d'atacs a l'administrador.

8. El control d'accés és inexistent. A menys que es programi per l'administrador, un usuari tindrà accés total o nul.

9. La metadata enmagatzemada està limitada i falta informació clau com el nom de servei, el timestamp monòton...

10. La rotació automàtica dels fitxers de log està disponible, però en la majoria de les implementacións no és ideal.
En comptes de fixar-se en la utilització de disc de forma contínua, només ho fa en intervals de temps fixe, el que provoca una vulnerabilitat contra atacs de DDOS.

11. El *rate limiting* està disponible en algunes implementacions però, generalment, no té en compte la utilització de disc o l'assignació de serveis.

12. La compressió  de l'estructura de logs normalment està disponible però només com un efecte de la rotació i té efectes negatius en el comportament de moltes operacions amb els logs.

13. El syslog més clàssic no suporta el log dels primers moments del boot o els últims moments del shutdown, encara que les noves implementacions sí que ho fan.

14. No es pot fer log de dades en binari, que en alguns casos és esencial.

## El Journal

El Journal soluciona la majoria de limitacions del syslog.

Els principals objectius en la creació del Journal són:

1. **Simplicitat:** Poc codi

2. **Manteniment Zero**

3. **Robustesa:** Els fitxers del journal es poden copiar a diferents hosts amb eines com *scp* o *rsync*.

4. **Portable:** Els fitxers són utilitzables en tots els tipus de sistemes Linux.

5. **Rendiment:** Les operacions per afegir o buscar al journal són rapides en termes de complexitat.

6. **Integració:** Està completament integrat en la resta del sistema.

7. **Mínim rastre:** Els fitxers són petits en tamany de disc.

8. **Emmagatzematge de qualsevol esdeveniment:** És capaç d'inserir qualsevol tipus d'entrada.

9. **Unificació:** Uneix els diferents tipus de tecnologies de logs.

10. **Base per a eines d'alt nivell**

11. **Escalabilitat:** Serveix tant per màquines petites com per a superordinadors.

12. **Universalitat:** S'adapta a les necessitats de totes les aplicacions.

13. **Clusterització i xarxa:** Accepta instalacions en multi-host.

14. **Seguretat:** Els fitxers de log estan autenticats de manera que fan impossible la manipulació sense detectar.

Les aplicacions generen entrades en el Journal passant-li camps al servei. El servei augmentarà l'entrada amb meta-camps.
El valor d'aquests camps serà determinat pel servei de journal i no pot ser manipulat per part del client.
En cas de que el hardware i el kernel estiguin implicats, el servei de journal augmentarà l'entrada amb la informació disponible sobre el dispositiu.

Els camps del Journal que començen per "\_" indiquen que és un camp confiable i no és proporcionat per un client potencialment maliciós.
Les aplicacions no poden passar noms de camps que comencin amb "\_".

Així podria ser una entrada enviada per un client després del seu augment:


		_SERVICE=systemd-logind.service
		MESSAGE=User harald logged in
		MESSAGE_ID=422bc3d271414bc8bc9570f222f24a9
		_EXE=/lib/systemd/systemd-logind
		_COMM=systemd-logind
		_CMDLINE=/lib/systemd/systemd-logind
		_PID=4711
		_UD=0
		_GID=0
		_SYSTEMD_CGROUP=/system/systemd-logind.service
		_CGROUPS=cpu:/system/systemd-logind.service
		PRIORITY=6
		_BOOT_ID=422bc3d271414bc8bc95870f222f24a9
		_MACHINE_ID=c686f3b205dd48e0b43ceb6eda479721
		_HOSTNAME=waldi
		LOGIN_USER=500

Els fitxers del Journal poden ser rotats, esborrats, copiats a altres màquines, barrejats o manipulats.

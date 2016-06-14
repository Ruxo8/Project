# Ús avançat del Journalctl

## Habilitar l'emmagatzematge persistent

Per defecte, el journal emmagatzema els fitxers en memòria o en un petit buffer circular en el directori */run/log/journal*.
Això es suficient per mostrar els logs recents amb journalctl. Aquest directori és volàtil i per tant les dades no s'emmagatzemen permanentment.

Amb el emmagatzemament habilitat, els fitxers del journal s'emmagatzement a */var/log/journal* el que vol dir que perduren després del boot.

Abans hem vist com habilitar-lo, per fer memòria:

Per a habilitar-ho, podem cambiar la configuraciño en el fitxer: */etc/systemd/journald.conf*
A sota de *[ Journal ]* establir la opció *Storage=* com a "persistent":

		. . .
		[Journal]
		Storage=persistent

Habilitar l'emmagatzematge persistent té els següents advantatges:

* Dades més complertes són emmagatzemades per solucionar errors durant un període de temps més gran.

* Per solucionar problemes recents, dades més complertes són disponibles després del reboot.

Però tambñe te inconvenients:

* Encara que estigui habilitat, la quantitat d'informació emmagatzemada depèn de la memòria, i per tant no hi ha cap garantia de cubrir un període
de temps en específic.

* És necessàri més espai en disc per als logs.

## Control de l'accés

Per defecte, els usuaris del journal sense privilegis de root només poden veure les entrades generades per ells mateixos.

L'administrador del sistema por afegir usuaris al grup *adm* per tal de otorgarlis accés complet als fitxers de log:

		usermod --append --groups=adm username

El usuari *username* rebrà el mateix output del journalctl que el usuari *root*.

És important saber que el control d'accés només funciona quan el emmagatzematge persistent està activat per al journal.

## Manteniment del journal

### Veure l'espai de disc utilitzat

Per veure l'espai de disc ocupat pel journal, podem utilitzar *--disk-usage*:

		journalctl --disk-usage

### Esborrar logs anitcs

Si utilitzem la opció *--vacuum-size*, reduirem el journal indicant la mida que volem que tingui.

Aquesta opció esborrarà els logs més antics fins que el tamany que ocupi el journal en el disc sigui l'indicat.

Per exemple, si volem que el journal ens ocupi només 1GB en el disc:

		sudo journalctl --vacuum-size=1G

Una altre manera de reduir el tamany del journal és indicantli un temps amb *--vacuum-time*.

Aquesta opció esborrarà les entrades anteriors a la data seleccionada.

Si volguesim esborrar els logs que tinguesin més d'un any d'antiguitat:

		sudo journalctl --vacum-time=1years

## Limitar el tamany del journal

Podem configurar el journal per posar-li límits en l'espai que pot ocupar si editem el fitxer de configuració */etc/systemd/journald.conf*

Les següents opcions són les que es poden utilitzar per limitar el tamany del journal:

* **SystemMaxUse=**: Especifica el tamany màxim d'emmagatzematge persistent que pot ser utilitzat pel journal.

* **SystemKeepFree=**: Especifica el tamany mínim d'emmagatzemantge que el journal ha de deixar lliure quan afegeix entrades al 
emmagatzematge persistent.

* **SystemMaxFileSize=**: Controla el tamany màxim d'un fitxer en emmagatzemantge persistent abans de ser rotat.

* **RuntimeMaxUse=**: Especifica el tamany màxim de disc que pot ser utilitzat en emmagatzematge volàtil (a */run*).

* **RuntimeKeepFree=**: Especifica la quantitat mínima d'espai que el journal ha de deixar lliure quan afegeix entrades al
emmagatzematge volàtil (a */run*)

* **RuntimeMaxFileSize=**: Especifica el tamany màxim d'un fitxer en emmagatzemament volàtil (a */run*) abans de ser rotat.

## Administrar els logs desde un entorn gràfic.

Primer hem d'instalar l'aplicació:

		sudo dnf install gnome-system-log

A continuació ja la podrem executar:

		gnome-system-log

Aquesta aplicació ens permet consultar i filtrar graficament qualsevol fitxer de logs existent.

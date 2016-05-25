# Journal2mysql

Programa que exporta els logs del journalctl en format JSON per a insertar-los en una base de dades mysql.

Es pot limitar l'àmbit de búsqueda dels logs mitjançant els paràmetres del journalctl.
Per a més informació mirar 'man journalctl'

Utilització:
> journalctl --output=json | journal2mysql.py \[--user\]\[--password\]\[--database\]\[--table\]\[--new\]\[--truncate\]

## Paràmetres:

> -u *username*, --user *username*

> > Especifica el nom d'usuari amb el que es conectarà a la base de dades.

> -p *password*, --password *password*

> > Especifica el password amb el que es conectarà a la base de dades.

> -d *dbname*, --database *dbname*

> > especifica el nom de la base de dades. Per defecte és "Journalctl"

> -t *tablename*, --table *tablename*

> > especifica el nom de la taula de la base de dades. Per defecte es "Logs"

> -n, --new

> > especifica si s'ha de crear la taula. Per defecte no es crea una de nova. ATENCIÓ! 
En cas de que s'especifiqui que s'ha de crear una taula nova i ja existeixi una amb el mateix nom, 
s'eliminarà la existent i se'n crearà una de nova.

> -T, --truncate

> > especifica si s'ha de truncar (buidar) la taula abans d'inserir les dades.

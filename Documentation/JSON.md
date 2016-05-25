# Per què utilizar JSON?

JSON s'utilitza principalment com a format per a intercanviar dades.
Un altre llenguatge utilitzat per al mateix motiu és el conegut XML.

## Extensible Markup Language

XML és l'abrebiatura per a Extensible Markup Language. El XML és fàcil i extremadament flexible.
El XML utilitza tags definits per l'usuari i utilitza elements i atributs per tal de descriure les dades.
El format XML pot ser parsejat utilitzant un parsejador de XML.

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

## JavaScript Object Nation

JSON és un acrònim per a JavaScript Object Nation. L'objectiu amb el qual es va desenvolupar el JSON era que fos 
un llenguatge d'intercanvi de dades fàcil de llegir per a humans i simple d'utilitzar i parsejar per ordinadors.
JSON és auto-descriptiu i simple d'entendre.
El format JSON està basat en text i la seva sintaxis un subconjunt de la sintaxis de JavaScript.

JSON utilitza arrays i objectes. Un array conté un conjunt ordenat de valors. En JSON els arrays començen amb '\[' i
acaben amb '\]' i els valors estan separats per comes. En JSON un objecte és un conjunt desordenat de parelles de nom/valor.
Comencen per '{' i acaben per '}'. El nom i el valor estan separats per ':' i les parelles que formen l'objecte estan separades
per comes.
Els objectes i els arrays poden ser niats.

Per exemple:

	{
	“Addresses”:
		{
		“Address”:
			[
				{
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
				}
			]  
		}
	}

JSON pot utilitzar multiples arrays:

	{
	“University”:
		{
		“Student”:
			[ 
				{
				“idno”: “134”,
				“name”: “Lakshmi”,
				“dept”: “CSE”,
				“age”: “19”
				},
				{
				“idno”: “132”,
				“name”: “Karuna”,
				“dept”: “CNS”,
				“age”: “18”
				}
			], 
		“Faculty”:
			[
				{
				“idno”: “1301”,
				“name”: “Krishna Mohan”,
				“dept”: “CSE”
				}, 
				{
				“idno”: “1404”,
				“name”: “Tirupathi Rao”,
				“dept”: “CSE”
				}
			]
		}
	}

En JSON els arrays es poden separar utilitzant comes. 

En comptes d'utilitzar un pasejador, una funció standard de
JavaScript pot ser utilitzada per a parsejar dades en JSON.

## Comparació entre XML i JSON

### XML
1. Conté Tags. A vegades sufreix a cause d'utilitzarlos massa freqüentment.
2. XML és més dificil que el JSON
3. Parsejar i formatar dades en XML és poc eficient.
4. Parsejar dades en XML requereix més temps.
5. Parsejar dades en XML requereix més memòria.
6. XML no pot utilitzar arrys.
7. XML és extremadament flexible.

### JSON
1. No conté Tags.
2. JSON és més concís que el XML.
3. Comparat amb el XML, JSON es pot parsejar eficientment.
4. Parsejar dades en JSON utilitza ments temps que pasejar XML.
5. Comparat amb el XML, parsejar JSON requereix menys memòria.
6. JSON pot utilitzar arrays.
7. JSON és bastant flexibgle i molt més efectiu que el XML.

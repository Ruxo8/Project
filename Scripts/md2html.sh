#! /bin/bash
# Sergi Ruiz
# isx48031044
# Transform from markdown to html
# Script que converteix tots els fitxers en format markdown del directori a html.
# Es necessàri que acabin en .md
#---------------------------------------------------------------------------------

# For all markdown files
for M in *.md;
do
	pandoc \
	$M \
	--from markdown \
	--to html \
	--standalone \
	--template=template.txt \
	--output ${M%.md}.html
	
	# Validate
	xmllint --valid --noout ${M%.md}.html 
done

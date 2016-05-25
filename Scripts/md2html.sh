#! /bin/bash
# Sergi Ruiz
# isx48031044
# Transform from markdown to html

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

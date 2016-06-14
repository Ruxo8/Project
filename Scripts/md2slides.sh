#! /bin/bash
# Sergi Ruiz
# isx48031044
# Script que converteix una presentació en format markdown a format html
#----------------------------------------------------------

# Create Presentation from markdown
pandoc --to=dzslides --standalone presentation.md --output=presentation.html

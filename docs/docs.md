# Documentation Server

## Overview 

Documentation server is independently hosted in a seperate Docker container. MkDocs framework is used for documentation.

## Changing Theme

Edit `theme` in `mkdocs.yml`.
Possible options are : 

* `material` : Current
* `readthedocs`
* `mkdocs`

## Adding new sections

Edit `nav` section in `mkdocs.yml` to add new sections. For each new section, you need to add corresponding markdown file.



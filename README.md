# FrozenWeb

[![Python Version](https://img.shields.io/badge/Python-3-brightgreen.svg?style=flat)](http://python.org)
[![Jinja Version](https://img.shields.io/badge/Jinja-2-brightgreen.svg?style=flat)](http://jinja.pocoo.org)

Simple static web site with Jinja2 on Python 3.5

Automatically minimise html, css, js files

## Install

    python setup.py install

Dependencies: **Jinja2**, **htmlmin**, **jsmin**, **cssmin**

## Usage

help

    python -m frozenweb

build static site

    python -m frozenweb -s -c context.py

run http web server

    python -m frozenweb -b -c context.py

## Folder structure

* **templates** folder contains Base Template of Jinja2
* **site** folder contains site content
  * **.jtpl** files will be rendered via Jinja2
* **build** folder used for building static site
* **context.py** file contains dictionary for Jinja2 template.render

example: 

    |-build
    |-site
        |-js
            |-raw.js
            |-my.js.jtpl
        |-img
            |-icon.png
        |-raw.html
        |-index.html.jtpl
    |-templates
        |-base.html
    |-context.py

## License
The MIT License (MIT)

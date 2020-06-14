# FrozenWeb

[![Python Version](https://img.shields.io/badge/Python-3-brightgreen.svg?style=flat)](http://python.org)
[![Jinja Version](https://img.shields.io/badge/Jinja-2-brightgreen.svg?style=flat)](http://jinja.pocoo.org)

Simple static web site with Jinja2 on Python 3.5+

Automatically minimise html, css, js files

## Install

    python setup.py install

Dependencies: **Jinja2**, **htmlmin**, **jsmin**, **cssmin**

## Usage
* build static site
  ```
  python -m frozenweb --build --context example/context.py --templates-folder example/templates --site-folder example/site --build-folder example/build
  ```
* run http web server
  ```
  python -m frozenweb --server --context example/context.py --templates-folder example/templates --site-folder example/site
  ```

## Folder structure

* **.frozen** config file
  ```
  [extension or file name]
  minimise=true // enable minimise content for css, js or html
  jinja=true // enable jinja tempates
  ```
* **templates** folder contains Jinja2 templates
* **site** folder contains site content
* **build** output folder for building static site
* **context.py** file contains dictionary for Jinja2 template.render

example:

    |-build
    |-site
        |-.frozen
        |-js
            |-.frozen
            |-raw.js
            |-my.js
        |-img
            |-icon.png
        |-raw.html
        |-index.html
    |-templates
        |-base.html
    |-context.py

## License
The MIT License (MIT)

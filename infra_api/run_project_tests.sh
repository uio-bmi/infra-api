#!/bin/bash

cd /home/github-repos/$1
ls
source virtual_env/bin/activate
nosetests --with-html --html-file=nose_report.html tests/*

deactivate


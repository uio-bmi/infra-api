#!/bin/bash

cd /home/github-repos/$1
source virtual_env/bin/activate
nosetests --cover-html --cover-html-dir=/var/www/html/app/coverage_reports/$1 --with-coverage --cover-package=/home/github-repos/$1 --with-html --html-file=/var/www/html/app/test_reports/$1.html --quiet tests/* > /dev/null

deactivate


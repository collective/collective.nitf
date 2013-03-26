# convenience Makefile to run tests and QA tools
# options: zc.buildout options
# src: source path
# minimum_coverage: minimun test coverage allowed
# pep8_ignores: ignore listed PEP 8 errors and warnings
# max_complexity: maximum McCabe complexity allowed
# css_ignores: skip file names matching find pattern (use ! -name PATTERN)
# js_ignores: skip file names matching find pattern (use ! -name PATTERN)

SHELL = /bin/sh

options = -N -q -t 3
src = src/collective/nitf/
minimum_coverage = 84
pep8_ignores = E501
max_complexity = 12
css_ignores = ! -name jquery\*
js_ignores = ! -name jquery\*

install-qa:
	npm install csslint -g
	npm install jshint -g

qa: install-qa
# QA runs only if an environment variable named QA is present
	@echo Quality Assurance
ifneq "$(QA)" ""
	@echo Validating Python files
	bin/flake8 --ignore=$(pep8_ignores) --max-complexity=$(max_complexity) $(src)

	@echo Validating CSS files
	find $(src) -type f -name *.css $(css_ignores) | xargs csslint

	@echo Validating JavaScript files
	find $(src) -type f -name *.js $(js_ignores) -exec jshint {} ';'

	@echo Validating minimun test coverage
	bin/coverage.sh $(minimum_coverage)
else
	@echo No QA environment variable present; skipping
endif

install:
	mkdir -p buildout-cache/downloads
	python bootstrap.py -c travis-multiversion.cfg
	bin/buildout -c travis-multiversion.cfg $(options)

tests:
	bin/test

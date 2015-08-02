VERSION := $(shell grep "version =" setup.py | perl -pe 's/^.+?([0-9.]+).,$$/$$1/g')

test: pep8 pep257 pyflakes lint
	nosetests tests/*.py

clean:
	python-coverage -e
	rm -rf dist/ MANIFEST htmlcov/

coverage:
	python-coverage run /usr/bin/nosetests tests/*.py 2> /dev/null
	@python-coverage report -m | grep "^libravatar"
	@python-coverage html

dist: test
	bzr commit -m "Bump version and changelog for release"
	bzr tag pylibravatar-$(VERSION)
	python setup.py sdist

pep8:
	pep8 libravatar.py

pep257:
	pep257 libravatar.py

pyflakes:
	pyflakes libravatar.py

lint:
	pylint --reports=no --disable=I0011 libravatar.py

upload:
	python setup.py sdist upload --sign

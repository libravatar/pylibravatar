test: pep8 pyflakes lint
	nosetests tests/*.py

clean:
	python-coverage -e
	rm -rf dist/ MANIFEST htmlcov/

coverage:
	python-coverage run /usr/bin/nosetests tests/*.py 2> /dev/null
	@python-coverage report -m | grep "^libravatar"
	@python-coverage html

dist: test
	python setup.py sdist

pep8:
	pep8 libravatar.py

pyflakes:
	pyflakes libravatar.py

lint:
	pylint --reports=no --include-ids=yes --disable=I0011 libravatar.py

upload: dist
	python setup.py sdist upload --sign

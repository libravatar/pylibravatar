test: pep8 pyflakes lint
	nosetests tests/*.py

clean:
	rm -rf dist/ MANIFEST

dist: test
	python setup.py sdist

pep8:
	pep8 libravatar.py

pyflakes:
	pyflakes libravatar.py

lint:
	pylint --reports=no libravatar.py

upload: dist
	python setup.py sdist upload --sign

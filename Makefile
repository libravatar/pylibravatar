test: lint

clean:
	rm -rf dist/ MANIFEST

dist: test
	python setup.py sdist

lint:
	pylint --reports=no libravatar.py

upload: dist
	python setup.py sdist upload --sign

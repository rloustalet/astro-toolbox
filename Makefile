install:
	pip install .

uninstall:
	pip uninstall astro_toolbox

doc:
	cd docs && make html
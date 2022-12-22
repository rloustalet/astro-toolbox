install:
	pip install .

uninstall:
	pip uninstall astro_toolbox

documentation:
	cd doc && make html
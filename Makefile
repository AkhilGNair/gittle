fmt:
	isort .
	black .

verify:
	black --check --diff .
	flake8 .
	mypy . --exclude build
	pytest .


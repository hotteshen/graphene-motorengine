clean:
	@rm -f .coverage 2> /dev/null
	@rm -rf .eggs 2> /dev/null
	@rm -rf .cache 2> /dev/null
	@rm -rf ./graphene_motorengine/.cache 2> /dev/null
	@rm -rf build 2> /dev/null
	@rm -rf dist 2> /dev/null
	@rm -rf graphene_motorengine.egg-info 2> /dev/null
	@find . -name "*.pyc" -delete
	@find . -name "*.swp" -delete
	@find . -name "__pycache__" -delete

lint:
	@flake8 graphene_motorengine

test: clean lint
	py.test graphene_motorengine/tests --cov=graphene_motorengine --cov-report=html --cov-report=term

register-pypitest:
	python setup.py register -r pypitest

deploy-pypitest: clean
	python setup.py sdist upload -r pypitest

register:
	python setup.py register -r pypi

deploy: clean
	python setup.py sdist upload -r pypi


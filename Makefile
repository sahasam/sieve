.PHONY: clean clean-build

clean:
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -type d | xargs rm -fr
	rm -fr docs/_build/

clean-build:
	rm -fr *.egg *.egg-info/ dist/ build/




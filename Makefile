lint:
	docker run --rm --env LINT_FOLDER_PYTHON=. -v $(CURDIR):/app divio/lint /bin/lint ${ARGS}

.PHONY: lint
lint:
	@echo 'Running linters in /backend...'
	@make -C backend/ lint
	@echo ''

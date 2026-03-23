.PHONY: dev setup

dev:
	overmind start -f Procfile.dev

setup:
	cd api && $(MAKE) setup
	cd web && bun install

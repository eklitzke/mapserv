mapserv/interfaces:
	make -C mapserv/interfaces

tests:
	PYTHONPATH=$$PWD:$$PYTHONPATH make -C tests

clean:
	find . -name '*.py[co]' -delete

.PHONY: mapserv/interfaces tests

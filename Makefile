mapserv/interfaces:
	make -C mapserv/interfaces

clean:
	find . -name '*.py[co]' -delete

.PHONY: mapserv/interfaces

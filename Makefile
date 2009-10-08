all_tests = $(shell find tests/_mapserv -name '*_test.py' -print)

mapserv/interfaces:
	make -C mapserv/interfaces

$(all_tests) :
	PYTHONPATH=$$PWD:$$PYTHONPATH python $@

tests: $(all_tests)

clean:
	find . -name '*.py[co]' -delete

.PHONY: mapserv/interfaces tests $(all_tests)

targets := $(patsubst %.thrift,%,$(wildcard *.thrift))

all: $(targets)

gen-py/%: %.thrift
	-rm -rf $@
	thrift -gen py:new_style $<

$(targets): % : gen-py/%
	rm -rf $@
	mv $< $@

clean:
	rm -rf gen-py $(targets)

VENV_PATH := venv
DEV_PYVER := 3
PWD        := $(shell pwd)


.PHONY : venv
venv   :
	virtualenv -p python$(DEV_PYVER) -q $(VENV_PATH)

.PHONY : dev
dev    : venv
	$(VENV_PATH)/bin/pip install -qr requirements.txt

.PHONY : clean
clean  :
	rm -fr $(VENV_PATH)

all clean install uninstall:
	$(MAKE) -C oncilla-sim-wizard $@
	$(MAKE) -C manual $@

check:
	$(MAKE) -C oncilla-sim-wizard $@



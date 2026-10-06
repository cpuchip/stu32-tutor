# Run in the exported core (make -C build/core-PIN -f tools/keyrun.mk): the firmware's own
# Makefile gives the source lists (CORE, SCREEN, APP) and flags, as its app_test is built.
include Makefile

build/keyrun: $(CORE) $(HDRS) $(ENGINE) $(SCREEN) $(APP) $(KEYRUN_SRC) $(TRACE_O) | build
	$(CC) $(CFLAGS) -Icore -Ifirmware -o $@ $(CORE) $(SCREEN) $(APP) $(KEYRUN_SRC) $(TRACE_O) $(ENGINE) -lm $(WRAP)

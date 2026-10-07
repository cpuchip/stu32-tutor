# Run in the exported core (make -C build/core-PIN -f tools/keyrun.mk): the firmware's own
# Makefile gives the source lists (CORE, SCREEN, APP, and ARCADE_O for the apps the app layer links)
# and flags, as its app_test is built.
include Makefile

build/keyrun: $(CORE) $(HDRS) $(ENGINE) $(SCREEN) $(APP) $(ARCADE_O) $(KEYRUN_SRC) $(TRACE_O) | build
	$(CC) $(CFLAGS) -Icore -Ifirmware $(ARCADE_INC) -o $@ $(CORE) $(SCREEN) $(APP) $(ARCADE_O) $(KEYRUN_SRC) $(TRACE_O) $(ENGINE) -lm $(WRAP)

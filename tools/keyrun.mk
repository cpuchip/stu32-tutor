# Run in the exported core (make -C build/core-PIN -f tools/keyrun.mk): the firmware's own
# Makefile gives the source lists (CORE, SCREEN, APP, and GAMES_O for the games its app layer
# lists, from 7776c7c's games.list; casim in ENGINE) and flags, as its app_test is built.
include Makefile

build/keyrun: $(CORE) $(HDRS) $(ENGINE) $(SCREEN) $(APP) $(GAMES_O) build/games/games.h $(KEYRUN_SRC) $(TRACE_O) | build
	$(CC) $(CFLAGS) -Icore -Ifirmware -Ibuild/games -o $@ $(CORE) $(SCREEN) $(APP) $(GAMES_O) $(KEYRUN_SRC) $(TRACE_O) $(ENGINE) $(LIBS) $(WRAP)

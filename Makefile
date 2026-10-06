# stu32-tutor: every lesson's examples run on the STU-32's own core. `make check` runs them all.
#
# The core is the firmware at CORE_PIN, a commit pushed to cpuchip/abacus-firmware, exported with
# git archive into build/ (never built in the firmware's own checkout). Its Makefile builds the
# runners with its own recipes; we add only the trace (tools/trace.c) at link time.
# On fermion, run it in the gcc:14 container: scripts/check-docker.sh.
CORE_PIN := f839cb9
FIRMWARE ?= ../abacus-firmware
CORE_DIR := build/core-$(CORE_PIN)
PYTHON ?= python3
TRACE_O := $(abspath build/trace.o)
WRAP := -Wl,--wrap=ab_do_arg -Wl,--wrap=ab_memory_clear -Wl,--wrap=ab_eqn_add
LESSONS ?= $(wildcard lessons/*/)

.PHONY: check controls tools clean
check: tools
	$(PYTHON) tools/check.py --core $(CORE_DIR) $(LESSONS)

# Proves the checker can fail: one planted fault at a time, each must turn it red for its own reason.
controls: tools
	$(PYTHON) tools/controls.py --core $(CORE_DIR) lessons/rpn-01-the-stack

$(CORE_DIR)/.exported: scripts/export-core.sh
	scripts/export-core.sh $(FIRMWARE) $(CORE_PIN) $(CORE_DIR)

# build/vectors in the export is the firmware's runner linked with the trace; build/keyrun is ours.
tools: $(CORE_DIR)/.exported tools/trace.c tools/keyrun.c tools/keyrun.mk
	$(MAKE) -s -C $(CORE_DIR) build/fmt_vectors
	$(MAKE) -s -C $(CORE_DIR) build/abn_intel.o build/intel/libbid.a
	cc -std=c11 -O2 -Wall -Wextra -Werror -I$(CORE_DIR)/core -c tools/trace.c -o build/trace.o
	rm -f $(CORE_DIR)/build/vectors $(CORE_DIR)/build/keyrun
	$(MAKE) -s -C $(CORE_DIR) build/vectors LIBS="-lm $(TRACE_O) $(WRAP)"
	$(MAKE) -s -C $(CORE_DIR) -f $(abspath tools/keyrun.mk) build/keyrun \
		KEYRUN_SRC=$(abspath tools/keyrun.c) TRACE_O=$(TRACE_O) WRAP="$(WRAP)"

clean:
	rm -rf build

# stu32-tutor: every lesson's examples run on the STU-32's own core. `make check` runs them all.
#
# The core is the firmware at CORE_PIN, a commit pushed to cpuchip/abacus-firmware, exported with
# git archive into build/ (never built in the firmware's own checkout). Its Makefile builds the
# runners with its own recipes; we add only the trace (tools/trace.c) at link time.
# Without a native toolchain, run it in the gcc:14 container: scripts/check-docker.sh.
CORE_PIN := 1556ade
FIRMWARE ?= ../abacus-firmware
CORE_DIR := build/core-$(CORE_PIN)
PYTHON ?= python3
TRACE_O := $(abspath build/trace.o)
WRAP := -Wl,--wrap=ab_do_arg -Wl,--wrap=ab_memory_clear -Wl,--wrap=ab_eqn_add -Wl,--wrap=ab_view_key
LESSONS ?= $(wildcard lessons/*/)
PLACEMENT ?= $(wildcard placement/*/)

.PHONY: check controls tools clean
check: tools
	$(PYTHON) tools/graph.py
	$(PYTHON) tools/check.py --core $(CORE_DIR) $(LESSONS) $(PLACEMENT)
	$(PYTHON) tools/judge_check.py --core $(CORE_DIR)

# Proves the checker can fail: one planted fault at a time, each must turn it red for its own reason.
# Every lesson and placement folder is run, so a new one cannot be skipped: controls.py fails one with none.
controls: tools
	$(PYTHON) tools/graph.py --selftest
	$(PYTHON) tools/accepted.py --selftest
	bash scripts/judge-controls.sh $(CORE_DIR)
	@set -e; for d in $(LESSONS) $(PLACEMENT); do echo "controls: $${d%/}"; \
	    $(PYTHON) tools/controls.py --core $(CORE_DIR) $${d%/}; done

$(CORE_DIR)/.exported: scripts/export-core.sh
	scripts/export-core.sh $(FIRMWARE) $(CORE_PIN) $(CORE_DIR)

# build/vectors in the export is the firmware's runner linked with the trace; build/keyrun is ours.
tools: $(CORE_DIR)/.exported tools/judge.c tools/judge.h tools/judge_test.c tools/trace.c tools/keyrun.c tools/resolve.c tools/resolve.h tools/report.c tools/report.h tools/device.c tools/device.h tools/keyrun.mk scripts/export-core.sh
	$(MAKE) -s -C $(CORE_DIR) build/fmt_vectors
	$(MAKE) -s -C $(CORE_DIR) build/abn_intel.o build/intel/libbid.a
	cc -std=c11 -O2 -Wall -Wextra -Werror -I$(CORE_DIR)/core -c tools/trace.c -o build/trace.o
	cc -std=c11 -O2 -Wall -Wextra -Werror -o build/judge_test tools/judge_test.c tools/judge.c
	rm -f $(CORE_DIR)/build/vectors $(CORE_DIR)/build/keyrun
	$(MAKE) -s -C $(CORE_DIR) build/vectors LIBS="-lm $(TRACE_O) $(WRAP)"
	$(MAKE) -s -C $(CORE_DIR) -f $(abspath tools/keyrun.mk) build/keyrun \
		KEYRUN_SRC="$(abspath tools/keyrun.c) $(abspath tools/resolve.c) $(abspath tools/report.c) $(abspath tools/device.c)" TRACE_O=$(TRACE_O) WRAP="$(WRAP)"

clean:
	rm -rf build

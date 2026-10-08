# stu32-tutor: every lesson's examples run on the STU-32's own core. `make check` runs them all.
#
# The core is the firmware at CORE_PIN, a commit pushed to cpuchip/abacus-firmware, exported with
# git archive into build/ (never built in the firmware's own checkout). Its Makefile builds the
# runners with its own recipes; we add only the trace (tools/trace.c) at link time.
# Without a native toolchain, run it in the gcc:14 container: scripts/check-docker.sh.
CORE_PIN := c7ab388
FIRMWARE ?= ../abacus-firmware
CORE_DIR := build/core-$(CORE_PIN)
PYTHON ?= python3
TRACE_O := $(abspath build/trace.o)
WRAP := -Wl,--wrap=ab_do_arg -Wl,--wrap=ab_memory_clear -Wl,--wrap=ab_eqn_add -Wl,--wrap=ab_view_key
LESSONS ?= $(wildcard lessons/*/)

.PHONY: check controls tools clean
check: tools
	$(PYTHON) tools/graph.py
	$(PYTHON) tools/check.py --core $(CORE_DIR) $(LESSONS)

# Proves the checker can fail: one planted fault at a time, each must turn it red for its own reason.
controls: tools
	$(PYTHON) tools/graph.py --selftest
	$(PYTHON) tools/controls.py --core $(CORE_DIR) lessons/rpn-01-the-stack
	$(PYTHON) tools/controls.py --core $(CORE_DIR) lessons/rpn-02-storing-numbers
	$(PYTHON) tools/controls.py --core $(CORE_DIR) lessons/rpn-03-the-display
	$(PYTHON) tools/controls.py --core $(CORE_DIR) lessons/num-01-order-of-operations
	$(PYTHON) tools/controls.py --core $(CORE_DIR) lessons/num-02-fractions
	$(PYTHON) tools/controls.py --core $(CORE_DIR) lessons/num-03-powers-and-roots
	$(PYTHON) tools/controls.py --core $(CORE_DIR) lessons/num-04-percent-and-powers-of-ten
	$(PYTHON) tools/controls.py --core $(CORE_DIR) lessons/eq-01-equations
	$(PYTHON) tools/controls.py --core $(CORE_DIR) lessons/eq-02-formulas
	$(PYTHON) tools/controls.py --core $(CORE_DIR) lessons/eq-03-two-answers-and-inequalities
	$(PYTHON) tools/controls.py --core $(CORE_DIR) lessons/fn-01-functions-as-programs
	$(PYTHON) tools/controls.py --core $(CORE_DIR) lessons/fn-02-a-table-of-values
	$(PYTHON) tools/controls.py --core $(CORE_DIR) lessons/fn-03-domain
	$(PYTHON) tools/controls.py --core $(CORE_DIR) lessons/lin-01-slope-and-intercept
	$(PYTHON) tools/controls.py --core $(CORE_DIR) lessons/lin-02-lines-through-data
	$(PYTHON) tools/controls.py --core $(CORE_DIR) lessons/lin-03-when-a-line-does-not-fit
	$(PYTHON) tools/controls.py --core $(CORE_DIR) lessons/poly-01-evaluating-a-polynomial
	$(PYTHON) tools/controls.py --core $(CORE_DIR) lessons/poly-02-roots-with-solve
	$(PYTHON) tools/controls.py --core $(CORE_DIR) lessons/poly-03-the-quadratic-formula
	$(PYTHON) tools/controls.py --core $(CORE_DIR) lessons/poly-04-complex-roots
	$(PYTHON) tools/controls.py --core $(CORE_DIR) lessons/exp-01-growth-and-decay
	$(PYTHON) tools/controls.py --core $(CORE_DIR) lessons/exp-02-the-number-e
	$(PYTHON) tools/controls.py --core $(CORE_DIR) lessons/exp-03-logarithms
	$(PYTHON) tools/controls.py --core $(CORE_DIR) lessons/exp-04-exponential-equations
	$(PYTHON) tools/controls.py --core $(CORE_DIR) lessons/trig-01-degrees-and-radians
	$(PYTHON) tools/controls.py --core $(CORE_DIR) lessons/trig-02-right-triangles
	$(PYTHON) tools/controls.py --core $(CORE_DIR) lessons/trig-03-the-unit-circle
	$(PYTHON) tools/controls.py --core $(CORE_DIR) lessons/trig-04-polar-and-rectangular
	$(PYTHON) tools/controls.py --core $(CORE_DIR) lessons/sys-01-two-equations-at-once
	$(PYTHON) tools/controls.py --core $(CORE_DIR) lessons/sys-02-the-built-in-solvers
	$(PYTHON) tools/controls.py --core $(CORE_DIR) lessons/seq-01-sequences-and-sums
	$(PYTHON) tools/controls.py --core $(CORE_DIR) lessons/cnt-01-counting
	$(PYTHON) tools/controls.py --core $(CORE_DIR) lessons/prob-01-probability
	$(PYTHON) tools/controls.py --core $(CORE_DIR) lessons/lim-01-approaching-a-limit
	$(PYTHON) tools/controls.py --core $(CORE_DIR) lessons/lim-02-rates-of-change
	$(PYTHON) tools/controls.py --core $(CORE_DIR) lessons/int-01-area-under-a-curve

$(CORE_DIR)/.exported: scripts/export-core.sh
	scripts/export-core.sh $(FIRMWARE) $(CORE_PIN) $(CORE_DIR)

# build/vectors in the export is the firmware's runner linked with the trace; build/keyrun is ours.
tools: $(CORE_DIR)/.exported tools/trace.c tools/keyrun.c tools/resolve.c tools/resolve.h tools/report.c tools/report.h tools/device.c tools/device.h tools/keyrun.mk scripts/export-core.sh
	$(MAKE) -s -C $(CORE_DIR) build/fmt_vectors
	$(MAKE) -s -C $(CORE_DIR) build/abn_intel.o build/intel/libbid.a
	cc -std=c11 -O2 -Wall -Wextra -Werror -I$(CORE_DIR)/core -c tools/trace.c -o build/trace.o
	rm -f $(CORE_DIR)/build/vectors $(CORE_DIR)/build/keyrun
	$(MAKE) -s -C $(CORE_DIR) build/vectors LIBS="-lm $(TRACE_O) $(WRAP)"
	$(MAKE) -s -C $(CORE_DIR) -f $(abspath tools/keyrun.mk) build/keyrun \
		KEYRUN_SRC="$(abspath tools/keyrun.c) $(abspath tools/resolve.c) $(abspath tools/report.c) $(abspath tools/device.c)" TRACE_O=$(TRACE_O) WRAP="$(WRAP)"

clean:
	rm -rf build

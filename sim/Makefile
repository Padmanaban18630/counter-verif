#=========================================================
# Counter Verification Makefile
# Location : sim/Makefile
#=========================================================

#---------------------------------------------------------
# Directories
#---------------------------------------------------------
RTL_DIR     = ../rtl
TB_DIR      = ../tb
LOG_DIR     = ../logs
CONFIG_DIR  = ../config

#---------------------------------------------------------
# Design
#---------------------------------------------------------
TOP      = counter_tb
OPT_TOP  = counter_tb_opt

#---------------------------------------------------------
# User Variables
#---------------------------------------------------------
TESTNAME ?= test1
SEED     ?= 1

#---------------------------------------------------------
# DEBUG Compile Option
# Usage:
# make compile DEBUG=1
#---------------------------------------------------------
ifdef DEBUG
COMPILE_DEFINES = +define+DEBUG
else
COMPILE_DEFINES =
endif

#=========================================================
# Create Work Library
#=========================================================
lib:
	vlib work

#=========================================================
# Compile RTL + Testbench
#=========================================================
compile: lib
	vlog $(COMPILE_DEFINES) \
	     $(RTL_DIR)/counter.sv \
	     $(TB_DIR)/counter_tb.sv \
	     -l $(LOG_DIR)/compile.log

#=========================================================
# Optimize Design
#=========================================================
opt:
	vopt +acc $(TOP) -o $(OPT_TOP)

#=========================================================
# Run Simulation
# Example:
# make sim TESTNAME=test1 SEED=1
#=========================================================
sim:
	vsim \
	$(OPT_TOP) \
	-do "source $(shell pwd)/run.do" \
	+TESTNAME=$(TESTNAME) \
	-sv_seed $(SEED) \
	-l $(LOG_DIR)/$(TESTNAME).log

#=========================================================
# Regression
#=========================================================
regress:
	@python3 -c "import yaml; d=yaml.safe_load(open('../config/test_config.yaml')); [print(t['name'], t['seed']) for t in d['tests']]" | \
	while read TEST SEED; do \
		echo "================================"; \
		echo "Running $$TEST  Seed=$$SEED"; \
		echo "================================"; \
		$(MAKE) sim TESTNAME=$$TEST SEED=$$SEED; \
	done
#=========================================================
# Clean
#=========================================================
clean:
	rm -rf work
	rm -f transcript
	rm -f vsim.wlf
	rm -f $(LOG_DIR)/*.log

.PHONY: lib compile opt sim regress clean

#=========================================================
# run.do - Counter Verification Waveform Script
#=========================================================

# Open Wave window
view wave

# Top-level DUT path
set TB /counter_tb
set DUT $TB/dut

#---------------------------------------------------------
# Clock & Reset
#---------------------------------------------------------
add wave -divider {CLOCK AND RESET}
add wave $TB/clk
add wave $TB/rst_n

#---------------------------------------------------------
# Testbench Signals
#---------------------------------------------------------
add wave -divider {TESTBENCH SIGNALS}
add wave $TB/en
add wave $TB/up_down
add wave $TB/exp_count
add wave $TB/error_count
add wave $TB/count

#---------------------------------------------------------
# DUT Signals
#---------------------------------------------------------
add wave -divider {DUT SIGNALS}
add wave $DUT/clk
add wave $DUT/rst_n
add wave $DUT/en
add wave $DUT/up_down
add wave $DUT/count

#---------------------------------------------------------
# Wave Configuration
#---------------------------------------------------------
configure wave -signalnamewidth 30
configure wave -valuecolwidth 12
configure wave -timelineunits ns

#---------------------------------------------------------
# Run Simulation
#---------------------------------------------------------
run -all

# Zoom Entire Waveform
wave zoom full

# Quit
quit -f

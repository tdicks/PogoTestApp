"""
X231 PCBA Automatic Test Equipment Control Software
Copyright (c) 2016 Captec Ltd

"""

# Import our modules
from ATE import gui, tests, suite, const, version, adc, digio
import sys
from threading import Thread
from getopt import getopt, GetoptError
import tkinter as tk
from time import sleep

# Create our Tk instance for the form
root = tk.Tk()
main_frm = gui.MainForm(root)

# Create our test suite instance and link to the form
test_suite = suite.TestSuite()
test_suite.form = main_frm

# Link the pass/fail/reset buttons to their actions
test_suite.form.pass_btn["command"] = test_suite.pass_test
test_suite.form.fail_btn["command"] = test_suite.fail_test
test_suite.form.reset_btn["command"] = test_suite.reset

# Define the tests we will run
test_suite.add_test(tests.Test0a_ConnectHardwareAndAwaitPowerOn())
test_suite.add_test(tests.Test1a_MeasurePowerOnDelay())
test_suite.add_test(tests.Test1b_PogoPowerInput())
test_suite.add_test(tests.Test1c_ChargeBatteryStep1())
test_suite.add_test(tests.Test1c_ChargeBatteryStep2())
test_suite.add_test(tests.Test1d_TabletCharged())
test_suite.add_test(tests.Test2a_BatteryBoardPowersTablet())
test_suite.add_test(tests.Test2b_PogoPinsIsolatedFromBatteryPower())
test_suite.add_test(tests.Test2c_LEDStatusNotInChargeState())
test_suite.add_test(tests.Test2d_BattBoardPowerInputViaPogoDisconnected())
test_suite.add_test(tests.Test3a_ActivationOfOTGPower())
test_suite.add_test(tests.Test3b_PogoPinsIsolatedFromOTGModePower())
test_suite.add_test(tests.Test3c_LEDStatusNotInChargeState())
test_suite.add_test(tests.Test3d_BattBoardPowerInputViaPogoDisconnected())
test_suite.add_test(tests.Test3e_NoExternalBattVoltageToTabletStep1())
test_suite.add_test(tests.Test3e_NoExternalBattVoltageToTabletStep2())
test_suite.add_test(tests.Test3f_USBCableContinuityTest())

# Disable input buttons to start with
main_frm.disable_test_buttons()

# Process command args.
# -f = expand GUI to full screen
#     (This is used on the Raspberry Pi)
opts, args = getopt(sys.argv, "f")

if args.count("-f") != 0:
    main_frm.fullscreen(root, True)

# Configure the Digital I/O pins as we want them.
# See ATE/const.py for pin assignments.
digio.setup()

# Update all readings (A/D and GPIO I/O each second)
def update_readings():
    readings = adc.read_all_voltages()
    readings.update(digio.read_all_inputs())
    readings.update(digio.read_all_outputs())
    main_frm.update_readings(readings)
    root.after(1000, update_readings)

# Attempt to set "OK" on each label.
def readings_display_test():
    main_frm.set_text("Initialising readings")
    readings = adc.read_all_voltages()
    readings.update(digio.read_all_inputs())
    readings.update(digio.read_all_outputs())

    for reading in readings.items():
        main_frm.set_reading_value(reading[0], "OK")
        main_frm.update()
        sleep(0.1)

# Kick off the readings display test
readings_display_test()

# Kick off the reading updates.
update_readings_thread = Thread(target = update_readings)
update_readings_thread.start()

# Set startup text on the display.
main_frm.set_text(const.INTRO_TEXT.format(hwrevision = version.HARDWARE_REVISION, swrevision = version.SOFTWARE_REVISION, swdate = version.SOFTWARE_RELEASE_DATE))

# Process GUI events.
root.mainloop()

"""
Example demonstrating how to create a test run using OpenHTF.

This script initializes a test run for a unit with the serial number "00102"
and part number "PCB01".
The test run is marked as successful (passed) with a single step.
"""

import openhtf as htf
from tofupilot.openhtf import TofuPilot


# Create a successful test step
def step_one(test):
    return htf.PhaseResult.CONTINUE


# Set up test run for unit "00102" adding a single line before test execution
def main():
    test = htf.Test(step_one, procedure_id="FVT1", part_number="PCB01")
    with TofuPilot(test):
        test.execute(lambda: "00102")


if __name__ == "__main__":
    main()

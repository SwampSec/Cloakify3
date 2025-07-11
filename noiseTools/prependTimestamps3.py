#!/usr/bin/python3
#
# Filename:  prependTimestamps.py
#
# Version: 1.0.1
#
# Original Author:  Joe Gervais (TryCatchHCF)
# Updated Author: Soapszzz (SwampSec)
#
# Summary:  Inserts datetimestamps in front of each line of a file. Used to
# add noise to a cloaked file (see cloakify.py) in order to degrade frequency
# analysis attacks against the cloaked payload.
#
# Description:
# Takes current date and randomly subtracts 1011-1104 days to generate a
# starting date. Then starts randomly incrementing the datetimestamp (between
# 0-664 seconds) for each entry in the cloaked file. If the datetimestamp
# reaches the current date, repeats the above steps to avoid generating
# timestamps into the future.
#
# Example:
#
#   $ ./prependTimestamps.py cloaked.txt > exfiltrateMe.txt
#
#   Remove timestamps before trying to decloak the file
#
#   $ cat exfiltrateMe.txt | cut -d" " -f 3- > cloaked.txt

import os, sys, datetime, random

minDaysBack = 1011
maxDaysBack = 1104

minSecondsStep = 0
maxSecondsStep = 664

# Argument validation
# If no arguments (len == 1 because sys.argv[0] is script name), generate sample.
# If one argument (len == 2), process the file.
# Otherwise, print usage.
if len(sys.argv) > 2:
    print("usage: prependTimestamps.py <cloakedFilename>")
    print("\nStrip timestamps prior to decloaking the cloaked file.\n")
    sys.exit(1) # Exit with an error code for incorrect usage

# Set the start date back around 2 years from today (give or take) for entropy range
# Randomize a little for each run to avoid a pattern in the first line of each file

today = datetime.date.today()
startDate = today - datetime.timedelta(days=random.randint(minDaysBack, maxDaysBack))
# Initialize the first time component
t = datetime.time(random.randint(0, 23), random.randint(0, 59), random.randint(0, 59))
fakeDate = datetime.datetime.combine(startDate, t)

if len(sys.argv) == 1:
    # Generate sample of noise generator output
    print("--- Sample Output of Prepend Timestamps Noise Generator ---\n")
    for i in range(20): # Using range for cleaner loop than while i<20
        print(str(fakeDate))
        step = datetime.timedelta(seconds=random.randint(minSecondsStep, maxSecondsStep))
        fakeDate += step
        # Reset date if it goes past today to keep it in a plausible historical range
        if fakeDate.date() > today:
            startDate = today - datetime.timedelta(days=random.randint(minDaysBack, maxDaysBack))
            fakeDate = datetime.datetime.combine(startDate, datetime.time(random.randint(0, 23), random.randint(0, 59), random.randint(0, 59)))
    print("\n-----------------------------------------------------------\n")

else:
    # Prepend noise generator output to file
    input_filename = sys.argv[1]

    try:
        # Read all lines from the cloaked file
        # Use 'utf-8' encoding for text files
        with open(input_filename, 'r', encoding='utf-8') as infile:
            cloakedFileLines = infile.readlines()
    except FileNotFoundError:
        print(f"\n!!! Oh noes! Input file '{input_filename}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"\n!!! Oh noes! Problem reading input file '{input_filename}'.")
        print(f"!!! Error: {e}\n")
        sys.exit(1)

    try:
        # Open the same file for writing, overwriting its contents
        # Use 'utf-8' encoding for text files
        with open(input_filename, "w", encoding='utf-8') as outfile:
            for line in cloakedFileLines:
                # 'line' already contains the newline character from readlines()
                # so we just prepend the timestamp and a space.
                outfile.write(f"{fakeDate} {line}")
                
                # Increment the timestamp for the next line
                step = datetime.timedelta(seconds=random.randint(minSecondsStep, maxSecondsStep))
                fakeDate += step
                
                # If the fake date goes into the future, reset it to a new starting point
                if fakeDate.date() > today:
                    startDate = today - datetime.timedelta(days=random.randint(minDaysBack, maxDaysBack))
                    fakeDate = datetime.datetime.combine(startDate, datetime.time(random.randint(0, 23), random.randint(0, 59), random.randint(0, 59)))
    except Exception as e:
        print(f"\n!!! Oh noes! Problem writing to file '{input_filename}'.")
        print(f"!!! Error: {e}\n")
        sys.exit(1)
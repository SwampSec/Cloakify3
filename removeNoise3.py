#!/usr/bin/python3
#
# Filename:  removeNoise3.py
#
# Version: 2.0.0
#
# Original Author:  Joe Gervais (TryCatchHCF)
# Upgrade Author: Soapszzz (SwampSec)
#
# Summary:  Removes random noise that has been prepended to a cloaked file
# (see cloakify3.py).
#
# Description:
# Read in the noise-enhanced cloaked file and reprint each line without the
# prepended noise.
#
# Example:
#
#   $ ./removeNoise3.py 2 noisyCloaked.txt cloaked.txt

import os, sys

if len(sys.argv) != 4:
    print("usage: removeNoise.py <numberOfColumnsToStrip> <noisyFilename> <outputFile>")
    print() # Print an empty line for spacing, matching original script's behavior
    sys.exit(1) # Use sys.exit(1) for a non-zero exit code indicating an error
else:
    try:
        # Convert the first argument to an integer.
        # This will raise a ValueError if the argument is not a valid integer.
        numberOfColumnsToStrip = int(sys.argv[1])
        if numberOfColumnsToStrip < 0:
            print(f"\n!!! Oh noes! <numberOfColumnsToStrip> must be a non-negative integer.")
            sys.exit(1)
    except ValueError:
        print(f"\n!!! Oh noes! Invalid value for <numberOfColumnsToStrip>: '{sys.argv[1]}'")
        print(f"!!! It must be an integer.\n")
        sys.exit(1)

    noisy_filename = sys.argv[2]
    output_filename = sys.argv[3]

    try:
        # Open the noisy input file for reading.
        # Using 'utf-8' encoding for text files is generally a good practice.
        with open(noisy_filename, 'r', encoding='utf-8') as infile:
            noisyFile = infile.readlines()
        # No need for infile.close() here; 'with' statement handles it automatically.
    except FileNotFoundError:
        print(f"\n!!! Oh noes! Noisy file '{noisy_filename}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"\n!!! Oh noes! Problem reading noisy file '{noisy_filename}'.")
        print(f"!!! Error: {e}\n")
        sys.exit(1)

    try:
        # Open the output file for writing.
        # Using 'utf-8' encoding for text files is generally a good practice.
        with open(output_filename, "w", encoding='utf-8') as outfile:
            for line in noisyFile:
                # Strip leading/trailing whitespace (including newline) from the line
                stripped_line = line.strip()
                if stripped_line: # Check if the line is not empty after stripping
                    # Split the line by spaces.
                    # If numberOfColumnsToStrip is 0, it will take all parts.
                    # If numberOfColumnsToStrip is greater than the number of parts,
                    # it will result in an empty list, which is handled correctly by join.
                    parts = stripped_line.split(' ')
                    # Join the parts from the specified column onwards with a single space.
                    # Add a newline character at the end of each written line.
                    outfile.write(' '.join(parts[numberOfColumnsToStrip:]) + '\n')
        # No need for outfile.close() here; 'with' statement handles it automatically.
    except Exception as e:
        print(f"\n!!! Oh noes! Problem writing to output file '{output_filename}'.")
        print(f"!!! Error: {e}\n")
        sys.exit(1)
#!/usr/bin/python3
#
# Filename:  prependID.py
#
# Version: 1.0.1
#
# Original Author:  Joe Gervais (TryCatchHCF)
# Updated Author: Soapszzz (SwampSec)
#
# Summary:  Inserts a randomized tag in front of each line of a file. Used to
# add noise to a cloaked file (see cloakify.py) in order to degrade frequency
# analysis attacks against the cloaked payload.
#
# Description:
# Generates a random 4-character ID and prints it in front of each line of the
# file, in the form of "Tag:WXYZ". Modify the write statement below to tailor
# to your needs.
#
# Example:
#
#   $ ./prependID.py cloaked.txt > exfiltrateMe.txt
#
#   Remove tag before trying to decloak the file
#
#   $ cat exfiltrateMe.txt | cut -d" " -f 2- > cloaked.txt

import os, sys, random # 'codecs' is not strictly necessary for this script in Python 3

arrayCode = list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")

# Argument validation logic
# If more than 2 arguments (script_name + filename), it's incorrect usage.
if len(sys.argv) > 2:
    print("usage: prependID.py <exfilFilename>") # Corrected script name in usage
    print("\nStrip tag prior to decloaking the cloaked file.\n")
    sys.exit(1) # Use sys.exit(1) for error exit codes
else:
    # If only script_name is provided (len == 1), generate sample output.
    if len(sys.argv) == 1:
        print("--- Sample Output of Prepend ID Noise Generator ---\n")
        for _ in range(20): # Use '_' for loop variable when not needed
            # Generate a 4-character random ID using f-string for clarity
            random_id = "".join(random.choice(arrayCode) for _ in range(4))
            print(f"Tag: {random_id}")
        print("\n---------------------------------------------------\n")
    # If script_name + filename is provided (len == 2), process the file.
    else:
        input_filename = sys.argv[1]
        try:
            # Open file for reading with UTF-8 encoding
            # .read().splitlines() is efficient for getting lines without trailing newlines
            with open(input_filename, 'r', encoding='utf-8') as infile:
                exfilFileLines = infile.read().splitlines()
        except FileNotFoundError:
            print(f"\n!!! Oh noes! Input file '{input_filename}' not found.")
            sys.exit(1)
        except Exception as e:
            print(f"\n!!! Oh noes! Problem reading input file '{input_filename}'.")
            print(f"!!! Error: {e}\n")
            sys.exit(1)

        try:
            # Open the same file for writing, overwriting its contents
            # Use UTF-8 encoding
            with open(input_filename, "w", encoding='utf-8') as outfile:
                for line in exfilFileLines:
                    # Original script had an 'if i != '\n':' check.
                    # .splitlines() already handles empty lines (they won't appear as '\n'),
                    # so this check is simplified to ensure 'line' is not empty.
                    if line.strip(): # Check if line is not just whitespace
                        # Generate a new random 4-character ID for each line
                        random_id = "".join(random.choice(arrayCode) for _ in range(4))
                        # Write the tag, a space, the original line, and then a newline
                        outfile.write(f"Tag: {random_id} {line}\n")
                    else:
                        # If an original line was empty, write just a newline to preserve blank lines
                        outfile.write("\n")
        except Exception as e:
            print(f"\n!!! Oh noes! Problem writing to file '{input_filename}'.")
            print(f"!!! Error: {e}\n")
            sys.exit(1)
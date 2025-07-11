#!/usr/bin/python3
#
# Filename:  prependEmoji.py
#
# Version: 1.0.0
#
# Original Author:  Joe Gervais (TryCatchHCF)
# Updated Author: Soapszzz (SwampSec)
#
# Summary: Inserts a random emoji in front of each line in a file. Used to
# add noise to a cloaked file (see cloakify.py) in order to degrade frequency
# analysis attacks against the cloaked payload. Works well with the emoji
# cipher.
#
#
# Description:
#
# Example:
#
#   $ ./prependEmoji.py exfiltrate.txt > exfiltrateNew.txt
#
#   Remove prepended emoji before trying to decloak the file

import os, sys, random

# Argument validation logic
# If more than 2 arguments (script_name + filename), it's incorrect usage.
if len(sys.argv) > 2:
    print("usage: prependEmoji.py <exfilFilename>")
    print("\nStrip leading emoji prior to decloaking the cloaked file.\n")
    sys.exit(1) # Use sys.exit(1) for error exit codes

else:
    # Load the emoji cipher.
    # The original script used a relative path "ciphers/emoji".
    # This assumes the script is run from the parent directory of 'ciphers/'.
    # Add error handling for FileNotFoundError.
    emoji_cipher_path = "ciphers/emoji"
    try:
        with open(emoji_cipher_path, 'r', encoding='utf-8') as file:
            # .strip() each line to remove trailing newlines from the cipher entries
            arrayCipher = [line.strip() for line in file.readlines()]
        if not arrayCipher:
            print(f"\n!!! Oh noes! Emoji cipher file '{emoji_cipher_path}' is empty or invalid.")
            sys.exit(1)
    except FileNotFoundError:
        print(f"\n!!! Oh noes! Emoji cipher file '{emoji_cipher_path}' not found.")
        print(f"!!! Verify the 'ciphers/' directory exists and 'emoji' file is inside it.")
        sys.exit(1)
    except Exception as e:
        print(f"\n!!! Oh noes! Problem reading emoji cipher file '{emoji_cipher_path}'.")
        print(f"!!! Error: {e}\n")
        sys.exit(1)


    if len(sys.argv) == 1:
        # Generate sample of noise generator output
        print("--- Sample Output of Prepend Emoji Noise Generator ---\n")
        for _ in range(20): # Use '_' for loop variable when not needed
            # Print a random emoji. The original had a trailing comma and "\n",
            # which in Python 2 would print with a space and then a newline.
            # In Python 3, print() adds a newline by default, so we just print the emoji.
            print(random.choice(arrayCipher))
        print("\n----------------------------------------------------\n")

    else:
        # Prepend noise generator output to file
        input_filename = sys.argv[1]
        try:
            # Read all lines from the cloaked file.
            # readlines() keeps the newline characters at the end of each line.
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
            # Open the same file for writing, overwriting its contents.
            with open(input_filename, "w", encoding='utf-8') as outfile:
                for line in cloakedFileLines:
                    # Choose a random emoji from the loaded cipher.
                    random_emoji = random.choice(arrayCipher)
                    # Write the emoji, followed by two spaces (as in original),
                    # and then the original line (which includes its newline).
                    # Using f-string for clear concatenation.
                    outfile.write(f"{random_emoji}  {line}")
        except Exception as e:
            print(f"\n!!! Oh noes! Problem writing to file '{input_filename}'.")
            print(f"!!! Error: {e}\n")
            sys.exit(1)
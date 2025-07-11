#!/usr/bin/python3
# 
# Filename:  cloakify3.py 
#
# Version: 2.0.0
#
# Original Author:  Joe Gervais (TryCatchHCF)
# Upgraded Author: Soapszzz (SwampSec)
#
# Summary:  Exfiltration toolset (see decloakify3.py) that transforms any filetype (binaries,
# archives, images, etc.) into lists of words / phrases / Unicode to ease exfiltration of 
# data across monitored networks, hiding the data in plain sight. Also facilitates social 
# engineering attacks against human analysts and their workflows. Bonus Feature: Defeats 
# signature-based malware detection tools (cloak your other tools during an engagement).
#
# Used by cloakifyFactory3.py, can be used as a standalone script as well (example below).
#
# Description:  Base64-encodes the given payload and translates the output using a list 
# of words/phrases/Unicode provided in the cipher. This is NOT a secure encryption tool, 
# the output is vulnerable to frequency analysis attacks. Use the Noise Generator scripts
# to add entropy to your cloaked file. You should encrypt the file before cloaking if
# secrecy is needed.
#
# Prepackaged ciphers include: lists of desserts in English, Arabic, Thai, Russian, 
# Hindi, Chinese, Persian, and Muppet (Swedish Chef); PokemonGo creatures; Top 100 IP 
# Addresses; Top Websites; GeoCoords of World Capitols; MD5 Password Hashes; An Emoji 
# cipher; Star Trek characters; Geocaching Locations; Amphibians (Scientific Names); 
# evadeAV cipher (simple cipher that minimizes size of the resulting obfuscated data).
#
# To create your own cipher:
#
#	- Generate a list of at least 66 unique words (Unicode-16 accepted)
#	- Remove all duplicate entries and blank lines
# 	- Randomize the list (see 'randomizeCipherExample.txt' in Cloakify directory)
#	- Provide the file as the cipher argument to the script.
#	- ProTip: Place your cipher in the "ciphers/" directory and cloakifyFactory 
#	  will pick it up automatically as a new cipher
# 
# Example:  
#
#   $ ./cloakify3.py payload.txt ciphers/desserts > exfiltrate.txt
# 

import os, sys, getopt, base64

# In Python 3, base64.encodestring is an alias for base64.encodebytes
# which returns bytes. We need to decode it to a string for array64.index.
# The original script implicitly handled this in Python 2.
# We also ensure array64 is a list of strings for consistent lookup.
array64 = list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789/+=")

def Cloakify(arg1, arg2, arg3):
    try:
        with open(arg1, 'rb') as payloadFile:
            payloadRaw = payloadFile.read()
        # base64.b64encode returns bytes, so we decode to 'ascii' to iterate over characters
        payloadB64 = base64.b64encode(payloadRaw).decode('ascii')
    except Exception as e:
        print(f"\n!!! Oh noes! Problem reading payload file '{arg1}'")
        print(f"!!! Error: {e}\n")
        sys.exit(1)

    try:
        with open(arg2, 'r', encoding='utf-8') as file:
            cipherArray = [line.strip() for line in file.readlines()]
            # Ensure the cipher has enough entries
            if len(cipherArray) < 66:
                print(f"\n!!! Oh noes! Cipher file '{arg2}' must contain at least 66 unique entries.")
                sys.exit(1)
    except Exception as e:
        print(f"\n!!! Oh noes! Problem reading cipher '{arg2}'")
        print(f"!!! Verify the location of the cipher file and its encoding.")
        print(f"!!! Error: {e}\n")
        sys.exit(1)

    if arg3 != "":
        try:
            with open(arg3, "w+", encoding='utf-8') as outFile:
                for char in payloadB64:
                    if char != '\n':  # base64 output can include newlines
                        outFile.write(cipherArray[array64.index(char)] + '\n') # Add newline for clarity in output
        except Exception as e:
            print(f"\n!!! Oh noes! Problem opening or writing to file '{arg3}'")
            print(f"!!! Error: {e}\n")
            sys.exit(1)
    else:
        for char in payloadB64:
            if char != '\n':
                # print() in Python 3 adds a newline by default, so we remove the comma
                print(cipherArray[array64.index(char)])


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage: cloakify.py <payloadFilename> <cipherFilename>")
        sys.exit(1) # Use sys.exit(1) for error exit codes

    else:
        Cloakify(sys.argv[1], sys.argv[2], "")
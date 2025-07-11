#!/usr/bin/python3
#
# Filename:  decloakify3.py
#
# Author:  Joe Gervais (TryCatchHCF)
# Upgrade Author: Soapszzz (SwampSec)
#
# Summary:  Exfiltration toolset (see cloakify3.py) that transforms data into lists
# of words / phrases / Unicode to ease exfiltration of data across monitored networks,
# essentially hiding the data in plain sight, and facilitate social engineering attacks
# against human analysts and their workflows. Bonus Feature: Defeats signature-based
# malware detection tools (cloak your other tools).
#
# Used by cloakifyFactory3.py, can be used as a standalone script as well (example below).
#
# Description:  Decodes the output of cloakify3.py into its underlying Base64 format,
# then does Base64 decoding to unpack the cloaked payload file. Requires the use of the
# same cipher that was used to cloak the file prior to exfitration, of course.
#
# Prepackaged ciphers include: lists of desserts in English, Arabic, Thai, Russian,
# Hindi, Chinese, Persian, and Muppet (Swedish Chef); Top 100 IP Addresses; GeoCoords of
# World Capitols; MD5 Password Hashes; An Emoji cipher; Star Trek characters; Geocaching
# Locations; Amphibians (Scientific Names); and evadeAV cipher, a simple cipher that
# minimizes the size of the resulting obfuscated data.
#
# Example:
#
#   $ ./decloakify3.py cloakedPayload.txt ciphers/desserts.ciph


import sys, base64

array64 = list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789/+=")

def Decloakify(arg1, arg2, arg3):
    try:
        with open(arg1, 'r', encoding='utf-8') as file:
            # .strip() removes leading/trailing whitespace, including newlines
            listExfiltrated = [line.strip() for line in file.readlines()]
    except Exception as e:
        print(f"\n!!! Oh noes! Problem reading cloaked file '{arg1}'")
        print(f"!!! Error: {e}\n")
        sys.exit(1)

    try:
        with open(arg2, 'r', encoding='utf-8') as file:
            # .strip() removes leading/trailing whitespace, including newlines
            arrayCipher = [line.strip() for line in file.readlines()]
            # Basic validation: ensure cipher is not empty and has enough entries
            if not arrayCipher or len(arrayCipher) < 66:
                print(f"\n!!! Oh noes! Cipher file '{arg2}' appears to be invalid or incomplete.")
                print(f"!!! It should contain at least 66 unique entries.")
                sys.exit(1)
    except Exception as e:
        print(f"\n!!! Oh noes! Problem reading cipher file '{arg2}'")
        print(f"!!! Verify the location of the cipher file and its encoding.")
        print(f"!!! Error: {e}\n")
        sys.exit(1)

    clear64_chars = []
    for word in listExfiltrated:
        try:
            clear64_chars.append(array64[arrayCipher.index(word)])
        except ValueError:
            print(f"\n!!! Oh noes! Word '{word}' not found in cipher. The cipher file might be incorrect or the cloaked file is corrupted.")
            sys.exit(1)

    clear64 = "".join(clear64_chars)

    # base64.b64decode expects bytes-like object
    # The output will be bytes, so we need to write in binary mode if saving to file
    # or decode to string if printing to console (if it's text data)
    try:
        decoded_payload = base64.b64decode(clear64)
    except Exception as e:
        print(f"\n!!! Oh noes! Problem Base64 decoding the data. The input might be corrupted.")
        print(f"!!! Error: {e}\n")
        sys.exit(1)

    if arg3 != "":
        try:
            # Open in binary write mode ('wb') as base64.b64decode returns bytes
            with open(arg3, "wb") as outFile:
                outFile.write(decoded_payload)
        except Exception as e:
            print(f"\n!!! Oh noes! Problem opening or writing to output file '{arg3}'")
            print(f"!!! Error: {e}\n")
            sys.exit(1)
    else:
        # If printing to stdout, attempt to decode to UTF-8 for readability if it's text
        # Otherwise, print bytes directly.
        try:
            print(decoded_payload.decode('utf-8'))
        except UnicodeDecodeError:
            print(decoded_payload) # Print raw bytes if not UTF-8 decodable


if __name__ == "__main__":
    if (len(sys.argv) != 3):
        print("usage: decloakify.py <cloakedFilename> <cipherFilename>")
        sys.exit(1) # Use sys.exit(1) for error exit codes
    else:
        Decloakify(sys.argv[1], sys.argv[2], "")
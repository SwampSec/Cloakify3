#!/usr/bin/python3
#
# Filename:  cloakifyFactory3.py
#
# Version: 2.0.0
#
# Original Author:  Joe Gervais (TryCatchHCF)
# Updated Auther: Soapszzz (SwampSec)
#
# Summary:  Cloakify Factory 3 is part of the Cloakify Exfiltration toolset that transforms
# any fileype into lists of words / phrases / Unicode to ease exfiltration of data across
# monitored networks, defeat data whitelisting restrictions, hiding the data in plain
# sight, and facilitates social engineering attacks against human analysts and their
# workflows. Bonus Feature: Defeats signature-based malware detection tools (cloak your
# other tools). Leverages other scripts of the Cloakify Exfiltration Toolset, including
# cloakify.py, decloakify.py, and the noise generator scripts.
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
#   - Generate a list of at least 66 unique words (Unicode-16 accepted)
#   - Remove all duplicate entries and blank lines
#   - Randomize the list
#   - Place in the 'ciphers/' subdirectory
#   - Relaunch cloakifyFactory and it will automatically detect the new cipher
#
# Example:
#
#   $ ./cloakifyFactory3.py
#

import os, sys, random
# cloakify and decloakify are assumed to be in the same directory or accessible via PYTHONPATH
# Ensure cloakify.py and decloakify.py are also converted to Python 3
import cloakify, decloakify 

# Load list of ciphers
# os.walk returns a tuple (dirpath, dirnames, filenames). We need the filenames.
try:
    gCipherFiles = [f for f in os.listdir("./ciphers/") if os.path.isfile(os.path.join("./ciphers/", f))]
    gCipherFiles.sort() # Sort for consistent display
except FileNotFoundError:
    print("\n!!! Error: 'ciphers/' directory not found. Please create it and place your cipher files there.\n")
    sys.exit(1)


# Load list of noise generators
gNoiseScripts = []
# Ensure noiseTools directory exists
if not os.path.isdir("./noiseTools"):
    print("\n!!! Warning: 'noiseTools/' directory not found. Noise generation features will be unavailable.\n")
else:
    for root, dirs, files in os.walk("./noiseTools"):
        for file in files:
            if file.endswith('.py'):
                # Exclude __init__.py if present and potentially other non-noise scripts
                if file not in ["__init__.py", "removeNoise.py"]: # removeNoise.py is called, not selected by user
                    gNoiseScripts.append(file)
    gNoiseScripts.sort() # Sort for consistent display

# If cloakify3.py or decloakify.py are not in the current directory or PYTHONPATH,
# you might get ModuleNotFoundError. If they are in a specific relative path,
# you might need to adjust imports or sys.path.
# For example, if they are in 'lib/' then:
# sys.path.append(os.path.join(os.path.dirname(__file__), 'lib'))
# import cloakify, decloakify

def CloakifyFile():
    print("\n==== Cloakify a File ====\n")
    sourceFile = input("Enter filename to cloak (e.g. ImADolphin.exe or /foo/bar.zip): ").strip()
    # Basic check for empty input
    if not sourceFile:
        print("\n!!! No source filename entered. Aborting Cloakify.\n")
        return

    cloakedFile = input("Save cloaked data to filename (default: 'tempList.txt'): ").strip()
    if cloakedFile == "":
        cloakedFile = "tempList.txt"

    if not gCipherFiles:
        print("\n!!! No ciphers found in the 'ciphers/' directory. Cannot cloak file.\n")
        return

    cipherNum = SelectCipher()
    if cipherNum is None: # User chose to cancel or invalid input
        return

    noiseNum = -1
    choice = input("Add noise to cloaked file? (y/n): ").strip().lower()
    if choice == "y":
        if not gNoiseScripts:
            print("\n!!! No noise generators found in the 'noiseTools/' directory. Cannot add noise.\n")
            # Continue without adding noise if no generators are found
        else:
            noiseNum = SelectNoise()
            if noiseNum is None: # User chose to cancel or invalid input
                return

    print(f"\nCreating cloaked file using cipher: {gCipherFiles[cipherNum]}")

    try:
        cloakify.Cloakify(sourceFile, os.path.join("ciphers", gCipherFiles[cipherNum]), cloakedFile)
    except Exception as e:
        print(f"\n!!! Well that didn't go well. Verify that your cipher is in the 'ciphers/' subdirectory.")
        print(f"!!! Also check if the source file '{sourceFile}' exists and is readable.")
        print(f"!!! Error: {e}\n")
        return # Return to main menu on error

    if noiseNum >= 0:
        print(f"Adding noise to cloaked file using noise generator: {gNoiseScripts[noiseNum]}")
        # Call the noise script using os.system
        # Ensure the noise script is executable (e.g., chmod +x noiseTools/*.py)
        # and has a proper shebang (#!) to be run directly by os.system
        try:
            # os.system returns the exit status of the command
            # The format string uses f-string for clarity
            command = f"noiseTools/{gNoiseScripts[noiseNum]} {cloakedFile}"
            result = os.system(command)
            if result != 0:
                print(f"\n!!! Warning: Noise generator '{gNoiseScripts[noiseNum]}' exited with code {result}.")
                print(f"!!! This might indicate an issue with the noise script or its execution.")
        except Exception as e:
            print(f"\n!!! Well that didn't go well. Verify that '{cloakedFile}'")
            print(f"!!! is in the current working directory or try again giving full filepath.")
            print(f"!!! Error: {e}\n")

    print(f"\nCloaked file saved to: {cloakedFile}\n")

    choice = input("Preview cloaked file? (y/n): ").strip().lower()
    if choice == "y":
        print()
        try:
            with open(cloakedFile, 'r', encoding='utf-8') as file:
                cloakedPreview = file.readlines()
                # Print up to 20 lines or fewer if the file is smaller
                for i in range(min(20, len(cloakedPreview))):
                    print(cloakedPreview[i].strip()) # .strip() to remove extra newlines
            print()
        except FileNotFoundError:
            print(f"!!! Error: Cloaked file '{cloakedFile}' not found for preview.\n")
        except Exception as e:
            print(f"!!! Error reading cloaked file '{cloakedFile}' for preview: {e}\n")

    input("Press return to continue... ")


def DecloakifyFile():
    decloakTempFile = "decloakTempFile.txt"

    print("\n==== Decloakify a Cloaked File ====\n")
    sourceFile = input("Enter filename to decloakify (e.g. /foo/bar/MyBoringList.txt): ").strip()
    if not sourceFile:
        print("\n!!! No source filename entered. Aborting Decloakify.\n")
        return

    decloakedFile = input("Save decloaked data to filename (default: 'decloaked.file'): ").strip()
    if decloakedFile == "":
        decloakedFile = "decloaked.file"

    choice = input("Preview cloaked file? (y/n default=n): ").strip().lower()
    if choice == "y":
        print()
        try:
            with open(sourceFile, 'r', encoding='utf-8') as file:
                cloakedPreview = file.readlines()
                for i in range(min(20, len(cloakedPreview))):
                    print(cloakedPreview[i].strip())
            print()
        except FileNotFoundError:
            print(f"\n!!! Oh noes! Cloaked file '{sourceFile}' not found for preview.")
            print("!!! Verify the filepath you gave.\n")
            return # Exit function if source file isn't found
        except Exception as e:
            print(f"\n!!! Well that didn't go well. Verify that '{sourceFile}'")
            print(f"!!! is in the current working directory or the filepath you gave.")
            print(f"!!! Error: {e}\n")
            # Continue anyway, as the user might have made a typo but wants to proceed

    # Check if noise was added and remove it first
    noiseNum = -1
    if gNoiseScripts: # Only ask if noise scripts are available
        choice = input("Was noise added to the cloaked file? (y/n default=n): ").strip().lower()
        if choice == "y":
            noiseNum = SelectNoise()
            if noiseNum is None: # User chose to cancel or invalid input
                return

            stripColumns = 2 # Assuming 'removeNoise.py' uses this for noise stripping

            if noiseNum >= 0: # If a noise generator was selected
                try:
                    # Remove Noise, save to temp file
                    print(f"Removing noise from noise generator: {gNoiseScripts[noiseNum]}")
                    command = f"./noiseTools/removeNoise.py {stripColumns} {sourceFile} {decloakTempFile}"
                    result = os.system(command)
                    if result != 0:
                        print(f"!!! Warning: removeNoise.py exited with code {result}. Decloaking might fail.")
                        # Do not return here, let decloakify attempt with the potentially problematic file
                    # Now, the 'sourceFile' for decloaking should be the temporary stripped file
                    sourceFile = decloakTempFile
                except Exception as e:
                    print(f"!!! Error while calling 'removeNoise.py'. Is it executable and in 'noiseTools/'?")
                    print(f"!!! Error: {e}\n")
                    # If removeNoise fails, it's critical. Exit or handle robustly.
                    print("!!! Aborting decloaking due to noise removal failure.\n")
                    # If removeNoise fails, we can't proceed.
                    # sys.exit(1) # Or gracefully return
                    return

    if not gCipherFiles:
        print("\n!!! No ciphers found in the 'ciphers/' directory. Cannot decloak file.\n")
        # Clean up temp file before returning
        if os.path.exists(decloakTempFile):
            try:
                os.remove(decloakTempFile)
            except OSError as e:
                print(f"!!! Warning: Could not delete temporary file '{decloakTempFile}': {e}\n")
        return

    cipherNum = SelectCipher()
    if cipherNum is None: # User chose to cancel or invalid input
        # Clean up temp file before returning
        if os.path.exists(decloakTempFile):
            try:
                os.remove(decloakTempFile)
            except OSError as e:
                print(f"!!! Warning: Could not delete temporary file '{decloakTempFile}': {e}\n")
        return

    print(f"Decloaking file using cipher: {gCipherFiles[cipherNum]}")

    # Call Decloakify()
    try:
        decloakify.Decloakify(sourceFile, os.path.join("ciphers", gCipherFiles[cipherNum]), decloakedFile)
        print(f"\nDecloaked file from '{sourceFile}', saved to '{decloakedFile}'")
    except Exception as e:
        print(f"\n!!! Oh noes! Error decloaking file.")
        print(f"!!! Did you select the same cipher it was cloaked with, and is the file not corrupted?")
        print(f"!!! Error: {e}\n")
    finally: # Ensure temp file is deleted regardless of success or failure
        try:
            if os.path.exists(decloakTempFile):
                os.remove(decloakTempFile)
        except OSError as e:
            print(f"\n!!! Oh noes! Error while deleting temporary file '{decloakTempFile}': {e}\n")

    input("Press return to continue... ")


def SelectCipher():
    print("\nCiphers:\n")
    if not gCipherFiles:
        print("No cipher files found in './ciphers/'. Please add some.")
        return None # Indicate no selection possible

    for i, cipherName in enumerate(gCipherFiles):
        print(f"{i + 1} - {cipherName}")
    print()

    selection = -1
    while True:
        try:
            cipherNum_str = input("Enter cipher #: ").strip()
            if not cipherNum_str:
                print("No input. Returning to main menu.")
                return None # Allow user to cancel by just pressing enter
            
            selection = int(cipherNum_str) - 1

            if 0 <= selection < len(gCipherFiles):
                print()
                return selection
            else:
                print("Invalid cipher number, try again...")
        except ValueError:
            print("Invalid cipher number, try again...")

def BrowseCiphers():
    print("\n======== Preview Ciphers ========\n")
    if not gCipherFiles:
        print("No cipher files found in './ciphers/'. Cannot browse.")
        input("\nPress return to continue... ")
        return

    cipherNum = SelectCipher()
    if cipherNum is None:
        return

    print(f"===== Cipher: {gCipherFiles[cipherNum]} =====")
    print()

    try:
        with open(os.path.join("ciphers", gCipherFiles[cipherNum]), 'r', encoding='utf-8') as cipherList:
            # Read and print the entire content of the cipher file
            print(cipherList.read())
    except FileNotFoundError:
        print(f"!!! Error: Cipher file '{gCipherFiles[cipherNum]}' not found.\n")
    except Exception as e:
        print(f"!!! Error opening cipher file: {e}\n")

    input("\nPress return to continue... ")


def SelectNoise():
    print("\nNoise Generators:\n")
    if not gNoiseScripts:
        print("No noise generator scripts found in './noiseTools/'. Please add some.")
        return None # Indicate no selection possible

    for i, noiseName in enumerate(gNoiseScripts):
        print(f"{i + 1} - {noiseName}")
    print()

    selection = -1
    while True:
        try:
            noiseNum_str = input("Enter noise generator #: ").strip()
            if not noiseNum_str:
                print("No input. Returning to previous menu.")
                return None # Allow user to cancel by just pressing enter

            selection = int(noiseNum_str) - 1

            if 0 <= selection < len(gNoiseScripts):
                return selection
            else:
                print("Invalid generator number, try again...")
        except ValueError:
            print("Invalid generator number, try again...")


def BrowseNoise():
    print("\n======== Preview Noise Generators ========\n")
    if not gNoiseScripts:
        print("No noise generator scripts found in './noiseTools/'. Cannot browse.")
        input("\nPress return to continue... ")
        return

    noiseNum = SelectNoise()
    if noiseNum is None:
        return

    print()
    if noiseNum >= 0:
        print(f"Sample output of prepended strings, using noise generator: {gNoiseScripts[noiseNum]}\n")
        # Execute the noise generator script directly to show its sample output
        try:
            # Ensure noise script is executable and has a proper shebang
            command = f"./noiseTools/{gNoiseScripts[noiseNum]}"
            result = os.system(command)
            if result != 0:
                print(f"\n!!! Warning: Noise generator '{gNoiseScripts[noiseNum]}' exited with code {result}.")
                print(f"!!! It might not be executable or there's an issue with its output generation.")
        except Exception as e:
            print(f"\n!!! Error while generating noise preview: {e}\n")

    input("\nPress return to continue... ")


def Help():
    print("\n===================== Using Cloakify Factory =====================\n")
    print("For background and full tutorial, see the presentation slides at")
    print("https://github.com/TryCatchHCF/Cloakify")
    print("\nWHAT IT DOES:\n")
    print("Cloakify Factory transforms any filetype (e.g. .zip, .exe, .xls, etc.) into")
    print("a list of harmless-looking strings. This lets you hide the file in plain sight,")
    print("and transfer the file without triggering alerts. The fancy term for this is")
    print("'text-based steganography', hiding data by making it look like other data.")
    print("\nFor example, you can transform a .zip file into a list made of Pokemon creatures")
    print("or Top 100 Websites. You then transfer the cloaked file however you choose,")
    print("and then decloak the exfiltrated file back into its original form. The ciphers")
    print("are designed to appear like harmless / ignorable lists, though some (like MD5")
    print("password hashes) are specifically meant as distracting bait.")
    print("\nBASIC USE:\n")
    print("Cloakify Factory will guide you through each step. Follow the prompts and")
    print("it will show you the way.")
    print("\nCloakify a Payload:")
    print("- Select 'Cloakify a File' (any filetype will work - zip, binaries, etc.)")
    print("- Enter filename that you want to Cloakify (can be filename or filepath)")
    print("- Enter filename that you want to save the cloaked file as")
    print("- Select the cipher you want to use")
    print("- Select a Noise Generator if desired")
    print("- Preview cloaked file if you want to check the results")
    print("- Transfer cloaked file via whatever method you prefer")
    print("\nDecloakify a Payload:")
    print("- Receive cloaked file via whatever method you prefer")
    print("- Select 'Decloakify a File'")
    print("- Enter filename of cloaked file (can be filename or filepath)")
    print("- Enter filename to save decloaked file to")
    print("- Preview cloaked file to review which Noise Generator and Cipher you used")
    print("- If Noise Generator was used, select matching Generator to remove noise")
    print("- Select the cipher used to cloak the file")
    print("- Your decloaked file is ready to go!")
    print("\nYou can browse the ciphers and outputs of the Noise Generators to get")
    print("an idea of how to cloak files for your own needs.")
    print("\nAnyone using the same cipher can decloak your cloaked file, but you can")
    print("randomize (scramble) the preinstalled ciphers. See 'randomizeCipherExample.txt'")
    print("in the Cloakify directory for an example.")
    print("\nNOTE: Cloakify is not a secure encryption scheme. It's vulnerable to")
    print("frequency analysis attacks. Use the 'Add Noise' option to add entropy when")
    print("cloaking a payload to help degrade frequency analysis attacks. Be sure to")
    print("encrypt the file prior to cloaking if secrecy is needed.\n")

def About():
    print("\n===================== About Cloakify Factory =====================\n")
    print("             \"Hide & Exfiltrate Any Filetype in Plain Sight\"")
    print("\n                         Written by TryCatchHCF")
    print("                       https://github.com/TryCatchHCF")
    print("\nData Exfiltration In Plain Sight; Evade DLP/MLS Devices; Social Engineering")
    print("of Analysts; Defeat Data Whitelisting Controls; Evade AV Detection. Text-based")
    print("steganography usings lists. Convert any file type (e.g. executables, Office,")
    print("Zip, images) into a list of everyday strings. Very simple tools, powerful")
    print("concept, limited only by your imagination.")
    print("\nCloakify Factory uses Python scripts to cloak / uncloak any file type using")
    print("list-based ciphers (text-based steganography). Allows you to transfer data")
    print("across a secure network's perimeter without triggering alerts, defeating data")
    print("whitelisting controls, and derailing analyst's review via social engineering")
    print("attacks against their workflows. As a bonus, cloaked files defeat signature-")
    print("based malware detection tools.")
    print("\nNOTE: Cloakify is not a secure encryption scheme. It's vulnerable to")
    print("frequency analysis attacks. Use the 'Add Noise' option to add entropy when")
    print("cloaking a payload to help degrade frequency analysis attacks. Be sure to")
    print("encrypt the file prior to cloaking if secrecy is needed.")
    print("\nDETAILS:\n")
    print("Cloakify first Base64-encodes the payload, then applies a cipher to generate")
    print("a list of strings that encodes the Base64 payload. Once exfiltrated, use")
    print("Decloakify with the same cipher to decode the payload. The ciphers are")
    print("designed to appear like harmless / ingorable lists, though some (like MD5")
    print("password hashes) are specifically meant as distracting bait.")
    print("\nPrepackaged ciphers include lists of:\n")
    print("- Amphibians (scientific names)")
    print("- Belgian Beers")
    print("- Desserts in English, Arabic, Thai, Russian, Hindi, Chinese, Persian, and")
    print("  Muppet (Swedish Chef)")
    print("- Emoji")
    print("- evadeAV (smallest cipher space, x3 payload size)")
    print("- GeoCoords World Capitals (Lat/Lon)")
    print("- GeoCaching Coordinates (w/ Site Names)")
    print("- IPv4 Addresses of Popular Websites")
    print("- MD5 Password Hashes")
    print("- PokemonGo Monsters")
    print("- Top 100 Websites")
    print("- Ski Resorts")
    print("- Status Codes (generic)")
    print("- Star Trek characters")
    print("- World Beaches")
    print("- World Cup Teams")
    print("\nPrepackaged scripts for adding noise / entropy to your cloaked payloads:\n")
    print("- prependEmoji.py: Adds a randomized emoji to each line")
    print("- prependID.py: Adds a randomized ID tag to each line")
    print("- prependLatLonCoords.py: Adds random LatLong coordinates to each line")
    print("- prependTimestamps.py: Adds timestamps (log file style) to each line")
    print("\nCREATE YOUR OWN CIPHERS:\n")
    print("Cloakify Factory is at its best when you're using your own customized")
    print("ciphers. The default ciphers may work for most needs, but in a unique")
    print("exfiltration scenario you may need to build your own.")
    print("\nCreating a Cipher:\n")
    print("- Create a list of at least 66 unique words/phrases/symbols (Unicode accepted)")
    print("- Randomize the list order")
    print("- Remove all duplicate entries and all blank lines")
    print("- Place cipher file in the 'ciphers/' subdirectory")
    print("- Re-run Cloakify Factory to automatically load the new cipher")
    print("- Test cloaking / decloaking with new cipher before using operationally\n")


def MainMenu():

    print("  ____ _         _   _  __        ______          _               ")
    print(" / __ \ |         | | |_|/ _|        | ___|          | |             ")
    print("| /  \/ | ___  __ _| | ___| |_ _   _ | |_ __ _  ___| |_ ___  _ __ _   _ ")
    print("| |   | |/ _ \ / ` | |/ / |  _| | | ||  _/ _` |/ __| __/ _ \| '__| | | |")
    print("| \__/\ | |_| | |_| |  <| | | | |_| || || |_| | |__| || |_| | |  | |_| |")
    print(" \____/_|\___/ \__,_|_|\_\_|_|  \__, | \_| \__,_|\___|\__\___/|_|   \__, |")
    print("                                __/ |                                 __/ |")
    print("                               |___/                                 |___/ ")
    print("\n             \"Hide & Exfiltrate Any Filetype in Plain Sight\"")
    print("\n                     Original Written by TryCatchHCF")
    print("                       https://github.com/TryCatchHCF")
    print("\n                     Updated Written by SwampSec")
    print("                       https://github.com/SwampSec")
    print("  (\~---.")
    print("  /   (\-`-/)")
    print(" (     ' '  )       data.xls image.jpg   \\     List of emoji, IP addresses,")
    print("  \ (  \_Y_/\\   ImADolphin.exe backup.zip   -->  sports teams, desserts,")
    print("   \"\"\ \___//      LoadMe.war file.doc   /    beers, anything you imagine")
    print("     `w  \"")

    selectionErrorMsg = "1-7 are your options. Try again."
    notDone = True

    while notDone:
        print("\n==== Cloakify Factory Main Menu ====\n")
        print("1) Cloakify a File")
        print("2) Decloakify a File")
        print("3) Browse Ciphers")
        print("4) Browse Noise Generators")
        print("5) Help / Basic Usage")
        print("6) About Cloakify Factory")
        print("7) Exit")
        print()

        invalidSelection = True

        while invalidSelection:
            try:
                # raw_input is replaced by input in Python 3
                choice = int(input("Selection: "))

                if 0 < choice < 8:
                    invalidSelection = False
                else:
                    print(selectionErrorMsg)
            except ValueError:
                print(selectionErrorMsg)

        if choice == 1:
            CloakifyFile()
        elif choice == 2:
            DecloakifyFile()
        elif choice == 3:
            BrowseCiphers()
        elif choice == 4:
            BrowseNoise()
        elif choice == 5:
            Help()
        elif choice == 6:
            About()
        elif choice == 7:
            notDone = False
        # else: This 'else' clause is technically unreachable due to the inner loop validation.
        #     print(selectionErrorMsg)

    byeArray = ("Bye!", "Ciao!", "Adios!", "Aloha!", "Hei hei!", "Bless bless!", "Hej da!", "Tschuss!", "Adieu!", "Cheers!")

    print(f"\n{random.choice(byeArray)}\n")

# ============================== Main Loop ================================
if __name__ == "__main__":
    MainMenu()
#!/usr/bin/python3
#
# Filename:  prependLatLonCoords.py
#
# Version: 1.0.1
#
# Original Author:  Joe Gervais (TryCatchHCF)
# Updated Author: Soapszzz (SwampSec)
#
# Summary:  Inserts random Lat/Lon coordinates in front of each line of a file.
# Used to add noise to a cloaked file (see cloakify.py) in order to degrade
# frequency analysis attacks against the cloaked payload.
#
# Description:
# Uses a bounding rectangle to generate random lat/lon coordinate pairs and
# insert them in the front of each line in a file. Defaults to Denver, with a
# bounding rectangle roughly 10 miles / 16km per side (varies with latitude,
# because sphere.
#
# Example:
#
#   $ ./prependLatLonCoords.py cloaked.txt > exfiltrateMe.txt
#
#   Remove coordinate pairs before trying to decloak the file
#
#   $ cat exfiltrateMe.txt | cut -d" " -f 3- > cloaked.txt


import os, sys, random

# Argument validation
# If no arguments (len == 1 because sys.argv[0] is script name), generate sample.
# If one argument (len == 2), process the file.
# Otherwise, print usage.
if len(sys.argv) > 2:
    print("usage: prependLatLonCoords.py <cloakedFilename>")
    print("\nStrip the coordinates prior to decloaking the cloaked file.\n")
    sys.exit(1) # Exit with an error code for incorrect usage

else:
    # Geocoords for Denver, USA. Replace with whatever is best for your needs
    baseLat = 39.739236
    baseLon = -104.990251

    # AT LATITUDE 40 DEGREES (NORTH OR SOUTH)
    # One minute of latitude =    1.85 km or 1.15 mi
    # One minute of longitude =   1.42 km or 0.88 mi

    # These values define the "spread" of the random coordinates.
    # A value of 0.0002 * 2000 = 0.4 degrees.
    # At 40 degrees latitude, 1 degree of latitude is about 111 km.
    # 0.4 degrees latitude is about 44.4 km (approx 27.6 miles).
    # 1 degree of longitude at 40 degrees latitude is about 85 km.
    # 0.4 degrees longitude is about 34 km (approx 21.1 miles).
    # So the bounding box is roughly 27.6 x 21.1 miles, centered around baseLat/Lon.
    sizeLat = 0.0002
    sizeLon = 0.0002

    if len(sys.argv) == 1:
        # Generate sample of noise generator output
        print("--- Sample Output of Prepend Latitude/Longitude Coords Noise Generator ---\n")
        for i in range(20): # Using range for cleaner loop than while i<20
            # Generate random offsets within the defined range
            # random.uniform(a, b) returns a random floating point number N such that a <= N <= b
            # This provides more granular control than integer multiplication for floats
            lat_offset = random.uniform(0, 2000 * sizeLat)
            lon_offset = random.uniform(0, 2000 * sizeLon)

            lat = baseLat + lat_offset
            lon = baseLon + lon_offset

            # Format to a reasonable number of decimal places for coordinates
            # Using f-string for cleaner output formatting
            print(f"{lat:.6f} {lon:.6f}") # .6f for 6 decimal places, common for GPS
        print("\n------------------------------------------------------------------------\n")

    else:
        input_filename = sys.argv[1]

        try:
            # Read all lines from the cloaked file
            # Use 'utf-8' encoding for text files for broader compatibility
            with open(input_filename, "r", encoding='utf-8') as infile:
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
                    # Generate random offsets for each line
                    lat_offset = random.uniform(0, 2000 * sizeLat)
                    lon_offset = random.uniform(0, 2000 * sizeLon)

                    lat = baseLat + lat_offset
                    lon = baseLon + lon_offset

                    # 'line' already contains the newline character from readlines()
                    # so we just prepend the coordinates and a space.
                    # Format to 6 decimal places for consistency
                    outfile.write(f"{lat:.6f} {lon:.6f} {line}")
        except Exception as e:
            print(f"\n!!! Oh noes! Problem writing to file '{input_filename}'.")
            print(f"!!! Error: {e}\n")
            sys.exit(1)
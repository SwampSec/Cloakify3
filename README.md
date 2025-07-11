# CloakifyFactory3
CloakifyFactory3 & the Cloakify3 Toolset - Data Exfiltration & Infiltration In Plain Sight; Evade DLP/MLS Devices; Social Engineering of Analysts; Defeat Data Whitelisting Controls; Evade AV Detection. Text-based steganography using lists. Convert any file type (e.g. executables, Office, Zip, images) into a list of everyday strings. Very simple tools, powerful concept, limited only by your imagination.

# Updated Author
Soapszzz (SwampSec)

# Original Author
Joe Gervais (TryCatchHCF)

# Why
DLP systems, MLS devices, and SecOps analysts know what data to look for: 
<img src=https://github.com/SwampSec/Cloakify3/blob/master/screenshots/payloadAcctSpreadsheet.png></img>

So transform that data into something they're <b>not</b> looking for: 
<img src=https://github.com/SwampSec/Cloakify3/blob/master/screenshots/CloakifyFactoryWorkflow.png></img>

# Tutorial
See my DEFCON24 slides (included in project) from Crypto & Privacy Village workshop and Demo Labs session. Complete tutorial on what the Cloakify3 Toolset can do, specific use cases, and more. (The examples in the presentation use the standalone scripts, I recommend using the new CloakifyFactory3 to streamline your efforts.)

For a quick start on CloakifyFactory3, see the cleverly titled file "README_GETTING_STARTED.txt" in the project for a walkthrough.

# Overview
CloakifyFactory3 transforms any filetype (e.g. .zip, .exe, .xls, etc.) into a list of harmless-looking strings. This lets you hide the file in plain sight, and transfer the file without triggering alerts. The fancy term for this is "text-based steganography", hiding data by making it look like other data. For example, you can transform a .zip file into a list of Pokémon creatures or Top 100 Websites. You then transfer the cloaked file however you choose, and then decloak the exfiltrated file back into its original form. 

With your payload cloaked, you can transfer data across a secure network’s perimeter without triggering alerts. You can also defeat data whitelisting controls - is there a security device that only allows IP addresses to leave or enter a network? Turn your payload into IP addresses, problem solved. Additionally, you can derail the security analyst’s review via social engineering attacks against their workflows. And as a final bonus, cloaked files defeat signature-based malware detection tools.

The pre-packaged ciphers are designed to appear like harmless / ignorable lists, though some (like MD5 password hashes) are specifically meant as distracting bait.

CloakifyFactory3 is also a great way to introduce people to crypto and steganography concepts. It's simple to use, guides the user through the process, and according to our kids is also fun!

# Requires
Python 3.9.x

# Run Cloakify Factory 3
$ python cloakifyFactory3.py

# Description
CloakifyFactory3 is a menu-driven tool that leverages Cloakify3 Toolset scripts. When you choose to Cloakify3 a file, the scripts  first Base64-encode the payload, then apply a cipher to generate a list of strings that encodes the Base64 payload. You then transfer the file however you wish to its desired destination. Once exfiltrated, choose Decloakify3 with the same cipher to decode the payload.

NOTE: Cloakify3 is not a secure encryption scheme. It's vulnerable to frequency analysis attacks. Use the 'Add Noise' option to add entropy when cloaking a payload to help degrade frequency analysis attacks. Be sure to encrypt the file prior to cloaking if secrecy is needed.

The supporting scripts (cloakify3.py and decloakify3.py) can be used as standalone scripts. Very small, simple, clean, portable. For scenarios where infiltrating the full toolset is impractical, you can quickly type the standalone script into a target’s local shell, generate a cipher in place, and cloakify -> exfiltrate.

Prepackaged ciphers include lists of:
- Amphibians (scientific names)
- Belgian Beers
- Desserts in English, Arabic, Thai, Russian, Hindi, Chinese, Persian, and Muppet (Swedish Chef)
- Emoji
- evadeAV (smallest cipher space, x3 payload size)
- GeoCoords World Capitals (Lat/Lon)
- GeoCaching Coordinates (w/ Site Names)
- IPv4 Addresses of Popular Websites
- MD5 Password Hashes
- PokemonGo Monsters
- Shortened URLs pointing to different Youtube videos of Rick Astley's "Never Gonna Give You Up"
- Ski Resorts
- Status Codes (generic)
- Star Trek characters
- Top 100 Websites
- World Beaches
- World Cup Teams

Prepackaged scripts for adding noise / entropy to your cloaked payloads:
- prependEmoji3.py: Adds a randomize emoji to each line
- prependID3.py: Adds a randomized ID tag to each line 
- prependLatLonCoords3.py: Adds randomized LatLong coordinates to each line
- prependTimestamps3.py: Adds timestamps (log file style) to each line

See comments in each script for details on how to tailor the Noise Generators for your own needs

# Create Your Own Ciphers

Cloakify Factory 3 is at its best when you're using your own customized ciphers. The default ciphers may work for most needs, but in a unique exfiltration scenario you may need to build your own. At the very least, you can copy a prepackaged cipher and randomize the order.

Creating a Cipher:
- Generate a list of at least 66 unique words / phrases / symbols (Unicode allowed)
- Remove all duplicate entries and all blank lines
- Randomize the list order
- Place in the "ciphers/" subdirectory
- Re-run CloakifyFactory3 and it will automatically load your new cipher as an option
- Test cloaking / decloaking with new cipher before using operationally

# Sample Cipher Gallery

<img src=https://github.com/SwampSec/Cloakify3/blob/master/screenshots/CipherGallery1.png></img>
<img src=https://github.com/SwampSec/Cloakify3/blob/master/screenshots/CipherGallery2.png></img>

# Standalone Scripts
Some of you may prefer to use the Cloakify3 Toolset scripts in standalone mode. The toolset is designed to support that.

# cloakify3.py Example
<img src=https://github.com/SwampSec/Cloakify3/blob/master/screenshots/cloak.png></img>

# decloakify3.py Example
<img src=https://github.com/SwampSec/Cloakify3/blob/master/screenshots/decloak.png></img>

# Adding Entropy via Standalone Scripts
Add noise to degrade frequency analysis attacks against your cloaked payloads. Here we use the 'PokémonGo' cipher, then use the 'prependLatLonCoords3.py' script to generate random geo-coordinates in a 10x10 mile grid. Strip noise from the file before decloaking, using the 'removeNoise3.py' script. 

Or of course: $ cat cloakedAndNoisy.txt | cut -d" " -f3- > cloakedNoiseStripped.txt
<img src=https://github.com/TryCatchHCF/Cloakify/blob/master/screenshots/pokemonGoExample.png></img>



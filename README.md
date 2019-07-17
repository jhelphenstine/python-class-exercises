# python-class-exercises
Exercises from a Python class I took

## packet-analysis-exercises.py
Probably the most involved of the exercises I worked through in this class, and it's far from polished. But, I enjoyed tackling the question of determining the default gateway in a packet capture of uncertain origin. I chose to focus on MAC addresses fronting multiple IPs as the most likely candidate for a default gateway, though talking about it later, I think there are additional tests, such as parsing DHCPOFFER packets, that might also have that data. This script gave me practice with closures and sets as well; the set allowed me to clean up my logic and avoid testing for ```if not in```; I just trust the set logic to ensure uniqueness.

## client.py && server.py
These are oddly named, as I wanted the server to simulate a beaconing agent -- so it actually initiates the connection to the "client"...in this sense, it's a "client for the user" rather than in the strict "client/server" model. This was a fun thing to work on, though I did get hung up using a 'with socket' for most of the day...turns out the with was closing my socket after one pass, resulting in code that worked once but then errored out. It's since been refactored and now functions as designed, though obv. more remains to be done re: parsing returns. I begin to see why frameworks don't brook any truck with raw command-line stuff, instead preferring plugins or other safe, wrapped cmdlets, lowering the formatting burden.

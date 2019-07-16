# python-class-exercises
Exercises from a Python class I took

## packet-analysis-exercises.py
Probably the most involved of the exercises I worked through in this class, and it's far from polished. But, I enjoyed tackling the question of determining the default gateway in a packet capture of uncertain origin. I chose to focus on MAC addresses fronting multiple IPs as the most likely candidate for a default gateway, though talking about it later, I think there are additional tests, such as parsing DHCPOFFER packets, that might also have that data. This script gave me practice with closures and sets as well; the set allowed me to clean up my logic and avoid testing for ```if not in```; I just trust the set logic to ensure uniqueness.

import sys
print (sys.version)
import requests

if len(sys.argv) < 2:
    print("Hello")
else:
    print(sys.argv[1])

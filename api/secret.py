import os
dir = os.path.dirname(__file__)
filename = os.path.join(dir, '../secret.txt')

with open(filename) as f:
    API_KEY = f.readline().strip()
    API_SECRET = f.readline().strip()
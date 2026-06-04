import math
import json

with open("temp.txt", "r") as f:
    lines = f.read().strip().splitlines()
    final = {}
    for index, line in enumerate(lines, 1):
        temp = eval(line)
        final[index] = temp

with open("temp.json", "w") as f:
    json.dump(final, f)
    
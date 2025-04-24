from core.io import parse_input_frame
import json

# Load the YAML file
with open("load.json", "r") as file:
    data = json.load(file)

frame = parse_input_frame(data)
output = frame.save_solution("load.txt")
print(output)

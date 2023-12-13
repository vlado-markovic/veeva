import json
import pandas as pd

# Load JSON data from file
with open('responseD.json', 'r') as f:
    json_data = json.load(f)

# Convert JSON to DataFrame
df = pd.DataFrame(json_data)

# Convert DataFrame to CSV
df.to_csv('output.csv', index=False)
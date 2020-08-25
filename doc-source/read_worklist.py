# 3rd party
from pandas import DataFrame

# this package
from mh_utils.worklist_parser import Worklist, read_worklist

# Replace 'worklist.wkl' with the filename of your worklist.
wkl: Worklist = read_worklist("worklist.wkl")

df: DataFrame = wkl.as_dataframe()

# Filter columns
df = df[["Sample Name", "Method", "Data File", "Drying Gas", "Gas Temp", "Nebulizer"]]

# Get just the filename from 'Method' and 'Data File'
df["Method"] = [x.name for x in df["Method"]]
df["Data File"] = [x.name for x in df["Data File"]]

# Show the DataFrame
print(df.to_string())

# save as CSV
df.to_csv("worklist.csv")

# save as JSON
df.to_json("worklist.json", indent=2)

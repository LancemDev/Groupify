import pandas as pd

# Read in the data from a CSV file
df = pd.read_csv("icsd _comm_skills.csv")

# Shuffle the rows randomly
df = df.sample(frac=1).reset_index(drop=True)

# Divide the data into 8 equally-sized groups
group_size = len(df) // 13
groups = [df[i:i+group_size] for i in range(0, len(df), group_size)]

# Make sure that the last group has the remaining rows if the number of rows is not evenly divisible by 8
groups[-1] = groups[-1].append(df[len(df)-len(groups[-1]):])

# Iterate through the groups and assign a group number to each row
for i, group in enumerate(groups):
    group["group"] = i+1

# Concatenate the groups back into a single DataFrame and save the result to a CSV file
result = pd.concat(groups)
result.to_csv("new2.csv", index=False)
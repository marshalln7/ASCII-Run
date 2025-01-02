

import pandas as pd

insights = {}

df = pd.read_csv("tic tac toe experience.csv")

data_dictionary = df.to_dict(orient="split")
data = data_dictionary["data"] #ends up with a list of lists of the actual data

for instance in data:
    key = str(instance[0:10])
    won = "won" in instance #becomes true if it was a "won" entry
    if key in insights:
        previous_entry = insights[key]
        new_number_of_instances = previous_entry[0] + 1
        new_percent_victory = (((previous_entry[1] * previous_entry[0]) + (1 if won else 0)) / new_number_of_instances)
        insights[key] = [new_number_of_instances, new_percent_victory]
    else:
        new_entry = [1, 1 if won else 0]
        insights[key] = new_entry

print(insights)
insights_dataframe = pd.DataFrame(data=insights).T
insights_dataframe.to_csv("tic tac toe insights.csv")

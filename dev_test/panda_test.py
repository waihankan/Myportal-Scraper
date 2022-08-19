import pandas as pd

df = pd.read_html("./dev_test/response.html") 

N = 17
first_n_column  = df[5].iloc[: , :N]
print(first_n_column)

first_n_column.to_csv("./dev_test/response.csv", index=True)
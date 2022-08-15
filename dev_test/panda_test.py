import pandas as pd

df = pd.read_html("../summer_CIS22C.html") 
N = 17
first_n_column  = df[5].iloc[: , :N]
print(first_n_column)
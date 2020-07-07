import pandas as pd

df=pd.read_csv(r'../DataGet/LaGou_全国.csv')
info=pd.DataFrame(df[['positionName','companyFullName','city','salary','education','companySize','industryField','positionLables']])
print(info.info())
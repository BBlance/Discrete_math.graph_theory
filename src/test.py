import pandas as pd

df1 = pd.DataFrame({'a': [3, 1], 'b': [4, 3]})  # 随机生成一个DataFrame 数据
df2 = df1.copy()
with pd.ExcelWriter('output.xlsx') as writer:
    for i in range(1, 4):
        name = 'Sheet_name_' + str(i)
        df1.to_excel(writer, sheet_name=name)
#       df2.to_excel(writer, sheet_name='Sheet_name_2')
writer.save()
writer.close()

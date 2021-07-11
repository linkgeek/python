import pandas as pd
import numpy as np
from pandas import DataFrame

df = pd.DataFrame(np.random.randn(10, 4), columns=list('abcd'))
df.style.format("{:.2f}")


# 正负
def color_neg_red(val):
    color = 'red' if val > 0 else 'green'
    return 'color:%s' % color


df.style.applymap(color_neg_red)

# 列名前缀
df.add_prefix('row_')
# df.style.applymap(color_col, subset=pd.IndexSlice[2, 3])
df.style.applymap(color_neg_red, subset=['row_2', 'row_3'])


# 某列最大值
def color_col_max(col):
    c = col == col.max()
    return ['background-color: yellow' if v else '' for v in c]


# 某列前2大值
def color_col_max2(col):
    s = np.sign(col) == np.sign(col.max())
    return ['background-color: red' if v else 'background-color: yellow' for v in s]


# 内置方法
df.style.highlight_max(axis=1)
df.style.highlight_min(axis=1)

# df.iat[0, 0] = np.nan
df.style.highlight_null(null_color='blue')

# 带样式写入xlsx
# df.style.applymap(color_neg_red).apply(color_col_max).highlight_null(null_color='blue').to_excel('data1.xlsx')
df.style.applymap(color_neg_red).apply(color_col_max2).to_excel('data1.xlsx')

# print(df)





























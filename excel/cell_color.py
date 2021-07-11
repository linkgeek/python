import pandas as pd
import numpy as np

columns = [['A', 'A', 'B', 'B', 'C'], ['a', 'b', 'c', 'd', 'e']]
# 创建形状为（10，5） 的DataFrame 并设置二级标题
demo_df = pd.DataFrame(np.arange(50).reshape(10, 5), columns=columns)
print(demo_df)


def style_color(df, colors):
    """

    :param df: pd.DataFrame
    :param colors: 字典 内容是 {标题:颜色}
    :return:
    """
    return df.style.apply(style_apply, colors=colors)


def style_apply(series, colors, back_ground=''):
    """
    :param series: 传过来的数据是DataFramt中的一列  类型为pd.Series
    :param colors: 内容是字典 其中key 为标题名  value 为颜色
    :param back_ground: 北京颜色
    :return:
    """
    series_name = series.name[0]
    a = list()
    # 为了给每一个单元格上色
    for col in series:
        # 其中 col 为pd.DataFrame 中的 一个小单元格  大家可以根据不同需求为单元格设置不同的颜色
        # 获取什么一级标题获取什么颜色
        if series_name in colors:
            for title_name in colors:
                if title_name == series_name:
                    back_ground = 'background-color: ' + colors[title_name]
                    # '; border-left-color: #080808'
        a.append(back_ground)
    return a


style_df = style_color(demo_df, {"A": '#1C1C1C', "B": '#00EEEE', "C": '#1A1A1A'})

with pd.ExcelWriter('df_style.xlsx', engine='openpyxl') as writer:
    # 注意： 二级标题的to_excel index 不能为False
    style_df.to_excel(writer, sheet_name='sheet_name')
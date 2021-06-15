import xlsxwriter
import time

times = int(time.time())

wb = xlsxwriter.Workbook("data/data" + str(times) + ".xls")
sheet1 = wb.add_worksheet("sheet1")

year_format = wb.add_format({"bold": True})
sheet1.write(0, 0, '2020年度', year_format)

sn_format = wb.add_format()
sn_format.set_bold()
sn_format.set_font_color("red")
sn_format.set_font_size(14)
sn_format.set_align("center")

sheet1.merge_range(1, 0, 2, 2, "第一季度销售统计", sn_format)

sheet1.write_row(3, 0, ["月份", "预期销售额", "实际销售额"])

data = (
    ["第一季度", 200, 150],
    ["第二季度", 250, 350],
    ["第三季度", 400, 450],
)

for idx, item in enumerate(data):
    sheet1.write_row(idx+4, 0, item)

sheet1.write_url(8, 0, "http://www.baidu.com", string="更多信息")
sheet1.insert_image(10, 0, "data/view.png")

# 创建树状图
chart = wb.add_chart({'type': "column"})
chart.set_title({'name': '第一季度销售统计'})
chart.set_x_axis({'name': '月份'})
chart.set_y_axis({'name': '销售额'})

chart.add_series({
    'name': '预期销售额',
    'categories': '=sheet1！$A$5：$A$7',
    'values': '==sheet1！$B$5：$B$7',
    'data_labels': {'value': True}
})

chart.add_series({
    'name': '实际销售额',
    'categories': '=sheet1！$A$5：$A$7',
    'values': ['sheet1', 4, 2, 6, 2],
    'data_labels': {'value': True}
    # 'line': {'color': 'red'},
})

# 插入图表
sheet1.insert_chart('A20', chart)

wb.close()
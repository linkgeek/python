import xlwt

# 创建工作簿
wb = xlwt.Workbook()

# 创建工作表
ws = wb.add_sheet("CNY")

# 填充数据
ws.write_merge(0, 1, 0, 5, "2020货币兑换表")

data = (
    ("用户id", "用户昵称", "玩牌局数", "付费金额", "绑定的手机号",	"金豆总量",	"累计在线时长(小时)",	 "最后登陆日期"),
    (1443032897, "葛伏敏", 383, 0, 0, 42225970,	825.4200000000001, "2020-05-23 06:45:22"),
    (2005316345, "无所谓", 60277, 0, 0, 42225970, 825.4200000000001,	"2020-05-27 22:14:48"),
)

for i, item in enumerate(data):
    for j, val in enumerate(item):
        ws.write(i+2, j, val)

ws_img = wb.add_sheet("image")
ws_img.insert_bitmap('./data/01.bmp', 0, 0)

# 保存
wb.save("data/2020-CNY.xls")


"""
群发工资条
"""

import openpyxl
from openpyxl import load_workbook
import yagmail  # 自动发邮件
import keyring
from datetime import *

# 加载Excel文件
wb = load_workbook("payslip.xlsx", data_only=True)  # data_only参数：会让系统计算出公式，而不是直接显示纯公式
sheet = wb.active

# 登陆邮箱
yagmail.register("941192051@qq.com", "rkljdalgwhbxbcjj")
pwd = keyring.get_password("yagmail", "941192051@qq.com")
yag = yagmail.SMTP(user="941192051@qq.com", host="smtp.qq.com", password=pwd)

count = 0
table_header = "<thead>"
for row in sheet:
    count += 1
    if count == 1:
        for cell in row:
            if cell.column != "B":
                table_header += f"<th>{cell.value}</th>"
        table_header += "</thead>"
        continue
    else:
        row_text = ""
        for cell in row:
            if cell.column == "B":
                continue
            row_text += f"<td>{cell.value}</td>"
        row_text += "</tr>"
        name = row[2].value
        email = row[1].value
        # 邮件正文
        contents = f"""
                <h3>{name}，您好！</h3>
                <p>感谢您在xxx的辛勤工作！请查收你{date.today().year}年{date.today().month}月的工资明细，如有任何疑问，请联系财务部核实。</p>
                <table border="1px solid black">{table_header}{row_text}</table>
        """
        # 发邮件
        yag.send(f"{email}", f"Python测试-{date.today().year}年{date.today().month}月工资明细", contents)
        print(f"{name}的工资条发送完毕")
print("所有员工工资条发送完毕！")

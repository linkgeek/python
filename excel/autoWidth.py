import xlwt
import copy

'''
利用python的xlwt模块自适应列宽写入excel
'''


# 获取每列所占用的最大列宽
def get_max_col(max_list):
    line_list = []
    # i表示行，j代表列
    for j in range(len(max_list[0])):
        line_num = []
        for i in range(len(max_list)):
            line_num.append(max_list[i][j])  # 将每列的宽度存入line_num
        line_list.append(max(line_num))  # 将每列最大宽度存入line_list
    return line_list


def write_excel():
    # 创建一个Workbook对象
    book = xlwt.Workbook(encoding="utf-8", style_compression=0)

    # 创建一个sheet对象
    sheet = book.add_sheet('person_msg', cell_overwrite_ok=True)

    # 个人信息：姓名，性别，年龄，手机号，固定电话，邮箱
    data = [
        ['姓名', '性别', '年龄', '手机号', '固定电话', '邮箱'],
        ['厘清', '女', '31', '18745214693', '0104784125', '5412546qq.com'],
        ['张三', '男', '26', '18245554693', '010-4784125', '无'],
        ['王武', '男', '19', '13245266693', '无', '785992546qq.com'],
        ['熊大', '男', '16', '无', '010-4784125', '115412546qq.com'],
        ['熊二', '男', '22', '18745214693', '010-47841251', '3654126qq.com'],
        ['熊二2', '男', '2222', '1874521469366', '010-478412566', '3654126qq.com1']
    ]

    col_num = [0 for x in range(0, len(data))]
    print(len(data), col_num, '\n') # 7 [0, 0, 0, 0, 0, 0, 0]
    # exit()

    row_num = 0  # 记录写入行数
    col_list = []  # 记录每行宽度

    # 写入数据
    for i in range(0, len(data)):
        for j in range(0, len(data[i])):
            print(j, data[i][j])
            sheet.write(row_num, j, data[i][j])
            col_num[j] = len(data[i][j].encode('gb18030'))  # 计算每列值的大小
        print(col_num, '\n')
        col_list.append(copy.copy(col_num))  # 记录每行每列写入的长度
        row_num += 1

    print(col_list, '\n')

    # 获取每列最大宽度
    col_max_num = get_max_col(col_list)
    print(col_max_num, '\n')  # [4, 4, 4, 11, 11, 15]
    exit()

    # 设置自适应列宽
    for i in range(0, len(col_max_num)):
        # 256*字符数得到excel列宽,为了不显得特别紧凑添加两个字符宽度
        sheet.col(i).width = 256 * (col_max_num[i] + 2)

    # 保存excel文件
    book.save('../data/person_msg.xls')


def main():
    for x in range(100):
        addr = '127.0.0.1 ac' + str(x) + '.xyz'
        print(addr)
    # write_excel()


if __name__ == '__main__':
    main()

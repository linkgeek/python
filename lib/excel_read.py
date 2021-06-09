import xlrd


# excel读处理类
class ExcelRead:
    workbook = None
    sheet = {}

    # 初始化
    def __init__(self):
        pass

    # xlrd读取
    def xlrd_read(self, file_path, sheet_name):
        self.workbook = xlrd.open_workbook(file_path)
        self.sheet = self.workbook.sheet_by_name(sheet_name)
        row_num = self.sheet.nrows
        col_num = self.sheet.ncols
        result = []
        for i in range(row_num):
            if i == 0:
                continue
            row_data = []
            for j in range(col_num):
                row_data.append(self.sheet.cell_value(i, j))
            result.append(row_data)
        return result


if __name__ == '__main__':
    xls_util = ExcelRead()
    data = xls_util.xlrd_read('./person_msg2.xls', 'person_msg')
    print(data)

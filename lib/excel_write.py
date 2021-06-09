import xlwt
import copy


# excel写处理类
class ExcelWrite:
    workbook = None
    sheets = {}
    style = {}

    # 初始化
    def __init__(self):
        # 创建一个Workbook对象
        self.workbook = xlwt.Workbook(encoding='utf-8', style_compression=0)
        # 初始化样式
        self.style = xlwt.XFStyle()

    # 新建工作簿
    def add_sheet(self, sheet_name):
        self.sheets[sheet_name] = self.workbook.add_sheet(sheet_name, cell_overwrite_ok=True)

    # xlwt写入
    def xlwt_write(self, data, header, sheet_name, path='test'):
        """
        :param data: array 表格数据
        :param header: array 表头数据
        :param sheet_name: array 表头数据
        :param path: string 输出路径
        """
        self.sheets[sheet_name] = self.workbook.add_sheet(sheet_name, cell_overwrite_ok=True)

        # 列数
        col_num = [0 for x in range(0, len(header))]
        # 记录每行每列宽度
        col_list = []

        # 表头
        for i, name in enumerate(header):
            self.sheets[sheet_name].write(0, i, name)
            # 设置行高
            self.sheets[sheet_name].row(0).height_mismatch = True
            self.sheets[sheet_name].row(0).height = 20 * 24  # 20为基准数，24磅
            # 计算每列值的大小
            col_num[i] = len(name.encode('gb18030'))
        # 记录一行每列写入的长度
        col_list.append(copy.copy(col_num))

        # 单元格
        for row in range(len(data)):  # 行
            for col in range(len(data[row])):  # 列
                val = data[row][col]
                self.sheets[sheet_name].write(row + 1, col, val)
                col_num[col] = len(str(val).encode('gb18030'))

            col_list.append(copy.copy(col_num))
            self.sheets[sheet_name].row(row + 1).height_mismatch = True
            self.sheets[sheet_name].row(row + 1).height = 20 * 22

        # 获取每列最大宽度
        col_max_num = self.get_max_col(col_list)

        # 设置自适应列宽
        for i in range(0, len(col_max_num)):
            # 256*字符数得到excel列宽, 为了不显得特别紧凑添加两个字符宽度
            self.sheets[sheet_name].col(i).width = 256 * (col_max_num[i] + 2)
        self.save_excel(path)

    # 获取每列所占用的最大列宽
    @staticmethod
    def get_max_col(max_list):
        line_list = []
        # i表示行，j代表列
        for j in range(len(max_list[0])):
            line_num = []
            for i in range(len(max_list)):
                line_num.append(max_list[i][j])  # 将每列的宽度存入line_num
            line_list.append(max(line_num))  # 将每列最大宽度存入line_list
        return line_list

    # 设置列宽度
    def set_col_width(self, col_idx, row_font_num, sheet_name):
        """
        设置列宽和自动换行       256是以0字符作为衡量单位，一行存放row_font_num个字符
        :param col_idx:        列的索引值
        :param row_font_num:   一列包含的字符数
        :param sheet_name:     单元格名称
        """
        self.sheets[sheet_name].col(col_idx).width = 256 * row_font_num

    # 保存表格
    def save_excel(self, path):
        """
        :param path: 保存的路径
        """
        self.workbook.save(path)


if __name__ == '__main__':
    xls_util = ExcelWrite()
    xls_util.xlwt_write([
        [1.0, '海底世界', '1.mp4', '1.png', 'animal:动物,coral:珊瑚', '神秘的海底世界', '免费'],
        [2.0, '沙滩上的一天', '2.mp4', '2.png', 'brown:棕色的,cute:可爱,desk:书桌', '沙滩，阳光，贝壳', '免费'],
        [3.0, '沙滩，我来了！', '3.mp4', '3.png', 'beach:海滩,shorts:短裤', '炎炎夏日，最好的去处当然是沙滩啦', '会员'],
        [4.0, '在度假中', '4.mp4', '4.png', 'beach:海滩', '让我们一起去看看我们小伙伴的度假时光吧', '会员']],
        ['编号', '名称', '视频文件', '封面文件', '单词', '简介', '权限'], 'Sheet1', 'test_new2.xlsx')

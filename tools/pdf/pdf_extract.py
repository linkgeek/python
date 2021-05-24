# 提取pdf 文字 文本 表格 table
import pdfplumber
import xlwt
import urllib.request
import pandas as pd
import PySimpleGUI as sg


# PDF提取文字
def extract_text(pdf_path, page=False):
    pdf = pdfplumber.open(pdf_path)
    save_path = r'./dd.txt'
    with open(save_path, 'a', encoding='utf-8') as f:
        # 提取第page页的所有文字
        if page is not False:
            parse_page = pdf.pages[page]
            text = parse_page.extract_text()
            f.write(text + '\n')
        else:  # 提取所有页的文字
            for page in pdf.pages:
                parse_page = pdf.pages[page]
                text = parse_page.extract_text()
                f.write(text + '\n')

    print('写入txt成功')
    return save_path


# PDF提取表格
def extract_table(pdf_path):
    pdf = pdfplumber.open(pdf_path)
    workbook = xlwt.Workbook()  # 定义workbook
    sheet = workbook.add_sheet('dd出行报销单')  # 添加sheet并命名
    i = 0  # Excel起始位置
    for page in pdf.pages:  # 获取所有页面的全部信息，包括表格中的文字
        for table in page.extract_tables():  # 遍历文档中的所有表格
            for row in table:  # 遍历每一个表格的每一行
                for j in range(len(row)):  # 将PDF表格里的每一行每一列都提取出来写进excel表里
                    sheet.write(i, j, row[j])
                i += 1

    pdf.close()
    save_path = r'./dd.xls'
    workbook.save(save_path)
    print('写入excel成功')
    return save_path


# PDF提取表格2
def extract_table2(pdf_path):
    pdf = pdfplumber.open(pdf_path)
    i = 0  # Excel起始位置
    for page in pdf.pages:  # 获取所有页面的全部信息，包括表格中的文字
        for table in page.extract_tables():  # 遍历文档中的所有表格
            pd.DataFrame(table).to_csv('./dd_{}.csv'.format(i + 1), index=False, mode='a')
        i += 1

    pdf.close()
    print('写入csv成功')


def web_gui():
    sg.theme('BluePurple')  # 主题颜色
    # All the stuff inside your window.
    layout = [
        [sg.Frame(layout=[
            [sg.Radio('获取文字', "RADIO1", default=True, size=(10, 1), key='text'),
             sg.Radio('获取表格', "RADIO1", key='table')]
        ], title='选项', title_color='red', relief=sg.RELIEF_SUNKEN)],
        [sg.Text('PDF文件路径:', size=(10, 1), auto_size_text=False, justification='right'),
         sg.InputText(enable_events=True, key='filePath'), sg.FileBrowse(button_text='打开')],
        [sg.Button(button_text='确认', target=(1, -1)), sg.Button(button_text='退出', target=(1, 0))],
        [sg.Text('本工具仅限测试使用', auto_size_text=False, justification='center')],
    ]

    # 创建一个窗口,第一个参数是窗口名称,有layout参数就是本窗口的内容
    window = sg.Window('PDF提取器', layout, default_element_size=(40, 1), grab_anywhere=False)
    while True:
        # Read()是阻塞式方法,会阻塞程序的进行，直到Button被点击才有返回值
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == '退出':
            break

        print('You entered ', event, values)
        if event == '确认':
            print(values)
            upload_path = values['filePath']
            if len(upload_path) == 0:
                sg.popup_error('请选择文件', title='提示')
                continue
            print(upload_path)
            exit()
            if values['text']:
                extract_text(upload_path)
            elif values['table']:
                extract_table2(upload_path)

    window.close()


def down_file(file_path=''):
    urllib.request.urlretrieve('https://files.cnblogs.com/files/alex-bn-lee/ESRI_01.zip', "demo.zip")


def main():
    # extract_text()
    # extract_table()
    web_gui()
    # down_file()


if __name__ == '__main__':
    main()

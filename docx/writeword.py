from docx import Document

doc = Document()

doc.add_heading('python docx 测试')

doc.save('../data/info.docx')
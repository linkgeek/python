from PIL import Image, ImageTk
from tkinter.filedialog import askopenfilename
from tkinter import *
import PIL
from main import PutLipsticks


class LipsticksChoose(object):
    def __init__(self):
        self.root = Tk()
        self.root.title('口红选择软件')
        self.root.geometry('1200x500')
        decoration = PIL.Image.open('static/bg.jpg').resize((1200, 500))  # 背景桌面
        render = ImageTk.PhotoImage(decoration)
        img = Label(image=render)
        img.image = render
        img.place(x=0, y=0)
        # 原图1的展示
        Button(self.root, text="打开图片", command=self.choosePic).place(x=50, y=120)

        Button(self.root, text="选择口红", command=self.showlipStickpic).place(x=50, y=280)

        Button(self.root, text="退出软件", command=quit).place(x=900, y=40)

        Label(self.root, text="口红色系", font=10).place(x=50, y=10)
        self.entry = Entry(self.root)
        self.entry.place(x=130, y=10)

        Label(self.root, text="图片1", font=10).place(x=380, y=120)
        self.cv_orinial = Canvas(self.root, bg='white', width=270, height=270)
        self.cv_orinial.create_rectangle(8, 8, 260, 260, width=1, outline='red')
        self.cv_orinial.place(x=280, y=150)
        self.label_Img_original = Label(self.root)
        self.label_Img_original.place(x=280, y=150)

        Label(self.root, text="口红效果", font=10).place(x=720, y=120)
        cv_seg = Canvas(self.root, bg='white', width=270, height=270)
        cv_seg.create_rectangle(8, 8, 260, 260, width=1, outline='red')
        cv_seg.place(x=620, y=150)
        self.label_Img_seg = Label(self.root)
        self.label_Img_seg.place(x=620, y=150)

        self.root.mainloop()

    # 原图1展示
    def choosePic(self):
        self.picPath = askopenfilename(title='选择文件')
        Img = PIL.Image.open(r'{}'.format(self.picPath))
        Img = Img.resize((270, 270), PIL.Image.ANTIALIAS)  # 调整图片大小至270,270
        img_png_original = ImageTk.PhotoImage(Img)
        self.label_Img_original.config(image=img_png_original)
        self.label_Img_original.image = img_png_original  # keep a reference
        self.cv_orinial.create_image(5, 5, anchor='nw', image=img_png_original)

    # 人脸融合效果展示
    def showlipStickpic(self):
        mor_img_path = PutLipsticks(self.picPath, self.entry.get())
        Img = PIL.Image.open(r'{}'.format(mor_img_path))
        Img = Img.resize((270, 270), PIL.Image.ANTIALIAS)  # 调整图片大小至256x256
        img_png_seg = ImageTk.PhotoImage(Img)
        self.label_Img_seg.config(image=img_png_seg)
        self.label_Img_seg.image = img_png_seg  # keep a reference

    def quit(self):
        self.root.destroy()


lips = LipsticksChoose()

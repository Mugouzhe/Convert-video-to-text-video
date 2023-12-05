import numpy as np
import PIL.Image
from PIL import ImageDraw,ImageFont
from tkinter import *
from tkinter import filedialog
import cv2


root=Tk()
root.geometry('600x500')
entry_text =StringVar()
enter=Entry(root,textvariable=entry_text)
enter.place(rely=0.01,relx=0.46,relwidth=0.39)
text=Label(text='请输入文字，并以中文符号‘；’分号隔开:\n注：不要输入重复的字')
text.place(relx=0.05,rely=0.01,relwidth=0.4)
wd = enter.get()
text1=Label(root,text='')
text1.place(relx=0.052,rely=0.1,width=500,height=20)

lb4=Label(root)
lb4.place(relx=0.08,rely=0.85)

text2=Label(root,text='命名为:')
text2.place(relx=0.65,rely=0.2,relwidth=0.08,height=25)
entry_text1 =StringVar()
enter1=Entry(root,textvariable=entry_text1)
enter1.place(rely=0.2,relx=0.73,relwidth=0.12,height=25)

def xiangsu(wd,zi):
    font_size = 36
    font = ImageFont.truetype("simsun.ttc", font_size)
    text = wd[zi-1]
    kk, h = font.getsize(text)
    img = PIL.Image.new('RGB', (kk, h), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    draw.text((0, 0), text, font=font, fill=(0, 0, 0))
    count = 0
    for x in range(kk):
        for y in range(h):
            pixel = img.getpixel((x, y))
            if sum(pixel) < 255 * 3 / 2:
                count += 1
    return count

def V_w():
    global c
    c = filedialog.askopenfilename()
    return c

b1=Button(root,text='选择转换视频',command=V_w)
b1.place(rely=0.09,relx=0.07)

def word_co(wd):
    print(wd)
    wd=wd.split('；')
    le=len(wd)
    wd_di={}
    while le:
        co=xiangsu(wd,le)
        wd_di[co]=wd[le-1]
        le -= 1
    wd_lik = sorted(wd_di.keys())
    wd_li=[]
    print(len(wd), len(wd_lik))
    for i in range(0,len(wd)):
        wd_li.append(wd_di[wd_lik[i]])
    print(wd_li)
    return wd_li

def run():
    global path
    global wd
    wd = enter.get()
    wl=word_co(wd)
    global c
    vc = cv2.VideoCapture(c)
    FPS=vc.get(cv2.CAP_PROP_FPS)
    aa = []
    cc = xuan2.get()
    while vc.isOpened():
        ret, frame = vc.read()
        if not ret:
            break
        aa.append(frame)
    if cc==2 or cc==3 or cc==4:
        aa=aa[0:len(aa):cc]
        fps=int(FPS/cc)
    elif cc==1:
        aa=aa
        fps=int(FPS)
    else:
        del aa[0:len(aa):(cc-2)]
        fps=int(FPS/(cc-2)*(cc-3))
    aa_len=len(aa)
    frame_wi=int(vc.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_he=int(vc.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print(frame_he,frame_wi)
    vc.release()

    lv=xuan.get()
    font_size = lb2.get()
    font = ImageFont.truetype("simsun.ttc", font_size)
    cv_lis=[]
    for j in range(0,aa_len):
        im=PIL.Image.fromarray(cv2.cvtColor(aa[j],cv2.COLOR_BGR2RGB))         #将OpenCV图像转化为PIL图像
        i = im.resize((int(im.width / lv), int(im.height / lv)), PIL.Image.ANTIALIAS)
        imag = i.convert('L')
        image = np.array(imag)
        new_pi=PIL.Image.new('RGB',(int(frame_wi/lv*font_size),int(frame_he/lv*font_size)),(255,255,255))  #创建背景图片
        print(j)
        for x in range(0,len(image)):
            for y in range(0,len(image[0])):
                xx=image[x][y]
                bbb=len(wl)-1
                for ij in range(0,len(wl)):
                    if (xx >= ((256 / len(wl)) * ij)) and (xx < ((256 / len(wl)) * (ij + 1))):
                        draw = ImageDraw.Draw(new_pi)
                        draw.text((int(y*font_size),int(x*font_size)), wl[bbb], font=font, fill=(0, 0, 0))
                        break
                    bbb-=1
        #new_pi .show()
        imge_lis_np = np.array(new_pi)
        op_im = cv2.cvtColor(imge_lis_np, cv2.COLOR_RGB2BGR)  #将pil图像转化为opencv图像
        cv_lis.append(op_im)
    name=enter1.get()
    video=cv2.VideoWriter(path+'/'+name+'.mp4',cv2.VideoWriter_fourcc(*"mp4v"),
                          fps,(int(frame_wi/lv*font_size),int(frame_he/lv*font_size)),True)
    for im in cv_lis:
        video.write(im)
    cv2.destroyAllWindows()
    video.release()
    print('合成完成')

lb=Label(root,text='请 降 低 分 辨 率:')
lb.place(relx=0.07,rely=0.42,height=20)
xuan=IntVar()
x1=Radiobutton(root,text='1/4',variable=xuan,value=3)
x2=Radiobutton(root,text='1/6',variable=xuan,value=6)
x3=Radiobutton(root,text='1/8',variable=xuan,value=8)
x4=Radiobutton(root,text='1/10',variable=xuan,value=10)
x1.place(relx=0.41,rely=0.42,height=20)
x2.place(relx=0.5,rely=0.42,height=20)
x3.place(relx=0.62,rely=0.42,height=20)
x4.place(relx=0.74,rely=0.42,height=20)

lb2=IntVar()
scl=Scale(root,orient=HORIZONTAL,length=380,from_=6,to=18,label='请选择合适字体像素',tickinterval=1,resolution=1,variable=lb2)
#scl.bind('<ButtonRelease-1>',show)
scl.place(relx=0.068,rely=0.52)

lb3=Label(root,text='将合成视频的帧率降低为原视频的:')
lb3.place(relx=0.07,rely=0.32,height=20)
xuan2=IntVar()
xx1=Radiobutton(root,text='1',variable=xuan2,value=1)
xx2=Radiobutton(root,text='1/2',variable=xuan2,value=2)
xx3=Radiobutton(root,text='1/3',variable=xuan2,value=3)
xx4=Radiobutton(root,text='1/4',variable=xuan2,value=4)
xx5=Radiobutton(root,text='2/3',variable=xuan2,value=5)
xx6=Radiobutton(root,text='3/4',variable=xuan2,value=6)
xx1.place(relx=0.41,rely=0.29,height=20)
xx2.place(relx=0.41,rely=0.34,height=20)
xx3.place(relx=0.53,rely=0.34,height=20)
xx4.place(relx=0.64,rely=0.34,height=20)
xx5.place(relx=0.53,rely=0.29,height=20)
xx6.place(relx=0.64,rely=0.29,height=20)
def yer():
    global c
    vc = cv2.VideoCapture(c)
    FPS = vc.get(cv2.CAP_PROP_FPS)
    frame_wi = int(vc.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_he = int(vc.get(cv2.CAP_PROP_FRAME_HEIGHT))
    vc.release()
    s = "当前视频帧率： " + str(FPS) + "   分辨率：" + str(frame_wi) + " * " + str(frame_he)
    text1.config(text=s)

butt3=Button(root,text='确定',command=yer)
butt3.place(rely=0.09,relx=0.75,relwidth=0.1)

entry_text2 =StringVar()
entry2 = Entry(root, textvariable=entry_text2)
entry2.place(relx=0.07,rely=0.2,relwidth=0.4,height=23)
def get_path():
    global path
   
    path = filedialog.askdirectory()

    entry_text2.set(path)

button4 = Button(root, text='选择保存路径', command=get_path)
button4.place(relx=0.47,rely=0.2,height=25)
butten2=Button(root,text='开始合成',command=run)
butten2.place(relx=0.4,rely=0.73,width=100,height=30)

root.mainloop()

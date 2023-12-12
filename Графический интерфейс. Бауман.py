from tkinter import *
from tkinter import ttk
import astropy.io.fits as pyfits
import matplotlib.pyplot as plt
import numpy as np

#/Users/User/Downloads/v523cas60s-001(1).fit

def changed(): # отслеживает, в каком состоянии находится наш флажок
    global gx
    global gy
    global g3d
    gx = 0
    gy = 0
    g3d = 0
    if var1.get() == 1:
        gx = 11
    if var2.get() == 1:
        gy = 11
    if var3.get() == 1:
        g3d = 11

def graph():
    global ent
    f = str(ent.get())
    hdulist = pyfits.open(f)
    scidata = hdulist[0].data
    global entx
    global enty
    global entr
    global entr1
    global entr2
    global xser
    global yser

    # находим кол-во пикселей в звезде
    x = int(entx.get())
    x = int(x)
    y = int(enty.get())
    y = int(y)
    r = int(entr.get())
    r = int(r)
    X1 = []
    X2 = []
    Y1 = []  # изменяем х
    Y2 = []
    for i in range(x - r, x + r):  # записываем х
        Y1.append(scidata[y][i])
        X1.append(i)
    for i in range(y - r, y + r):
        Y2.append(scidata[i][x])
        X2.append(i)

    if gx == 11:
        plt.figure()  # создает полотно для нескольких графиков
        plt.title('                          Изменение светимости звезды от координаты')
        plt.plot(X1, Y1)
        plt.xlabel('Изменение координаты Х')
        plt.ylabel('Значение энергии')
        plt.show()

    if gy == 11:
        plt.figure()
        plt.title('                          Изменение светимости звезды от координаты')
        plt.plot(X2, Y2)
        plt.xlabel('Изменение координаты Y')
        plt.ylabel('Значение энергии')
        plt.show()

    Z = np.empty((len(Y2), len(X2)), dtype=int)
    x1 = np.empty((len(X1), 1), dtype=int)
    y1 = np.empty((len(X2), 1), dtype=int)
    for i in range(len(X2)):
        y1[i] = int(X2[i])

    for i in range(len(Y1)):
        x1[i] = int(X1[i])

    X, Y = np.meshgrid(x1, y1)

    for i in range(x - r, x + r):
        for j in range(y - r, y + r):
            Z[j - y + r][i - x + r] = int(scidata[j][i])

    if g3d == 11:
        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')
        surf = ax.plot_surface(X, Y, Z)
        ax.set_xlabel('Номер пикселя')
        ax.set_ylabel('Номер пикселя')
        ax.set_zlabel('Изменение энергии по Y')
        plt.title('Профиль 3d')
        plt.show()
        hdulist.close()

def photometry():
    f = str(ent.get())
    hdulist = pyfits.open(f)
    scidata = hdulist[0].data

    # находим кол-во пикселей в звезде
    xser = int(entx.get())
    yser = int(enty.get())
    r = int(entr.get())

    exp = hdulist[0].header['exptime']

    pix = 0
    value_star = 0
    for i in range(xser - r, xser + r):
        for j in range(yser - r, yser + r):
            if (i - xser)**2 + (j - yser)**2 <= r**2:
                pix += 1
                value_star += scidata[j][i]
    value_star_sec = value_star / exp  # энергия звезды за одну секунду

    # считаем среднее значение фона на 1 пикселе за 1 секунду
    r1 = int(entr1.get())  # Внутренний радиус колечка
    r2 = int(entr2.get())  # Внешний радиус колечка
    #R = abs(r2 - r1)


    # колечко
    value_col = 0
    count = 0
    for i in range(xser - r2, xser + r2):
        for j in range(yser - r2, yser + r2):
            if ((i - xser) ** 2 + (j - yser) ** 2 >= r ** 2) and ((i - xser) ** 2 + (j - yser) ** 2 <= r2 ** 2):
                count += 1
                value_col += scidata[j][i]
    sr_fon = (value_col / exp / count)  # среднее значение фона на 1 пикселе за 1 секунду (колечко)

    # считаем фон звезды
    fon_star = pix * sr_fon

    # энергия звезды за вычетом фона
    value_bez_fon = value_star_sec - fon_star
    lblv["text"] = value_bez_fon


root = Tk() # создаём корневой объект - окно
root.title("Новое окно") # утсанавливаем заголовок окна
root.geometry("800x500") # устанавливаем размеры окна, если geometry не указать, то окно занимает то пространство, которое необходимо

# создаём конфигурацию grid
for c in range(10):
    root.columnconfigure(index=c)
for r in range(10):
    root.rowconfigure(index=r)

# окно ввода пути к фитс файлу
lblp = ttk.Label(text="Путь к fits-файлу")
lblp.grid(row=0,column=0)
ent = ttk.Entry()
ent.grid(row=1, column=0)

# окно ввода координат интересующей звёзды
lblx = ttk.Label(text="Координата x звезды")
lblx.grid(row=2, column=0)
entx = ttk.Entry()
entx.grid(row=3, column=0)
lbly = ttk.Label(text="Координата y звезды")
lbly.grid(row=4, column=0)
enty = ttk.Entry()
enty.grid(row=5, column=0)

# окна ввода радиуса звёзды и внешнего и внутреннего радиусов фона
lblr = ttk.Label(text="Радиус звёзды")
lblr.grid(row=6, column=0)
entr = ttk.Entry()
entr.grid(row=7, column=0)
lblr1 = ttk.Label(text="Внутренний радиус фона")
lblr1.grid(row=8, column=0)
entr1 = ttk.Entry()
entr1.grid(row=9, column=0)
lblr2 = ttk.Label(text="Внешний радиус фона")
lblr2.grid(row=10, column=0)
entr2 = ttk.Entry()
entr2.grid(row=11, column=0)

# кнопка, при нажатии которой выполняется фотометрия данной звёзды и поток(в отсчетах) выводится пользователю
btnp = ttk.Button(text="Поток", command=photometry) # создали кнопку
btnp.grid(row=0, column=1, ipadx=30, ipady=6, padx=47, pady=4)

lblv = ttk.Label(font=("Arial", 15))
lblv.grid(row=2, column=1)

# chekbutton или radiobutton, позволяющие пользователю выбрать,
# какие графики для данной звёзды он хотел бы получить (профиль по координате Х, профиль по координате Y, 3D профиль)

var1 = IntVar()
chbtn = ttk.Checkbutton(text="Профиль по координате Х", variable=var1, command=changed)
chbtn.grid(row=6, column=1)

var2 = IntVar()
chbtn = ttk.Checkbutton(text="Профиль по координате Y", variable=var2, command=changed)
chbtn.grid(row=8, column=1)

var3 = IntVar()
chbtn = ttk.Checkbutton(text="3D профиль", variable=var3, command=changed)
chbtn.grid(row=10, column=1)

# кнопка для вывода графика
btng = ttk.Button(text="Графики", command=graph)
btng.grid(row=0, column=2, ipadx=30, ipady=6, padx=47, pady=4)


root.mainloop() # не даёт окну закрыться
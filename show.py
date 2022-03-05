from mod.tkinter import*
from sql_fun import*
from main_fun import*
from mod.matplotlib import pyplot as p




def enter():
    name = En.get()
    img(name)

def img(tmp_dt):
    if tb_cre(tmp_dt):
        con = c.connect(host = 'localhost',user = 'root',passwd = '0000',database = tmp_dt)
        cur = con.cursor()
    
        cur.execute("select* from ussage")
        tmp_data = cur.fetchall()

        lst = []
        for i in tmp_data:
            tHH = (int(i[1]))*(3600)
            tMM = (int(i[2]))*(60)
            tSS = (int(i[3]))
            tTT = tHH + tMM + tSS

            lst += [[i[0],tTT]]


        x = bubblesort(lst)[:6]
        name_lst = []
        time_lst = []
        pres_lst = []
        explode = [0.1]

        for i in x:
            tt = i[1]
            th = str(tt // 3600)
            tm = str((tt % 3600) // 60)
            ts = str(tt % 60)

            name_lst += [i[0]]
            pres_lst += [i[0] + " = " + "{} H, {} M, {} S".format(th,tm,ts)]
            time_lst += [tt]



        
        for i in range (len(name_lst) - 1):
            explode += [0]


        p.style.use('ggplot')
        p.title('USSAGE PATERN ON '+ tmp_dt.upper() ,color='red')
        p.pie(x = time_lst , explode = explode , labels = pres_lst , autopct="%.1f%%",shadow=True,startangle=0)
        p.axis('equal')
        p.legend(loc='upper left')
        p.show()



root = Tk()
root.geometry('200x200')
name_var = StringVar()

Lab = Label(text='Enter the date')
Lab2 = Label(text = 'Format <"MMM":"DD":"YYYY">')
Lab.pack()
Lab2.pack()

En = Entry(root,textvariable = name_var)
En.pack()

But = Button(root,text="Enter" , command = enter)
But.pack()

root.mainloop()


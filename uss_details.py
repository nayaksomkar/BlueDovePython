from sql_fun import*



tmp_dt = input('Enter the date  /  Format <"MMM":"DD":"YYYY">       :       ')
print("\n"*2,'USSAGE PATERN ON '+ tmp_dt.upper(),"\n"*2,sep ="")

if tb_cre(tmp_dt):
    con = c.connect(host = 'localhost',user = 'root',passwd = '0000',database = tmp_dt)
    cur = con.cursor()

    cur.execute("select* from app_ussage")
    tmp_data = cur.fetchall()
    cont_lst = ["APP_NAME" ,"TASK_NAME","USS_TIME","START_TIME","END_TIME"]

    for i in tmp_data:
        print("{}     =       ".format(cont_lst[0]),i[0])
        print("{}    =       ".format(cont_lst[1]),i[1])
        print("{}     =       ".format(cont_lst[2]),i[2])
        print("{}   =       ".format(cont_lst[3]),i[3])
        print("{}     =       ".format(cont_lst[4]),i[4])
        print("\n")




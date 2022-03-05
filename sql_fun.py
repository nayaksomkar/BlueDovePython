from mysql import connector as c
from main_fun import*



def db_cre(db_name):
    def_db = 'mysql'
    con = c.connect(host = 'localhost',user = 'root',passwd = '0000',database = def_db)
    cur = con.cursor()

    cur.execute("show databases")
    tmp_data = cur.fetchall()
   
    lst = []
    for i in tmp_data:
        lst += [i[0]]

    if db_name.lower() in lst:
          return True
    else:
        cur.execute("create database {}".format(db_name))



def tb_cre(db_name):
    if db_cre(db_name):
        con = c.connect(host = 'localhost',user = 'root',passwd = '0000',database = db_name)
        cur = con.cursor()

        cur.execute("show tables")
        tmp_data = cur.fetchall()

        lst = []
        for i in tmp_data:
            lst += [i[0]]

        if "app_ussage" not in lst:
            query_01 = "\
            create table app_ussage(app_name varchar(1000),\
            task varchar(1000),\
            uss_time time ,\
            start_time datetime ,\
            end_time datetime);"
            
            cur.execute(query_01)
            con.commit()
            con.close()
    
           
        elif "ussage" not in lst:
            query_02 = "\
            create table ussage(app_name varchar(1000),\
            HH varchar(2) ,\
            MM varchar(2) ,\
            SS varchar(2));"

            cur.execute(query_02)
            con.commit()
            con.close()

        else:
            return True
                    
        
            
def tb1_val(db_name , ap , tk , us , st , et):

    if tb_cre(db_name):
        con = c.connect(host = 'localhost',user = 'root',passwd = '0000',database = db_name)
        cur = con.cursor()

        query = "insert into app_ussage(app_name,task,uss_time,\
                   start_time,end_time) values('{}','{}','{}','{}','{}'\
                    )".format(ap,tk,us,st,et)


        cur.execute(query)
        con.commit()
        con.close()



def tb2_val(db_name , ap , hh , mm , ss):

    if tb_cre(db_name):
        con = c.connect(host = 'localhost',user = 'root',passwd = '0000',database = db_name)
        cur = con.cursor()

        query = "insert into ussage(app_name,HH,MM,SS) values('{}','{}','{}','{}')".format(ap,hh,mm,ss)
                
        cur.execute(query)
        con.commit()
        con.close()



def sql_time(tup , hh , mm , ss):
    tHH = (int(tup[0]) + int(hh))*(3600)
    tMM = (int(tup[1]) + int(mm))*(60)
    tSS = (int(tup[2]) + int(ss))
    tTT = tHH + tMM + tSS
    
    tHH = str(tTT // 3600)
    tMM = str((tTT % 3600) // 60)
    tSS = str(tTT % 60)

    yup = [tHH,tMM,tSS]

    return yup



def tb2_up(db_name , ap , hh , mm , ss):
    
    if tb_cre(db_name):
        con = c.connect(host = 'localhost',user = 'root',passwd = '0000',database = db_name)
        cur = con.cursor()
    
        cur.execute("select* from ussage")
        tmp_data = cur.fetchall()

        lst = []
        for i in tmp_data:
            lst += [i[0]]

        if ap in lst:
            xt = tmp_data[lst.index(ap)][1:]
            yo = sql_time(xt, hh , mm ,ss)

            query_01 = "update ussage set HH = '{}' where app_name = '{}';".format(yo[0] , ap)
            query_02 = "update ussage set MM = '{}' where app_name = '{}';".format(yo[1] , ap)
            query_03 = "update ussage set SS = '{}' where app_name = '{}';".format(yo[2] , ap)

            cur.execute(query_01)
            cur.execute(query_02)
            cur.execute(query_03)

            con.commit()
            con.close()

        else:
            tb2_val(db_name , ap , hh , mm , ss)


# a function to sort a list using bubble sort algorithm
def bubblesort(lst):
        # get the length of the list
        n = len(lst)
        # go through the list n number of times
        for i in range(n):
                # variable to keep check for any swaps
                swap = False
                # traverse through all adjacent elements
                for j in range(0, n-i-1):
                    # if current element smaller than next element, swap them
                    if not lst[j][1]>lst[j+1][1]:
                        lst[j], lst[j+1] = lst[j+1], lst[j]
                        swap = True
                # if no swaps, then break out of the loop
                if swap == False:
                        break
        
        return (lst)




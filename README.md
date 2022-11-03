# Blue-Dove
Activity tracking and monitoring for PC digital wellbeing, by using python and MySQL.


\\     data structure used in blue_dove.py         

                    tmp_dct = {
                                "APP_NAME" : cr[se_last][0],
                                "TASK_NAME" : cr[se_last][1],
                                "TIME" : cr[la_last][2],
                                "HOURS" : cr[la_last][3],
                                "MINUTES" : cr[la_last][4],
                                "SECONDS" : cr[la_last][5],
                                "START_TIME" : cr[la_last][6],
                                "END_TIME" : cr[la_last][7]
                                                         }

                                                                                                   </>
   


\\       Undefined Error       

from win32gui import GetForegroundWindow, GetWindowText  #is working fine

but mod.win32gui , triggers unable to found module error

<File "c:\Users\DELL\OneDrive\Desktop\TEST\blue_dove.py", line 3>

                                                                                                    </>    



\\ changes needed in sql_fun.py file 

In the sql_fun section in order to store data or do anykind of action with your mysql database,
you have to change the password in the sql_fun section.

def_db = 'mysql' , a database which already exist.
con = c.connect(host = 'localhost',user = 'root',passwd = '0000',database = def_db)
As you can see in my section the password is '0000'.

The def_db (default database) it's created by mysql during installation of mysql,
in order to store some required variables and all. 

                                                                                                    </>

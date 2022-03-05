from main_fun import*
import datetime as d
from win32gui import GetForegroundWindow, GetWindowText  
from sql_fun import*



current_windowTile = "" 
lst , cr = [] , []
tmp_dt = date_cv(d.date.today())

while True:
    new_WindowTile = GetWindowText(GetForegroundWindow()) 

    if new_WindowTile != current_windowTile :
        current_windowTile = new_WindowTile 
        start_time = str(d.datetime.now())[:19]

        ap_name  = current_windowTile.split("-")
        ap_name = ap_name[-1].strip()

        if len(current_windowTile) > 0:
            lst += [start_time]
            
            if len(lst) > 0:
                sec_last_ele = len(lst) - 2
                end_time = lst[sec_last_ele]

                USG = uss_time(end_time,start_time)
                ust = [USG[2],USG[3][0],USG[3][1],USG[3][2]]
            
                tmp_lst = [
                            app_name(ap_name),
                            current_windowTile,
                            ust[0],
                            ust[1],
                            ust[2],
                            ust[3],
                            end_time,
                            start_time
                                             ]

                cr += [tmp_lst]
                x = len(cr)

                if x >= 2:
                    la_last = x - 1
                    se_last = x - 2


                    db_cre(tmp_dt)
                    tb_cre(tmp_dt)
                    tb1_val(tmp_dt, cr[se_last][0] , cr[se_last][1] , cr[la_last][2] ,  cr[la_last][6] ,cr[la_last][7])
                    tb2_up(tmp_dt, cr[se_last][0] , cr[la_last][3] , cr[la_last][4] , cr[la_last][5])





                    
                    


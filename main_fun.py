from sql_fun import*


def date_cv(acc_date):
    acc_date = str(acc_date)
    acc_date = acc_date.split("-")

    mm_dic = {
    "01"  : "JAN",
    "02"  : "FEB",
    "03"  : "MAR",
    "04"  : "APR",
    "05"  : "MAY",
    "06"  : "JUN",
    "07"  : "JUL",
    "08"  : "AUG",
    "09"  : "SEP",
    "10" : "OCT",
    "11" : "NOV",
    "12" : "DEC"
} 

    if acc_date[1]  in mm_dic:
        return(mm_dic[acc_date[1]] + acc_date[2] + acc_date[0])

def app_name(full_name):
    tmp_str = ""
    for i in full_name:
        if i.isalpha() or i == " ":
            tmp_str += i

    if "Telegram" in tmp_str:
        tmp_str = "Telegram"

    tmp_str = tmp_str.replace("  "," ")

    return tmp_str

def uss_time(s_time,e_time):
    s_timeHH = (int(s_time[11:13]))*(3600)
    s_timeMM = (int(s_time[14:16]))*(60)
    s_timeSS = int(s_time[17:19])
    s_timeTT = s_timeHH + s_timeMM + s_timeSS

    e_timeHH = (int(e_time[11:13]))*(3600)
    e_timeMM = (int(e_time[14:16]))*(60)
    e_timeSS = int(e_time[17:19])
    e_timeTT = e_timeHH + e_timeMM + e_timeSS

    tmp_time = e_timeTT - s_timeTT
    tmp_timeHH = tmp_time // 3600
    tmp_timeMM = (tmp_time % 3600) // 60
    tmp_timeSS = tmp_time % 60

    tmp_tt = [str(tmp_timeHH),str(tmp_timeMM),str(tmp_timeSS)]

    for i in range (len(tmp_tt)):
        if len(tmp_tt[i]) != 2:
            tmp_tt[i] = '0' + tmp_tt[i]

    tmp_time = tmp_tt[0] + ":" + tmp_tt[1] + ":" +  tmp_tt[2]
    tmp_tup = (s_time,e_time,tmp_time,tmp_time.split(":"))
    
    return tmp_tup




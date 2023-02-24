import sys 
import datetime
import win32gui


active_window_name = ""
activity_name = ""
start_time = str(datetime.datetime.now())

while True:
    new_window_name = win32gui.GetWindowText(win32gui.GetForegroundWindow())

    if len(new_window_name) > 0 and active_window_name != new_window_name:
        active_window_name = new_window_name


        task_name = active_window_name.split('-')
        window_name = task_name[-1].strip()
        print("Window Name  :  ",window_name)
        print("Task Name    :  ",active_window_name)
        print("Start Time   :  ",start_time[11:19])
        end_time = str(datetime.datetime.now())
        print("End Time     :  ",end_time[11:19])

        delta = datetime.datetime.strptime(end_time[11:19], "%H:%M:%S") - datetime.datetime.strptime(start_time[11:19], "%H:%M:%S")

        start_time = end_time

        sec = delta.total_seconds()
        print(f"Opend for    :   {sec//60} minutes")
        # time difference in seconds

        if sec > 60:
            print(f"Opend for    :   {sec - (60 * sec//60)} seconds")
        else:
            print(f"Opend for    :   {sec} seconds")


        print()


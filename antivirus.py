from threading import *
from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror
import tkinter, tkinter.scrolledtext
import re, csv
import threading
import os, sys
import urllib.request
import glob
import time
import hashlib
import socket
import subprocess
#self-made
import quarantaene

os_name = sys.platform
verzeichnisse = []
files = []
partitionen = []
terminations = []

if "win" in os_name:
    if not os.path.exists("AntiVirus\\Quarantine\\"):
        os.makedirs("AntiVirus\\Quarantine\\")
    if not os.path.exists("AntiVirus\\sf\\"):
        os.makedirs("AntiVirus\\sf\\")
    if not os.path.exists("AntiVirus\\Large_Update_File\\"):
        os.makedirs("AntiVirus\\Large_Update_File")
    quarantine_folder = "AntiVirus\\Quarantine\\*"
    file_to_quarantine = "AntiVirus\\Quarantine\\"
    partitionen_folder = "AntiVirus\\sf\\sf.txt"
    links_current = "AntiVirus\\Large_Update_File\\links_current.txt"
    links_downloaded = "AntiVirus\\Large_Update_File\\links_downloaded.txt"
    large_signatures = "AntiVirus\\Large_Update_File\\signatures.txt"
    f = open(partitionen_folder, "a")
    f.close()
    f = open(links_current, "a")
    f.close()
    f = open(links_downloaded, "a")
    f.close()
    f = open(large_signatures, "a")
    f.close()
else:
    if not os.path.exists("AntiVirus//Quarantine//"):
        os.makedirs("AntiVirus//Quarantine//")
    if not os.path.exists("AntiVirus//sf//"):
        os.makedirs("AntiVirus//sf//")
    if not os.path.exists("AntiVirus//Large_Update_File//"):
        os.makedirs("AntiVirus//Large_Update_File//")
    quarantine_folder = "AntiVirus//Quarantine//*"
    file_to_quarantine = "AntiVirus//Quarantine//"
    partitionen_folder = "AntiVirus//sf//sf.txt"
    links_current = "AntiVirus//Large_Update_File//links_current.txt"
    links_downloaded = "AntiVirus//Large_Update_File//links_downloaded.txt"
    large_signatures = "AntiVirus//arge_Update_File//signatures.txt"
    f = open(partitionen_folder, "a")
    f.close()
    f = open(links_current, "a")
    f.close()
    f = open(links_downloaded, "a")
    f.close()
    f = open(large_signatures, "a")
    f.close()

files_len = counter = 0
main = None
update_button = None
scan_button = None
fullscan_button = None
quit_button = None
b_delete = None
b_delete_all = None
b_restore = None
b_restore_all = None
b_add_file = None
text_box = None
e = None
li = None
rb1 = None
rb2 = None
method = None
bgc = None
fgc = None
special = None
special_text = None
t_time = None
daytime = int(time.strftime("%H", time.localtime()))

#Adjusting the brightness for the current day_time
#It's totally unnecessary but I wanted to play around a little
if daytime >= 18 or daytime <= 4:
    bgc = "black"
    fgc = "white"
    special = "brown"
    special_text = "（°_°）☽ ☆ Good evening " + os.getlogin() + " ☆ ☾（°_°）\n"
elif daytime > 4 and daytime <= 8:
    special_text = "＼(o￣∇￣o)/ Good morning " + os.getlogin() + " ＼(o￣∇￣o)/\n"
    bgc = "#b4d60c"
    fgc = "black"
    special = "orange"
else:
    bgc = "white"
    fgc = "black"
    special = "#1ccaed"
    special_text = ":) Welcome to RAPID HEAL ANTIVIRUS " + os.getlogin() + " (:\n"

def clock_thread():
    global e
    months = ["January", "February", "March", "April", "May", "June", "Juli", "August", "September", "October", "November", "December"]
    while True:
        string_time = "%H:%M:%S o'clock, on %d.{0}.%Y"
        month_name = time.strftime("%B", time.localtime())
        for i in range(len(months)):
            if months[i] == month_name:
                month_name = str(i+1)
                if int(month_name) < 10:
                    month_name = "0" + month_name
                break
        string_time = string_time.format(month_name)
        current_time = time.strftime(string_time, time.localtime())
        e.delete(0, len(e.get()))
        e.update()
        e.insert(0, current_time)
        e.update()
        time.sleep(1)

def ScanSystemFiles():
    global files
    global text_box
    global files_len
    text_box.insert(END, "[ * ] Scanning system for files...\n")
    text_box.see(END)
    text_box.update()
    time.sleep(3)
    text_box.see(END)
    text_box.update()
    SystemFileScanner.partitions(partitionen_folder)
    f = open(partitionen_folder, "r")
    content = f.read()
    f.close()
    content = content.splitlines()
    files = content
    files_len = len(files)
    text_box.insert(END, "[ + ] System successfully prepared\n", 'positive')
    text_box.tag_config("positive", foreground="green")
    text_box.see(END)
    text_box.update()

def getFileData():
    # get an initial scan of file size and data modified. save
    programs = glob.glob("*.py")
    programList=[]
    for p in programs:
        programSize= os.path.getsize(p)
        programModified= os.path.getmtime(p)
        programData=[p,programSize,programModified]
        programList.append(programData)
    return programList

def WriteFileData(programs):
    if os.path.exists("fileData.txt"):
        return
    with open("fileData.txt","w") as file:
        wr=csv.writer(file)
        wr.writerows(programs)

def full_scan():
    global verzeichnisse
    global files
    global text_box
    global e
    global fullscan_button
    global files_len
    global lock
    global t_time
    global counter
    text_box.insert(END,"\n\n###### check for heuristic changes in files ######\n")
    # open the fileData.txt file and compare each line
    # to the current file size and dates
    with open("fileData.txt") as file:
        fileList=file.read().splitlines()
    orginalFileList=[]
    for each in fileList:
        items = each.split(',')
        orginalFileList.append(items)
    # get current data from directory
    currentFileList=getFileData()
    # compare old and new
    for c in currentFileList:
        for o in orginalFileList:
            if(c[0]==o[0]): # filename matched
                if str(c[1])!=str(o[1]) or str(c[2])!=str(o[2]):
                    # filesize or date don't match
                    text_box.insert(END,"\nalert!!! File mismatch\n","important")
                    text_box.tag_config("important", foreground="red")
                    #print data of each file
                    text_box.insert(END,"\ncurrent values= "+str(c)+"\n", "important")
                    text_box.insert(END,"\norginal values= "+str(o)+"\n", "important")
                else:
                    text_box.insert(END,"\nfile "+c[0]+" appears to be unchanged\n", "positive")

def quarantine():
    global text_box
    global terminations
    global li
    global b_delete
    global b_delete_all
    global b_restore
    global b_restore_all
    global b_add_file
    k = 0
    while True:
        tmp = len(li.get(k))
        if tmp == 0:
            break
        else:
            li.delete(0, tmp)
        k += 1
        li.update()
    terminations = glob.glob(quarantine_folder)
    if terminations == []:
        text_box.insert(END, "[ + ] No files in quarantine\n", "positive")
        text_box.tag_config('positive', foreground="green")
        text_box.see(END)
        text_box.update()
    else:
        text_box.insert(END, "[ + ] Files in quarantine:\n", "positive")
        text_box.tag_config('positive', foreground="green")
        text_box.see(END)
        text_box.update()
        for i in terminations:
            text_box.insert(END, "[ * ] " + i + "\n", "info")
            text_box.tag_config("info", background = "red")
            text_box.see(END)
            text_box.update()
            li.insert(END, i)
            li.update()
    b_delete_all["command"] =lambda:button_action_handler("delete_all")
    b_delete["command"] = lambda:button_action_handler("delete")
    b_restore["command"] = lambda:button_action_handler("restore")
    b_restore_all["command"] = lambda:button_action_handler("restore_all")
    b_add_file["command"] = lambda:button_action_handler("add_file")

def delete(file, ALL):#ALL = 1 => deletes all objects in quarantine
    global li
    global text_box
    global terminations
    if len(terminations) != 0:
        if ALL == 1:
            for i in range(len(terminations)):
                os.remove(terminations[i])
                text_box.insert(END, "[ + ] Deletion successful: \n" + terminations[i] + "\n", "positive")
                text_box.tag_config("positive", foreground="green")
                text_box.see(END)
                text_box.update()
                li.delete(0, len(terminations[i]))
                li.update()
        elif ALL == 0:
            os.remove(file)
            li.delete(ACTIVE, len(file))
            li.update()
            text_box.insert(END, "[ + ] Deletion successful:\n" + file + "\n", "positive")
            text_box.tag_config("positive", foreground="green")
            text_box.see(END)
            text_box.update()
        terminations = glob.glob(quarantine_folder)
        for i in terminations:
            li.insert(END, i)
            li.update()
    else:
        text_box.insert(END, "[ - ] Unable to locate any files\n", "negative")
        text_box.tag_config("negative", foreground="red")
        text_box.see(END)
        text_box.update()

def restore(file, ALL):
    global li
    global text_box
    global terminations
    if len(terminations) != 0:
        if ALL == 1:
            for i in range(len(terminations)):
                file = terminations[i]
                result = quarantaene.anti_virus_backup_restore(file, 2)
                if result == -1:
                    text_box.insert(END, "[ - ] Restoration Unsuccessful: \n" + file + "\n", "negative")
                    text_box.tag_config("negative", foreground="red")
                    text_box.see(END)
                    text_box.update()
                else:
                    text_box.insert(END, "[ + ] Restoration Successful: \n" + file + "\n", "positive")
                    text_box.tag_config("positive", foreground="green")
                    text_box.see(END)
                    text_box.update()
                li.delete(0, len(terminations[i]))
                li.update()
        elif ALL == 0:
            result = quarantaene.anti_virus_backup_restore(file, 2)
            if result == -1:
                text_box.insert(END, "[ - ] Restoration Unsuccessful: \n" + file + "\n", "negative")
                text_box.tag_config("negative", foreground="red")
                text_box.see(END)
                text_box.update()
            else:
                text_box.insert(END, "[ + ] Restoration Successful: \n" + file + "\n", "positive")
                text_box.tag_config("positive", foreground="green")
                text_box.see(END)
                text_box.update()
            li.delete(ACTIVE, len(file))
            li.update()
        terminations = glob.glob(quarantine_folder)
        for i in terminations:
            li.insert(END, i)
            li.update()
    else:
        text_box.insert(END, "[ - ] Unable to locate any files\n", "negative")
        text_box.tag_config("negative", foreground="red")
        text_box.see(END)
        text_box.update()

def restore_all():
    global li
    global text_box
    global terminations
    if len(terminations) != 0:
        for i in range(len(terminations)):
            file = terminations[i]
            result = quarantaene.anti_virus_backup_restore(file, 2)
            if result == -1:
                text_box.insert(END, "[ - ] Restoration Unsuccessful: \n" + file + "\n", "negative")
                text_box.tag_config("negative", foreground="red")
                text_box.see(END)
                text_box.update()
            else:
                text_box.insert(END, "[ + ] Restoration Successful: \n" + file + "\n", "positive")
                text_box.tag_config("positive", foreground="green")
                text_box.see(END)
                text_box.update()
            li.delete(0, len(terminations[i]))
            li.update()
        terminations = glob.glob(quarantine_folder)
        for i in terminations:
            li.insert(END, i)
            li.update()
    else:
        text_box.insert(END, "[ - ] Unable to locate any files\n", "negative")
        text_box.tag_config("negative", foreground="red")
        text_box.see(END)
        text_box.update()

def add_file():
    global text_box
    global terminations
    global li
    files = filedialog.askopenfilenames()
    n = 0
    if files == "":
        return
    else:
        while True:
            if files[n] == "":
                break
            try:
                shutil.copy2(files[n], file_to_quarantine)
            except Exception as e:
                showerror("Error", e)
            if os.path.exists(file_to_quarantine + os.path.basename(files[n])):
                text_box.insert(END, "[ + ] Successfully added: \n" + file_to_quarantine + os.path.basename(files[n]) + "\n", "positive")
                text_box.tag_config("positive", foreground="green")
                text_box.see(END)
                text_box.update()
                li.insert(END, file_to_quarantine + os.path.basename(files[n]))
                li.update()
            else:
                text_box.insert(END, "[ - ] Error adding: \n" + file_to_quarantine + os.path.basename(files[n]) + "\n", "negative")
                text_box.tag_config("negative", foreground="red")
                text_box.see(END)
                text_box.update()
            n += 1

def update_antivirus():
    global text_box
    global fullscan_button
    global update_button
    update_button["state"] = DISABLED
    time.sleep(3)
    text_box.insert(END, "\n###### DOWNLOAD OF SIGNATURES HAS STARTED ######\n")
    if "win" in os_name:
        links = "https://raw.githubusercontent.com/XGHeaven/Antivirus-Project/master/AntiVirus/Large_Update_File/links_current.txt"
    else:
        links = "https://raw.githubusercontent.com/XGHeaven/Antivirus-Project/master/AntiVirus/Large_Update_File/links_current.txt"
    with urllib.request.urlopen(links) as response:
        txt = response.read()
    txt = str(txt).split(" ")
    tmp = ""
    for i in range(len(txt)):
        txt[i] = str(txt[i]).replace("b'", "")
        txt[i] = str(txt[i]).replace(",'", "")
        txt[i] = str(txt[i]).replace("'", "")
        tmp += txt[i]
    links = tmp.split("\\n")
    txt = ""
    for i in range(len(links)):
        txt += links[i] + "\n"
    links = txt.split("\n")
    if "win" in os_name:
        links_downloaded = "AntiVirus\\Large_Update_File\\links_downloaded.txt"
        with open(links_downloaded, "w") as file:
            file.write(str(txt))
        file.close()
    else:
        links_downloaded = "AntiVirus//Large_Update_File//links_downloaded.txt"
        with open(links_downloaded, "w") as file:
            file.write(str(txt))
        file.close()
    counter = 0
    for i in links:
        if len(i) == 0:
            continue
        counter += 1
    i = 0
    for i in range(len(links)):
        if len(links[i]) == 0:
            continue
        if "win" in os_name:
            local = "AntiVirus\\Large_Update_File\\"
            links[i] = str(links[i]).replace(" ", "")
            filename = str(links[i]).split("/")
            filename = filename[len(filename)-1]
            local = local + filename
        else:
            local = "AntiVirus//Large_Update_File//"
            links[i] = str(links[i]).replace(" ", "")
            filename = str(links[i]).split("/")
            filename = filename[len(filename)-1]
            local = local + filename
        links[i] = str(links[i]).replace(" ", "")
        text_box.insert(END, "\n###### File Download Started ######\n")
        text_box.see(END)
        text_box.update()
        try:
            urllib.request.urlretrieve(links[i], local)
        except Exception as e:
            showerror("Error", e)
            text_box.insert(END, "\n###### ERROR Downloading ######\n", "error")
            text_box.see(END)
            text_box.update()
        time.sleep(0.5)
        text_box.insert(END, "\n###### File Download Successful ######\n")
        text_box.see(END)
        text_box.update()
    text_box.insert(END, "\n###### ALL DOWNLOADS HAVE FINISHED ######\n")
    text_box.see(END)
    text_box.update()
    if "win" in os_name:
        large_signatures = "AntiVirus\\Large_Update_File\\signatures.txt"
    else:
        large_signatures = "AntiVirus//arge_Update_File//signatures.txt"
    with urllib.request.urlopen(large_signatures) as response:
        txt = response.read()
    if "win" in os_name:
        large_signatures = "AntiVirus\\Large_Update_File\\signatures.txt"
    else:
        large_signatures = "AntiVirus//arge_Update_File//signatures.txt"
    with open(large_signatures, "w") as file:
        file.write(str(txt))
    file.close()
    update_button["state"] = NORMAL
    fullscan_button["state"] = NORMAL

def button_action_handler(action):
    global li
    global b_delete
    global b_delete_all
    global b_restore
    global b_restore_all
    global b_add_file
    if action == "delete_all":
        delete("whatever", 1)
    if action == "delete":
        delete(li.get(ACTIVE), 0)
    if action == "restore_all":
        restore("whatever", 1)
    if action == "restore":
        restore(li.get(ACTIVE), 0)
    if action == "add_file":
        add_file()

def thread_method(method):
    global text_box
    global fullscan_button
    global lock
    global t_time
    lock.acquire()
    fullscan_button["state"] = DISABLED
    if method == 1:
        t_time = 30
        scan()
        text_box.see(END)
        text_box.update()
    elif method == 2:
        t_time = 60
        text_box.see(END)
        text_box.update()
        scan()
        full_scan()
        fullscan_button["state"] = NORMAL
        update_button["state"] = NORMAL
    else:
        t_time = 90
        fullscan_button["state"] = DISABLED
        text_box.insert(END, "\n###### FULL SYSTEM SCAN INITIALIZED ######\n")
        text_box.see(END)
        text_box.update()
        scan()
        full_scan()
        fullscan_button["state"] = NORMAL
        update_button["state"] = NORMAL
    fullscan_button["state"] = NORMAL
    lock.release()

def scan():
    global text_box
    global files
    global files_len
    global lock
    global t_time
    global update_button
    global scan_button
    global fullscan_button
    global quit_button
    global rb1
    global rb2
    global method
    text_box.delete(1.0, END)
    t_time = 0
    text_box.tag_config('info', foreground="black")
    text_box.tag_config('positiv', foreground="green")
    text_box.tag_config('medium', foreground="blue")
    text_box.tag_config('warning', foreground="orange")
    text_box.tag_config('negative', foreground="red")
    scan_button["state"] = NORMAL
    fullscan_button["state"] = NORMAL
    update_button["state"] = NORMAL
    quit_button["state"] = NORMAL
    rb1["state"] = NORMAL
    rb2["state"] = NORMAL
    method["state"] = NORMAL
    if files_len == 0:
        text_box.insert(END, "[ - ] No files in quarantine\n", "negative")
        text_box.tag_config('negative', foreground="red")
        text_box.see(END)
        text_box.update()
    else:
        text_box.insert(END, "[ + ] Files in quarantine:\n", "positiv")
        text_box.tag_config('positiv', foreground="green")
        text_box.see(END)
        text_box.update()
        for i in range(files_len):
            text_box.insert(END, "[ * ] " + files[i] + "\n", "info")
            text_box.tag_config('info', foreground="black")
            text_box.see(END)
            text_box.update()
        text_box.insert(END, "\n###### FULL SYSTEM SCAN INITIALIZED ######\n")
        text_box.see(END)
        text_box.update()
    lock.acquire()

def button_action():
    global fullscan_button
    global scan_button
    global update_button
    global rb1
    global rb2
    global method
    method = IntVar()
    rb1 = Radiobutton(main, text="Quick Scan", variable=method, value=1, command=lambda:thread_method(1))
    rb2 = Radiobutton(main, text="Medium Scan", variable=method, value=2, command=lambda:thread_method(2))
    rb3 = Radiobutton(main, text="Full Scan", variable=method, value=3, command=lambda:thread_method(3))
    update_button = Button(main, text="Update Antivirus", state=DISABLED, command=update_antivirus)
    scan_button = Button(main, text="Scan System", state=DISABLED, command=scan)
    fullscan_button = Button(main, text="Full System Scan", state=DISABLED, command=lambda:thread_method(3))
    quit_button = Button(main, text="QUIT", fg="red", command=main.quit)
    b_delete = Button(main, text="Delete from Quarantine", state=NORMAL, command=lambda:button_action_handler("delete"))
    b_delete_all = Button(main, text="Delete ALL from Quarantine", state=NORMAL, command=lambda:button_action_handler("delete_all"))
    b_restore = Button(main, text="Restore from Quarantine", state=NORMAL, command=lambda:button_action_handler("restore"))
    b_restore_all = Button(main, text="Restore ALL from Quarantine", state=NORMAL, command=lambda:button_action_handler("restore_all"))
    b_add_file = Button(main, text="Add file to quarantine", state=NORMAL, command=lambda:button_action_handler("add_file"))
    li = Listbox(main, bg=bgc, fg=fgc, selectbackground=special)
    li.insert(END, "Files in quarantine: ")
    li.config(selectmode=EXTENDED)
    li.config(height=3)
    li.config(width=0)
    li.config(listvariable=terminations)

    text_box = scrolledtext.ScrolledText(main, wrap=WORD, width=60, height=20, bg=bgc, fg=fgc)
    text_box.tag_config('info', foreground="black")
    text_box.tag_config('positive', foreground="green")
    text_box.tag_config('medium', foreground="blue")
    text_box.tag_config('warning', foreground="orange")
    text_box.tag_config('negative', foreground="red")
    text_box.tag_config('important', foreground="red")
    text_box.insert(END, special_text, "info")

    b_restore_all.grid(row=1, column=0)
    b_restore.grid(row=1, column=1)
    b_delete.grid(row=1, column=2)
    b_delete_all.grid(row=1, column=3)
    b_add_file.grid(row=1, column=4)
    li.grid(row=0, column=0, columnspan=10)
    text_box.grid(row=3, column=0, columnspan=10)
    rb1.grid(row=2, column=1)
    rb2.grid(row=2, column=2)
    rb3.grid(row=2, column=3)
    update_button.grid(row=2, column=4)
    scan_button.grid(row=2, column=5)
    fullscan_button.grid(row=2, column=6)
    quit_button.grid(row=2, column=7)

    update_button.config(height=1, width=15)
    scan_button.config(height=1, width=15)
    fullscan_button.config(height=1, width=15)
    quit_button.config(height=1, width=15)
    b_delete.config(height=1, width=15)
    b_delete_all.config(height=1, width=15)
    b_restore.config(height=1, width=15)
    b_restore_all.config(height=1, width=15)
    b_add_file.config(height=1, width=15)

    method.set(1)

    text_box.see(END)
    text_box.update()
    return (text_box, li)

class SystemFileScanner:

    @staticmethod
    def partitions(file):
        partitions = subprocess.getoutput("wmic logicaldisk get caption")
        f = open(file, "w")
        f.write(partitions)
        f.close()

def main_method():
    global main
    global lock
    global t_time
    global text_box
    global li
    global rb1
    global rb2
    global method
    global update_button
    global scan_button
    global fullscan_button
    global quit_button
    text_box, li = button_action()
    lock = threading.Lock()
    lock.acquire()
    update_button["state"] = DISABLED
    main.mainloop()

def start_threaded():
    main_thread = threading.Thread(target=main_method)
    clock = threading.Thread(target=clock_thread)
    clock.start()
    main_thread.start()

if __name__ == "__main__":
    start_threaded()

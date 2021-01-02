"""
In this version I'm using:
{
    "last_exec": 1609623191.449078, 
    "ran": true, 
    "queue": ["file(1).pdf", "file(2).pdf"]
}


but dont need "ran" and can use if "queue" empty to get same/better results

"""

import os
import time
#import shutil      # File copy and move stuff
import json
from datetime import datetime

#all_printers = win32print.EnumPrinters(2)

pdf_dir = "C:\\Users\\Tom\\Desktop\\drive-download-20201231T010209Z-001"
archive_dir = "C:\\HOTFOLDER_DRUCK\\ARCHIV\\"
problem = "C:\\HOTFOLDER_DRUCK\\PROBLEMJOBS\\"
schedule_file = "C:\\hotfolder_schedule.json"
delay = 2*60   # in seconds * 60 (minutes...duh)

def fileList():
    files = []
    filesInFolder = sorted(os.listdir(pdf_dir))
    for f in filesInFolder:
        if f[-4:] == ".pdf":
            files.append(f)
    return files

def checkForNewFiles():
    queue = readQueue()     # Have to rasterize these as variables or else they calculated x ( x = no. of files ) times
    newList = fileList()    # in the function below (Exponentially for no reason)
    return not all(item in queue for item in newList)    # https://www.techbeamers.com/program-python-list-contains-elements/#all-method

def getLogTime():
    now = datetime.now()
    t = now.strftime("%Y-%m-%d_%H%M")
    return t

def moveFile(f):
    while f in os.listdir(pdf_dir):
        try:              
            time.sleep(3)
            print(getLogTime() + " REMOVING "+f+" FROM INPUT FOLDER!")
            os.remove(os.path.join(pdf_dir,f))
        except Exception as e:
            print(e)
            time.sleep(5)
    return None

"""
scheduleAhead accepts x which is an array of files in the folder that will now be the queue.

Right now this ignores any extra files which were in the queue that no longer exist in the folder and justs queues up what's there currently without informing or logging

"""
def scheduleAhead(x):
    json_data = {"last_exec": 0, "ran": 0, "queue": []}
    try:
        with open(schedule_file, "r") as jsn:
            json_data = json.load(jsn)
        json_data["last_exec"] = time.time()
        json_data["queue"] = x
        json_data["ran"] = False
    except IOError:
        print("No schedule file found, creating one...")
    except:
        raise SystemExit('Something is wrong with the schedule ahead JSON file, possibly the format. Script cannot run. \nHINT: You can delete the queue file and start a fresh.')
    with open(schedule_file, 'w') as jsn:
        json.dump(json_data, jsn)

def readQueue():
    try:
        with open(schedule_file, "r") as jsn:
            json_data = json.load(jsn)
        return json_data["queue"]
    except:
        raise SystemExit('Something is wrong with the schedule ahead JSON file, possibly the format. Script cannot run. \nHINT: You can delete the queue file and start a fresh.')

def checkScheduleCanRun():
    try:
        with open(schedule_file, "r") as jsn:
            json_data = json.load(jsn)
        if not json_data["ran"]:   # 1-liners are boring so traditional if else
            return ( time.time() - json_data["last_exec"] ) > delay   # okay maybe not that boring
        else:
            return False
    except:
        raise SystemExit('Something is wrong with the schedule ahead JSON file, possibly the format. Script cannot run. \nHINT: You can delete the queue file and start a fresh.')

def startPrinting():
    print("thullu mera")

def main():
    if checkForNewFiles():
        scheduleAhead(fileList())
    if checkScheduleCanRun():
        startPrinting()

main()
a=checkScheduleCanRun()
print(a)


# while False:
#     time.sleep(10) # 10 sec intervals... not needed but 
#     files = checkForNewFiles()
#     time.time()
#     if len(files) > 0:
#         time.sleep(6) # WARTEN BIS SWITCH DEN PREFIX ENTFERNT HAT 
#         files = checkForNewFiles() # ANSCHLIESSEND ORDNER NEU EINLESEN
#         for f in files:
#             pattern = re.compile('\_([a-zA-Z0-9\s\-]+)\.pdf')
#             match = pattern.search(f)
#             try:
#                 printer = match.group(1)
#                 defaultPrinter = win32print.GetDefaultPrinter()
#                 if defaultPrinter != printer:
#                     win32print.SetDefaultPrinter(printer)
#                 print getActualTime()+" PRINTING FILE "+ f +" on "+printer
#                 win32api.ShellExecute(0,"print", os.path.join(pdf_dir,f), None,  ".",  0)
#                 print getActualTime()+" COPY "+f+" to ARCHIVE!"
#                 shutil.copy(os.path.join(pdf_dir,f),os.path.join(archive_dir,f))
#                 deleteFile(f)
#                 print getActualTime()+" FILE "+f+" SUCCESSFULLY PRINTED!"
#             except Exception as e:
#                 print e
#                 shutil.copy(os.path.join(pdf_dir,f),os.path.join(problem,f))
#                 deleteFile(f)

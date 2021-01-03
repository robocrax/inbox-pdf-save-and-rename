import os
import time
import sys
#import shutil      # File copy and move stuff.. not yet ready
import json
import win32print
from datetime import datetime

#all_printers = win32print.EnumPrinters(2)

pdf_dir = "C:\\Users\\Tom\\Desktop\\"
archive_dir = "C:\\HOTFOLDER_DRUCK\\ARCHIV\\"
# problem = "C:\\HOTFOLDER_DRUCK\\PROBLEMJOBS\\"       # Not implemented yet
queue_file = "C:\\hotfolder_queue.json"    # Just a temp file
delay = 2*60   # in seconds * 60 (minutes...duh)
force_printer = "Upstairs"

def fileList(x):
    files = []
    filesInFolder = sorted(os.listdir(x))
    for f in filesInFolder:
        if f[-4:] == ".pdf":
            files.append(f)
    return files

def checkForNewFiles(x):
    return not (queue() == fileList(x))

def getLogTime():
    now = datetime.now()
    t = now.strftime("%Y-%m-%d_%H%M")
    return t

def moveFile(f):
    while f in os.listdir(x):
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

Right now this ignores any extra files which were in the queue that no longer exist in the folder and just overrides queue with what's there currently, also without informing or logging

"""
def scheduleAhead(x):
    json_data = {"last_detect": 0, "queue": []}
    try:
        with open(queue_file, "r") as jsn:
            json_data = json.load(jsn)
        json_data["last_detect"] = time.time()
        json_data["queue"] = x
    except IOError:
        print("Generating schedule file...")
    except:
        raise SystemExit('Something is wrong with the schedule ahead JSON file, possibly the format. Script cannot run. \nHINT: You can delete the queue file and start a fresh.')
    with open(queue_file, 'w') as jsn:
        json.dump(json_data, jsn)

def jsonFileFix():
    try:
        sys.argv[1]
    except IndexError:   # Not sure if I should also catch NameError
        pass
    else:
        if sys.argv[1] == "reset":
            try:
                os.remove(queue_file)
                raise SystemExit('Schedule reset!')
            except FileNotFoundError:   # This can never be caught unless function called directly 
                raise SystemExit('No schedule file detected. No reset required.')
            #return True
        else:
            pass
    raise SystemExit('Damaged schedule JSON file, possibly the format. Script cannot run. \nHINT: You can run the following to start a fresh.\n\n          `'+sys.argv[0]+' reset`')

def queue():
    try:
        with open(queue_file, "r") as jsn:
            json_data = json.load(jsn)
        return json_data["queue"]
    except IOError:
        scheduleAhead([])
        return []
    except:
        print(jsonFileFix())

def canRunSchedule():
    try:
        with open(queue_file, "r") as jsn:
            json_data = json.load(jsn)
        if len(json_data["queue"])>0:    # 1-liners are boring so traditional if else
            return ( time.time() - json_data["last_detect"] ) > delay   # okay maybe not that boring
        else:
            return False
    except:
        print(jsonFileFix())

def dropFromQueue(x):
    try:
        with open(queue_file, "r") as jsn:
            json_data = json.load(jsn)
        json_data["queue"].remove(x)
        with open(queue_file, 'w') as jsn:
            json.dump(json_data, jsn)
    except:
        print(jsonFileFix())

def viewAllPrinters():
    printers = win32print.EnumPrinters(2)
    default_printer = win32print.GetDefaultPrinter()
    for printer in printers:
        if printer[2] == default_printer:
            print(printer[2] + " <== Default")
        else:
            print(printer[2])
    exit()

def startPrinting(x):
    if force_printer:
        try:
            if win32print.GetDefaultPrinter() != force_printer:
                win32print.SetDefaultPrinter(force_printer)
        except:
            print('\nCannot set your printer as default. Please see list below and choose one.')
            viewAllPrinters()
    for file in x:
        print('Processed '+file)
        dropFromQueue(file)

def main():
    if checkForNewFiles(pdf_dir):
        scheduleAhead(fileList(pdf_dir))
    if canRunSchedule():
        startPrinting(queue())

if __name__ == "__main__":
    try:
        sys.argv[1]
    except IndexError:   # Not sure if I should also catch NameError
        pass
    else:
        if sys.argv[1] == "view_printers":
            viewAllPrinters()
        elif sys.argv[1] == "reset":
            print('NOTE: This is an optional command and only resets if needed or else program will continue normally.')
    print('Watching '+pdf_dir)
    while True:
        try:
            time.sleep(1)
            main()
        except KeyboardInterrupt:
            exit('\nNo longer watching... Adios!')

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

#!/bin/env python3

import os
import re
import winreg
import sys
import shutil
from datetime import date

before1 = date.today()
after1 = date.today()

def printhelp():
	print('This is the automated log file zipper created by Rubik. \n Zip file will be located at the program directory.\nFor date specific runs, dates need to be typed in this format: \nyyyy-mm-dd, 4 digit year, 2 digit month, 2 digit day. \nFor questions or comments, please Rubik on discord or in Neos. \nUsage:\nFor today\'s logs zipped, run NeosLogs.cmd\nFor all logs to be zipped, run NeosLogs.cmd all\nFor logs after a certain date, run NeosLogs.cmd <date>\nFor logs between two dates, run NeosLogs.cmd <date1> <date2>')
	sys.exit(1)
if len(sys.argv) >= 3:
	try:
		before1 = date(int(sys.argv[2][0:4]), int(sys.argv[2][5:7]), int(sys.argv[2][8:10]))
		print('argv 3')
	except IndexError:
		printhelp()
	except TypeError:
		printhelp()
	except ValueError:
		if sys.argv[2] != 'all':
			printhelp()
		before1 = date(2000,1,1)	
elif len(sys.argv) >= 4:
	try:
		after1 = date(int(sys.argv[3][0:4]), int(sys.argv[3][5:7]), int(sys.argv[3][8:10]))
	except IndexError:
		pass
elif len(sys.argv) == 2:
	print('This is the automated log file zipper created by Rubik. \n Zip file will be located at the program directory.\nFor date specific runs, dates need to be typed in this format: \nyyyy-mm-dd, 4 digit year, 2 digit month, 2 digit day. \nFor questions or comments, please Rubik on discord or in Neos. \nUsage:\nFor today\'s logs zipped, run NeosLogs.cmd\nFor all logs to be zipped, run NeosLogs.cmd all\nFor logs after a certain date, run NeosLogs.cmd <date>\nFor logs between two dates, run NeosLogs.cmd <date1> <date2>\n\nProgram will continue.')
	
before = min(before1, after1)
after = max(before1, after1)

try:
	key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\Valve\\Steams")
except FileNotFoundError:
    try: # 64-bit
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\Wow6432Node\\Valve\\Steam")
    except FileNotFoundError as e:
        print("Failed to find Steam Install directory")
        raise(e)
STEAM_PATH = winreg.QueryValueEx(key, "InstallPath")[0]
_STEAM_KEY = "91597DC019EB19394E3A1E4EB010F025"

def get_libraries():
    """ 
    Get a list of paths to all Steam Libraries from
    Steam\\steamapps\\libraryfolders.vdf

    :returns: a list of file paths
    """
    libraries = [STEAM_PATH]
    with open(f"{STEAM_PATH}\\steamapps\\libraryfolders.vdf", 'r', encoding="utf8") as f:
        lf = f.read()
        libraries.extend([fn.replace("\\\\", "\\") for fn in
            re.findall(r'^\s*"\d*"\s*"([^"]*)"', lf, re.MULTILINE)])
    return libraries

def find_neos():
	SteamDirs = get_libraries()
	for loc in SteamDirs:
		if os.path.isdir(os.path.abspath(f"{loc}\\steamapps\\common\\NeosVR")):
			return os.path.abspath(f"{loc}\\steamapps\\common\\NeosVR\\Logs")	
	return -1

NEOS_PATH = find_neos()

if NEOS_PATH == -1:
	print("Error: Neos not installed through Steam.")
	sys.exit(1)

#os.mkdir("temp")

ZIP_PATH = f"Neos {date.today().year}-{date.today().month}-{date.today().day}.zip"

UNITY_PATH = os.path.abspath(f"{sys.argv[1]}\\..\\LocalLow\\Solirax\\NeosVR\\")

CRASH_PATH = os.path.abspath(f"{sys.argv[1]}\\..\\Local\\Temp\\Solirax\\NeosVR\\Crashes\\")

HEADLESS_PATH = os.path.abspath(f"{NEOS_PATH}\\..\\HeadlessClient\\Logs")

TEMP_PATH = "temp"

try:
	os.mkdir(TEMP_PATH)
except WindowsError:
	pass

for loc in os.listdir(NEOS_PATH):
	data = loc.split(" ")
	z = date(1900,1,1)
	if len(data) == 2: # old format
		q = data[1].split('_')
		z = date(int(q[2]),int(q[0]),int(q[1]))
		#print("neos 2")
	elif len(data) == 3: #new format
		q = data[1].split('-')
		z = date(int(q[0]), int(q[1]), int(q[2]))
		#print("neos 3")
	#print(f"{before} {z} {after}")
	if z >= before and z <= after:
		#print(f"shutil.copyfile({os.path.join(NEOS_PATH, loc)}, {os.path.join(TEMP_PATH, loc)})")
		try:
			shutil.copyfile(os.path.join(NEOS_PATH, loc), os.path.join(TEMP_PATH, loc))
		except FileExistsError:
			pass

try:
	for loc in os.listdir(HEADLESS_PATH):
		data = loc.split(" ")
		z = date(1900,1,1)
		if len(data) == 2: # old format
			q = data[1].split('_')
			z = date(int(q[2]),int(q[0]),int(q[1]))
		elif len(data) == 3: #new format
			q = data[1].split('-')
			z = date(int(q[0]), int(q[1]), int(q[2]))
		if z >= before and z <= after:
			try:
				shutil.copyfile(os.path.join(HEADLESS_PATH, loc), os.path.join(TEMP_PATH, f"{loc.split(' ')[0]}_HEADLESS {loc.split(' ')[1]}"))
			except FileExistsError:
				pass
except FileNotFoundError:
	pass

try:
	shutil.copyfile(os.path.join(UNITY_PATH, 'Player.log'), os.path.join(TEMP_PATH, 'Player.log'))
except WindowsError:
	pass

try:
	shutil.copyfile(os.path.join(UNITY_PATH, 'Player-prev.log'), os.path.join(TEMP_PATH, 'Player-prev.log'))
except WindowsError:
	pass
try:
	for loc in os.listdir(CRASH_PATH):
		data = loc.split('_')
		q = data[1].split('-')
		z = date(int(q[0]), int(q[1]), int(q[2]))
		if z >= before and z <= after:
			try:
				shutil.copytree(os.path.join(CRASH_PATH, loc), os.path.join(TEMP_PATH, loc))
			except FileExistsError:
				pass
except FileNotFoundError:
	pass
	
shutil.make_archive(f"Logs {str(date.today())}", 'zip', TEMP_PATH)
shutil.rmtree(TEMP_PATH)

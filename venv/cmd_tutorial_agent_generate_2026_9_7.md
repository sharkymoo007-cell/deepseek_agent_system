# Windows CMD (Command Prompt) Tutorial

A practical guide to the most common commands used in the Windows Command Prompt (`cmd.exe`).

> **How to open CMD:** Press `Win + R`, type `cmd`, and press `Enter`.
> Run any command with `command /?` (e.g. `dir /?`) to view its full help and options.

---

## Table of Contents

1. [Getting Help](#1-getting-help)
2. [Navigation & Directory Commands](#2-navigation--directory-commands)
3. [File & Folder Management](#3-file--folder-management)
4. [Viewing & Editing Files](#4-viewing--editing-files)
5. [System & Hardware Info](#5-system--hardware-info)
6. [Network Commands](#6-network-commands)
7. [Process & Task Management](#7-process--task-management)
8. [Environment Variables](#8-environment-variables)
9. [Useful Utilities](#9-useful-utilities)
10. [CMD Syntax Essentials](#10-cmd-syntax-essentials)
11. [Simple Batch Script Examples](#11-simple-batch-script-examples)

---

## 1. Getting Help

```cmd
help                  Displays a list of all available commands
help <command>        Shows help for a specific command (e.g., help dir)
<command> /?          Same as help, works with most commands (e.g., dir /?)
```

---

## 2. Navigation & Directory Commands

```cmd
dir                   Lists files and folders in the current directory
dir /w                Wide list format
dir /p                Pause after each screen
dir /a                Show all files including hidden ones
dir C:\Users          List contents of a specific folder

cd                    Show the current directory path (print working directory)
cd ..                 Go up one folder level
cd \                  Go to the root of the current drive
cd C:\Users\Name      Change to a specific directory
cd /d D:\Projects     Change drive AND folder at once (the /d switch)

cls                   Clear the screen
```

---

## 3. File & Folder Management

```cmd
mkdir <name>          Create a folder            (alias: md)
mkdir a\b\c           Create nested folders at once
rmdir <name>          Remove an empty folder     (alias: rd)
rmdir /s <name>       Remove folder and all contents (be careful!)
rmdir /s /q <name>    Force-remove without asking for confirmation

del <file>            Delete a file              (alias: erase)
del *.tmp             Delete files by wildcard
del /s *.log          Delete matching files in current folder and subfolders
del /f <file>         Force-delete a read-only file

copy <src> <dst>      Copy a file
copy file.txt C:\backup\
copy /y a.txt b.txt   Overwrite destination without prompting

xcopy src dst /e      Copy folders including empty subfolders
xcopy src dst /i      Assume destination is a folder
robocopy src dst /e   More powerful copy tool (folder mirroring)

move <src> <dst>      Move or rename a file/folder
rename <old> <new>    Rename a file              (alias: ren)
```

---

## 4. Viewing & Editing Files

```cmd
type <file>           Print the whole contents of a text file to the screen
type file.txt | more  View long files page by page
more <file>           Same as above

find "text" file.txt          Search for text inside a file
findstr "text" file.txt       More powerful text search (supports regex)
findstr /s /i "text" *.txt    Recursive + case-insensitive search

fc file1.txt file2.txt        Compare two files and show the differences
tree                        Display the folder structure as a tree
tree /f                     Include files in the tree view
```

---

## 5. System & Hardware Info

```cmd
systeminfo            Full system information (OS, RAM, manufacturer, etc.)
systeminfo | find "OS Name"     Filter for a single line

ver                   Show the Windows version
whoami                Show the current username
hostname              Show the computer name
date                  Show/set the date
time                  Show/set the time

chkdsk                Check disk for errors (may require admin)
chkdsk C: /f          Fix errors on drive C:
```

---

## 6. Network Commands

```cmd
ipconfig              Show IP configuration of all adapters
ipconfig /all         Detailed info (MAC address, DHCP, DNS, etc.)
ipconfig /release     Release the current DHCP lease
ipconfig /renew       Request a new IP address from DHCP
ipconfig /flushdns    Clear the DNS cache

ping <host>           Test connectivity to a host (e.g., ping google.com)
ping -t <host>        Ping continuously until stopped with Ctrl+C
ping -n 10 <host>     Ping 10 times

tracert <host>        Trace the route packets take to a host
pathping <host>       Combination of ping + tracert with loss statistics
nslookup <domain>     Look up DNS records for a domain
netstat -a            Show all active connections and listening ports
netstat -n            Show addresses/ports in numeric form
netstat -o            Show the owning Process ID (PID) of each connection

getmac                Display the MAC address of the network adapters
arp -a                Show the ARP table (IP-to-MAC mappings)
```

---

## 7. Process & Task Management

```cmd
tasklist              List all running processes
tasklist | find "chrome"    Find a specific process

taskkill /IM chrome.exe         Kill all processes named chrome.exe
taskkill /PID 1234              Kill a process by its Process ID
taskkill /PID 1234 /F           Force-kill a process
```

---

## 8. Environment Variables

```cmd
set                   Show all environment variables
set PATH              Show the value of one variable
set MYVAR=hello       Create/set a variable for this session only
set MYVAR=            Clear a variable

echo %PATH%           Display the PATH variable's value
echo %USERNAME%       Show current username
echo %DATE% %TIME%    Show current date and time

setx MYVAR value      Permanently set a variable (persists across sessions)
setx PATH "%PATH%;C:\NewFolder"   Append a folder to PATH permanently
```

---

## 9. Useful Utilities

```cmd
echo Hello            Print text to the screen
echo.                 Print an empty line

start notepad         Launch a program / open a file with its default app
start .               Open the current folder in File Explorer

shutdown /s          Shut down the computer
shutdown /r          Restart the computer
shutdown /r /t 60    Restart after a 60-second delay
shutdown /a          Abort a scheduled shutdown

where <program>       Locate where an executable is installed (e.g., where python)
where /r C:\ file.txt     Search recursively for a file

attrib                Show file attributes (read-only, hidden, etc.)
attrib +h file.txt    Hide a file
attrib -h file.txt    Unhide a file

sort < file.txt       Sort lines of a file
vol                   Show volume label and serial number of a drive
exit                  Close the Command Prompt window
```

---

## 10. CMD Syntax Essentials

### Command chaining

```cmd
command1 & command2      Run command2 after command1 finishes (always)
command1 && command2     Run command2 ONLY if command1 succeeded
command1 || command2     Run command2 ONLY if command1 failed
```

### Redirection (input/output)

```cmd
dir > list.txt           Send output to a file (overwrites it)
dir >> list.txt          Append output to the end of a file
command 2> errors.txt    Redirect error messages to a file
command < input.txt      Read input from a file
dir | find "txt"         Pipe: send output of one command into another
```

### Wildcards

```cmd
*    Matches any number of characters  (e.g., *.txt, report*, *2024*)
?    Matches exactly one character     (e.g., file?.doc)
```

### Useful keyboard shortcuts in CMD

| Shortcut          | Action                                   |
|-------------------|------------------------------------------|
| `↑` / `↓`         | Recall previous / next command           |
| `Tab`             | Auto-complete file/folder names          |
| `Ctrl + C`        | Stop the running command                 |
| `Ctrl + A`        | Select all text on the line              |
| `F7`              | Show command history in a selectable list|
| `Right-click`     | Paste text (when QuickEdit is enabled)   |
| `Alt + Enter`     | Toggle full screen                       |

---

## 11. Simple Batch Script Examples

Save any of these with a `.bat` or `.cmd` extension and double-click to run.

### Example 1: Hello world script

```bat
@echo off
echo Hello, World!
echo This is my first batch script.
pause
```

### Example 2: Backup a folder

```bat
@echo off
echo Copying files from Documents to backup folder...
xcopy "%USERPROFILE%\Documents" "D:\Backup\Documents" /e /i /y
echo Backup completed.
pause
```

### Example 3: Loop over files and show sizes

```bat
@echo off
echo Files in current folder:
for %%f in (*.*) do echo %%f - %%~zf bytes
pause
```

### Example 4: If/else example

```bat
@echo off
if exist "C:\Windows" (
    echo Windows folder found.
) else (
    echo Windows folder NOT found.
)
pause
```

---

## Quick Reference Cheat Sheet

| Task                        | Command                          |
|-----------------------------|----------------------------------|
| List files                  | `dir`                            |
| Change directory            | `cd path`                        |
| Clear screen                | `cls`                            |
| Create folder               | `mkdir name`                     |
| Delete folder (with files)  | `rmdir /s /q name`               |
| Delete file                 | `del file.txt`                   |
| Copy file/folder            | `copy` / `xcopy` / `robocopy`    |
| Move/rename                 | `move` / `ren`                   |
| View file contents          | `type file.txt`                  |
| IP configuration            | `ipconfig`                       |
| Test connection             | `ping host`                      |
| Trace route                 | `tracert host`                   |
| Show processes              | `tasklist`                       |
| Kill process                | `taskkill /IM name.exe /F`       |
| System info                 | `systeminfo`                     |
| Show variables              | `set`                            |
| Restart PC                  | `shutdown /r`                    |
| Help                        | `help` or `command /?`           |

---

*Tip: press `command /?` for details about any command — every built-in command has a built-in manual.*

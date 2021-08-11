See UNLICENSE.txt.

Should you want to upload your edits, use compile.bat.
It outputs two folders, one containing a copy of the Python 3 source
code, another containing an .exe file. These can then be compressed into 
.zip files, for easy upload to DFFD or mirrors.

compile.bat requires pyinstaller to create the .exe file. It can be found here:
https://www.pyinstaller.org/ or downloaded using pip; "pip install pyinstaller".
compile.bat was made in/for Windows 10, but I reckon it could be
UNIX-compatible, considering how basic the commands are (but you still need
pyinstaller for whatever non-windows machine you're running, then).
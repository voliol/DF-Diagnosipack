@echo off
Rem This is a batch file, which "compiles" DF Diagnosipack into one folder for the python version, and one folder for the exe version.
Rem !!!Remember to change the version number before!!! (using ctrl-h or whatever)

@echo on
@echo Creating folders, copying files...
@echo off

Rem creates a "temp_settings.txt"
Rem it will later be copied over each folder and renamed
Rem if you've added a new setting in the source code, remember to add it to here
@echo on
@echo Raw folder path: [HERE]/raw/objects > temp_settings.txt
@echo Create .txt file output: True	>> temp_settings.txt
@echo Output folder path: [HERE]		>> temp_settings.txt
@echo Use "name mode" on DF Duplisearch: True >> temp_settings.txt
@echo DF Creaturescale gives very detailed output: True >> temp_settings.txt
@echo Format output of DF Biomeviewer for mediawiki: True >> temp_settings.txt
@echo off

Rem creates the folders
md v1.2
md v1.2\DF_Diagnosipack_1.2

Rem copies over most files (including this one)
copy df_diagnosipack.py v1.2\DF_Diagnosipack_1.2
copy df_diagnosipack_base.py v1.2\DF_Diagnosipack_1.2

copy df_creatureclasser.py v1.2\DF_Diagnosipack_1.2
copy df_creaturescale.py v1.2\DF_Diagnosipack_1.2
copy df_cvunpack.py v1.2\DF_Diagnosipack_1.2
copy df_duplisearch.py v1.2\DF_Diagnosipack_1.2
copy df_biomeviewer.py v1.2\DF_Diagnosipack_1.2

copy verticalscrolledframe.py v1.2\DF_Diagnosipack_1.2

copy icon.ico v1.2\DF_Diagnosipack_1.2
copy logo.png v1.2\DF_Diagnosipack_1.2

copy changelog.txt v1.2\DF_Diagnosipack_1.2
copy temp_settings.txt v1.2\DF_Diagnosipack_1.2

copy UNLICENSE.txt v1.2\DF_Diagnosipack_1.2
copy readme_compile.txt v1.2\DF_Diagnosipack_1.2
copy compile.bat v1.2\DF_Diagnosipack_1.2

Rem creates new (empty) file for errorlog
type NUL > v1.2\DF_Diagnosipack_1.2\df_diagnosipack_errorlog.txt
Rem renames temp_settings.txt
ren v1.2\DF_Diagnosipack_1.2\temp_settings.txt df_diagnosipack_settings.txt

Rem runs pyinstaller to create the exe version
@echo on
pyinstaller -i icon.ico -F df_diagnosipack.py 
@echo Moving more files...
@echo off

Rem moves the dist folder, renames it, and copies over the needed files
move dist v1.2\DF_Diagnosipack_exe_1.2

copy icon.ico v1.2\DF_Diagnosipack_exe_1.2
copy logo.png v1.2\DF_Diagnosipack_exe_1.2
copy changelog.txt v1.2\DF_Diagnosipack_exe_1.2
copy temp_settings.txt v1.2\DF_Diagnosipack_exe_1.2
copy UNLICENSE.txt v1.2\DF_Diagnosipack_exe_1.2

type NUL > v1.2\DF_Diagnosipack_exe_1.2\df_diagnosipack_errorlog.txt
ren v1.2\DF_Diagnosipack_exe_1.2\temp_settings.txt df_diagnosipack_settings.txt

Rem cleans up
@echo on
@echo Cleaning up...
@echo off
del temp_settings.txt
del df_diagnosipack.spec
@echo on
@echo Remove
rd /s build

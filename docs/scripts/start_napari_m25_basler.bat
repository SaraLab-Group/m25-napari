@echo off

@REM Turn on the cameras
cd "C:\Program Files (x86)\Windows Kits\10\Tools\x64"
call devcon.exe enable =PylonUSB
call conda activate napari-pymmcore
call napari -w m25-napari

@REM Shut down the cameras
cd "C:\Program Files (x86)\Windows Kits\10\Tools\x64"
call devcon.exe enable =PylonUSB

pause
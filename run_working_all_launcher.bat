@echo off
echo Starting working_all.py...
echo %TIME% > "C:\gh\oomlout_base\lock\working_all.lock"
cd /d "C:\gh\oomlout_base\templates\oomp_project_base"
python working_all.py
python working_all.py
del "C:\gh\oomlout_base\lock\working_all.lock"
echo Done!
pause

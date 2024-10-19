@echo off

set TASK_NAME=WPSS

REM Remove the scheduled task
schtasks /delete /tn %TASK_NAME% /f

pause
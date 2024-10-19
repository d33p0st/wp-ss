@echo off

REM Define the task name and the command to run (in the background)
set TASK_NAME=WPSS
set COMMAND=wpss

REM Create a scheduled task to run the command at every startup
schtasks /create /tn %TASK_NAME% /tr %COMMAND% /sc onlogon /rl highest /f

REM Confirm task creation
if %errorlevel%==0 (
    echo Task created successfully to run on each startup.
) else (
    echo Failed to schedule task.
)

pause
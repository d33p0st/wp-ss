@echo off

REM Check if the command with arguments is provided
if "%*"=="" (
    echo Error: No command provided.
    echo Usage: schedule.bat "command with arguments"
    exit /b 1
)

REM Define the task name and the command to run (in the background)
set TASK_NAME=WPSS

REM Create a scheduled task to run the command at every startup
schtasks /create /tn %TASK_NAME% /tr "%*" /sc onlogon /rl highest /f

REM Confirm task creation
if %errorlevel%==0 (
    echo Task created successfully to run on each startup.
) else (
    echo Failed to schedule task.
)

pause
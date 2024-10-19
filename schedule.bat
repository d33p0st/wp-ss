@echo off

@REM REM Check if the command with arguments is provided
@REM if "%~1"=="" (
@REM     echo Error: No command provided.
@REM     echo Usage: schedule.bat "command with arguments"
@REM     exit /b 1
@REM )

REM Define the task name and the command to run (in the background)
set TASK_NAME=WPSS

REM Combine all arguments into a single command string
setlocal enabledelayedexpansion
set "COMMAND="
for %%I in (%*) do (
    set "COMMAND=!COMMAND! %%I"
)
endlocal & set "COMMAND=%COMMAND:~1%"

REM Create a scheduled task to run the command at every startup
schtasks /create /tn %TASK_NAME% /tr "powershell -WindowStyle Hidden -Command ^\"Start-Process '%COMMAND%' -WindowStyle Hidden^\"" /sc onlogon /rl highest /f

REM Confirm task creation
if %errorlevel%==0 (
    echo Task created successfully to run on each startup.
) else (
    echo Failed to schedule task.
)

pause
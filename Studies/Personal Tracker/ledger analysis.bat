@echo off
set "RESPONSE="
set "NDAYS="
goto 'input'

: 'input'
set /p ndays=Enter the aggregation interval: 
set /p response=Do you want to edit the excel? (y/n): 
if /I %response%==y goto 'edit_excel'
goto 'run_script'


: 'edit_excel'
start /wait excel "E:\GitDevelop\Studies\Personal Tracker\DailyLedger.xlsx"

: 'run_script'
python "E:\GitDevelop\Studies\Personal Tracker\ledger_analysis.py" %ndays%
:: Set the root directory--we do this because we want to use Anaconda prompt instead of the default command prompt
set root=C:\ProgramData\Anaconda3

:: Call Anaconda Prompt
call %root%\Scripts\activate.bat %root%

:: Change directory to the precheck files
cd C:\BI_WH_Solution\BI_WH_Solution\Zack_Python_Code\UKG\Reports as a service\Labor distribution

:: Call a labor distribution program
call python EarningsByCode.py

:: Pause for 10 seconds to avoid issues connecting to the API too fast
timeout /T 10 /nobreak

:: Call a labor distribution program
call python employee_allocation.py

:: Pause for 10 seconds to avoid issues connecting to the API too fast
timeout /T 10 /nobreak

:: Call a labor distribution program
call python employee-list.py

:: Pause for 10 seconds to avoid issues connecting to the API too fast
timeout /T 10 /nobreak

:: Call a labor distribution program
call python location_address.py

:: Pause for 10 seconds to avoid issues connecting to the API too fast
timeout /T 10 /nobreak

:: Call a labor distribution program
call python locations.py

:: Pause for 10 seconds to avoid issues connecting to the API too fast
timeout /T 10 /nobreak

:: Call a labor distribution program
call python organizational_levels.py

:: Pause for 10 seconds to avoid issues connecting to the API too fast
timeout /T 10 /nobreak

:: Call a labor distribution program
call python pay_period.py


echo The program is finished

pause
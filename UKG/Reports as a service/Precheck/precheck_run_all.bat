:: Set the root directory--we do this because we want to use Anaconda prompt instead of the default command prompt

set root=C:\ProgramData\Anaconda3



:: Call Anaconda Prompt

call %root%\Scripts\activate.bat %root%



:: Change directory to the precheck files

cd C:\BI_WH_Solution\BI_WH_Solution\Zack_Python_Code\UKG\Reports as a service\Precheck

:: Call a precheck program

call python employee-list.py



:: Pause for 10 seconds to avoid issues connecting to the API too fast

timeout /T 10 /nobreak



:: Call a precheck program

call python precheck-deduction-v2.py



:: Pause for 10 seconds to avoid issues connecting to the API too fast

timeout /T 10 /nobreak



:: Call a precheck program

call python precheck-earnings.py



:: Pause for 10 seconds to avoid issues connecting to the API too fast

timeout /T 10 /nobreak



:: Call a precheck program

call python precheck-master-v2.py



:: Pause for 10 seconds to avoid issues connecting to the API too fast

timeout /T 10 /nobreak



:: Call a precheck program

call python precheck-tax.py



echo The program is finished


pause
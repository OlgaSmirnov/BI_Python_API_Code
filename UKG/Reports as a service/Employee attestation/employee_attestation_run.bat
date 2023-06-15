:: Set the root directory--we do this because we want to use Anaconda prompt instead of the default command prompt

set root=C:\ProgramData\Anaconda3



:: Call Anaconda Prompt

call %root%\Scripts\activate.bat %root%



:: Change directory to the attestation files

cd C:\BI_WH_Solution\Zack_Python_Code\BI_Python_API_Code\UKG\Reports as a service\Employee attestation

:: Call a precheck program

call python employee_attestation.py




echo The program is finished


pause
'''This code will run all 4 pre-check reports at once'''

#Import the papermill python library (this is used for running the jupyter notebooks)
import papermill as pm

#Execute the pre-check notebooks
pm.execute_notebook(
   'C:\UKG\Reports as a service\Precheck\precheck-deduction-v2.ipynb',
   'C:\UKG\Reports as a service\Precheck\precheck-earnings.ipynb',
   'C:\UKG\Reports as a service\Precheck\precheck-master-v2.ipynb',
    'C:\UKG\Reports as a service\Precheck\precheck-tax.ipynb'
   parameters = dict(alpha=0.6, ratio=0.1)
)
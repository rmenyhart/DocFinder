IF exist C:\antiword (echo Antiword OK!) ELSE (powershell -command "Expand-Archive -Force 'antiword-0_37-windows.zip' 'C:\'")
PATH=%PATH%;C:\antiword;
pip install textract
cmd /k
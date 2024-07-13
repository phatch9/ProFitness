CALL python3 -m venv venv
CALL .\venv\Scripts\pip.exe install --upgrade pip
CALL .\venv\Scripts\pip.exe install -r requirements.txt

echo:
echo "------"
echo "venv created."
echo "Use '. \Scripts\activate' to use the venv."

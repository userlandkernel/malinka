# malinka (малинка)[https://www.youtube.com/watch?v=MtZTFMwxgNo]
Generate malicious MS Windows shortcuts

## Supported platforms
- Microsoft Windows

## How to install?
1. Install python and make sure it is in your path environment variable
2. pip install -r requirements.txt
3. If you get an error about win32com, install pywin32 with pip

## Payloads
1. You can add custom powershell payloads to the payloads directory
2. In order to use the powershell_reverse_tcp payload, you need to edit the host and port variable in the payload file to match your connectback listener

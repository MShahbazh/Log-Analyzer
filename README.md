# Log Analyzer

A Simple CLI based log Analyzer. It accepts a server log file as input and handles corrupted/damaged lines, parses multiple timestamps and response time formats. It then produces a per line result file `Lines_Result.txt`. JSON format log lines are also supported   

## Repo Structure  
root  
├── scripts  
│   └── generation.py     
├── test_logs  
│   ├── file.log           
│   └── Lines_Result.txt   
├── main.py    
├── ANSWERS.md  
└── README.md  

## Requirements  

- Python 3.8 or higher  
- No External Dependencies. Only Python Standard Library (datetime,sys,json,random)    

## Installing Python (If you don't have)  
### Windows  
1. Go to https://www.python.org/downloads/  
2. Click Download Python 3.x.x  
3. Run the Installer. Tick "Add Python to PATH" before installation  
4. Open CMD and verify : 
```bash
python --version
```

## How to Run  
1. (Optional) Generate a test log file by running this command:  
```bash
python scripts/generation.py  
```
or if you want to specify the number of logs generated, then write number of logs in command line.  
```bash
python scripts/generation.py 600
```  
The above command will generate 600 log lines. In case of no argument, the program will generate 10 log lines by default.

2. Run the Analyzer
```bash
python main.py /path/to/custom/file
```
this command also takes another argument. Add the path of file in case of custom log file. In the absence of user provided log file, it analyzes `test_logs/file.log` by default


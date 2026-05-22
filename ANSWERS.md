# ANSWERS

## 1) HOW TO RUN
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

## 2) STACK CHOICE
I had the option of Js, RUST, C++ and Python for this project. However due to time constraints i decided to go with Python CLI as the basic version. Moreover Python also gives immense advantage in string, file and date handling which is difficult to obtain in C++ and RUST. Even tho C++ and RUST are stronger and faster for handling such large data, i had to avoid them due to time constraints. 

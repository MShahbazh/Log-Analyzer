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
I looked at JS, C++ and RUST and Python for this project but went with Python CLI version due to tight time constraints. Even though RUST and C++ gives superior performance and efficiency for large datasets, they require more development time. Python accelerated the development speed due to its built-in functions. Its built in support for json, filing, string and date manipulation allowed me to quickly code the basic CLI version. 

## 3) ONE REAL EDGE CASE
Although I tried to implement all the edge cases which were mentioned. One of the edge cases which i implemented is to parse without depending on the position. Rather, it will parse based on patterns and formats which allowed me to code the solution easily. Moreover, I implemented parsing for mutiple ways of timestamps such as epoch, separate date and time, different formats. Without it, solving the problem would have been a lot harder. 


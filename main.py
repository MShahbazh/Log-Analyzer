import sys   
from datetime import datetime, time, date
import json

methods=['GET','POST','DELETE','PUT']
UNIX_CHECK_DIGITS=5

def check_response_time(b):
    if 'ms' in b:
        b=b.split('ms')[0]
    elif 's' in b:
        b=b.split('s')[0]
    if b.isdigit():
        return True
    else:
        return False

def nonjson_parser(line):
    a=line.split()
    # print(a)
    info={}
    index={}
    method_flag=False
    route_flag=False 
    status_flag=False
    time_flag=False
    ip_flag=False
    timestamp=False

    if a[0][0].lower()>='a' and a[0][0].lower()<='z' or a[0][0]=='#':
        return info
    
    i=-1
    for part in a:
        i+=1
        if part.isdigit() and len(part)>=UNIX_CHECK_DIGITS:
            t=int(part)
            if 0<=t<=999999999999:
                timestamp=True
                t=datetime.fromtimestamp(t)
                t1=t.strftime('%d/%m/%y')
                t2=t.strftime('%H/%M/%S')
                index['TimeStamp']=i
                info['Date']=t1
                info['Orig_Time']=t2
                break
    
    if not timestamp:
        i=-1
        for part in a:
            i+=1
            if 'T' in part: 
                count1=0
                count2=0
                for j in part: 
                    if j==':':
                        count1+=1
                    if j=='-' or j=='/':
                        count2+=1
                if count1==2 and count2==2:
                    timestamp=True 
                    part = part.replace('/', '-')
                    times=datetime.fromisoformat(part)
                    t1=times.strftime('%d/%m/%y')
                    t2=times.strftime('%H/%M/%S')
                    index['TimeStamp']=i
                    info['Date']=t1
                    info['Orig_Time']=t2
                    break
            if timestamp: 
                break
    if not timestamp:
        count1=0
        count2=0
        times_index=-1
        dates_index=-1
        i=-1
        for part in a:    
            i+=1
            count1=0
            for j in part:                
                if j==':':
                    count1+=1
            if count1==2:
                times_index=i
            if times_index!=-1:
                break
        i=-1
        for part in a:
            i+=1
            count2=0
            if '/api' not in part:
                for j in part: 
                    if j=='-' or j=='/':
                        count2+=1
                if count2==2:
                    dates_index=i
                if dates_index!=-1:
                    break
                    
        if times_index!=-1:
            t1=time.fromisoformat(a[times_index])
            t1=t1.strftime('%H:%M:%S')
            index['Orig_Time']=times_index
            info['Orig_Time']=t1
        if dates_index!=-1:
            a[dates_index]=a[dates_index].replace('/','-')
            t1=date.fromisoformat(a[dates_index])
            t1=t1.strftime('%d/%m/%y')
            index['Date']=dates_index
            info['Date']=t1
        if dates_index!=-1 and times_index!=-1:
            timestamp=True
    i=-1
    j=''
    for part in a: 
        count=0
        i+=1
        for p in part:
            if p=='.':
                count+=1
        if count==3:
            ips=part.split('.')
            if len(ips)==4:
                k=3 
                while True:
                    if k<0:
                        break
                    if k!=0:
                        if not (ips[k].isdigit() and int(ips[k])>=0 and int(ips[k]  )<=255):
                            break 
                    else:
                        if not int(ips[0]):
                            break
                        else:
                            if int(ips[1]==255) and int(ips[0])>=0 and int(ips[0]  <=10):
                                ip_flag=True
                            if int(ips[1]!=255) and int(ips[0])>=0 and int(ips[0])  <=255:
                                ip_flag=True                         
                    k-=1
                if ip_flag:
                    break
    if ip_flag:
        info['Ip']=a[i]
        index['Ip']=i

    i=-1
    for part in a:
        i+=1
        if not method_flag:
            for j in methods:
                if j in part:
                    method_flag=True
                    break 
            if method_flag: 
                info['Method']=part 
                index['Method']=i
                break
    i=-1
    for part in a:
        i+=1
        if not route_flag:
            if '/api/' in part:
                route_flag=True
                info['Route']=part 
                index['Route']=i
                break
        pass
    # handling status 
    if route_flag:
        if a[index['Route']+1]=='-':
            status_flag=True
            info['Status']=a[index['Route']+1]
            index['Status']=index['Route']+1
            if index['Route']+2<len(a) and check_response_time(a[index['Route']+2]):
                time_flag=True
                index['Time']=index['Route']+2
                k=a[index['Route']+2]
                l=-1
                if 'ms' in a[index['Route']+2]:
                    k=k.split('ms')[0]
                    l=int(k)
                if 's' in a[index['Route']+2]:
                    k=k.split('s')[0]
                    l=int(k)*1000
                info['Time']=l
            else:
                time_flag=True
                index['Time']=-1
                info['Time']="NO_TIME"
        else:
            
            test=''
            if a[index['Route']+1].isdigit():
                if index['Route']+2<len(a):
                   if check_response_time(a[index['Route']+2]):
                    time_flag=True
                    index['Time']=index['Route']+2
                    if a[index['Route']+2].isdigit() or 'ms' in a[index['Route']+2]:
                        k=a[index['Route']+2].split('ms')[0]
                        info['Time']=int(k)
                    else:
                        if 's' in a[index['Route']+2]:
                            k=a[index['Route']+2].split('s')[0]
                            info['Time']=int(k)*1000
                    status_flag=True
                    index['Status']=index['Route']+1
                    info['Status']=a[index['Route']+1]
                   else:
                    time_flag=True
                    index['Time']=index['Route']+1
                    info['Time']=int(a[index['Route']+1])
                    status_flag=True
                    index['Status']=-1
                    info['Status']="NO_STATUS"
                else:  
                    time_flag=True
                    index['Time']=index['Route']+1
                    info['Time']=int(a[index['Route']+1])
                    status_flag=True
                    index['Status']=-1
                    info['Status']="NO_STATUS"
            else:
                if check_response_time(a[index['Route']+1]):
                    time_flag=True
                    index['Time']=index['Route']+1
                    if 'ms' in a[index['Route']+1]:
                        info['Time']=int(a[index['Route']+1].split('ms')[0])
                    elif 's' in a[index['Route']+1]:
                        info['Time']=int(a[index['Route']+1].split('s')[0])*1000
                else:
                    time_flag=True
                    index['Time']=-1
                    info['Time']="NO_TIME"
                status_flag=True
                index['Status']=-1
                info['Status']="NO_STATUS"

    if method_flag and route_flag and time_flag and ip_flag and timestamp:
        return info 
    else: 
        return {}

def json_parser(line):
    line=json.loads(line)
    main_string=''
    for i in line.values():
        main_string+=f'{i} '
    main_string=nonjson_parser(main_string)
    return main_string

def status_table(result):
    stat={}
    for i in result.values():
        if i['Status'] != '-':
            if i['Status'] in stat: 
                stat[i['Status']] += 1
            else:
                stat[i['Status']] = 1 
    stat=dict(sorted(stat.items(),key=lambda x:x[1]))
    return stat

def ip_table(result):
    stat={}
    for i in result.values():
        if i['Ip'] in stat: 
            stat[i['Ip']] += 1
        else:
            stat[i['Ip']] = 1 
    stat=dict(sorted(stat.items(),key=lambda x:x[1]))
    return stat

def method_table(result):
    stat={}
    for i in result.values():
        if i['Method'] in stat: 
            stat[i['Method']]+=1
        else:
            stat[i['Method']]=1 
    stat=dict(sorted(stat.items(),key=lambda x:x[1]))
    return stat

def route_table(result):
    stat={}
    for i in result.values():
        if i['Route'] in stat: 
            stat[i['Route']]+=1
        else:
            stat[i['Route']]=1 
    stat=dict(sorted(stat.items(),key=lambda x:x[1]))
    return stat
    
def generate_analysis_report(a,b,c,d,res,e,f,g,h):
    fd=open('Report.txt','r+')
    k=list(res.keys())
    fd.write(f"TOTAL LOGS COUNT: {e}\n")
    fd.write(f"VALID LOGS COUNT: {g}\n")
    fd.write(f"CORRUPTED LOGS COUNT: {f}\n\n")
    fd.write(f"AVERAGE RESPONSE TIME: {h}ms\n\n")
    fd.write("LOG WITH LOWEST REPONSE TIME:\n")
    fd.write(f"                     Date: {res[k[0]]['Date']}\n")
    fd.write(f"                     Time: {res[k[0]]['Orig_Time']}\n")
    fd.write(f"                     IP Address: {res[k[0]]['Ip']}\n")
    fd.write(f"                     Method: {res[k[0]]['Method']}\n")
    fd.write(f"                     Route: {res[k[0]]['Route']}\n")
    fd.write(f"                     Status: {res[k[0]]['Status']}\n")
    fd.write(f"                     Response Time: {res[k[0]]['Time']}ms\n")
    fd.write("\nLOG WITH HIGHEST REPONSE TIME:\n")
    fd.write(f"                     Date: {res[k[-1]]['Date']}\n")
    fd.write(f"                     Time: {res[k[-1]]['Orig_Time']}\n")
    fd.write(f"                     IP Address: {res[k[-1]]['Ip']}\n")
    fd.write(f"                     Method: {res[k[-1]]['Method']}\n")
    fd.write(f"                     Route: {res[k[-1]]['Route']}\n")
    fd.write(f"                     Status: {res[k[-1]]['Status']}\n")
    fd.write(f"                     Response Time: {res[k[-1]]['Time']}ms\n")
    fd.write("\n\nSTATUS TABLE AND FREQUENCIES\n")
    for i,j in a.items():
        fd.write(f"Status {i} | Frequency {j}\n")
    fd.write("\n\nIP TABLE AND FREQUENCIES\n")
    for i,j in b.items():
        fd.write(f"IP {i} | Frequency {j}\n")
    fd.write("\n\nROUTE TABLE AND FREQUENCIES\n")
    for i,j in c.items():
        fd.write(f"Route {i} | Frequency {j}\n")
    fd.write("\n\nMETHOD TABLE AND FREQUENCIES\n")
    for i,j in d.items():
        fd.write(f"Method {i} | Frequency {j}\n")
    fd.close()
    

def cli_menu(results):
     k=list(results.keys())
     while True:
        print("========== LOG ANALYZER ==========\n1. Show Summary\n2. Slowest Endpoints\n3. Fastest Endpoints\n4. Results\n5. Frequency Tables\n6. Exit")
        print("Enter your choice: ")
        x=int(input())
        if x==1:
            print("\n-----> Summary Generated...\n       You can View it through generated Report.txt file\n")
        elif x==2:
            if len(k)==0:
                print("\n-----> No Valid Log Found\n")
            else:
                print(f"\n-----> Enter the number of top slowest end points to display (must be less than or equal to  {len(k)}):")
                y=int(input())
                if 0<=y<=len(k):
                    for i in range(0,y):
                        print(f'\n==> {i+1}. {results[k[-1-i]]['Route']} ({results[k[-1-i]]['Time']}ms)')
                    print('\n\n')
                else:
                    print("\n-----> Out of Range Number\n")
        elif x==3:
            if len(k)==0:
                print("\n-----> No Valid Log Found\n")
            else:
                print(f"\n-----> Enter the number of top fastest end points to display (must be less than or equal to  {len(k)}):")
                y=int(input())
                if 0<=y<=len(k):
                    for i in range(0,y):
                        print(f'\n==> {i+1}. {results[k[i]]['Route']} ({results[k[i]]['Time']}ms)')
                    print('\n\n')
                else:
                    print("\n-----> Out of Range Number\n")                    
        elif x==4:
            print("\n-----> Results Generated...\n       You can View it through generated Lines_Result.txt file\n")
        elif x==5:
            print("\n-----> Frequency Tables Generated...\n       You can View it through generated Report.txt file\n")
        elif x==6:
            print('\n-----> Leaving Analyzer...\n')
            break
        else:
            print('\n-----> Enter Valid Number\n')



def main():
    file=''
    if len(sys.argv)>1:
        file=sys.argv[1]
    else:
        file='test_logs/file.log'
    fd=open(file,'r')
    res_fd=open('Lines_Result.txt','r+')
    lines=[]
    status={}
    results={}
    for line in fd:
        lines.append(line) 
    fd.close()
    total_logs=len(lines)
    valid_logs=0
    corrupted_logs=0
    average_response_time=0
    for i in range(0,len(lines)):
        res=''
        if lines[i][0]=='\n':
            status[i]=False 
            corrupted_logs+=1
            continue
        lines[i]=lines[i].split('\n')[0]
        if lines[i][0]=='{':
            res=json_parser(lines[i])
        else:
            res=nonjson_parser(lines[i])
        if len(res)==0:
            status[i]=False
            corrupted_logs+=1
        else:
            valid_logs+=1
            status[i]=True
            results[i]=res 
    
    for i in range(0,len(lines)):
        res_fd.write(f"==================== LINE {i+1} ====================\n")
        res_fd.write(f"            LINE: {lines[i]}\n")
        res_fd.write(f"            STATUS: {status[i]}\n")
        if status[i]==True:
            average_response_time+=results[i]['Time']
            res_fd.write(f"            RESULTS:\n")
            res_fd.write(f"                     Date: {results[i]['Date']}\n")
            res_fd.write(f"                     Time: {results[i]['Orig_Time']}\n")
            res_fd.write(f"                     IP Address: {results[i]['Ip']}\n")
            res_fd.write(f"                     Method: {results[i]['Method']}\n")
            res_fd.write(f"                     Route: {results[i]['Route']}\n")
            res_fd.write(f"                     Status: {results[i]['Status']}\n")
            res_fd.write(f"                     Response Time: {results[i]['Time']}\n")
        res_fd.write('\n\n')
    res_fd.close()

    status_tables=status_table(results)
    ip_tables=ip_table(results)
    method_tables=method_table(results)
    route_tables=route_table(results)
    results = dict(sorted(results.items(),key=lambda x:x[1]['Time']))
    generate_analysis_report(status_tables,ip_tables,route_tables,method_tables,results,total_logs,corrupted_logs,valid_logs,average_response_time)
    cli_menu(results)
   




if __name__ =="__main__":
    main()
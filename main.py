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

    if a[0][0].lower()>='a' and a[0][0].lower()<='z':
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
                info['Time']=a[index['Route']+2]
            else:
                time_flag=True
                index['Time']=-1
                info['Time']="NO_TIME"
        else:
            # now consdering the situtation that status may or may not be there at all 
            test=''
            if a[index['Route']+1].isdigit():
                if index['Route']+2<len(a):
                   if check_response_time(a[index['Route']+2]):
                    time_flag=True
                    index['Time']=index['Route']+2
                    if a[index['Route']+2].isdigit():
                        info['Time']=a[index['Route']+2]+'ms'
                    else:
                        info['Time']=a[index['Route']+2]
                    status_flag=True
                    index['Status']=index['Route']+1
                    info['Status']=a[index['Route']+1]
                   else:
                    time_flag=True
                    index['Time']=index['Route']+1
                    info['Time']=a[index['Route']+1]+'ms'
                    status_flag=True
                    index['Status']=-1
                    info['Status']="NO_STATUS"
                else:  
                    time_flag=True
                    index['Time']=index['Route']+1
                    info['Time']=a[index['Route']+1]+'ms'
                    status_flag=True
                    index['Status']=-1
                    info['Status']="NO_STATUS"
            else:
                if check_response_time(a[index['Route']+1]):
                    time_flag=True
                    index['Time']=index['Route']+1
                    info['Time']=a[index['Route']+1]
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


    
        


def main():
    file=''
    if len(sys.argv)>1:
        file=sys.argv[1]
    else:
        file='test_logs/file.log'
    fd=open(file,'r')
    lines=[]
    status={}
    results={}
    for line in fd:
        lines.append(line) 
    for i in range(0,len(lines)):
        res=''
        if lines[i][0]=='\n':
            status[i]=False 
            continue
        lines[i]=lines[i].split('\n')[0]
        if lines[i][0]=='{':
            res=json_parser(lines[i])
        else:
            # then it is definitely non json incl gibberish 
            res=nonjson_parser(lines[i])
        if len(res)==0:
            status[i]=False
        else:
            status[i]=True
            results[i]=res 
    
    for i in range(0,len(lines)):
        print("STATUS: ",status[i])
        if status[i]==True:
            print(results[i])

if __name__ =="__main__":
    main()
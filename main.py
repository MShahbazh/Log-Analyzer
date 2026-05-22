import sys   

methods=['GET','POST','DELETE','PUT']

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
    print(a)
    info={}
    index={}
    method_flag=False
    route_flag=False 
    status_flag=False
    time_flag=False
    ip_flag=False

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

    print(index)
    return info
        


def main():
    file=''
    if len(sys.argv)>1:
        file=sys.argv[1]
    else:
        file='test_logs/file.log'
    fd=open(file,'r')
    lines=[]
    status={}
    for line in fd:
        lines.append(line) 
    for i in range(0,1):
        if lines[i][0]=='\n':
            status[i]=False 
        lines[i]=lines[i].split('\n')[0]
        if lines[i][0]=='#' or lines[i][0]=='{':
            pass
            # then i will consider it as json
        else:
            # then it is definitely non json incl gibberish 
            res=nonjson_parser(lines[i])
            if res is None:
                status[i]=False
            else:
                print(res)



if __name__ =="__main__":
    main()
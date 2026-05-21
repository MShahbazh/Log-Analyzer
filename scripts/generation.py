import random 
import sys 
from datetime import date,datetime,timedelta

random_words=['Hello','Timestamp','Why','WHO','the','IS','hello world','happy nation','ip','']
methods=['GET','POST','DELETE','PUT','']
routes=['/api/user','/api/login','/api/register','']
status=['200','400','500','-','']
units=['ms','s','']

def generate_datetimes():
    if random.random()<=0.2:
        format_sign=''
        space=''
        if random.choice([0,1])==0:
            format_sign='-'
        else:
            format_sign='/'
        if random.choice([0,1])==0:
            space='T'
        error_date=f"{random.randint(2000,2100)}+{format_sign}+{random.randint(-12,12)}+{format_sign}+{random.randint(-30,30)}+{space}+{format_sign}+{random.randint(-23,23)}+{format_sign}+{random.randint(-30,30)}+{format_sign}+{random.randint(-59,59)}+{format_sign}+{random.randint(-59,59)}+{format_sign}"
        if random.choice([0,1])==0:
            error_date+='Z'        
        return error_date
        
    date1=datetime.now()
    date2=datetime(2000,1,1,0,0,0,0)
    diff=date1-date2
    new_date=date1+timedelta(days=random.randint(0,diff.days))
    unix_sec=new_date.timestamp()

    if random.choice([0,1])==0:
        f=''
        if random.choice([0,1])==0:
            f="%Y-%m-%d"
        else:
            f="%Y/%m/%d"
        f+=" %H:%M:%S"
        new_date=new_date.strftime(f)
        
        x=random.choice([0,1])
    else:
        new_date=str(new_date)
    x=random.choice([0,1,2])
    x=0
    if x==0: 
        if random.choice([0,1]) == 0:
            return new_date
        else:
            date3=new_date.split(' ')
            if random.random()<=0:
                print("ENRINER ")
                if random.choice([0,1])==0:
                    return f"{date3[0]}T{date3[1]}Z"
                else:
                    return f"{date3[0]}T{date3[1]}"
            else:
                empty_spot=''
                
                date3=new_date.split(' ')
                e=[False,False]
                if random.random()<=0.5: 
                    empty_spot+=date3[0]
                    e[0]=True
                
                if random.random()<=0.5: 
                    empty_spot+=date3[1]
                    e[1]=True
                
                if e[0] and e[1]:
                    if random.choice([0,1])==0:
                        empty_spot=f"{date3[0]}T{date3[1]}Z"
                    else:
                        empty_spot=f"{date3[0]}T{date3[1]}"
                return empty_spot         
    elif x==1:
        return str(int(unix_sec))
       
def generate_ip():
    ip=[0]*4
    ip[3]=random.randint(0,255)
    ip[2]=random.randint(0,255)
    ip[1]=random.randint(0,255)
    if ip[1]==255: 
        ip[0]=random.randint(0,10)
    else:
        ip[0]=random.randint(0,255)
    return f"{ip[0]}.{ip[1]}.{ip[2]}.{ip[3]}"
    
def json_generator():
        a=generate_datetimes()
        s='{"Timestamp":"'
        if a=='':
           s+=''
        else:
            s+=a

        a=generate_ip()
        s+='","Ip":"'
        if a=='':
           s+=''
        else:
            s+=a

        s+='","Methods":"'
        a=methods[random.randint(0,len(methods)-1)]
        if a=='':
           s+=''
        else:
            s+=a

        s+='","Routes":"'
        a=routes[random.randint(0,len(routes)-1)]
        if a=='':
           s+=''
        else:
            s+=a

        s+='","Status":"'
        a=status[random.randint(0,len(status)-1)]
        if a=='':
           s+=''
        else:
            s+=a

        s+='","Response Time":"'
        a=units[random.randint(0,len(units)-1)]
        s+=str(random.randint(0,1000))
        if a=='':
           s+=''
        else:
            s+=a
        s+='"}'
        return s

fd=open('test_logs/file.log','w+')
nums=10
if len(sys.argv)==1:
    print(f"NO NUMBER OF ENTRIES PROVIDED. TAKING DEFAULT AS {nums}")
else:
    nums=int(sys.argv[1])

for _ in range(0,nums):
    k=json_generator()
    k+='\n'
    fd.write(k)
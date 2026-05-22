import random 
import sys 
from datetime import datetime,timedelta

random_words=['Hello','Timestamp','Why','WHO','the','IS','hello world','happy nation','ip','RANDOM','WORDS','-','#','ERROR']
methods=['GET','POST','DELETE','PUT','']
routes=['/api/user','/api/login','/api/register','']
status=['200','400','500','-','']
units=['ms','s','']
CRASH_PROB=0
UNCONTROLLED_FORMAT=0
DATETIMESPLIT=0.2
GIBB_TEXTEND=0.02

def damage_string(text,type):
    if random.random()<=CRASH_PROB:
        if random.random()<=0.5:
            t=text[:random.randint(0,len(text)-1)]
            if t: 
                text=t
        if random.random()<=0.5:
            if type=='json':
                text=text.replace('{','#')
            # elif type=='non':
            #     text=text.replace(' ','(')
        if random.random()<=0.5:
            parts=text.split(' ')
            p=parts
            p.pop(random.randint(0,len(parts)-1)) 
            if p:
                parts=p 
            text=''
            for i in range(0,len(parts)):
                text+=parts[i]
    return text
        
def generate_random_gibberish(x=1):
    s=''
    for i in range(0,x):
        s+=random_words[random.randint(0,len(random_words)-1)]
        if i!=x-1 and i!=0:
            s+=' '
    return s

def generate_datetimes():
    main_string=''
    if random.random()<=UNCONTROLLED_FORMAT:
        format_sign=''
        space=''
        if random.choice([0,1])==0:
            format_sign='-'
        else:
            format_sign='/'
        if random.choice([0,1])==0:
            space='T'
        error_date=f"{random.randint(2000,2100)}{format_sign}{random.randint(-12,12)}{format_sign}{random.randint(-30,30)}{space}{random.randint(-23,23)}{format_sign}{random.randint(-30,30)}{format_sign}{random.randint(-59,59)}{format_sign}{random.randint(-59,59)}"
        if random.choice([0,1])==0:
            error_date+='Z'        
        main_string=error_date
    else:
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
        else:
            new_date=str(new_date)
        new_date=new_date.split('.')[0]
        
        x=random.choice([0,1])
        
        if x==0: 
            if random.choice([0,1]) == 0:
                main_string=new_date
            else:
                date3=new_date.split(' ')
                if random.random()>=-DATETIMESPLIT:
                    if random.choice([0,1])==0:
                        main_string= f"{date3[0]}T{date3[1]}Z"
                    else:
                        main_string= f"{date3[0]}T{date3[1]}"
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
                    if not e[0] and not e[1]:
                        empty_spot=new_date
                    main_string=empty_spot                      
        elif x==1:
            main_string=str(int(unix_sec))

    return main_string
       
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

        s+='","Response-Time":"'
        a=units[random.randint(0,len(units)-1)]
        s+=str(random.randint(0,1000))
        if a=='':
           s+=''
        else:
            s+=a
        s+='"}'
        

        if random.random()<=CRASH_PROB:
            s=damage_string(s,'json')
        return s

def non_json_generator():
        s=''
        a=generate_datetimes()
        if a=='':
           s+=''
        else:
            s+=a
        a=generate_ip()
        s+=' '
        if a=='':
           s+=''
        else:
            s+=a
        s+=' '
        a=methods[random.randint(0,len(methods)-1)]
        if a=='':
           s+=''
        else:
            s+=a
        s+=' '
        a=routes[random.randint(0,len(routes)-1)]
        if a=='':
           s+=''
        else:
            s+=a
        s+=' '
        a=status[random.randint(0,len(status)-1)]
        if a=='':
           s+=''
        else:
            s+=a
        s+=' '
        a=units[random.randint(0,len(units)-1)]
        s+=str(random.randint(0,1000))
        if a=='':
           s+=''
        else:
            s+=a
        if random.random()<=CRASH_PROB:
            s=damage_string(s,'non')
        if random.random()<=GIBB_TEXTEND:   
            s+=' '
            s+=generate_random_gibberish(random.randint(0,(random_words)-1))
        return s


fd=open('test_logs/file.log','w+')
nums=10
if len(sys.argv)==1:
    print(f"NO NUMBER OF ENTRIES PROVIDED. TAKING DEFAULT AS {nums}")
else:
    nums=int(sys.argv[1])

for _ in range(0,nums):
    k=''
    x=random.random()
    if x>=0.5:
        k=json_generator()
    elif x<=0.5:
        k=non_json_generator()
    # elif x>=0.05:
    #     k=generate_random_gibberish(random.randint(0,len(random_words)-1))
    # elif x>=0:
    #     k=''
    k+='\n'
    fd.write(k)

    
    
        


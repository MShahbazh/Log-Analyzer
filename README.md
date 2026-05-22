# Log-Analyzer



 if a[0][0].lower()>='a' and a[0][0].lower()<='z':
        # cosidering that if there is a letter in a[0][0] that means whole line is gibberish
        return {}
    else:
        # if 'a' has unix time that means a[0] should definitely have seconds e:g 1913496232. otherwise it has the possibility of 2024/03/01T03:34:34Z format or just 2024/03/01 format or 03:34:34
        #  I am going to check these conditions based on availibity of T first and then / or -
        if 'T' in a[0]:
            #  POSSIBLE FORMATS: 
            # 2024/03/01T03:34:34Z
            # 2024/03/01T03:34:34
            # 2024-03-01T03:34:34Z
            # 2024-03-01T03:34:34
            pass
        
        #  the above if will give us timestamp as separate field and date as separate which will be evluated and checked below

            #  POSSIBLE FORMATS: 
            # 2024/03/01 
            # 2024-03-01 
            # 1913496232
            # 03:34:34
        if ':' in a[0]:
                # 03:34:34
            pass
        elif '/' in a[0] or '-' in a[0]:
            # 2024/03/01 
            # 2024-03-01 
            pass
        else:
            # 1913496232
            pass

        pass
   
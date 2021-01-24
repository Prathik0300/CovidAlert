import multiprocessing as mp
import time

def GetLocation(event,child,status):
    print("Location")
    res=False
    stat = None
    while(res==False):
        try:
            stat = status.recv()
            res=True
        except:
            res = False

    while(stat):
        child.send([22.2,23.55])
        time.sleep(30)
        res=False
        while res==False:
            try:
                stat = status.recv()
                res=True
            except:
                res=False

    child.close()
    status.close()
    return 

def Functions(event,status,parent):
    inp = input("Enter: ")
    print("Functionssss")
    i=1
    loc1=0
    loc2=0
    while inp!="bye":
        res = False
        while(res==False):
            try:
                loc1,loc2 = parent.recv()
                res=True
            except:
                res=False
        print(loc1,loc2,i)
        i+=1
        time.sleep()
        status.send([True])
        inp = input("Enter: ")
    status.send([False])
    status.close()
    parent.close()
    return 


def UserFunctions():   
    e = mp.Event()  
    func,loc = mp.Pipe()
    OutStatus,InStatus = mp.Pipe()
    p2 = mp.Process(target=Functions,args=(e,OutStatus,func))
    p1 = mp.Process(target=GetLocation,args=(e,loc,InStatus))
    p1.start()
    p2.start()
    e.set()
    
    print("Inside Function")

if __name__ == '__main__':
    UserFunctions()
    

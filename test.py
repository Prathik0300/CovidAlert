from itertools import combinations as c

l = ["fever","dry cough","tiredness","aches and pains","sore throat","diarrhoea","conjunctivitis","headache","loss of taste or smell","a rash on skin, or discolouration of fingers or toes","difficulty breathing or shortness of breath","chest pain or pressure","loss of speech or movement"]
l1 = len(l)
count = 0
d = {}
for i in range(1,l1+1):
    cc = c(l,i)
    temp=[]
    for ele in cc:
        print("length is ",i)
        temp.append(ele)
    if tuple(temp) not in d:
        count+=len(temp)
        d[tuple(temp)]=1
print(count)

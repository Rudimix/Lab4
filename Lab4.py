from random import randint
import math

i=0
L=int(input("Введите длину кодировки "))
N=int(input("Введите количество шагов алгоритма "))

def decToBin (d):
    b = ''
    while d > 0:
        b = str(d % 2) + b
        d = d // 2
    return b.zfill(L)

def mu(x):
    if(x==0):
        return round(5*math.sin(x)+math.log(0.000000001),2)
    else:
        return round(5*math.sin(x)+math.log(x),2)

def bin_dec(data):
    number = 0
    len_dat = len(data)
    for i in range(0, len_dat):
        number += int(data[i]) * (2**(len_dat - i -1))
    return number

def muPodm(podm):
    arr=[]
    for i in range(len(podm)):
        arr.append(mu(bin_dec(podm[i])))
    return arr

def podm(x):
    podm=[]
    for i in range(0,2**L):
        if(hamming_distance(decToBin(i),x)==1):
            podm.append(decToBin(i))
    return podm

def hamming_distance(str_1:str, str_2:str) -> int:
    distance = 0
    for i in range(len(str_1)):
        if str_1[i] != str_2[i]:
            distance += 1
    return distance

def monteKarlo():
    localMax=0
    localMaxS=''
    for i in range (0,N):
        index=randint(0,2**L-1)
        print("Выбираем sj ",decToBin(index),"её приспособленность ",mu(index))
        if(localMax):
            print("Текущий max: ", localMax)
            print("Текущий maxS: ", localMaxS)
        if(localMax<mu(index)):
            ("Происходит замена: ",localMaxS,"-->",decToBin(index))
            localMax=mu(index)
            localMaxS=decToBin(index)
            localIndex=index
    return localIndex

def depthSearch():
    localIndex=randint(0, 2**L-1)
    localSj=decToBin(localIndex)
    localmaxS=localSj
    localmax=mu(localIndex)
    localPodm=podm(localmaxS)
    Index=0
    for i in range (0,N):
        if(len(localPodm)!=0):
            localIndex=randint(0, len(localPodm)-1)
            mp=muPodm(localPodm)
            print("")
            print("Текущий max: ", localmax)
            print("Текущий maxS: ", localmaxS)
            print("Подмножество: ", localPodm)
            print("Их приспособленности: ", mp)
            localSj=localPodm[localIndex]
            print("Выбираем: ", localSj, "её приспособленность",mp[localIndex])
            localPodm.pop(localIndex)
            if(localmax<mp[localIndex]):
                print("Происходит замена: ",localmaxS,"-->",localSj)
                localmaxS=localSj
                localmax=mp[localIndex]
                localPodm=podm(localSj)
                Index=bin_dec(localmaxS)
    return Index

def wideSearch():
    localIndex=randint(0, 2**L-1)
    localSj=decToBin(localIndex)
    localmaxS=localSj
    localmax=mu(localIndex)
    localPodm=podm(localmaxS)
    Index=0
    for i in range (0,N):
        if(len(localPodm)!=0):
            localBuf=0
            mp=muPodm(localPodm)
            print("")
            print("Текущий max: ", localmax)
            print("Текущий maxS: ", localmaxS)
            print("Подмножество: ", localPodm)
            print("Их приспособленности: ", mp)
            for i in range (len(localPodm)):
                localSj=localPodm[i]
                print("Выбираем: ", localSj, "её приспособленность",mp[i])
                if (localBuf<mp[i]):
                    buf=i
                    localBuf=mp[i]
            if(localmax<mp[buf]):
                localSj=localPodm[buf]
                print("Происходит замена: ",localmaxS,"-->",localSj)
                localmaxS=localSj
                localmax=mp[buf]
                localPodm=podm(localSj)
                Index=bin_dec(localmaxS)
            else: 
                print("Оптимум найден, алгоритм прекращён")
                break
    return Index

max=0
maxS=''
methodMax=[0]*3
methodMaxS=['']*3

for i in range (0,2**L):
    if(i<32):
        print(decToBin(i),"-",mu(i))

for i in range (0,N):
    k=randint(0,2)
    print('')
    print("Итерация: ", i+1)
    if (k==0):
        print("Выбран метод Монте-Карло")
        index=monteKarlo()
        if(methodMax[0]<mu(index)):
            methodMaxS[0]=decToBin(index)
            methodMax[0]=mu(index)
        print("Результат работы метода: sj=",methodMaxS[0],"приспособленность= ",methodMax[0])
    elif (k==1):
        print("Выбран метод поиска в глубину")
        index=depthSearch()
        if(methodMax[1]<mu(index)):
            methodMaxS[1]=decToBin(index)
            methodMax[1]=mu(index)
        print("Результат работы метода: sj=",methodMaxS[1],"приспособленность= ",methodMax[1])
    else:
        print("Выбран метод поиска в ширину")
        index=wideSearch()
        if(methodMax[2]<mu(index)):
            methodMaxS[2]=decToBin(index)
            methodMax[2]=mu(index)
        print("Результат работы метода: sj=",methodMaxS[2],"приспособленность= ",methodMax[2])
    for i in range(0,2):
        if(max<methodMax[i]):
            max=methodMax[i]
            maxS=methodMaxS[i]
print('')
print("Конечный результат работы: Sj= ",maxS,"её приспособленность: ",max)
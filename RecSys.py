import csv
import statistics as st
import math
import requests
import json


movieRate=[]
movieContext=[]
days={"Mon":False,"Tue":False,"Wed":False,"Thu":False,"Fri":False,"Sat":True,"Sun":True,"-":False}
sim_films=[]

def readcsvFile(filename):
    with open(filename) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            movieRate.append([int(item[1:len(item)]) for item in row if (item[1:2]!="M" and item[0:1]!="U" and item!='')])
        movieRate.remove([])

def readcsvContext(filename):
    with open(filename) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            movieContext.append([item[1:len(item)] for item in row if (item[1:6]!="Movie" and item[0:4]!="User" and item!='')])
    movieContext.remove([])

def getWorkMovieRate():
    for i in range(0,len(movieRate)):
        for j in range(0,len(movieRate[i])):
            if (days[movieContext[i][j]]):
                movieRate[i][j]=movieRate[i][j]*(-1);

def avgMark(user):
   return st.mean([i for i in user if (i>0)])

#u and v - row in table - users
def findSim(u,v):
    sumu2=0
    sumv2=0
    sumi=0
    for i in range(0,len(u)):
        if (u[i]>0 and v[i]>0):
            sumi+=u[i]*v[i]
            sumu2+=u[i]*u[i]
            sumv2+=v[i]*v[i]
    return sumi/(math.sqrt(sumu2)*math.sqrt(sumv2))

def find5Sim(user):
    l_sim_films={}
    for cur_user in movieRate:
        if cur_user!=user:
            l_sim_films[movieRate.index(cur_user)]=findSim(user,cur_user)
    sim_films= sorted(l_sim_films.items(),key=lambda x:x[1])
    return sim_films[len(sim_films)-5:len(sim_films)]

def findRating(user_id, film_id):
    sum=0
    modSum=0
    for item in sim_films:
        if (movieRate[item[0]][film_id]>0):
            sum+=item[1]*(movieRate[item[0]][film_id]-avgMark(movieRate[item[0]]))
            modSum+=abs(item[1])
    return (avgMark(movieRate[user_id])+sum/modSum)

readcsvFile('data.csv')
my_user=31
sim_films=find5Sim(movieRate[my_user])
res={}
for film_id in range(0,len(movieRate[my_user])):
    if (movieRate[my_user][film_id ]<0):
        res["movie "+str(film_id+1)]=round(findRating(my_user,film_id),3)
data={}
data["user"]=my_user+1
data["1"]=res
readcsvContext("context.csv")
getWorkMovieRate();
ratings={}
for film_id in range(0,len(movieRate[my_user])):
    if (movieContext[my_user][film_id ]=='-'):
        ratings["movie "+str(film_id+1)]=round(findRating(my_user,film_id),3)
el=max(ratings.items(), key=lambda x: x[1])
data["2"]={el[0]:el[1]}

json_data=json.dumps(data);

url ='https://cit-home1.herokuapp.com/api/rs_homework_1'
headers = {'content-type': 'application/json'}
print(res)
#r = requests.post(url, data=json_data,headers=headers)
#print(r.json())



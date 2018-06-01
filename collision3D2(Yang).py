# -*- coding: utf-8 -*-
import numpy as np
from numpy.random import rand
import random
from math import sqrt
import time as timer
from visual import *
import threading
import copy

particles=[]
showtime=0.1
roomsize=(100,100,100)
r=2
N=100
atoms=[]
dt=0.01

class database:
    """
    the database is used to store 3 particles' data  of different time, and is able to refresh it.
    """
    def __init__(self):
        self.data1=[]
        self.data2=[]
        self.data3=[]
        self.data4=[]
        self.data5 = []
        self.time1=0
        self.time2=0
        self.time3=0
        self.time4=0
        self.time5 = 0
        self.ready=1
    def getdata(self,time):
        """
        return the newest data according to the given time, and the time of the data
        :param time:
        :return data and time of the data:
        """
        while self.ready==0:
            print("wait ready")
        if self.time1<time<self.time5:
            if self.time4<time:
                return self.data4,self.time4
            elif self.time3<time:
                return self.data3,self.time3
            elif self.time2<time:
                return self.data2,self.time2
            else:
                return self.data1,self.time1
        else:
            raise ValueError("data wrong")

    def savedata(self,data,time):
        """
        save a new data in, and refresh the data.
        :param data:
        :param time:
        :return:
        """
        self.ready=0
        if self.data1==[]:
            self.data1=copy.deepcopy(data)
            self.time1=time
        elif self.data2==[]:
            self.data2=copy.deepcopy(data)
            self.time2=time
        elif self.data3==[]:
            self.data3=copy.deepcopy(data)
            self.time3=time
        elif self.data4==[]:
            self.data4=copy.deepcopy(data)
            self.time4=time
        elif self.data5==[]:
            self.data5=copy.deepcopy(data)
            self.time5=time
        else:
            self.data1,self.data2,self.data3,self.data4,self.data5=self.data2,self.data3,self.data4,self.data5,copy.deepcopy(data)
            self.time1,self.time2,self.time3,self.time4,self.time5=self.time2,self.time3,self.time4,self.time5,time
        self.ready=1
base=database()

def solve2func(a,b,c):
    """calculate the Quadratic Equations and """
    derta=b**2-4*a*c
    if derta <0:
        return -1
    else:
        return (-b-sqrt(derta))/2/a

xaxis = visual.curve(pos=[(0, 0, 0), (roomsize[0], 0, 0)], color=color.blue, radius=0.05)
yaxis = visual.curve(pos=[(0, 0, 0), (0, roomsize[1], 0)], color=color.blue, radius=0.05)
zaxis = visual.curve(pos=[(0, 0, 0), (0, 0, roomsize[2])], color=color.blue, radius=0.05)
xaxis2 = visual.curve(pos=[roomsize, (0, roomsize[1], roomsize[2]), (0, 0, roomsize[2]), (roomsize[0], 0, roomsize[2])], color=color.blue, radius=0.05)
yaxis2 = visual.curve(pos=[roomsize, (roomsize[0], 0, roomsize[2]), (roomsize[0], 0, 0), (roomsize[0], roomsize[1], 0)], color=color.blue, radius=0.05)
zaxis2 = visual.curve(pos=[roomsize, (roomsize[0], roomsize[1], 0), (0, roomsize[1], 0), (0, roomsize[1], roomsize[2])], color=color.blue, radius=0.05)


def generate_particle(N,Lrange,Vrange,r=r):
    """generate N particles whose position is in Lrange and velocity is in Vrange"""
    global particles
    global atoms
    colors = [color.red, color.green, color.blue,
              color.yellow, color.cyan, color.magenta]
    for a in range(N):
        v=Vrange-rand(3,)*Vrange*2
        l=rand(3,)*(Lrange-2*r)+2*r
        particles+=[[l,v,10000,8888]]
        atoms += [visual.sphere(pos=particles[a][0], radius=r, color=colors[a % 6])]
    base.savedata(particles,0)



def time2wall(L,V,r=r,roomsize=roomsize):
    """teturn the shortest time of collision to walls if the particle didn't collide with any other particles"""
    time=8888 #a lucky number that large enough
    wall=0
    for a in range(3):
        if V[a]>0:
            t=(roomsize[a]-r-L[a])/V[a]
        elif V[a]<0:
            t=(r-L[a])/V[a]
        if t < time:
            time=t
            wall=-a-1
    if time<0:
        time=0
    return time,wall        #-1,-2,-3 for x,y,z



def parti_collision(L1,L2,V1,V2,r=r):
    """
    given two particles' location and velocity and return the new velocity after collision
    :param L1: the location of the first particle which is an array
    :param L2: the location of the second particle which is an array
    :param V1: the velocity of the first particle which is an array
    :param V2: the velocity of the second particle which is an array
    :param r: radius
    :return: new velovities of the particles
    """
    dertaL=L1-L2
    orien=(dertaL)/sqrt(np.dot(dertaL,dertaL))
    derta=orien*(np.dot(orien,V1)-np.dot(orien,V2))
    resV1=V1-derta
    resV2=V2+derta
    return resV1,resV2

def collision(ind1,ind2):
    """
    given two index of particles or wall and change the velocity data in the list<particles> by calling parti_collision
    :param ind1: the particle to calculate the new velocity which is a number in[0,N]
    :param ind2: a index of the target which the first particle collision with
    :return:change the two index into a list without index of walls
    """
    global particles
    if ind2<0: # ind2 is means collision to walls -1:x -2:y -3:z
        particles[ind1][1][-ind2-1]= - particles[ind1][1][-ind2-1] #collision to wall, change the V on that direction
        return [ind1]
    else:
        L1,V1,partim1,partar1=particles[ind1]
        L2,V2,partim2,partar2=particles[ind2]
        particles[ind1][1],particles[ind2][1]=parti_collision(L1,L2,V1,V2)
        return [ind1,ind2]


def collision_check(L1,L2,V1,V2,t,r=r):
    """
    check whether two particles with given location and velocity will collision together by solving a function
    if ture, return the time to the collision
     if not, return -1
    :param L1:the location of the first particle which is an array
    :param L2:the location of the second particle which is an array
    :param V1:the velocity of the first particle which is an array
    :param V2:the velocity of the second particle which is an array
    :param r:radius
    :return:
    """
    deltaV=V1-V2
    deltaL=L1-L2
    #if not ((- 2*r < t * (deltaV[1]) - (deltaL[1]) < 2*r)and(- 2*r < t * (deltaV[2]) - (deltaL[2]) < 2*r)):#这样到了14秒（九几）
        #return -1
    c=np.dot(deltaL,deltaL)-4*r*r
    b=2*(np.dot(deltaL,deltaV))
    a=np.dot(deltaV,deltaV)
    answer=solve2func(a,b,c)
    return answer


def collision_time(index,N=N):
    """
    check a particle according index when will it collision and who it will collision with
    :param index:a number which is the index of the particle
    :param N:total particles
    :return:the time of the collision and the target both are numbers
    """
    global particles
    l,v,t,target=particles[index]
    time,target=time2wall(l,v)
    leasttime=[]
    for parind in list(range(index))+list(range(index+1,N)):
        parl,parv,partim,partar=particles[parind]
        if (parl[0]!=l[0])and(parv[0]==v[0]):
            continue
        coltim1=(parl[0]-l[0]-2*r)/(v[0]-parv[0])  #roughly time
        coltim2=(parl[0]-l[0]+2*r)/(v[0]-parv[0])
        if coltim1>coltim2:
            coltim1,coltim2=coltim2,coltim1
        if coltim1<0<coltim2:
            coltim1=0
        if (0<=coltim1<partim) and(coltim1<time):
            leasttime+=[(coltim1,coltim2,parind)]      #time for collision, if will happen
    leasttime.sort()
    for a in range(len(leasttime)):
        (t1,t2,ind)=leasttime[a]
        parl,parv,partim,partar=particles[ind]
        result=collision_check(l,parl,v,parv,t)
        if (0<result<time)and(result<particles[ind][2]):
            if a < len(leasttime)-1:
                a+=1
                while (leasttime[a][0]-t1)*(leasttime[a][1]-t2)<=0:
                    newind=leasttime[a][2]
                    parl, parv, partim, partar = particles[newind]
                    newresult=collision_check(l,parl,v,parv,t)
                    a+=1
                    if 0<newresult<result:
                        result=newresult
                        ind=newind
                    if a>=len(leasttime):
                        break
            return (result,ind)
    return time,target

def initialize(N=N):
    global particles,roomsize
    generate_particle(N, min(roomsize)-2, 10)
    #particles=[[array([ 21.84312541,  26.24446285,  14.68825246]), array([ 3.04962868, -2.61817943, -0.45164528]), 10000, 8888], [array([ 20.7089008 ,  11.64901738,   7.16653974]), array([-3.63523515,  2.66523554, -2.5583785 ]), 10000, 8888], [array([ 23.98222286,   3.03907979,  25.92303535]), array([ 3.21580443,  1.00652479,  4.39526376]), 10000, 8888], [array([  9.2798995 ,   4.45723378,  15.31415236]), array([-3.23813526, -2.61680752, -2.98732961]), 10000, 8888], [array([ 20.9026019 ,   2.38703395,   8.75498084]), array([ 1.53154164,  1.69398268, -4.90912508]), 10000, 8888], [array([ 20.99574661,   9.16236896,  29.75788399]), array([-0.87779724,  0.50653061,  1.04625966]), 10000, 8888], [array([ 20.24429977,  13.15314023,  11.48298164]), array([-4.47286884, -0.31616435,  0.90587565]), 10000, 8888], [array([ 28.65757413,   7.95799144,  14.97971148]), array([-0.09019593, -3.10076391,  2.42535585]), 10000, 8888], [array([ 39.50247412,  28.60620495,  26.01646515]), array([-2.8496129 , -2.90739034, -4.35496209]), 10000, 8888], [array([ 13.79143346,  24.85255274,  36.44856363]), array([ 0.54114201,  4.15371068, -0.70293296]), 10000, 8888]]
    print(particles)
    next_colli=88 #next collision time
    next_parti=[] #the partical or wall to be caltulated
    for a in range(N):
        time,target=collision_time(a,N)
        assert time>0
        particles[a][2],particles[a][3]=time,target
        if time < next_colli:
            next_colli=time
            next_parti.append((a,target))
        elif time==next_colli:
            next_parti.append(a)
            next_parti.append((a,target))
        if target>=0:
            particles[target][2],particles[target][3]=time,a
    clock=0
    return next_colli,next_parti,clock

#print(particles)
#print(collision(48,49))
#print(particles)

def cycle(N=N,dt=dt):
    """
    when the database need refresh
    calculate and refresh the location, velocity and target and next collision time of all the particles
    for important time-point(when a collision happens)
    and save the new data to the database
    """
    next_colli,next_parti,clock=initialize()
    print(clock,next_colli)
    global particles
    global showtime
    while True:
        if base.time5>base.time4>base.time3>base.time2>showtime: #check whether the database need refresh
            continue
        clock+=next_colli
        for a in range(N):
            particles[a][2]=particles[a][2]-next_colli
            particles[a][0]+=particles[a][1]*next_colli
        colli_parti = []
        for (a, b) in next_parti:
            colli_parti += collision(a, b)  # calculate new collision
        base.savedata(particles[:], clock)
        for parti in colli_parti:  # calculate which particle will collision next
            assert particles[parti][2]>=0
            time, target = collision_time(parti)
            particles[parti][2], particles[parti][3] = time, target
            if target >= 0:
                particles[target][2], particles[target][3] = time, parti
        next_colli=88 #a lucky number which is large enough
        next_parti=[]
        for a in range(N): #get the least time and form them into a list
            t=particles[a][2]
            target=particles[a][3]
            if t<next_colli:
                next_colli=t
                next_parti=[(a,target)]
            elif (t==next_colli)and((target,a) not in next_parti):
                next_parti.append((a,target))

def refresh(dt=dt):
    """
    refresh the particles on the screen
    """
    timer.sleep(5)#wait a short period for the database to get ready
    global showtime,particles
    t1,t2=0,0
    while True:
        visual.rate(100)
        data,time=base.getdata(showtime)
        t=showtime-time
        assert t>0
        for i in range(N):
            atoms[i].pos = data[i][0]+data[i][1]*t
            #print("showparticle",data[i][0]+data[i][1]*t,showtime,time,t)
            #atoms[i].pos = data[i][0]
        t1, t2 = t2, timer.clock()
        #print(t2-t1)
        if (t2-t1)<0.01:
            timer.sleep(0.03-t2+t1)
        showtime+=dt

t1 = threading.Thread(target=cycle)
t2 = threading.Thread(target=refresh)
t1.setDaemon(True)
t1.start()
t2.setDaemon(True)
t2.start()

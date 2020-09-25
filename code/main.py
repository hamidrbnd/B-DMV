# -*- coding: utf-8 -*-
"""
Created on Sat May 18 12:48:10 2019

@author: Hamidreza Bandeali
"""

import numpy as np
import time
import math
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import scipy.io
from multiprocessing import Pool
import networkx as nx
import scipy as sp
import pandas as pd

from Pairwise import pairwise
from B_DMV import B_DMV
from AB_DMV1 import AB_DMV1
from AB_DMV2 import AB_DMV2
from network_generator import net_gen

#To determine the type of graph
G=input("There are ten different graph topology for network :\n\
enter 'c' for Complete,\n\
enter 'm' for Mesh,\n\
enter 'g' for Grid,\n\
enter 'e' for Erdos-Reyni\n\
enter 'r' for Ring\n\
enter 'cir' for circular: ")
cir_par=0
if (G == 'cir'):
    cir_par = int(input("Please eneter the second parameter of circular graph : "))
    
#To determine the type of algorithm
algorithm=input("There are four different algorithms :\n\
enter 'p' for pairwise,\n\
enter 'b' for B-DMV,\n\
enter 'a1' for Accelerated B-DMV1,\n\
enter 'a2' for Accelerated B-DMV2\n : ")

#To determine the size of network
number_agent=int(input("Please enter number of agents\n\
**Notice that it should be square of a natural number for mesh and grid one: "))

#To determine the integrity of the number entered
a=math.sqrt(number_agent)  
if( math.sqrt(number_agent)%1 != 0 and (G == 'm' or G == 'g')):
    number_agent =  (int(math.sqrt(number_agent)))**2   

range_ctrl = 0    
range_ctrl = int(input("Please enter '1' if your range is different number of agents or enter '0' if it is different amounts of rho : "))

#To produce adjacency matrix    
d, adj_matrix = net_gen(G, number_agent, cir_par)

#Number of running for an averaging
avg_len = 50

#Range of running
rng_len = 5

#Array for the result of time and message complexity
Msg0=np.zeros(rng_len)#Total number of messages
Msg1=np.zeros(rng_len)#Number of messages in first phase
Msg2=np.zeros(rng_len)#Number of messages in second phase
Opr0=np.zeros(rng_len)#Total number of interactions
Opr1=np.zeros(rng_len)#Number of interactions in first phase
Opr2=np.zeros(rng_len)#Number of interactions in second phase

temp=set()
temp1=list()
temp2=set()

num_maj = int((53/100)*number_agent)


topr0=np.zeros(avg_len)
tmsg0=np.zeros(avg_len)
topr1=np.zeros(avg_len)
tmsg1=np.zeros(avg_len)
topr2=np.zeros(avg_len)
tmsg2=np.zeros(avg_len)

for r_num in range (rng_len) :  
    
    if(range_ctrl == 1): #For different number of agents
        #number of agents in the range of running
        number_agent = (5+3*r_num)*(5+3*r_num)
        adj_matrix = net_gen(G, number_agent, cir_par)    
    else: #For different number of ones
        #number of ones in the range of running
        num_maj = int(((53 + 2*r_num)/100)*number_agent)
      
    for a_num in range (avg_len): #Performing various executions and then averaging them  
        mem = [[set() for x in range(number_agent)] for y in range(number_agent)]
        v = [{0} for i in range(number_agent)]
        list_num_maj = list()
        while((len(list_num_maj))!=num_maj):
            rnd=int(np.random.uniform(0,number_agent,1))
            if(rnd not in list_num_maj):
                list_num_maj.append(rnd)
        for i in range (number_agent):
            mem[i][1]={0}
        for i in range (num_maj):
            v[(int(list_num_maj[i]))]={1}
            mem[(int(list_num_maj[i]))][1]={1}      
        msgcnt=0    
        oprcnt=0
        end=0 #end of algorithm
        p1_end=0 #end of first phase

        while(end==0):
            #countring the number of operations
            oprcnt = oprcnt + 1
            #Starter agent
            init = int(np.random.uniform(0,number_agent,1))
            if(algorithm == 'p'):
                v, mem = pairwise(init , adj_matrix , v , mem)
                msgcnt=msgcnt+2
            elif(algorithm == 'b'):
                msgcnt, v, mem = B_DMV(msgcnt, init , adj_matrix , v , mem)                                
            elif(algorithm == 'a1'):
                msgcnt, v, mem = AB_DMV1(msgcnt, init , adj_matrix , v , mem)                                
            elif(algorithm == 'a2'):
                msgcnt, v, mem = AB_DMV2(msgcnt, init , adj_matrix , v , mem)                                
            #End of total algorithm
            end=1
            for i in range (number_agent):
                if((mem[i][1]!={1})):
                    end=0
                    
            #End of first phase
            if(p1_end==0):
                p1_end=1
                for i in range (number_agent):
                    if((len(v[i])==1)):
                        if(v[i]!={1}):
                            p1_end=0  
                if(p1_end==1):
                    topr1[a_num]=oprcnt
                    tmsg1[a_num]=msgcnt
                
        topr0[a_num]=oprcnt
        tmsg0[a_num]=msgcnt
        topr2[a_num]=oprcnt-topr1[a_num]
        tmsg2[a_num]=msgcnt-tmsg1[a_num]    

    Opr0[r_num]=np.mean(topr0)/number_agent
    Msg0[r_num]=np.mean(tmsg0)
    
    Opr1[r_num]=np.mean(topr1)/number_agent
    Msg1[r_num]=np.mean(tmsg1)
    
    Opr2[r_num]=np.mean(topr2)/number_agent
    Msg2[r_num]=np.mean(tmsg2)
        


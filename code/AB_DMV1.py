# -*- coding: utf-8 -*-
"""
Created on Sat May 18 17:53:34 2019

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

temem=list()

def AB_DMV1(msgcnt, init,adj_matrix,v,mem):
    tmp_choice=list()
    neighbor = [i for i,val in enumerate(adj_matrix[init]) if val==1] #list of neighbors of agent init
    for i in range (len(neighbor)):
        tmp_choice=tmp_choice+list(v[neighbor[i]])
    #for these algorithm    
    tmp_rpt = [tmp_choice.count(list(set(tmp_choice))[i]) for i in range(len(list(set(tmp_choice))))]
    cntrl_mem = 0
    if(len(tmp_rpt) != 0):
        if(tmp_rpt.count(max(tmp_rpt)) == 1):
            cntrl_mem = 1
            mem_update = {list(set(tmp_choice))[tmp_rpt.index(max(tmp_rpt))]}
    #end    
    msgcnt = msgcnt + len(neighbor) + 1
    for i in range(len(neighbor)):
        resp = np.random.choice(neighbor)
        neighbor.remove(resp)
        if(len(tmp_choice)!=0):    
            temp = list(set(tmp_choice))
            v[resp] = set(tmp_choice)
            mem[resp][len(v[resp])]=v[resp]
            for j in range(len(temp)):
                tmp_choice.remove(temp[j])
        else:
            v[resp] = set()
            mem[resp][len(v[resp])]=v[resp]
      
    if(cntrl_mem == 1):
        neighbor = [i for i,val in enumerate(adj_matrix[init]) if val==1]
        for i in range(len(neighbor)):
            mem[neighbor[i]][len(mem_update)] = mem_update
            
    return msgcnt, v, mem
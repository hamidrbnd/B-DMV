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


def pairwise(init,adj_matrix,v,mem):
    resp = np.random.choice([i for i,val in enumerate(adj_matrix[init]) if val==1 and i != init],1)[0]
    vor=v[init]|v[resp]
    vand=v[init]&v[resp]
    if((len(v[init]))<=(len(v[resp]))):
        v[init]=vor
        v[resp]=vand
        mem[init][len(v[init])]=v[init]
        mem[resp][len(v[resp])]=v[resp]
    else:
        v[init]=vand
        v[resp]=vor
        mem[init][len(v[init])]=v[init]
        mem[resp][len(v[resp])]=v[resp]
    return v, mem
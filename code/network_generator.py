# -*- coding: utf-8 -*-
"""
Created on Sat May 18 18:01:01 2019

@author: Jahan
"""

import numpy as np
import math
import networkx as nx

def net_gen(graph, n_agent, cir_par):
    ln=int(math.sqrt(n_agent))
    adj_matrix = [[0 for x in range(n_agent)] for y in range(n_agent)]
    
    ### For complete graph
    if(graph=='c'):
        adj_matrix = [[1 for x in range(n_agent)] for y in range(n_agent)]
        d=n_agent-1
    
    ### For Ring graph
    if(graph=='r'):
        G = nx.generators.classic.circulant_graph(n_agent, [1])
        A = nx.adjacency_matrix(G)
        b=A.todense()
        adj_matrix=b.tolist()
        for i in range(n_agent):
            adj_matrix[i][i]=1
        d=2
    
    ### For Erdos-Renyi graph
    if(graph=='e'):
        G = nx.generators.erdos_renyi_graph(n_agent, 0.3, seed=None, directed=False)
        nx.draw_circular(G)
        A = nx.adjacency_matrix(G)
        b=A.todense()
        adj_matrix=b.tolist()
        for i in range(n_agent):
            adj_matrix[i][i]=1
        d=20
                
        
    ### For Mesh graph
    if(graph=='m'):
        G = nx.generators.grid_2d_graph(ln, ln, periodic=False, create_using=None)
        #nx.draw_circular(G)
        Adj = nx.adjacency_matrix(G)
        Adj_m = Adj.todense()
        adj_matrix = Adj_m.tolist()
        for i in range(n_agent):
            adj_matrix[i][i]=1
            if(i==0):
                adj_matrix[0][ln-1]=1
                adj_matrix[0][n_agent-ln]=1              
            elif(i==ln-1):
                adj_matrix[ln-1][0]=1
                adj_matrix[ln-1][n_agent-1]=1
            elif(i==n_agent-ln):
                adj_matrix[n_agent-ln][0]=1
                adj_matrix[n_agent-ln][n_agent-1]=1   
            elif(i==n_agent-1):    
                adj_matrix[n_agent-1][ln-1]=1
                adj_matrix[n_agent-1][n_agent-ln]=1    
            elif((i>0)and(i<ln-1)):
                adj_matrix[i][i+n_agent-ln]=1
            elif((i>n_agent-ln)and(i<n_agent-1)):
                adj_matrix[i][i-n_agent+ln]=1
            elif((i%ln==0)):
                adj_matrix[i][i+ln-1]=1
            elif(((i+1)%ln==0)):
                adj_matrix[i][i-ln+1]=1
        d=4
                
        
    ### For Grid graph
    if(graph=='g'):
        G = nx.generators.grid_2d_graph(ln, ln, periodic=False, create_using=None)
        #nx.draw_circular(G)
        Adj = nx.adjacency_matrix(G)
        Adj_m = Adj.todense()
        adj_matrix = Adj_m.tolist()
        for i in range(n_agent):
            adj_matrix[i][i]=1
        d=20
    
### For Circular graph
    if(graph=='cir'):
        G = nx.generators.classic.circulant_graph(n_agent, [1,cir_par])
        nx.draw_circular(G)
        A = nx.adjacency_matrix(G)
        b=A.todense()
        adj_matrix=b.tolist()
        for i in range(n_agent):
            adj_matrix[i][i]=1
        d=1+int(cir_par!=0)

    return d, adj_matrix
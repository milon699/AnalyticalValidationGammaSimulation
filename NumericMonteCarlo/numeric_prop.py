# -*- coding: utf-8 -*-
"""
Created on Wed Nov 24 15:32:51 2021

@author: milon
"""

import numpy as np


N = 10
c_c = np.zeros(6)

L = np.log(2)

Sigma_C = 0.3
Sigma_PP = 0.5
Sigma_PH = 0.2
Sigma_TOT = Sigma_C + Sigma_PP + Sigma_PH

#----------Left hand side of the tree (only Compton + escape and the last node's absorption------)

def compton_paths(r_in, L, coll = 0):
    #in case of a collision
    if r_in < L and coll != 5:
        #count collisions and check if the sum with another random number is still within the detector
        coll += 1
        r_out = np.random.exponential(1)
        coll = compton_paths(r_out, L-r_in, coll)        
    return coll

for i in range(N):
    r = np.random.exponential(1)       
    coll = compton_paths(r, L)
    c_c[coll] += 1
    
    
P = c_c/N 
cross_section = np.array([Sigma_TOT, Sigma_C, Sigma_C**2, Sigma_C**3, Sigma_C**4, Sigma_C**4*(Sigma_PH+Sigma_PP)])  

P = cross_section*P
for i in range(len(P)-1):
    print("The probability for {} Compton collision(s) + escape is {:.8f}".format(i, P[i]))

print("The probability for 4 Compton collisions + any absorption is {:.8f}".format(P[5]))

#-----------now consider pair production------------------------------------------

c_pp = 0
for i in range(N):
    r_in = np.random.exponential(1)
    if r_in < L:
        r_out_fw = np.random.exponential(1)
        r_out_up = np.random.exponential(1)
        if r_out_fw > L - r_in and r_out_up > L:
            c_pp += 1

P_pp = c_pp/N*Sigma_PP

print("The probability is {:.8f}".format(P_pp))
            
            
            



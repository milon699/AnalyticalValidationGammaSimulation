# -*- coding: utf-8 -*-
"""
Created on Wed Jan 26 09:09:06 2022

@author: milon
"""

import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.size'] = 25.0
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['font.weight'] = 'bold'
plt.rcParams['axes.labelsize'] = 'medium'
plt.rcParams['axes.labelweight'] = 'bold'
plt.rcParams['axes.linewidth'] = 1.2
plt.rcParams['lines.linewidth'] = 0.3


data = np.loadtxt('results_openmc_multilayered.txt')

PHT = np.zeros((100, 33))
for i in range(100):
    PHT[i] = data[i*33:33*(i+1)]   
    
#Calculate mean and std  
mean = np.zeros(33)
std = np.zeros(33)

for i in range(33):
    mean[i] = np.mean(PHT[:,i])
    std[i] = np.std(PHT[:,i])

for i in range(33):
    if mean[32-i] <= 0.000000000000001:
        mean = np.delete(mean, 32-i)
        std = np.delete(std, 32-i)
    
print('This are the mean values\n {}'.format(mean))

print('This are the std \n {}'.format(std))

#Comparison to Sood 2004

Sood04 = np.array([0.56116619, 0.02409558, 0.06195740, 0.02156830, 0.049044545, 0.00280990, 0.01297187, 0.00226777,
                   0.10942557, 0.02979685, 0.01372311, 0.03354201, 0.00528230, 0.01193924, 0.00302856, 0.0573804])
    
analy_0 = {0: 0.561329022358257,
 0.2: 0.0237685679449077,
 0.4: 0.0630209468948048,
 0.6: 0.0197690310224596,
 0.8: 0.0499450800617007,
 1.0: 0.00280989550115659,
 1.2: 0.0130114829651646,
 1.4: 0.00218852928949916,
 1.6: 0.109465181289042,
 2.0: 0.0303790151051969,
 2.2: 0.0125587643222950,
 2.4: 0.0342983395143937,
 2.6: 0.00500296971417419,
 2.8: 0.0120878716787918,
 3.0: 0.00287259688207117,
 3.2: 0.0574927054560848}

analy = np.array(list(analy_0.values()))

energy = np.array(list(analy_0.keys()))

plt.close('all')
fig, axarray = plt.subplots(2, 1, figsize=(10,5), sharex=True, gridspec_kw={'height_ratios': [2, 1]}) #sharex = geteilte xAchse
axarray[0].bar(energy+0.025, mean, width = 0.05, color="red", label = "OpenMC")
axarray[0].bar(energy-0.025, analy, width = 0.05, color='green', label = "Analytical")
axarray[1].errorbar(energy, mean-analy, yerr=std, color='black', fmt='.', marker='o', markeredgecolor='black', linewidth=1.5, label = '$\u03C3_{OC}$')
axarray[1].axhline(y=0, color='black', linestyle='--', linewidth=2)
axarray[0].set_ylabel('Pulse height')
axarray[0].set_yscale('log')
axarray[1].set_ylabel('\u0394PHT')
axarray[1].set_xlabel('Energy in MeV')
axarray[0].grid()
axarray[0].legend()
axarray[1].legend(loc="upper right", ncol=1)



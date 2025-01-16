# -*- coding: utf-8 -*-
"""
Created on Wed Jan 26 13:38:52 2022

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


data = np.loadtxt('results_openmc_generalization.txt')

PHT = np.zeros((100, 65))
for i in range(100):
    PHT[i] = data[i*65:65*(i+1)] 
    
#Calculate mean and std  
mean = np.zeros(65)
std = np.zeros(65)

for i in range(65):
    mean[i] = np.mean(PHT[:,i])
    std[i] = np.std(PHT[:,i])

for i in range(65):
    if mean[64-i] == 0:
        mean = np.delete(mean, 64-i)
        std = np.delete(std, 64-i)
        
        
analy_0 = {0: 0.500000000000000, 1.6: 0.138629436111989, 2.0: 0.0746698950015237, 2.1: 0.0250228622548878, 2.15: 0.0260112277513859, 2.2: 0.0211852814204668, 2.25: 0.00398473435756507, 2.3: 0.00492437756233282, 2.35: 0.00308372437110359, 2.4: 0.0496861803935810, 2.5: 0.00637526853479801, 2.55: 0.00600359053692474, 2.6: 0.00616267799052242, 2.65: 0.00294769963134043, 2.7: 0.00370329558580204, 2.75: 0.00245643826892625, 2.8: 0.0108502851325008, 2.85: 0.000708066831514507, 2.9: 0.00381264383430959, 2.95: 0.00325390115987561, 3.0: 0.00260934740333079, 3.05: 0.000483178150384506, 3.1: 0.000548119830865488, 3.15: 0.000319185711783679, 3.2: 0.102568582172286}


analy = np.array(list(analy_0.values()))

energy = np.array(list(analy_0.keys()))

plt.close('all')
fig, axarray = plt.subplots(2, 1, figsize=(10,5), sharex=True, gridspec_kw={'height_ratios': [2, 1]}) #sharex = geteilte xAchse
axarray[0].bar(energy+0.0125, mean, width = 0.025, color="red", label = "OpenMC")
axarray[0].bar(energy-0.0125, analy, width = 0.025, color='green', label = "Analytical")
axarray[1].errorbar(energy, mean-analy, yerr=std, color='black', fmt='.', marker='o', markeredgecolor='black', linewidth=1.5, label = '$\u03C3_{OC}$')
axarray[1].axhline(y=0, color='black', linestyle='--', linewidth=2)
axarray[0].set_ylabel('Pulse height')
axarray[1].set_ylabel('\u0394PHT')
axarray[1].set_xlabel('Energy in MeV')
axarray[0].set_yscale('log')
axarray[0].grid()
axarray[0].legend(loc="upper center", bbox_to_anchor=(0.2, 1.00))
axarray[1].legend(loc="upper center", bbox_to_anchor=(0.2, 1.00), ncol=1)

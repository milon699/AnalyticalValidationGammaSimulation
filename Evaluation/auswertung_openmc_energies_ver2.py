# -*- coding: utf-8 -*-
"""
Created on Sun Feb  6 17:25:38 2022

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


data = np.loadtxt('results_openmc_energies_ver2.txt')

PHT = np.zeros((100, 173))
for i in range(100):
    PHT[i] = data[i*173:173*(i+1)] 
    
#Calculate mean and std  
mean = np.zeros(173)
std = np.zeros(173)

for i in range(173):
    mean[i] = np.mean(PHT[:,i])
    std[i] = np.std(PHT[:,i])

for i in range(173):
    if mean[172-i] == 0:
        mean = np.delete(mean, 172-i)
        std = np.delete(std, 172-i)
        
analy_0 = {0: 3.71703186841267e-5, 0.6: 4.54975388785209e-5, 0.75: 2.23289114392209e-6, 0.85: 6.82463083177814e-5, 0.9: 0.00245376209001642, 1.05: 0.00252389933744619, 1.0625: 3.79111607876404e-6, 1.16875: 5.81511470600442e-6, 1.2: 0.394959740015041, 1.275: 0.00366633873258673, 1.38125: 1.17157353786733e-5, 1.4875: 0.00539959979503170, 1.59375: 0.00615438864924763, 1.7: 0.584667802357442} 
analy = np.array(list(analy_0.values()))

energy = np.array(list(analy_0.keys()))

plt.close('all')
fig, axarray = plt.subplots(2, 1, figsize=(10,5), sharex=True, gridspec_kw={'height_ratios': [2, 1]}) #sharex = geteilte xAchse
axarray[0].bar(energy+0.0025, mean, width = 0.005, color="red", label = "OpenMC")
axarray[0].bar(energy-0.0025, analy, width = 0.005, color='green', label = "Analytical")
axarray[1].errorbar(energy, mean-analy, yerr=std, color='black', fmt='.', marker='o', markeredgecolor='black', linewidth=1.5, label = '$\u03C3_{OC}$')
axarray[1].axhline(y=0, color='black', linestyle='--', linewidth=2)
axarray[0].set_ylabel('Pulse height')
axarray[1].set_ylabel('\u0394PHT')
axarray[1].set_xlabel('Energy in MeV')
axarray[0].set_yscale('log')
axarray[0].grid()
axarray[0].legend(loc="upper center", bbox_to_anchor=(0.2, 1.00))
axarray[1].legend(loc="upper center", bbox_to_anchor=(0.2, 1.00), ncol=1)

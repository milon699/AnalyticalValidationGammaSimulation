# -*- coding: utf-8 -*-
"""
Created on Sat Jan 22 18:24:15 2022

@author: milon
"""
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.size'] = 15.0
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['font.weight'] = 'bold'
plt.rcParams['axes.labelsize'] = 'medium'
plt.rcParams['axes.labelweight'] = 'bold'
plt.rcParams['axes.linewidth'] = 1.2
plt.rcParams['lines.linewidth'] = 0.3


plt.close('all')

PHT_num =np.array([0.50000054,0.19061027,0.06076106,0.02511863,0.06859774,0.01000618
,0.02417576,0.00574457,0.11498523])

PHT_err = np.array([4.73445782e-05,4.15574443e-05,2.39842346e-05,1.70584144e-05
,2.50403046e-05,9.99079484e-06,1.36697460e-05,7.09027091e-06
,3.10845696e-05])

PHT_num = np.array([0.50002643,0.19062839,0.06076089,0.02510122,0.06862141,0.00999607
,0.02417993,0.00573887,0.11494679])

PHT_err = np.array([4.95950898e-04,3.75398724e-04,2.16506567e-04,1.74584325e-04
,2.50811371e-04,9.46284085e-05,1.59196284e-04,7.82403563e-05
,3.05859482e-04])

PHT_2003 =np.array([0.500000000000000, 0.190615474653985, 0.0607580302103937, 0.0251175286445900, 0.0685966790287873, 0.0100059394283484, 0.0241757433575836, 0.00574519376414233, 0.114985410912170])

PHT_2004 =np.array([0.5, 0.190615, 0.059594, 0.027446, 0.067084, 0.010565, 0.023878, 0.006057, 0.114760])

energy =np.array([0, 1.6, 2.0, 2.2, 2.4, 2.6, 2.8, 3.0, 3.2])

plt.close('all')
fig, axarray = plt.subplots(2, 1, figsize=(10,5), sharex=True, gridspec_kw={'height_ratios': [2, 1]}) #sharex = geteilte xAchse
axarray[0].bar(energy-0.025, PHT_num, width = 0.05, color="red", label = "Numerical")
axarray[0].bar(energy+0.025, PHT_2003, width = 0.05, color='green', label = "ProbTree/Sood2003")
axarray[1].errorbar(energy, PHT_num-PHT_2003, yerr=PHT_err, color='black', fmt='.', marker='o', markeredgecolor='black', linewidth=1.5, label = '$\u03C3_{num}$')
axarray[1].axhline(y=0, color='black', linestyle='--', linewidth=2)
axarray[0].set_ylabel('Pulse height', fontsize = 20)
axarray[1].set_ylabel('\u0394PHT', fontsize = 20)
axarray[1].set_xlabel('Energy in MeV', fontsize = 20)

axarray[0].grid()
axarray[0].legend(fontsize = 20)
axarray[1].legend(loc="upper center", bbox_to_anchor=(0.2, 1.00), ncol=2, fontsize = 17)

fig, axarray = plt.subplots(2, 1, figsize=(10,5), sharex=True, gridspec_kw={'height_ratios': [2, 1]}) #sharex = geteilte xAchse
axarray[0].bar(energy-0.025, PHT_num, width = 0.05, color="red", label = "Numerical")
axarray[0].bar(energy+0.025, PHT_2004, width = 0.05, color = 'green', label = 'Sood2004')
axarray[1].errorbar(energy, PHT_num-PHT_2004, yerr=2*PHT_err, color='black', fmt='.', marker='o', markeredgecolor='black', linewidth=1.5, label = '$2\u03C3_{num}$')
axarray[1].axhline(y=0, color='black', linestyle='--', linewidth=2)
axarray[0].set_ylabel('Pulse height', fontsize = 20)
axarray[1].set_ylabel('\u0394PHT', fontsize = 20)
axarray[1].set_xlabel('Energy in MeV', fontsize = 20)
axarray[0].grid()
axarray[0].legend(fontsize = 20)
axarray[1].legend(loc="upper center", bbox_to_anchor=(0.2, 1.00), ncol=2, fontsize = 17)
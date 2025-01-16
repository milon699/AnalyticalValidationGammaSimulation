# -*- coding: utf-8 -*-
"""
Created on Wed Jan 26 13:38:52 2022

@author: milon
"""

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as mticker

plt.rcParams['font.size'] = 20.0
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['font.weight'] = 'bold'
plt.rcParams['axes.labelsize'] = 'medium'
plt.rcParams['axes.labelweight'] = 'bold'
plt.rcParams['axes.linewidth'] = 1.2
plt.rcParams['lines.linewidth'] = 0.3




mean =  np.array([0.56129066,0.02377495,0.06302373,0.01977156,0.04995287,0.0028113
,0.01300355,0.00218707,0.1094734,0.03036055,0.01256979,0.03432312
,0.00499659,0.01210236,0.00286827,0.05749022] )

std = np.array( [3.43413335e-04,1.04759739e-04,1.38512062e-04,6.24820467e-05
,1.01626500e-04,1.87570446e-05,4.78052859e-05,1.49473396e-05
,1.92905287e-04,1.30669146e-04,8.22827529e-05,1.29489922e-04
,5.43542489e-05,7.85705363e-05,3.76008382e-05,1.86325076e-04])
        
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

Sood04 = np.array([0.561166189, 0.0240955759, 0.061957400, 0.0215683040, 0.0490454497,
          0.0028098961, 0.0129718688, 0.0022677653, 0.1094255676, 0.0297968460,
          0.0137231110, 0.0335420060, 0.0052822959, 0.0119392397, 0.0030285574,
          0.0573802425])

analy = np.array(list(analy_0.values()))

energy = np.array(list(analy_0.keys()))

plt.close('all')
fig, axarray = plt.subplots(2, 1, figsize=(10,5), sharex=True, gridspec_kw={'height_ratios': [2, 1]}) #sharex = geteilte xAchse
axarray[0].bar(energy+0.025, mean, width = 0.05, color="red", label = "Numerical")
axarray[0].bar(energy-0.025, analy, width = 0.05, color='green', label = "ProbTree")
axarray[1].errorbar(energy, mean-analy, yerr=std, color='black', fmt='.', marker='o', markeredgecolor='black', linewidth=1.5, label = '$\u03C3_{num}$')
axarray[1].axhline(y=0, color='black', linestyle='--', linewidth=2)
axarray[0].set_ylabel('Pulse height')
axarray[0].set_yscale('log')
axarray[1].set_ylabel('\u0394PHT')
axarray[1].set_xlabel('Energy in MeV')
axarray[0].grid()
axarray[0].legend()
axarray[1].legend(loc="lower right", ncol=1, fontsize = 17)


fig, axarray = plt.subplots(2, 1, figsize=(10,5), sharex=True, gridspec_kw={'height_ratios': [2, 1]}) #sharex = geteilte xAchse
axarray[0].bar(energy+0.025, mean, width = 0.05, color="red", label = "Numerical")
axarray[0].bar(energy-0.025, Sood04, width = 0.05, color='green', label = "Sood2004")
axarray[1].errorbar(energy, mean-Sood04, yerr=3*std, color='black', fmt='.', marker='o', markeredgecolor='black', linewidth=1.5, label = '$3\u03C3_{num}$')
axarray[1].axhline(y=0, color='black', linestyle='--', linewidth=2)
axarray[0].set_ylabel('Pulse height')
axarray[0].set_yscale('log')
axarray[1].set_ylabel('\u0394PHT')
axarray[1].set_xlabel('Energy in MeV')
axarray[0].grid()
axarray[0].legend()
axarray[1].legend(loc="lower right", ncol=1, fontsize = 17)

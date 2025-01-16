# -*- coding: utf-8 -*-
"""
Created on Thu Dec  9 15:34:08 2021

@author: Milon Miah
"""
#This is a class providing tools to build up the probability tree for given parameters

from particle import Particle
import numpy as np
import sympy as sp
from anytree import AnyNode
from anytree.exporter import UniqueDotExporter
from anytree.search import findall
import operator
from tqdm import tqdm

class ProbTree(object):
    
    #constructor
    def __init__(self, e_ini, e_cut, e_th, l, r, sigma_C, sigma_PP, sigma_PH):
        self.E_ini = e_ini
        self.E_cut = e_cut
        self.E_th = e_th
        self.L = l
        self.R = r
        self.Sigma_C = sigma_C
        self.Sigma_PP = sigma_PP
        self.Sigma_PH = sigma_PH
        self.Sigma_TOT = round(sigma_C + sigma_PP + sigma_PH, 10)
        x = sp.Symbol('x')
        self.P = Particle(e_ini)
        self.Root = self.create_Node(PULSE = 0, E = [self.P.Energy], D = [self.P.Direction])
        self.buildTree(self.P, self.Root)

    #function to create nodes from AnyNode (handy for default variables)
    def create_Node(self, PULSE, E, D, parent = None, color = "black", interac = [[False, False, False, False]]):
        return AnyNode(id = PULSE, E = E, D = D, parent = parent, color = color, interac = interac)
    
    #function to implement the tree for possible particle histories
    def mergeTree(self, node1, node2, root):
        
        #create the merged node with corresponding properties
        newroot = self.create_Node(PULSE = round(node1.id+node2.id, 10), E = np.append(node1.E, node2.E), D = np.append(node1.D, node2.D), parent = root, interac = node1.interac + node2.interac)
        
        #save the children in handy variables
        c1 = node1.children
        c2 = node2.children
        
        #merge subtrees if the children of node1 and node2 are not already leafs
        if self.children_are_leafs(node1) == False or self.children_are_leafs(node2) == False:
            if c2 == ():
                for i in range(len(c1)):
                    self.mergeTree(c1[i], node2, newroot)
            elif c1 == ():
                for j in range(len(c2)):
                    self.mergeTree(node1, c2[j], newroot)
            else:
                for i in range(len(c1)):
                    for j in range(len(c2)):
                        self.mergeTree(c1[i], c2[j], newroot)        
        
        #if all children are leafs create corresponding leaf nodes
        else:
            if c1 != () or c2 != ():
                leafs1, no_leafs1 = self.count_leafs(node1)
                leafs2, no_leafs2 = self.count_leafs(node2)    
                for f in range(no_leafs1):
                    for k in range(no_leafs2):
                       PHT = round(leafs1[f].id + leafs2[k].id, 10) 
                       self.create_Node(PULSE = PHT, E = np.append(leafs1[f].E, leafs2[k].E) , D = np.append(leafs1[f].D, leafs2[k].D), parent = newroot, interac = leafs1[f].interac + leafs2[k].interac) 
        return newroot

    def buildTree(self, p, root, PHT = 0):
        #set energy before any collision back to its root values
        p.set_energy(root.E[0])
        PHT = root.id
        
        #COMPTON collision, threshold energy corresponding
        if p.Energy >= (2*self.E_cut) and self.Sigma_C != 0: 
            PHT += p.Energy/2
            p.comp()
            K = self.create_Node(PULSE = round(PHT, 10), E = [p.Energy], D = [p.Direction], parent = root, color = "LightBlue")
            K.interac = [[True, False, False, False]]
            self.buildTree(p, K, PHT)  
            
        p.set_energy(root.E[0])
        PHT = root.id
        
        #PAIR PRODUCTION, threshold energy corresponding
        if p.Energy >= (4*self.E_cut) and self.Sigma_PP != 0: 
            PHT += p.Energy/2
            p_sec = p.pairp(self.E_th)
            
            #creating both nodes for the two created particles and apply buildTree() again
            left = self.create_Node(PULSE = round(PHT, 10), E = [p.Energy], D = [p.Direction], parent = None,  color= "DarkBlue")
            left.interac = [[False, True, False, False]]
            self.buildTree(p, left, PHT)
            right = self.create_Node(PULSE = 0, E = [p_sec.Energy], D = [p_sec.Direction], parent = None, color = "DarkBlue")
            right.interac = [[False, True, False, False]]
            self.buildTree(p_sec, right, 0)
            
            #merge two nodes of left and right node
            self.mergeTree(left, right, root)
        
        p.set_energy(root.E[0]) 
        PHT = root.id
        
        #ESCAPE, create corresponding node (leaf, so no recursion here)
        K = self.create_Node(PULSE = round(PHT, 10), E = [p.Energy], D = [p.Direction], parent = root)
        K.interac = [[False, False, True, False]]
        
        #radial or axial exit -> different edge color
        if p.Direction == 0: 
            K.color = "green"
        else:
            K.color = "orange"
        
        #ANY ABSORPTION (if threshold energy for C or PP is not reached, also absorption occurs)
        PHT += p.Energy
        p.ph_elec()
        K = self.create_Node(PULSE = round(PHT, 10), E = [p.Energy], D = [p.Direction], parent = root, color= "red")
        K.interac = [[False, False, False, True]]
        
    #count paths
    def count_leafs(self, root):
        leafs = findall(root, filter_=lambda node: node.is_leaf)
        
        return leafs, len(leafs)
    
    #An important function for recursive mergeTree() function
    def children_are_leafs(self, node):
        boolean = True
        for i in range(len(node.children)):
            if node.children[i].is_leaf == False:
                boolean = False
                break
        return boolean
    
    #Gives the paths in one single array, without root node
    def paths(self):
        paths = []
        leafs, counts = self.count_leafs(self.Root)
        for i in range(len(leafs)):
            #add leafs to the path
            path = np.append(np.array(leafs[i].ancestors), leafs[i])
            path = np.delete(path, 0)
            #put them together in one list
            paths.append(np.array(path))
        return paths
    
    
    #Create a handy animation
    #color edges
    def edgeattrfunc(self, node, child):
        return 'color="{}"'.format(child.color)
    
    #function to properly set up the nodes' labels
    def label(self, node):
        label = 'label=<'
        for i in range(len(node.E)):
            label += 'E_{} = {}, {}°'.format(i+1, node.E[i], node.D[i]) 
            if i+1 != len(node.E):
                label += '<br />'
        if node.is_leaf == True:
            label += '<br /> <FONT COLOR="red">PHT = {} </FONT>'.format(node.id)
        label += '>, fontsize=9'
        return label
    
    #Convert nodes structure into a graphviz dotfile
    def create_dotfile(self, string):
            UniqueDotExporter(self.Root, nodeattrfunc=lambda n: self.label(n), 
                      edgeattrfunc=self.edgeattrfunc).to_dotfile(string)
            
#----------- Probabilities ----------------------------------------------------       
    #calculate the factorial of a given integer
    def fac(self, n):
        factorial = 1
        if int(n) >= 1:
            for i in range(1, int(n)+1):
                factorial = factorial * i
        return factorial        

    #calculate the convolution of arbitrary functions
    def convolution(self, f, g):
        x = sp.Symbol('x')
        y = sp.Symbol('y')
        return sp.integrate(f.subs(x, y)*g.subs(x, x-y), (y, 0, x))

    #function to obtain the corresponding pdf function
    def pdf(self, k):
        x = sp.Symbol('x')
        f = [self.Sigma_TOT*sp.exp(-self.Sigma_TOT*x)]
        for i in range(k):
            if i == 0:
                f.append(self.convolution(f[i], f[i]))
            else:
                f.append(self.convolution(f[i], f[0]))
        return f[k-1]

    
    #calculate the corresponding probability
    #probability for an absorption adter k collisions

    def P_A(self, y, k):
        sums = 0
        for i in range(k):
            sums += (y*self.Sigma_TOT)**i/self.fac(i)
        return 1 - sp.exp(-self.Sigma_TOT*y)*sums
    
    #probability for an escape after k Kollisions
    def P_E(self, y, k):
        return sp.exp(-self.Sigma_TOT*y)*(self.Sigma_TOT*y)**k/self.fac(k)          
    
    def adapt_L(self, node, no_p, history, N_pp):
        K = len(history)
        if node.D[no_p] % 360 == 0:
            
            if K % 4 != 1:
                history[K-2] = history[K-2]+history[K-1]
                history = np.delete(history, K-1) 
            
            r_new = 0
            for i in range(int((N_pp-1)/2+1)):
                r_new += (-1)**i*history[2*i]
                
        elif node.D[no_p] % 360 == 90: 
            
            if K % 4 != 2:
                history[K-2] = history[K-2]+history[K-1]
                history = np.delete(history, K-1)
            
            r_new = self.R
            for i in range(int((N_pp-2)/2+1)):
                r_new += (-1)**i*history[2*i+1]
                  
        elif node.D[no_p] % 360 == 180:
            
            if K % 4 != 3:
                history[K-2] = history[K-2]+history[K-1]
                history = np.delete(history, K-1)
            
            r_new = self.L
            for i in range(int((N_pp-1)/2+1)):
                x_ind = sp.Symbol('x_{}'.format(2*i+1))
                r_new += (-1)**(i+1)*history[2*i]
        
        elif node.D[no_p] % 360 == 270:
            
            if K % 4 != 4:
                history[K-2] = history[K-2]+history[K-1]
                history = np.delete(history, K-1)
            
            r_new = self.R
            for i in range(int((N_pp-2)/2+1)):
                    
                    r_new += (-1)**(i+1)*history[2*i+1]
                  
        return r_new, history
            
    #function to calculate the probability of a single path
    def prob_path(self, path, l, r, sigma = 1, k = 0, no_p = 0, history = np.array([]), N_pp = 0, c_var = 0):
        for i in range(len(path)):
            
            po = 0
            if len(path[i].parent.E) != len(path[i].E):
                for q in range(no_p):
                    if path[i].interac[q+po][1] == True and path[i].interac[q+po+1][1] == True:
                        po += 1
                no_p += po    
      
            # in case of Compton scattering
            if path[i].interac[no_p][0] == True:
                k += 1
                sigma = sigma * self.Sigma_C/self.Sigma_TOT
                
            #in case of pair production
            elif path[i].interac[no_p][1] == True:
                                
                k += 1
                sigma = sigma * self.Sigma_PP/self.Sigma_TOT
                
                if path[i].E[no_p]*4 >= self.E_th:
                    N_pp += 1
                    c_var += 1
                    var = sp.Symbol('x_{}'.format(c_var))
                    history = np.append(history, var)
                    
                    r_new, history = self.adapt_L(path[i], no_p, history, N_pp)
                    
                    P_1 = self.P_E(var, k-1)
                    P_2 = self.prob_path(path[i+1:], r, r_new,  sigma = 1, k = 0, no_p = no_p + 1, history = history, N_pp = N_pp, c_var = c_var)
                    P_3 = self.prob_path(path[i+1:], l-var, r, sigma = 1, k = 0, no_p = no_p, history = history, N_pp = N_pp - 1, c_var = c_var)
                    
                    #integrate over all possible var
                    proba = sp.integrate((self.Sigma_TOT*P_1*P_2*P_3).expand(), (var, 0, l))
                    proba = proba *sigma
                    break
                        
                #if E < 1 MeV
                else: 
                    z = sp.Symbol('z')
                    
                    #find the probabilities of all particle histories for arbitrary location y where PP occurs
                    P_1 = self.P_E(z, k-1)
                    P_2 = self.prob_path(path[i+1:], l-z, r, sigma = 1, k = 0, no_p = no_p, N_pp = N_pp)
                    P_3 = self.prob_path(path[i+1:], l-z, r, sigma = 1, k = 0, no_p = no_p + 1, N_pp = N_pp)
                    
                    #integrate over all possible z
                    proba = sp.integrate((self.Sigma_TOT*P_1*P_2*P_3).expand(), (z, 0, l))
                    proba = proba * sigma
                    break
                
            #in case of escape
            elif path[i].interac[no_p][2] == True:                
                proba = self.P_E(l, k)
                proba = proba* sigma
                break
            #in case of absorption
            else: 
                k += 1
               
                #adapt absorption cross-section, depending on the reaction leading to a killed photon
                if path[i].parent.E[no_p - po] >= (4*self.E_cut):
                    sigma = sigma*self.Sigma_PH/self.Sigma_TOT
                elif (2*self.E_cut) <= path[i].parent.E[no_p - po] < (4*self.E_cut):
                    sigma = sigma*(self.Sigma_PH+self.Sigma_PP)/self.Sigma_TOT
                else:
                    sigma = sigma*self.Sigma_TOT/self.Sigma_TOT
                    
                #probability for absorption after k collisions    
                proba = self.P_A(l, k)
                proba = proba*sigma
                break
        return proba.evalf()
    
    #save the probabilites in a handy array
    def prob_tree(self):
        Pr = []
        paths = self.paths()
        print("The analytical probabilties are being calculated ...")
        for i in tqdm(range(len(paths)), position = 0):
            #print(i)
            pr = self.prob_path(paths[i], self.L, self.R)
            Pr.append(pr)
        return Pr
           
    #now count how many different PHT values occur and put them in an array
    def prob_PHT(self):
        Pr = self.prob_tree()
        leafs, counts = self.count_leafs(self.Root)

        #finally add up the calculated probabilites to the corresponding PHT values
        #create a dictionary for handy access to data
        P_PHT = {}

        for i in range(len(leafs)):
            PHT = leafs[i].id 
            if PHT not in P_PHT.keys():
                P_PHT[PHT] = Pr[i]
            else: 
                P_PHT[PHT] += Pr[i]
        
        #sort dictionary
        P_PHT = dict(sorted(P_PHT.items(), key=operator.itemgetter(0)))

        #display also the sum of the probabilities
        P_sum = 0
        for key in P_PHT:
            P_sum += P_PHT[key]
        P_PHT['SUM'] = P_sum
        
        return P_PHT
        
    def create_dist(self):
        return np.random.exponential(1/self.Sigma_TOT, 1)[0]
        
    def particle_run(self, length, radius, E, history = np.array([]), N_pp = 0):
        pht = 0
        
        if E < self.E_cut:
            return pht + E
        
        k = "on"
        
        while k == "on":
            dis = self.create_dist()
            
            if dis > length:
                return pht
            
            length -= dis
            
            reaction_prob = np.random.random()
            if(0.0 <= reaction_prob < self.Sigma_PH/self.Sigma_TOT):
                pht += E
                return pht
            
            elif (self.Sigma_PH/self.Sigma_TOT <= reaction_prob < (self.Sigma_PH+self.Sigma_C)/self.Sigma_TOT):
                pht += E/2
                E = E/2
                
            elif ((self.Sigma_C+self.Sigma_PH)/self.Sigma_TOT <= reaction_prob < 1.0) and (E >= self.E_th):
                history = np.append(history, dis)
                K = len(history)
                N_pp += 1
                pht += E/2
                k = "off"
                if N_pp % 4 == 1:
                    if K % 4 != 1:
                        history[K-2] = history[K-2]+history[K-1]
                        history = np.delete(history, K-1)
                    new_radius = 0
                    for i in range(int((N_pp-1)/2)+1):
                        new_radius += (-1)**i*history[2*i]
                elif N_pp % 4 == 2:
                    if K % 4 != 2:
                        history[K-2] = history[K-2]+history[K-1]
                        history = np.delete(history, K-1)
                    new_radius = self.R
                    for i in range(int((N_pp-2)/2)+1):
                        new_radius += (-1)**i*history[2*i+1]
                elif N_pp % 4 == 3:
                    if K % 4 != 3:
                        history[K-2] = history[K-2]+history[K-1]
                        history = np.delete(history, K-1)
                    new_radius = self.L
                    for i in range(int((N_pp-1)/2)+1):
                        new_radius += (-1)**(i+1)*history[2*i]
                elif N_pp % 4 == 0:
                    if K % 4 != 4:
                        history[K-2] = history[K-2]+history[K-1]
                        history = np.delete(history, K-1)
                    new_radius = self.R
                    for i in range(int((N_pp-2)/2)+1):
                        new_radius += (-1)**(i+1)*history[2*i+1]
                
                pht += self.particle_run(radius, new_radius, E/4, history = history, N_pp = N_pp) + self.particle_run(length, radius, E/4, history = history, N_pp = N_pp - 1)
                
            elif ((self.Sigma_C+self.Sigma_PH)/self.Sigma_TOT <= reaction_prob < 1.0) and (E < self.E_th):
                pht += E/2
                k = "off"
                pht += self.particle_run(length, radius, E/4, N_pp = N_pp) + self.particle_run(length, radius, E/4, N_pp = N_pp )
                
            if E < self.E_cut:
                return pht + E
            
        return pht

    def prob_num(self, N, step = None):
        if step == None:
            step = N
        print("The numerical probabilties are being calculated ...")
        counter_dic = {}
        for i in tqdm(range(N + 1), position = 0):
            pht = np.round(self.particle_run(self.L, self.R, self.E_ini, history = []), 10)
            if pht not in counter_dic.keys():
                counter_dic[pht] = 1
            else:
                counter_dic[pht] += 1  
            if (i>0) and (i % step) == 0:
                print('\n')
                print(i)
                counter_dic = dict(sorted(counter_dic.items(), key=operator.itemgetter(0)))
                total = sum(counter_dic.values(), 0.0)
                prob_dic = {k: v / total for k, v in counter_dic.items()}
                for j in prob_dic:
                    print(str(j).ljust(5), prob_dic[j])
        
        return prob_dic
            
        
            
    def particle_run_ax(self, length, radius, E):
        distance_ahead = length
      
        
        if E < self.E_cut:
            return 0
        
        k = "on"
        
        while k == "on":
            dis = self.create_dist()
            
            if dis > distance_ahead:
                return E
            
            
            distance_ahead -= dis
            
            reaction_prob = np.random.random()
            if(0.0 <= reaction_prob < self.Sigma_PH/self.Sigma_TOT):
                return 0
            
            elif (self.Sigma_PH/self.Sigma_TOT <= reaction_prob < (self.Sigma_PH+self.Sigma_C)/self.Sigma_TOT):
                E = E/2
                if E < self.E_cut:
                    return 0
                
            elif ((self.Sigma_C+self.Sigma_PH)/self.Sigma_TOT <= reaction_prob < 1.0) and (E >= self.E_th):
                E = E/4
                if E < self.E_cut:
                    return 0
                              
            elif ((self.Sigma_C+self.Sigma_PH)/self.Sigma_TOT <= reaction_prob < 1.0) and (E < self.E_th):
                k = "off"
                if E/4 < self.E_cut:
                    return 0
                E = self.particle_run_ax(distance_ahead, radius, E/4) + self.particle_run_ax(distance_ahead, radius, E/4)
                if E == 0.4:
                    return 0.2
                
        return E
    
    def prob_num_ax(self, N, step):
        counter_dic = {}
        for i in tqdm(range(N + 1), position = 0):
            E = np.round(self.particle_run_ax(self.L, self.R, self.E_ini), 1)
            if type(E) == np.ndarray:
                if E[0] not in counter_dic.keys():
                    counter_dic[E[0]] = 2
                else:
                    counter_dic[E[0]] += 2
            else:
                if E not in counter_dic.keys():
                    counter_dic[E] = 1
                else:
                    counter_dic[E] += 1  
            
            if (i>0) and (i % step) == 0:
                print('\n')
                print(i)
                counter_dic = dict(sorted(counter_dic.items(), key=operator.itemgetter(0)))
                total = sum(counter_dic.values(), 0.0)
                prob_dic = {k: v / total for k, v in counter_dic.items()}
                for j in prob_dic:
                    print(str(j).ljust(5), prob_dic[j])
        
        return prob_dic
    
    
    
    
    
    
    
    

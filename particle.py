# -*- coding: utf-8 -*-
"""
Created on Sun Nov  7 16:41:37 2021

@author: Milon Miah
"""

#particle class
class Particle(object):
    
    def __init__(self, energy, direction = 0):
        self.Energy = energy
        self.Direction = direction 
    
    #give and set methods to have access to the particles characteristics    
    def get_energy(self):
        return self.Energy
    
    def set_energy(self, new_energy):
        self.Energy = new_energy
    
    def get_direction(self):
        return self.Direction
    
    def set_direction(self, new_direction):
        self.Direction = new_direction
        
    #photoelectric effect (moron absorption)    
    def ph_elec(self):
        self.set_energy(0)
      
    
    #compton effect (odium, secondary particle (not considered that it's actually a different particle), same direction)
    def comp(self):
        self.set_energy(self.Energy/2) 
        
    
    #pair production (kneeon)
    def pairp(self, E_th):
        D = self.Direction
        if self.Energy >= E_th: #MeV
            self.set_energy(self.Energy/4)
            p_sec = Particle(self.Energy, D+90)
        else: 
            self.set_energy(self.Energy/4)
            p_sec = Particle(self.Energy, D)
        
        return p_sec
        
            
            
        

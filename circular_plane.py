#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  7 10:40:44 2021

@author: in2293
"""

class circular_plane:
    
    def __init__(self,x,y,z):
        
        super(circular_plane,self).__init__()
        
        self.x = x
        self.y = y
        self.z = z
        
        N = y.ravel().shape[0]
        H = np.zeros((N,3))
        H[:,0] = x.ravel()
        H[:,1] = y.ravel()
        H[:,2] = np.ones(N)
        self.H = H
        
        
    def call(self,d):
        print(d)
        zcol = self.z.ravel()[None,:].T
        self.params = np.linalg.inv(self.H.T@self.H)@self.H.T@zcol
        
    #def predict(self):
        
     #   self.predictions = self.H@self.params
        
      #  self.MSE = np.mean((self.predictions.ravel()-self.z.ravel())**2)
        

#%%

x = np.random.rand(20)
y = np.random.rand(20)
z = x*3 + y*1 + 2 + np.random.randn(20)/2

C = circular_plane(x,y,z)
C('hi')
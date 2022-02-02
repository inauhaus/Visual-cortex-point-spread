#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  4 16:23:10 2021

@author: in2293
"""

from scipy.io import loadmat
from retinotopy_unwrap import retinotopy_unwrap

fits = loadmat('/Users/in2293/Desktop/Random Matlab code/Data/xt7/xt7_004_001/fits.mat',simplify_cells = True)
xyLocations = loadmat('/Users/in2293/Desktop/Random Matlab code/Data/xt7/xt7_004_001/xyLocations.mat',simplify_cells = True)

fits = fits['fits']
xyLocations = xyLocations['xyLocations']

hor = fits['Hor']['pref_sphase']
vert = fits['Vert']['pref_sphase']

hor_unwrapped, vert_unwrapped = retinotopy_unwrap(hor[1:],vert[1:],xyLocations)
 

#%%
import numpy as np
import matplotlib.pyplot as plt

pix_per_mm = 700/.9  / 1.6
period = 64  #degrees between bars
deg_per_phase = period/360
dom = np.concatenate((xyLocations, np.ones((xyLocations[:,0].shape[0],1))),axis = 1)
dom = dom / pix_per_mm
hor = hor_unwrapped*deg_per_phase
vert = vert_unwrapped*deg_per_phase

y = hor[:,None]
slopes = np.linalg.inv(dom.T@dom)@dom.T@y
H_hat = dom@slopes

H_degpermm_x = slopes[0]
H_degpermm_y = slopes[1]

print(f'dHdx = {H_degpermm_x} dHdy = {H_degpermm_y}')

y = vert[:,None]
slopes = np.linalg.inv(dom.T@dom)@dom.T@y
V_hat = dom@slopes

V_degpermm_x = slopes[0]
V_degpermm_y = slopes[1]

MagFac =  np.sqrt(abs(H_degpermm_x*V_degpermm_y - H_degpermm_y*V_degpermm_x))

print(f'dVdx = {V_degpermm_x} dVdy = {V_degpermm_y}')

print(f'MagFac = {MagFac}')


plt.figure()
plt.subplot(2,1,1)
plt.plot(H_hat,hor,'.')
plt.plot(np.array([0,90]),np.array([0,90]))
plt.subplot(2,1,2)
plt.plot(V_hat,vert,'.')
plt.plot(np.array([0,90]),np.array([0,90]))




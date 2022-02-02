#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""


@author: in2293
"""


import os
import matplotlib.pyplot as plt
import numpy as np


from analyzer_mod import analyzer
from wf_analysis_mod import wf_analyzer





#%% Pick an animal and experiment

#global AUE ACQinfo Analyzer datadir
#global Analyzer

#anim = 'xt7'
#expt = 'u009_004'; #epi ret expt
#ISIflag = 1


#anim = 'xt8'
#expt = 'u003_009' 
#ISIflag = 1
#pixpermm = 79 

anim = 'yd3'
expt = 'u001_002'
pixpermm = 79
ISIflag = 0


#%%


rootanadir = '/Volumes/TOSHIBA EXT/AnalyzerFiles/'

anafname = anim + '_' + expt + '.analyzer'
anapath = os.path.join(*[rootanadir, anim , anafname])

analyzerX = analyzer(anapath) #Create the analyzer object. Uses analyzer file.

#%%

rootdatadir = '/Volumes/TOSHIBA EXT/ISIData/'

datapath = os.path.join(*[rootdatadir,anim,expt])  #Just the folder. Each frame is a separate file.

wfX = wf_analyzer(datapath,analyzerX)  #Create the widefield analysis object.


#%% Set trial averaging window


# #%%


if ISIflag:
    baselineWin = [-500, 500] #ms [start, stop]
    responseWin = [1000,  analyzerX.P['stim_time']*1000+2000]


else:   #GCaMP
    baselineWin = [-500, 0] #ms [start, stop]
    responseWin = [100, analyzerX.P['stim_time']*1000+500]




#%% Select region-of-interest

dum = wfX.loadtrial(0,[1000,1000],analyzerX)
#tcr,Tlim,analyzer)

#dum = GetTrialData([1000 1000],1); #Get a single frame
plt.figure()
plt.imshow(dum)
bw = np.ones(wfX.imsize)

#%%


# Get a baseline and response image for each trial

RMat = np.zeros((wfX.imsize[0],wfX.imsize[1],analyzerX.ntrials));
BMat = np.zeros((wfX.imsize[0],wfX.imsize[1],analyzerX.ntrials));

for tno in range(analyzerX.ntrials):
    
    print(tno)
    Rxt = wfX.loadtrial(tno,responseWin,analyzerX)
    Bxt = wfX.loadtrial(tno,baselineWin,analyzerX)
    
    if ISIflag:              #Invert, b/c ISI is a negative signal.
        bitdepth = 16;  #Pco Panda
        Rxt = 2^bitdepth - Rxt;
  
        
    RMat[:,:,tno] = np.mean(Rxt,axis = 2); #Store the mean response image of this trial
    BMat[:,:,tno] = np.mean(Bxt,axis = 2); #Store the mean baseline image of this trial



#%%


# Or, just subtract baseline on each trial?

#RMat2 = RMat2
#RMat2 = (RMat-BMat) + mean(BMat,3)
RMat2 = (RMat-BMat)/BMat

#%% Organize by condition number

RMat3 = np.zeros((wfX.imsize[0],wfX.imsize[1],analyzerX.nconditions))
BMat3 = np.zeros((wfX.imsize[0],wfX.imsize[1],analyzerX.nconditions))

for c in range(analyzerX.nconditions):
    
    nr = analyzerX.nrepeats(c);
  
    tnos = np.zeros(nr).astype(int)
    for r in range(nr):
        tnos[r] = analyzerX.trialno(c,r)

    RMat3[:,:,c] = np.mean(RMat2[:,:,tnos],axis = 2)  #mean over repeats
    BMat3[:,:,c] = np.mean(BMat[:,:,tnos],axis = 2)
    
    
blankflag = 0
if analyzerX.loops['conds'][-1]['symbol'][0] == 'blank':
    blankflag = 1

#%% All the code up until here could be applied to any experiment.  
# Here is where it starts to assume certain looper variable 

#get the index within the looper
for p in range(len(analyzerX.L['param'])):
    if analyzerX.L['param'][p][0] == 's_phase2':
        phaseDim = p

    if analyzerX.L['param'][p][0] == 'ori2':
        oriDim = p



#valmat is a matrix containing the looper values for each condition

valMat = np.zeros((len(analyzerX.loops['conds'][c]['val']),analyzerX.nconditions-blankflag))
                  
for c in range(analyzerX.nconditions-blankflag):
    for p in range(len(analyzerX.loops['conds'][c]['val'])):
        valMat[p,c] = analyzerX.loops['conds'][c]['val'][p]
        


oridom = list(set(valMat[oriDim,:]))
phasedom = list(set(valMat[phaseDim,:]))


#%% Plot mean response to each condition


plt.figure()
k = 1
for ori in range(len(oridom)):
    for p in range(len(phasedom)):
   
        #id = find(valMat[oriDim,:] == oridom[ori] and valMat[phaseDim,:] == phasedom[p]);
        a = np.where(valMat[oriDim,:] == oridom[ori])[0]
        b = np.where(valMat[phaseDim,:] == phasedom[p])[0]
        id = np.intersect1d(a,b)[0]
        
        imdum = RMat3[:,:,id];
        
        plt.subplot(len(oridom),len(phasedom),k)
  
        
        plt.imshow(imdum*bw)
        
        k += 1

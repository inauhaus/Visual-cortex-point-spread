#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 28 08:59:12 2022

@author: in2293
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.io import loadmat


class wf_analyzer:

    def __init__(self,datadir,analyzer):
        
        self.datadir = datadir
        
        
        try: #to load the first frame
            
            
            
            datapath = datadir + '/' + 'u' + analyzer.M['unit'] + '_' + analyzer.M['expt'] + '_000_f3.mat'
            #loadmat('/Volumes/TOSHIBA EXT/ISIData/yd3/u001_002/u001_002_000_f1.mat',simplify_cells = True)['im']
            
            loadmat(datapath,simplify_cells = True)['im']
            
            print('Data successfully loaded.')
            
            
        except:
            
            print('Could not load a file from this location')
         
            
         
        self.imsize = (analyzer.ACQ['ROIcrop'][3],analyzer.ACQ['ROIcrop'][2])
    
    def ntrialframes(self,analyzer,trialno): #get no. of widefield frames in the trial
    
    
        return len(analyzer.syncInfo[trialno])
    
    
    def loadtrial(self,tcr,Tlim,analyzer):
    
        
        #Tlim is a 2 element vector in ms
        #tcr is a 1 or 2 element list.  If its a one 
        
        def getframeidx(Tlim, trialno, analyzer):
            
        #trialno starts at 0
        
            try:
                STIMfrate = analyzer.frameRate
            except:
                STIMfrate = 60
                print('Frame rate does not exist in Analyzer. Setting to 60Hz')
            
            
            preScreenFlips = round(analyzer.P['predelay']*STIMfrate)
            preDelayEnd = preScreenFlips/STIMfrate
            
            
            aS = analyzer.syncInfo[trialno]
            aS = aS - aS[0]
            
            dS = [0, preDelayEnd]        #Display sync time: beginning of pre delay
            
            sttime = dS[1] + Tlim[0]/1000
            sttime_id = np.argmin(abs(aS-sttime)) #closest acquisition frame to requested start time
            
            endtime = dS[1] + Tlim[1]/1000
            endtime_id = np.argmin(abs(aS-endtime)) #closest acquisition frame to requested end time 
            
            return sttime_id, endtime_id
        
        
        if type(tcr) is int: #if the trial no. is already given
            trialno = tcr
        elif len(tcr) == 2: #if tcr = [condition, repeat], get trial
            trialno = analyzer.loops['conds'].trialno(tcr[0],tcr[1])-1

        #format the trial number string to be like the file name
        s = ['0','0','0']
        s[3-len(str(trialno)):] = str(trialno)
        trialno_str = ''
        for i in s:
            trialno_str += i
        
        
        fname_prefix = self.datadir + '/' + 'u' + analyzer.M['unit'] + '_' + analyzer.M['expt'] +  '_' + trialno_str
        
        
        Flim = [0,0]
        if Tlim[0] == '-inf' and Tlim[1] == 'inf': #get the entire trial
            Flim[0] = 1
            Flim[1] = ntrialframes(analyzer,trialno)
        else:
            Flim = getframeidx(Tlim,trialno,analyzer)
            

        print(Flim)
        print(Tlim)
        #Each frame is its own file
        
        Fdom = np.arange(Flim[0],Flim[1]+1,1)
        Tens = np.zeros((analyzer.ACQ['ROIcrop'][3],analyzer.ACQ['ROIcrop'][2],len(Fdom))) #pre-Allocate
        for i,f in enumerate(Fdom):
            
            fnamedum = fname_prefix + '_' + 'f' + str(f+1) + '.mat'
            Tens[:,:,i] = loadmat(fnamedum,simplify_cells = True)['im']
            

    
        return Tens
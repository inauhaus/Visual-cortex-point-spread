#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 28 09:41:07 2022

@author: in2293
"""


#This module is a set of generic functions used to access and manipulate the .analyzer file


import scipy.io as spio
from scipy import io

import numpy as np


def organizemat(data):
    '''
    this function should be called instead of direct spio.loadmat
    as it cures the problem of not properly recovering python dictionaries
    from mat files. It calls the function check keys to cure all entries
    which are still mat-objects
    
    '''

    def _check_keys(d):
        '''
        checks if entries in dictionary are mat-objects. If yes
        todict is called to change them to nested dictionaries
        '''
        for key in d:
            if isinstance(d[key], spio.matlab.mio5_params.mat_struct):
                #print(key)
                #print(d[key])
                d[key] = _todict(d[key])
        return d

    def _todict(matobj):
        '''
        A recursive function which constructs from matobjects nested dictionaries
        '''
        d = {}
        for strg in matobj._fieldnames:
            elem = matobj.__dict__[strg]
            if isinstance(elem, spio.matlab.mio5_params.mat_struct):
                d[strg] = _todict(elem)
            elif isinstance(elem, np.ndarray):
                d[strg] = _tolist(elem)
            else:
                d[strg] = elem
        return d

    def _tolist(ndarray):
        '''
        A recursive function which constructs lists from cellarrays
        (which are loaded as numpy ndarrays), recursing into the elements
        if they contain matobjects.
        '''

        elem_list = []
        try:
            for sub_elem in ndarray:
                if isinstance(sub_elem, spio.matlab.mio5_params.mat_struct):
                    elem_list.append(_todict(sub_elem))
                elif isinstance(sub_elem, np.ndarray):
                    elem_list.append(_tolist(sub_elem))
                else:
                    elem_list.append(sub_elem)
        except:
            pass

        
        return elem_list
    #data = spio.loadmat(filename, struct_as_record=False, squeeze_me=True)
    
    return _check_keys(data)






class analyzer:
    
    def __init__(self,filepath):
        
        analyzer_all = io.loadmat(filepath, struct_as_record=False, squeeze_me=True) #Loads Matlab .mat file
        analyzer_all = organizemat(analyzer_all)    #Turn Matlab structure into a Python dictionary
        
        Analyzer = analyzer_all['Analyzer'] 
        
        self.M = Analyzer['M']          #dict of values in main window
        self.L = Analyzer['L']          #dict of values in Looper window
        self.loops = Analyzer['loops']  #looper parameters on each trial
        
        #Put the parameter list into a dictionary, 'P', for convenience
        self.P = {}
        for i in Analyzer['P']['param']:
            self.P[i[0]] = i[2]  #first element is always the symbol, 3rd element is always the value
        
        self.stimulus_module = Analyzer['P']['type'] #e.g. 'PG' for periodic grater
        
        #Put acq sync info in a list, each element is the list of frame grab time stamps in a trial
        try: 
            syncInfoAll = []
            for k,v in analyzer_all.items():
                if k[0:4] == 'sync':        
                    syncInfoAll.append(analyzer_all[k]['acqSyncs'])
                    
            self.syncInfo = syncInfoAll
            self.frameRate = analyzer_all['syncInfo1']['frameRate']
        except:
            print('No widefield acquisition time stamps.')
        
        
        self.nconditions = len(self.loops['conds'])
        
        self.ntrials = 0
        for i in self.loops['conds']:
            self.ntrials += len(i['repeats'])
            
            
            
        #Create a dictionary, 'self.ACQ' with the desired keys
        if 'ACQ' in Analyzer: #Only widefield experiments have ACQ.  And some really old WF do not either.
            
            ACQparams = ['FPS', 'bin', 'timecourseBit', 'btwTrialShutter', 'MechbtwTrialShutter',
                'ROIcrop', 'sensorGain','Gamma', 'camera', 'chipSIZE']
            self.ACQ = dict(zip(ACQparams, [None]*len(ACQparams)))
            for k in self.ACQ.keys():
                if k in Analyzer['ACQ']:
                    self.ACQ[k] = Analyzer['ACQ'][k]
                
    def nrepeats(self,c):  #Number of repeats for a given condition
        
        return len(self.loops['conds'][c]['repeats'])
        
    
    def condrep(self,trialno):  #(condition, repeat) index for a given trial index
        
        #N.B. trial no. starts at 1 in the analyzer file, cond and repeat start at 0.
        
        for c in range(self.nconditions):
            
            reps = len(self.loops['conds'][c]['repeats'])
            
            for r in range(reps):
                trialno_cr = self.loops['conds'][c]['repeats'][r]['trialno']-1
                
                if trialno == trialno_cr:
                    return c, r   

    def trialno(self,c,r): #trial number for a given condition and repeat index
        
        #N.B. trial no. starts at 1 in the analyzer file, cond and repeat start at 0.
    
        return self.loops['conds'][c]['repeats'][r]['trialno']-1


    def datapath(self,floc): #string, folder location of the data
    
    
        return self.datapath


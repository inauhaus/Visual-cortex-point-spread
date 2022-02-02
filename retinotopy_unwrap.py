


def retinotopy_unwrap(hor,vert,xyLocations):
    
    
    from scipy.io import loadmat
    import numpy as np
    import matplotlib.pyplot as plt
    from sklearn.mixture import GaussianMixture

    hor_vec = np.exp(hor*1j*np.pi/180) #convert phase to vector
    vert_vec = np.exp(vert*1j*np.pi/180)
    
    mu_hor = np.mean(hor_vec);  #Get the resultant
    mu_vert = np.mean(vert_vec);
    
    hor_vec = hor_vec*np.conj(mu_hor)*np.exp(1j*np.pi);  #subtract the resultant and add pi
    vert_vec = vert_vec*np.conj(mu_vert)*np.exp(1j*np.pi);
    
    hor_mod = np.angle(hor_vec)*180/np.pi;   #convert back to phase
    vert_mod = np.angle(vert_vec)*180/np.pi;
    
    #Gaussian mixture model of horizontal retinotopy
    X = np.concatenate((hor_mod.reshape(-1,1),xyLocations),axis =1) #Ncell x 3 matrix
    X = (X - np.mean(X,axis = 0))/np.std(X,axis = 0)                #Zscore each feature
    idx_H = GaussianMixture(n_components=2, n_init = 50).fit_predict(X)
    
    #Gaussian mixture model of vertical retinotopy
    X = np.concatenate((vert_mod.reshape(-1,1),xyLocations),axis =1) #Ncell x 3 matrix
    X = (X - np.mean(X,axis = 0))/np.std(X,axis = 0) #Zscore each feature
    idx_V = GaussianMixture(n_components=2, n_init = 50).fit_predict(X)
    
    
    idh = idx_H ==1
    idv = idx_V ==1
    
    #% Plot the unwrapped data, with cluster ids
    
    plt.figure()
    
    plt.subplot(4,2,1)
    
    plt.scatter(xyLocations[~idh,0],hor_mod[~idh])
    plt.scatter(xyLocations[idh,0],hor_mod[idh]) 
    
    plt.subplot(4,2,3)
    
    plt.scatter(xyLocations[~idh,1],hor_mod[~idh])
    plt.scatter(xyLocations[idh,1],hor_mod[idh]) 
    
    plt.subplot(4,2,5)
    
    plt.scatter(xyLocations[~idv,0],vert_mod[~idv])
    plt.scatter(xyLocations[idv,0],vert_mod[idv]) 
    
    plt.subplot(4,2,7)
    
    plt.scatter(xyLocations[~idv,1],vert_mod[~idv])
    plt.scatter(xyLocations[idv,1],vert_mod[idv]) 
    
    
    #Unwrap horizontal: find cluster with smaller values, on average, and add 360
    mu1 = np.mean(hor_mod[~idh]);
    mu2 = np.mean(hor_mod[idh]);
    hor_unwrapped = hor_mod.copy()
    if mu1<mu2:
        hor_unwrapped[~idh] += 360
    else:
        hor_unwrapped[idh] += 360
    
    
    #Unwrap horizontal: find cluster with smaller values, on average, and add 360
    mu1 = np.mean(vert_mod[~idv]);
    mu2 = np.mean(vert_mod[idv]);
    vert_unwrapped = vert_mod.copy()
    if mu1<mu2:
        vert_unwrapped[~idv] += 360;
    else:
        vert_unwrapped[idv] += 360;
    
    
    plt.subplot(4,2,2)
    plt.scatter(xyLocations[:,0],hor_unwrapped)
    plt.subplot(4,2,4)
    plt.scatter(xyLocations[:,1],hor_unwrapped)
    plt.subplot(4,2,6)
    plt.scatter(xyLocations[:,0],vert_unwrapped)
    plt.subplot(4,2,8)
    plt.scatter(xyLocations[:,1],vert_unwrapped)
    
    return hor_unwrapped, vert_unwrapped

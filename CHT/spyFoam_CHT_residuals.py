"""
Created on Wed Nov 29 13:44:18 2023
Author: Jakub Trušina
Name: spyFoam_CHT_residuals.py
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
 

def residuals(case_name, regions):
    
    start_time = 0

    # plt.close("all")
    
    plt.style.use("dark_background")
    for param in ['text.color', 'axes.labelcolor', 'xtick.color', 'ytick.color']:
        plt.rcParams[param] = '0.9'  # very light grey
    for param in ['figure.facecolor', 'axes.facecolor', 'savefig.facecolor']:
        plt.rcParams[param] = '#212946'  # bluish dark grey
    plt.rcParams['axes.edgecolor'] = "2A3459" # '#2A546D'
    
    fig = plt.figure(num=1, figsize=(12,8), dpi=80 )
    fig.canvas.manager.set_window_title("Residuals for regions " + " ".join(regions) )
    fig.clear()
    for region in regions:
    
        folder_path_quan = f"residuals(p,p_rgh,U,h,e,k,omega,nuTilda,T,region={region})"
        folder_path = os.path.join(".\\",case_name,"postProcessing",region,folder_path_quan)
        subdirectories = sorted( ([dd for dd in os.listdir(folder_path) ]) )
        # print(subdirectories)
        
        inp = os.path.join(folder_path,str(start_time),"residuals.dat")
        df = pd.read_csv(inp, skiprows=1, delimiter="\t" ) # ,low_memory=False)
        df=df.drop(df.index[0])
        print(df)
        # print(df.columns.values)
        
        Time = df['# Time        ']
        
        try:
            p = df['p             '].apply(pd.to_numeric)
            plt.plot(Time, p, linewidth= 3, label="$p$" +" "+region +" = "+str("%.2E"%(p.iloc[-1])) )
            plt.text(Time.iloc[-1], p.iloc[-1] , "$p$" +" "+region , fontsize= 14 , horizontalalignment='right', verticalalignment='bottom',  )
        except: pass
        try:
            p_rgh = df['p_rgh         '].apply(pd.to_numeric)
            plt.plot(Time, p_rgh, linewidth= 3, label="$p_{rgh}$" +" "+region +" = "+str("%.2E"%(p_rgh.iloc[-1])) )
            plt.text(Time.iloc[-1], p_rgh.iloc[-1] , "$p_{rgh}$" +" "+region , fontsize= 14 , horizontalalignment='right', verticalalignment='bottom',  )
        except: pass
        try:
            Ux = df['Ux            '].apply(pd.to_numeric)
            plt.plot(Time, Ux, linewidth= 3, label="$U_x$" +" "+region +" = "+str("%.2E"%(Ux.iloc[-1])) )
            plt.text(Time.iloc[-1], Ux.iloc[-1] , "$U_x$" +" "+region , fontsize= 14 , horizontalalignment='right', verticalalignment='bottom',  )
        except: pass
        try:
            Uy = df['Uy            '].apply(pd.to_numeric)
            plt.plot(Time, Uy, linewidth= 3, label="$U_y$" +" "+region +" = "+str("%.2E"%(Uy.iloc[-1])) )
            plt.text(Time.iloc[-1], Uy.iloc[-1] , "$U_y$" +" "+region , fontsize= 14 , horizontalalignment='right', verticalalignment='bottom',  )
        except: pass
        try:
            Uz = df['Uz            '].apply(pd.to_numeric)
            plt.plot(Time, Uz, linewidth= 3, label="$U_z$" +" "+region +" = "+str("%.2E"%(Uz.iloc[-1])) ) 
            plt.text(Time.iloc[-1], Uz.iloc[-1] , "$U_z$" +" "+region , fontsize= 14 , horizontalalignment='right', verticalalignment='bottom',  )
    
        except: pass
        try:
            h = df['h             '].apply(pd.to_numeric)
            plt.plot(Time, h, linewidth= 3, label="$h$" +" "+region +" = "+str("%.2E"%(h.iloc[-1])) )
            plt.text(Time.iloc[-1], h.iloc[-1] , "$h$" +" "+region , fontsize= 14 , horizontalalignment='right', verticalalignment='bottom',  )
        except: pass
        try:
            e = df['e             '].apply(pd.to_numeric)
            plt.plot(Time, e, linewidth= 3, label="$e$" +" "+region +" = "+str("%.2E"%(e.iloc[-1])) )
            plt.text(Time.iloc[-1], e.iloc[-1] , "$e$" +" "+region , fontsize= 14 , horizontalalignment='right', verticalalignment='bottom',  )
        except: pass
        try:
            k = df['k             '].apply(pd.to_numeric)
            plt.plot(Time, k, linewidth= 3, label="$k$" +" "+region +" = "+str("%.2E"%(k.iloc[-1])) )
            plt.text(Time.iloc[-1], k.iloc[-1] , "$k$" +" "+region , fontsize= 14 , horizontalalignment='right', verticalalignment='bottom',  )
        except: pass
        try:
            omega = df['omega         '].apply(pd.to_numeric)
            plt.plot(Time, omega, linewidth= 3, label="$omega$" +" "+region +" = "+str("%.2E"%(omega.iloc[-1])) )
            plt.text(Time.iloc[-1], omega.iloc[-1] , "$omega$" +" "+region , fontsize= 14 , horizontalalignment='right', verticalalignment='bottom',  )
        except: pass
        
    plt.title( "Residuals for regions - " + " ".join(regions) + "\nIteration = " +str("%.0f"%(Time.size-1)) +", Time = "+str((Time.iloc[-1])) , fontsize= 18)
    plt.ylabel('[-] ', fontsize = 14 )
    plt.xlabel(' Time [s]', fontsize = 14)
    plt.hlines(y= 1E-3 , xmin= 0, xmax = Time.iloc[-1], linestyles="--",   linewidth= 1 )
    plt.hlines(y= 1E-4 , xmin= 0, xmax = Time.iloc[-1], linestyles="--",   linewidth= 1 )
    plt.rc('xtick', labelsize= 14)   
    plt.rc('ytick', labelsize= 14) 
    
    plt.yscale('log')
    
    num_curves = len(plt.gca().get_lines())
    import matplotlib as mpl
    cmap = mpl.cm.get_cmap('viridis', num_curves)
    lines = plt.gca().get_lines()
    for ci, line in enumerate(lines):
        line.set_color(cmap(ci))
    plt.legend(loc='best',  ncol=2, shadow= True, fontsize= 12)
    plt.grid(linestyle= '--', linewidth= 1, color='#2A3459')
    plt.tight_layout() 
    plt.show(block= False )  
    fig.canvas.draw()
    plt.style.use("default")
            
    def escape_key(event):
        if event.key == 'escape':  # 'escape' corresponds to 'Esc' key
            plt.close(event.canvas.figure)
    fig.canvas.mpl_connect('key_press_event', escape_key)
    
    
if __name__ == '__main__':

    case_name = r"Y:\home\trusinja\FOAM_WORK_UBUNTU\Open_FOAM_12\Cooling_Ikea_Mug"  
    
    regions = [ "AIR" , "WATER" , "MUG" ]
    # regions = [ "WATER" ]

    residuals(case_name, regions)














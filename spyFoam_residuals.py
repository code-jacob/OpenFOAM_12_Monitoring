"""
Created on Wed Nov 29 13:44:18 2023
Author: Jakub Trušina
Name: spyFoam_plot_residuals.py
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

def residuals(case_name,angles,rho,compressible):
    
    def run():
        
        folder_path_quan = r"postProcessing\residuals(p,p_rgh,U,h,e,k,omega,nuTilda)"
        folder_path = os.path.join(".\\",folder,folder_path_quan)
        subdirectories = sorted( ([dd for dd in os.listdir(folder_path) ]) )
        print(subdirectories)
        
        for ddd in subdirectories:
            inp = os.path.join(".\\",folder,folder_path_quan,str(ddd),"residuals.dat")
            df = pd.read_csv(inp, skiprows=1, delimiter="\t")
    
            df=df.drop(df.index[0])
            print(df)
            print(df.columns.values)
            
            Time = df['# Time          '].apply(pd.to_numeric)
            p = df['p               '].apply(pd.to_numeric)
            Ux = df['Ux              '].apply(pd.to_numeric)
            Uy = df['Uy              '].apply(pd.to_numeric)
            Uz = df['Uz              '].apply(pd.to_numeric)
            k = df['k               '].apply(pd.to_numeric)
            omega = df['omega           '].apply(pd.to_numeric)
            if compressible == 1:
                h = df['h               '].apply(pd.to_numeric)
            
            
            plt.style.use("dark_background")
            for param in ['text.color', 'axes.labelcolor', 'xtick.color', 'ytick.color']:
                plt.rcParams[param] = '0.9'  # very light grey
            for param in ['figure.facecolor', 'axes.facecolor', 'savefig.facecolor']:
                plt.rcParams[param] = '#212946'  # bluish dark grey
            plt.rcParams['axes.edgecolor'] = "2A3459" # '#2A546D'
            
            if ddd == "0":
                if angles == []:
                    fig = plt.figure(num=0, figsize=(12, 9), dpi=80 )
                    fig.canvas.manager.set_window_title("Residuals")    
                    plt.title( "Residuals"+", Iteration = " + str("%.0f"%(Time.size))+", Time = "+str((Time.iloc[-1])) , fontsize= 18)
                else:
                    fig = plt.figure(num=angle, figsize=(12, 9), dpi=80 )
                    fig.canvas.manager.set_window_title("Residuals for " + "angle " + str(angle) + "°" )
                    plt.title( "Residuals for "+ "angle " + str(angle) + "°"+", Iteration = " + str("%.0f"%(Time.size))+", Time = "+str((Time.iloc[-1])) , fontsize= 18)
                    fig.clear()
                
            plt.plot(Time, p, 'k-',  linewidth= 3, label="$p$"+ " (pressure)" +" = "+str("%.2E"%(p.iloc[-1])) )
            plt.plot(Time, Ux, 'r-',  linewidth= 3, label="$U_x$"+ " (x-velocity)" +" = "+str("%.2E"%(Ux.iloc[-1])) )
            plt.plot(Time, Uy, 'g-',  linewidth= 3, label="$U_y$"+ " (y-velocity)" +" = "+str("%.2E"%(Uy.iloc[-1])) )
            plt.plot(Time, Uz, 'b-',  linewidth= 3, label="$U_z$"+ " (z-velocity)" +" = "+str("%.2E"%(Uz.iloc[-1])) )
            plt.plot(Time, k, 'm-',  linewidth= 3, label="$k$"+ " (turbulence kinetic energy)" +" = "+str("%.2E"%(k.iloc[-1])) )
            plt.plot(Time, omega, 'c-',  linewidth= 3, label="$omega$"+ " (specific turbulence dissipation rate)" +" = "+str("%.2E"%(omega.iloc[-1])) )
            if compressible == 1:
                plt.plot(Time, h, 'y-',  linewidth= 3, label="$h$"+ " (enthalpy)" +" = "+str("%.2E"%(h.iloc[-1])) )
            
            # plt.text(Time.iloc[-1], Ux.iloc[-1] , str("%.2E"%(Ux.iloc[-1])), fontsize= 15 , color="r", )
            
        plt.ylabel('[-] ', fontsize = 20)
        plt.xlabel(' Time [s]', fontsize = 14)
        plt.hlines(y= 1E-3 , xmin= 0, xmax = Time.iloc[-1], linestyles="--",   linewidth= 1.1 )
        plt.hlines(y= 1E-4 , xmin= 0, xmax = Time.iloc[-1], linestyles="--",   linewidth= 1.1 )
        plt.rc('xtick', labelsize= 14)   
        plt.rc('ytick', labelsize= 14) 
        
        plt.yscale('log')
        # plt.xscale('log')
        
        num_curves = len(plt.gca().get_lines())
        import matplotlib as mpl
        cmap = mpl.cm.get_cmap('viridis', num_curves)
        lines = plt.gca().get_lines()
        for ci, line in enumerate(lines):
            line.set_color(cmap(ci))
        plt.legend(loc='best',  ncol=2, shadow= True, fontsize= 13)
        plt.grid(linestyle= '--', linewidth= 1, color='#2A3459')
        plt.tight_layout()
        plt.show(block= False )  
        fig.canvas.draw() 
        plt.style.use("default")
        
    if angles == []:
        folder = case_name
        run()
    else:
        for angle in angles: 
            folder = case_name + "_" + str(angle)
            run()

if __name__ == '__main__':

    # case_name = "Y:/home/trusinja/FOAM_WORK_UBUNTU/Open_FOAM_12/DN3200_in_straight_pipe/all_incompressibleFluid/case"
    
    # angles = [ 0 ]
    # rho = 998.23
    # if "incompressible" in case_name:
    #     compressible = 0
    # else:  compressible = 1
    
    # residuals(case_name,angles,rho,compressible)


    
    
    case_name = r"C:\Users\trusinja\Desktop\FOAM_WORK\Pipe_Elbow\Hexahedral"
    case_name = r"C:\Users\trusinja\Desktop\FOAM_WORK\Pipe_Elbow\Hexcore"
    case_name = r"C:\Users\trusinja\Desktop\FOAM_WORK\Pipe_Elbow\Polyhedral"
    # case_name = r"C:\Users\trusinja\Desktop\FOAM_WORK\Pipe_Elbow\Tetrahedral"
    
    angles = [  ]
    rho = 998.23
    compressible = 0
    
    residuals(case_name,angles,rho,compressible)
    
    
    
    
    
    




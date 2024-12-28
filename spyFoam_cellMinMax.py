
"""
Created on Tue Dec  5 10:41:39 2023
Author: Jakub Trušina
Name: spyFoam_cellMinMax.py
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re
import os

def cellMinMax(case_name,angles,rho,compressible):
    
   
    def run():
        global rho
        
        folder_data = 0
        
        inp = os.path.join(".\\", folder , r".\postProcessing\cellMaxMag(U)",str(folder_data),"volFieldValue.dat")
        df = pd.read_csv(inp, skiprows=2, delimiter="\t")
        print(df.columns.values)
        
        Time = df["# Time          "]
        
        
        if angles == []:
            fig = plt.figure(num=0, figsize=(12, 9), dpi=80 )
            fig.canvas.manager.set_window_title("cellMinMax")
            plt.title("cellMinMax"+", iteration = " + str("%.0f"%(Time.size-1))+", time = "+str((Time.iloc[-1])), fontsize=20)
        else:
            fig = plt.figure(num=angle+2, figsize=(12, 9), dpi=80 )
            fig.canvas.manager.set_window_title("cellMinMax for " + "angle " + str(angle) + "°")
            plt.title("cellMinMax for "+ "angle " + str(angle) + "°"+", iteration = " + str("%.0f"%(Time.size-1))+", time = "+str((Time.iloc[-1])), fontsize=20)
            fig.clear()
        
        # inp = os.path.join(".\\", folder , r".\postProcessing\cellMaxMag(U)",str(folder_data),"volFieldValue.dat")
        # df = pd.read_csv(inp, skiprows=3, delimiter="\t")
        # print(df.columns.values)
        name_quant = "maxMag(U)"
        clr = "k"
        Quant = df[name_quant]
        print(name_quant + " =", Quant.iloc[-1] )
        plt.plot(Time, Quant , label= name_quant +" = "+str("%.1f"%(Quant.iloc[-1])), linestyle=':', linewidth= 3, color=clr )
        
        inp = os.path.join(".\\", folder , r".\postProcessing\cellMin(U,p,T,rho)",str(folder_data),"volFieldValue.dat")
        with open(inp, 'r') as file:
            lines = file.readlines()
        lines = [line for line in lines if not line.startswith('#')]
        pattern = r'[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?'
        data = [re.findall(pattern, line) for line in lines]
        if compressible == 1:
            rho = 1
            df = pd.DataFrame(data, columns=['Time', 'min(UX)', 'min(UY)', 'min(UZ)', 'min(p)', 'min(T)', 'min(rho)' ])
        else: df = pd.DataFrame(data, columns=['Time', 'min(UX)', 'min(UY)', 'min(UZ)', 'min(p)' ])
        df = df.apply(pd.to_numeric)
        print(df.columns.values)
        
        name_quant = "min(UX)"
        Quant = df[name_quant]
        print(name_quant + " =", Quant.iloc[-1] )
        plt.plot(Time, Quant , label= name_quant +" = "+str("%.1f"%(Quant.iloc[-1])), linestyle='--', linewidth= 3, color=clr )
        
        name_quant = "min(UY)"
        Quant = df[name_quant]
        print(name_quant + " =", Quant.iloc[-1] )
        plt.plot(Time, Quant , label= name_quant +" = "+str("%.1f"%(Quant.iloc[-1])), linestyle='--', linewidth= 3, color=clr )
        
        name_quant = "min(UZ)"
        Quant = df[name_quant]
        print(name_quant + " =", Quant.iloc[-1] )
        plt.plot(Time, Quant , label= name_quant +" = "+str("%.1f"%(Quant.iloc[-1])), linestyle='--', linewidth= 3, color=clr )
        
        name_quant = "min(p)"
        Quant = df[name_quant]*rho
        print(name_quant + " =", Quant.iloc[-1] )
        plt.plot(Time, Quant , label= name_quant +" = "+str("%.1f"%(Quant.iloc[-1])), linestyle='--', linewidth= 3, color=clr )
        
        if compressible == 1:
            name_quant = "min(T)"
            Quant = df[name_quant]
            print(name_quant + " =", Quant.iloc[-1] )
            plt.plot(Time, Quant , label= name_quant +" = "+str("%.1f"%(Quant.iloc[-1])), linestyle='--', linewidth= 3, color=clr )
            
            name_quant = "min(rho)"
            Quant = df[name_quant]
            print(name_quant + " =", Quant.iloc[-1] )
            plt.plot(Time, Quant , label= name_quant +" = "+str("%.2f"%(Quant.iloc[-1])), linestyle='--', linewidth= 3, color=clr )
        
        
        inp = os.path.join(".\\", folder , r".\postProcessing\cellMax(U,p,T,rho)",str(folder_data),"volFieldValue.dat")
        with open(inp, 'r') as file:
            lines = file.readlines()
        lines = [line for line in lines if not line.startswith('#')]
        pattern = r'[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?'
        data = [re.findall(pattern, line) for line in lines]
        if compressible == 1:
            df = pd.DataFrame(data, columns=['Time', 'max(UX)', 'max(UY)', 'max(UZ)', 'max(p)', 'max(T)', 'max(rho)' ])
        else: df = pd.DataFrame(data, columns=['Time', 'max(UX)', 'max(UY)', 'max(UZ)', 'max(p)'])
        df = df.apply(pd.to_numeric)
        print(df.columns.values)
        
        name_quant = "max(UX)"
        Quant = df[name_quant]
        print(name_quant + " =", Quant.iloc[-1] )
        plt.plot(Time, Quant , label= name_quant +" = "+str("%.1f"%(Quant.iloc[-1])), linestyle='-', linewidth= 3, color=clr )
        
        name_quant = "max(UY)"
        Quant = df[name_quant]
        print(name_quant + " =", Quant.iloc[-1] )
        plt.plot(Time, Quant , label= name_quant +" = "+str("%.1f"%(Quant.iloc[-1])), linestyle='-', linewidth= 3, color=clr )
        
        name_quant = "max(UZ)"
        Quant = df[name_quant]
        print(name_quant + " =", Quant.iloc[-1] )
        plt.plot(Time, Quant , label= name_quant +" = "+str("%.1f"%(Quant.iloc[-1])), linestyle='-', linewidth= 3, color=clr )
    
        name_quant = "max(p)"
        Quant = df[name_quant]*rho
        print(name_quant + " =", Quant.iloc[-1] )
        plt.plot(Time, Quant , label= name_quant +" = "+str("%.1f"%(Quant.iloc[-1])), linestyle='-', linewidth= 3, color=clr )
        
        if compressible == 1:
            name_quant = "max(T)"
            Quant = df[name_quant]
            print(name_quant + " =", Quant.iloc[-1] )
            plt.plot(Time, Quant , label= name_quant +" = "+str("%.1f"%(Quant.iloc[-1])), linestyle='-', linewidth= 3, color=clr )
            
            name_quant = "max(rho)"
            Quant = df[name_quant]
            print(name_quant + " =", Quant.iloc[-1] )
            plt.plot(Time, Quant , label= name_quant +" = "+str("%.2f"%(Quant.iloc[-1])), linestyle='-', linewidth= 3, color=clr )
        
        plt.rc('xtick', labelsize= 14)   
        plt.rc('ytick', labelsize= 14) 
        # plt.yscale('symlog')
        # plt.xscale('log')
        # plt.ylabel('$Moment$' + ' $[Nm]$ ', fontsize = 20)
        plt.xlabel('$Time$' + ' $[-]$ ' , fontsize = 14)
        
        num_curves = len(plt.gca().get_lines())
        import matplotlib as mpl
        cmap = mpl.cm.get_cmap('hsv', num_curves)
        lines = plt.gca().get_lines()
        for i, line in enumerate(lines):
            line.set_color(cmap(i))
        plt.legend(loc='best', shadow= True,  ncol=2, fontsize= 13)
        plt.grid(linestyle= '-', linewidth= 1)
        plt.tight_layout()
        plt.show(block= False )  
        fig.canvas.draw() 

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
  
    
    cellMinMax(case_name,angles,rho,compressible)



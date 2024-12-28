
"""
Created on Tue Dec  5 10:41:39 2023
Author: Jakub Trušina
Name: spyFoam_CHT_probe.py
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re
import os

def probe(case_name, regions):
    
    regions = [ "WATER" ]
    
    probe = "probes_1"
    units = 1
    
    # plt.close("all")

    plt.style.use("dark_background")
    for param in ['text.color', 'axes.labelcolor', 'xtick.color', 'ytick.color']:
        plt.rcParams[param] = '0.9'  # very light grey
    for param in ['figure.facecolor', 'axes.facecolor', 'savefig.facecolor']:
        plt.rcParams[param] = '#212946'  # bluish dark grey
    plt.rcParams['axes.edgecolor'] = "2A3459" # '#2A546D'
    
    fig = plt.figure(num=3, figsize=(12,8), dpi=80 )
    fig.canvas.manager.set_window_title("Probe for regions - " + " ".join(regions) )
    fig.clear()
    
    for region in regions:
        print()
        print(region)
        folder_path_quan = "T"
        folder_path = os.path.join(".\\",case_name,"postProcessing",region,probe)
        subdirectories = sorted( ([time for time in os.listdir(folder_path) ]) )
        print("subdirectories =",subdirectories)
            
        for folder_data in subdirectories:
            inp = os.path.join(folder_path,str(folder_data),folder_path_quan)
            with open(inp, 'r') as file:
                lines = file.readlines()
            lines = [line for line in lines if not line.startswith('#')]
            pattern = r'[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?'
            data = [re.findall(pattern, line) for line in lines]
        
            df = pd.DataFrame(data, columns=['Time', 'T' ])    
            # print(df)
            Time = df["Time"].apply(pd.to_numeric)/units
            clr = "r" #"#094BDD" #"#F5D300" #"#094BDD"    
            df = df.apply(pd.to_numeric)
            df_columns = np.delete(df.columns.values,0)
            print(df.columns.values)  
            for name_quant in df_columns:
                Quant = df[name_quant]  - 273.15
                print(name_quant + " =", Quant.iloc[-1] )
                plt.plot(Time, Quant , color=clr, linestyle='-', linewidth= 3)
                # plt.plot(Time.iloc[-1], Quant.iloc[-1] , "o", color=clr, markersize=8 )
                # plt.text(Time.iloc[-1], Quant.iloc[-1] , name_quant +" "+region +" = "+str("%.1f"%(Quant.iloc[-1])), fontsize= 20 , horizontalalignment='right', verticalalignment='bottom',  )
        
            x_axis = Time ; y_axis = Quant
            y_border = 20
            n_shades = 8
            diff_linewidth = 1.05
            alpha_value = 1 / n_shades
            aa=0
            for n in range(1, n_shades+1):
                plt.plot( x_axis, y_axis , color=clr, linewidth=2+(diff_linewidth*n), alpha=alpha_value  ) 
            for n in range(0,n_shades):
                aa+=1
                y_0 = np.array(y_axis)*(aa/n_shades) + y_border*(1-((aa)/n_shades))
                plt.fill_between(x=x_axis,y2=y_0,y1=y_axis,color=clr,alpha=alpha_value/2)        
        
        plt.plot(Time, Quant , color=clr, label=name_quant +" "+region +" = "+str("%.1f"%(Quant.iloc[-1])), linestyle='-', linewidth= 3)
                
        plt.title("Probes for regions - " + " ".join(regions) + "\nIteration = " +str("%.0f"%(Time.size-1)) +", Time = "+str((Time.iloc[-1])), fontsize=20)
        plt.rc('xtick', labelsize= 14)   
        plt.rc('ytick', labelsize= 14) 
        # plt.yscale('symlog')
        # plt.xscale('log')
        plt.ylabel('$Temperature$' + ' $[°C]$ ', fontsize = 14)
        if units == 1:
            unit = "s"
        if units == 60:
            unit = "min"
            plt.xlabel('$Time$' + f' $[{unit}]$ ' , fontsize = 14)
        if units == 3600:
            unit = "h"
            plt.xlabel('$Time$' + f' $[{unit}]$ ' , fontsize = 14)

        # Experiment 
        
        time_ex = np.array([ 0,  60, 2*60, 3*60, 4*60, 5*60 , 10*60, 15*60, 20*60, 25*60, 30*60, 35*60,  40*60, 45*60, 50*60,  55*60,  60*60,  65*60,  70*60,  75*60,  80*60, 90*60, 100*60, 110*60, 120*60, 130*60,  140*60, 160*60    ]) /units
        T_ex =    np.array([ 90, 85, 80,    76,   73,   71,    63,    58,    54,    51,    48,     46,   44,     42,     40,     39,    37,     36,      35,    34,     33,     32,    31,    30,      29,       28,     28,    27 ])
        clr = "#093BDD" #"#094BDD" #'#08F7FE'  "#808080"
        plt.plot(time_ex, T_ex , color=clr, label="T WATER Experiment = "+str("%.1f"%(T_ex[-1])), marker='H', linestyle='-', linewidth= 3, markersize=6 )
        
        x_axis = time_ex ; y_axis = T_ex
        y_border = 20
        n_shades = 8
        diff_linewidth = 1.5
        alpha_value = 0.8 / n_shades
        aa=0 
        for n in range(1, n_shades+1):
            plt.plot( x_axis, y_axis , color=clr, linewidth=2+(diff_linewidth*n), alpha=alpha_value  ) 
        for n in range(0,n_shades):
            aa+=1
            y_0 = np.array(y_axis)*(aa/n_shades) + y_border*(1-((aa)/n_shades))
            plt.fill_between(x=x_axis,y2=y_0,y1=y_axis,color=clr,alpha=alpha_value/2)
        
                # ylim_min = 0+273   ;   ylim_max = 100+273
        # plt.ylim(ylim_min,ylim_max)     
        
        plt.legend(loc='best', shadow= True,  ncol=1, fontsize= 14)
        plt.tight_layout()
        plt.grid(linestyle= '--', linewidth= 1, color='#2A3459')
        plt.show(block= False )  
        fig.canvas.draw() 
        plt.style.use("default")
        
    def escape_key(event):
        if event.key == 'escape':  # 'escape' corresponds to 'Esc' key
            plt.close(event.canvas.figure)
    fig.canvas.mpl_connect('key_press_event', escape_key)
    
if __name__ == '__main__':

    case_name = r"\\wsl.localhost\Ubuntu\home\trusinja\FOAM_WORK_UBUNTU\Cooling_Mug\Whole"
    case_name = r"\\wsl.localhost\Ubuntu\home\trusinja\FOAM_WORK_UBUNTU\Cooling_Mug\Symmetry"
    
    # regions = [ "AIR" , "WATER" , "MUG" ]
    regions = [ "WATER" ]

    probe(case_name, regions)


"""
Created on Tue Dec  5 10:41:39 2023
Author: Jakub Trušina
Name: spyFoam_CHT_cellMinMax.py
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re
import os

counter = 0
def cellMinMax(case_name, regions):
    global counter
    
    start_time = 0
    
    # plt.close("all")
    plt.style.use("dark_background")
    for param in ['text.color', 'axes.labelcolor', 'xtick.color', 'ytick.color']:
        plt.rcParams[param] = '0.9'  # very light grey
    for param in ['figure.facecolor', 'axes.facecolor', 'savefig.facecolor']:
        plt.rcParams[param] = '#212946'  # bluish dark grey
    plt.rcParams['axes.edgecolor'] = "2A3459" # '#2A546D'
    
    fig = plt.figure(num=2, figsize=(12,8), dpi=80)
    fig.canvas.manager.set_window_title("cellMinMax for regions " + " ".join(regions) )
    
    # xlim = plt.gca().get_xlim()
    # ylim = plt.gca().get_ylim()
    fig.clear()   
    
    for region in regions:
    
        print()
        print(region)
        
        # folder_path_quan = f"cellMin(U,p,T,p_rgh,region={region})"
        # folder_path = os.path.join(".\\",case_name,"postProcessing",region,folder_path_quan)   
        # inp = os.path.join(folder_path,str(start_time),"volFieldValue.dat")
        # with open(inp, 'r') as file:
        #     lines = file.readlines()
        # lines = [line for line in lines if not line.startswith('#')]
        # pattern = r'[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?'
        # data = [re.findall(pattern, line) for line in lines]
    
        # try:
        #     df = pd.DataFrame(data, columns=['Time', 'min(UX)', 'min(UY)', 'min(UZ)', 'min(p)', 'min(T)', 'min(p_rgh)' ])    
        # except:
        #     pass
        # try:
        #     df = pd.DataFrame(data, columns=['Time', 'min(T)', ])
        # except:
        #     pass
        # Time = df["Time"].apply(pd.to_numeric)
        # df = df.apply(pd.to_numeric)
        # df_columns = np.delete(df.columns.values,0)
        # print(df.columns.values)  
        # try:
        #     for name_quant in df_columns:
        #         Quant = df[name_quant]
        #         print(name_quant + " =", Quant.iloc[-1] )
        #         plt.plot(Time, Quant , label=name_quant +" "+region +" = "+str("%.3f"%(Quant.iloc[-1])), linestyle='--', linewidth= 3)
        #         # plt.plot(Time.iloc[-1], Quant.iloc[-1] , "s", color=clr, markersize=8 )
        #         plt.text(Time.iloc[-1], Quant.iloc[-1] , name_quant +" "+region +" = "+str("%.3f"%(Quant.iloc[-1])), fontsize= 14 , horizontalalignment='right', verticalalignment='bottom',  )
        # except:
        #     pass
        
        # folder_path_quan = f"cellMax(U,p,T,p_rgh,region={region})"
        # folder_path = os.path.join(".\\",case_name,"postProcessing",region,folder_path_quan)   
        # inp = os.path.join(folder_path,str(start_time),"volFieldValue.dat")    
        # with open(inp, 'r') as file:
        #     lines = file.readlines()
        # lines = [line for line in lines if not line.startswith('#')]
        # pattern = r'[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?'
        # data = [re.findall(pattern, line) for line in lines]
        # try:
        #     df = pd.DataFrame(data, columns=['Time', 'max(UX)', 'max(UY)', 'max(UZ)', 'max(p)', 'max(T)', 'max(p_rgh)' ])
        # except:
        #     pass
        # try:
        #     df = pd.DataFrame(data, columns=['Time', 'max(T)', ])
        # except:
        #     pass
        # Time = df["Time"].apply(pd.to_numeric)
        # df = df.apply(pd.to_numeric)
        # df_columns = np.delete(df.columns.values,0)
        # print(df.columns.values)
        # try:
        #     for name_quant in df_columns:
        #         Quant = df[name_quant]
        #         # if name_quant == 'max(T)':
        #         print(name_quant + " =", Quant.iloc[-1] )
        #         plt.plot(Time, Quant , label= name_quant +" "+region +" = "+str("%.3f"%(Quant.iloc[-1])), linestyle='-', linewidth= 3)
        #         # plt.plot(Time.iloc[-1], Quant.iloc[-1] , "s", color=clr, markersize=8 )
        #         plt.text(Time.iloc[-1], Quant.iloc[-1] , name_quant +" "+region +" = "+str("%.3f"%(Quant.iloc[-1])), fontsize= 14 , horizontalalignment='right', verticalalignment='bottom',)
        # except:
        #     pass


        try:
            folder_path_quan = f"cellMaxMag(U,region={region})"
            folder_path = os.path.join(".\\",case_name,"postProcessing",region,folder_path_quan)   
            inp = os.path.join(folder_path,str(start_time),"volFieldValue.dat")
            df = pd.read_csv(inp, skiprows=2, delimiter="\t")
            print(df.columns.values)
            Time = df["# Time        "].apply(pd.to_numeric)
            name_quant = "maxMag(U)"
            Quant = df[name_quant]
            print(name_quant + " =", Quant.iloc[-1] )
            plt.plot(Time, Quant , label= name_quant +" "+region +" = "+str("%.3f"%(Quant.iloc[-1])), linestyle='-', linewidth= 3, )
            # plt.plot(Time.iloc[-1], Quant.iloc[-1] , "s", color=clr, markersize=8 )
            plt.text(Time.iloc[-1], Quant.iloc[-1] , name_quant +" "+region +" = "+str("%.3f"%(Quant.iloc[-1])), fontsize= 14 , horizontalalignment='right', verticalalignment='bottom',)    
        except:
            pass
        
        plt.title( "cellMinMax for regions - " + " ".join(regions) + "\nIteration = " +str("%.0f"%(Time.size-1)) +", Time = "+str((Time.iloc[-1])) , fontsize= 18)
    
    
        plt.rc('xtick', labelsize= 14)   
        plt.rc('ytick', labelsize= 14) 
        plt.gca().ticklabel_format(axis='y', style='sci', scilimits=(0, 0))
        # plt.yscale('symlog')
        # plt.xscale('log')
        # plt.ylabel('$Moment$' + ' $[Nm]$ ', fontsize = 20)
        plt.xlabel('$Time$' + ' $[-]$ ' , fontsize = 14)
        
        num_curves = len(plt.gca().get_lines())
        import matplotlib as mpl
        cmap = mpl.cm.get_cmap('rainbow', num_curves)
        lines = plt.gca().get_lines()
        for ci, line in enumerate(lines):
            line.set_color(cmap(ci))
        
        plt.legend(loc='lower center', shadow= True,  ncol=1, fontsize= 12, bbox_to_anchor=(-0.3, 0))
        plt.tight_layout()
        plt.grid(linestyle= '--', linewidth= 1, color='#2A3459')
        plt.show(block= False )  

    # if counter != 0:
    #     print(counter)
    #     plt.xlim(xlim)
    #     plt.ylim(ylim)
    # counter+=1
    fig.canvas.draw()
    plt.style.use("default")

    def escape_key(event):
        if event.key == 'escape':  # 'escape' corresponds to 'Esc' key
            plt.close(event.canvas.figure)
    fig.canvas.mpl_connect('key_press_event', escape_key)
        
if __name__ == '__main__':

    case_name = r"\\wsl.localhost\Ubuntu\home\trusinja\FOAM_WORK_UBUNTU\Cooling_Mug\Whole"
    case_name = r"\\wsl.localhost\Ubuntu\home\trusinja\FOAM_WORK_UBUNTU\Cooling_Mug\Symmetry"

    
    regions = [ "AIR" , "WATER" , "MUG" ]
    # regions = [ "MUG" ]

    cellMinMax(case_name, regions)








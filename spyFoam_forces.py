"""
Created on Fri Dec  1 13:32:11 2023
Author: Jakub Trušina
Name: spyFoam_forces.py
"""

import pandas as pd
import matplotlib.pyplot as plt
import re
import os

def forces(case_name,angles,rho,compressible):
    
    sym = 1
    
    # name_quant = 'FX'
    # name_quant = 'FY'
    # name_quant = 'FZ'
    # name_quant = 'MX'
    name_quant = 'MY'
    # name_quant = 'MZ'
    
    for angle in angles:
        
        folder = case_name + "_" + str(angle)
        # folder_path_quan = r"postProcessing\forces_1"
        
        surfaces = [ "disk" ]
        kk = 0
        for surface in surfaces:
            kk += 1
            folder_path = os.path.join(".\\",folder,"postProcessing",surface)
            subdirectories = sorted( ([dd for dd in os.listdir(folder_path) ]) )
            print(subdirectories)
        
            for folder_data in subdirectories:
                inp = os.path.join(".\\",folder,"postProcessing",surface,str(folder_data),"forces.dat")
            
                with open(inp, 'r', encoding="utf-8") as file:
                    lines = file.readlines()
            
                lines = [line for line in lines if not line.startswith('#')]
                pattern = r'[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?'
                data = [re.findall(pattern, line) for line in lines]
                
                df = pd.DataFrame(data, columns=[
                    'Time', 'FX pressure', 'FY pressure', 'FZ pressure',
                    'FX viscous', 'FY viscous', 'FZ viscous',
                    'MX pressure', 'MY pressure', 'MZ pressure',
                    'MX viscous', 'MY viscous', 'MZ viscous'])
            
                df = df.apply(pd.to_numeric)
                Time = df['Time']
                
                if folder_data == "0":
                    fig = plt.figure(num=angle+3, figsize=(12, 9), dpi=80 )
                    fig.canvas.manager.set_window_title("Force / Torque for " + "angle " + str(angle) + "°")
                if kk == 1: 
                    fig.clear()
                plt.title("Force / Torque for "+ "angle " + str(angle) + "°"+", iteration = " +str("%.0f"%(Time.size-1)) +", time = "+str((Time.iloc[-1])) , fontsize=20)
                
                df[name_quant] = df[name_quant + ' pressure']+df[name_quant + ' viscous']
                pd.set_option('display.max_columns', None)
            
                print(df)
                print("Iteration = ", df['Time'].size-1)
                print('FX pressure =', str("%.0f"%(sym*df['FX pressure'].iloc[-1])))
                print('FY pressure =', str("%.0f"%(sym*df['FY pressure'].iloc[-1])))
                print('FZ pressure =', str("%.0f"%(sym*df['FZ pressure'].iloc[-1])))
                print('FX viscous =', str("%.0f"%(sym*df['FX viscous'].iloc[-1])))
                print('FY viscous =', str("%.0f"%(sym*df['FY viscous'].iloc[-1])))
                print('FZ viscous =', str("%.0f"%(sym*df['FZ viscous'].iloc[-1])))
                print('MX pressure =', str("%.0f"%(sym*df['MX pressure'].iloc[-1])))
                print('MY pressure =', str("%.0f"%(sym*df['MY pressure'].iloc[-1])))
                print('MZ pressure =', str("%.0f"%(sym*df['MZ pressure'].iloc[-1])))
                print('MX viscous =', str("%.0f"%(sym*df['MX viscous'].iloc[-1])))
                print('MY viscous =', str("%.0f"%(sym*df['MY viscous'].iloc[-1])))
                print('MZ viscous =', str("%.0f"%(sym*df['MZ viscous'].iloc[-1])))
                print()
                
                name_M = name_quant + ' pressure'
               
                Torque = df[name_M]*sym
                print(name_M + " ("+surface+")" + " =", str("%.0f"%(Torque.iloc[-1])) )
                plt.plot(Time, Torque , label= name_M + " ("+surface+")" +" = "+ str("%.0f"%(Torque.iloc[-1])) , linestyle='-', linewidth= 3 )
                
                name_M = name_quant + ' viscous'
                Torque = df[name_M]*sym
                print(name_M + " ("+surface+")" + " =", str("%.0f"%(Torque.iloc[-1])) )
                plt.plot(Time, Torque , label= name_M + " ("+surface+")" +" = "+ str("%.0f"%(Torque.iloc[-1])) , linestyle='-', linewidth= 3 )
                
                name_M = name_quant
                Torque = df[name_M]*sym
                print(name_M + " ("+surface+")" + " =", str("%.0f"%(Torque.iloc[-1])) )
                plt.plot(Time, Torque , label= name_M + " ("+surface+")" +" = "+ str("%.0f"%(Torque.iloc[-1])), linestyle='-', linewidth= 3 )
                       
        num_curves = len(plt.gca().get_lines())
        import matplotlib as mpl
        cmap = mpl.cm.get_cmap('viridis_r', num_curves)
        lines = plt.gca().get_lines()
        for ci, line in enumerate(lines):
            line.set_color(cmap(ci))
        plt.grid(linestyle= '-', linewidth= 1 ) 
        plt.rc('xtick', labelsize= 14)   
        plt.rc('ytick', labelsize= 14) 
        plt.ylabel('$Force$' + ' $[N]$ ' +' / '+ '$Torque$' + ' $[Nm]$ ' , fontsize = 14)
        plt.xlabel('$Time$' + ' $[-]$ ' , fontsize = 14)
        plt.legend(loc='best', shadow= True,  ncol=1, fontsize= 13)    
        # ylim_min = -300e3   ;   ylim_max = 200e3
        ylim_min = sym*df[name_quant].iloc[-1]-sym*abs(df[name_quant].iloc[-1])/20   ;   ylim_max = sym*df[name_quant].iloc[-1]+sym*abs(df[name_quant].iloc[-1])/20
        # print( df[name_quant].iloc[-1])
        # print( abs(df[name_quant].iloc[-1]))
        # plt.ylim(ylim_min,ylim_max)
        plt.tight_layout()
        plt.show(block= False )  
        fig.canvas.draw() 

if __name__ == '__main__':
    
    case_name = "Y:/home/trusinja/FOAM_WORK_UBUNTU/Open_FOAM_12/DN3200_in_straight_pipe/all_incompressibleFluid/case"
    
    angles = [ 0 ]
    rho = 998.23
    if "incompressible" in case_name:
        compressible = 0
    else:  compressible = 1
    
    
    forces(case_name,angles,rho,compressible)












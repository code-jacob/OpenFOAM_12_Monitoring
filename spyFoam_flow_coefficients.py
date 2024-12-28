"""
Created on Tue Nov 28 20:44:20 2023
Author: Jakub Trušina
Name: spyFoam_flow_coefficients.py
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import interpolate
import re
import os


def flow_coefficients(case_name,angles,rho,compressible):
    
    surface = "force"
    
    sym = 1
    
    nu = 1e-6 # m**2/s
    K = 70E-6 # m
    
    # DN = 2000   /1000 # m
    DN = 100 /1000
        
    # L = 30 # m
    # L = 2.140
    # L = 2.265
    # L = 32.140
    L = 0
    # L = 16+32
    
    # axis = "X"
    # axis_pipe = "Y"
    # tangent_pipe = "Z"
    
    # axis = "Z"
    # axis_pipe = "Y"
    # tangent_pipe = "X"
    
    axis = "Y"
    axis_pipe = "X"
    tangent_pipe = "Z"
    
    if angles == []:
        len_angles = 1
    else: len_angles =  len(angles)
    dp_total_angles = np.zeros((len_angles))
    Q_angles = np.zeros((len_angles))
    zeta_angles = np.zeros((len_angles))
    zeta_valve_angles = np.zeros((len_angles))
    pi_M_angles = np.zeros((len_angles))
    pi_F_axial_angles = np.zeros((len_angles))
    pi_F_tangential_angles = np.zeros((len_angles))
    M_angles = np.zeros((len_angles))
    M_pressure_angles = np.zeros((len_angles))
    M_viscous_angles = np.zeros((len_angles))
        
    if compressible == 1:
        norm_rho = rho # kg/m**3
    
    global i
    i = 0
    def run():
        
        global rho, i
        
    
        # folder = case_name + "_" + str(angle)
        folder_data = 0
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
        
        M_pressure = df["M"+axis+' pressure']*sym 
        M_viscous = df["M"+axis+' viscous']*sym 
        M = M_pressure + M_viscous
        F_axial = df["F"+axis_pipe+' pressure']*sym + df["F"+axis_pipe+' viscous']*sym
        F_tangential = df["F"+tangent_pipe+' pressure']*sym + df["F"+tangent_pipe+' viscous']*sym
        
        inp = os.path.join(".\\", folder , r".\postProcessing\patchFlowRate(patch=inlet)",str(folder_data),"surfaceFieldValue.dat")
        df_Q_inlet = pd.read_csv(inp, skiprows=3, delimiter="\t")
        
        inp = os.path.join(".\\", folder , r".\postProcessing\patchFlowRate(patch=outlet)",str(folder_data),"surfaceFieldValue.dat")
        df_Q_outlet = pd.read_csv(inp, skiprows=3, delimiter="\t")
        
        if compressible == 1:
            inp_inlet = os.path.join(".\\", folder , r".\postProcessing\patchAverage(patch=inlet,fields=(ptotal(p)mag(U)rhoT))",str(folder_data),"surfaceFieldValue.dat")
            inp_outlet = os.path.join(".\\", folder , r".\postProcessing\patchAverage(patch=outlet,fields=(ptotal(p)mag(U)rhoT))",str(folder_data),"surfaceFieldValue.dat")
        else:
            inp_inlet = os.path.join(".\\", folder , r".\postProcessing\patchAverage(patch=inlet,fields=(pstatic(p)total(p)mag(U)))",str(folder_data),"surfaceFieldValue.dat")
            inp_outlet = os.path.join(".\\", folder , r".\postProcessing\patchAverage(patch=outlet,fields=(pstatic(p)total(p)mag(U)))",str(folder_data),"surfaceFieldValue.dat")
        
        df_inlet = pd.read_csv(inp_inlet, skiprows=3, delimiter="\t")
        df_outlet = pd.read_csv(inp_outlet, skiprows=3, delimiter="\t")
        
        print(df_inlet.columns.values)
        print("Time =", Time.iloc[-1] ) #, ", Angle =", angle )
        print("symmetry = 1/"+str(sym))
        
        if compressible == 1:
           
            p_static_inlet = df_inlet["areaAverage(p)"]
            p_static_outlet = df_outlet["areaAverage(p)"]
            dp_static = p_static_inlet - p_static_outlet
            
            p_total_inlet = df_inlet["areaAverage(total(p))"]
            p_total_outlet = df_outlet["areaAverage(total(p))"]
            dp_total = p_total_inlet - p_total_outlet
            
            T_inlet = df_inlet["areaAverage(T)"]
            T_outlet = df_outlet["areaAverage(T)"]
            T = (T_inlet + T_outlet)/2
            
            rho_inlet = df_inlet["areaAverage(rho)"]
            rho_outlet = df_outlet["areaAverage(rho)"]
            rho = (rho_inlet + rho_outlet)/2
            
            Qm_inlet = df_Q_inlet["sum(phi)"]*sym 
            Qm_outlet = df_Q_outlet["sum(phi)"]*sym 
            Q_m = (abs(Qm_inlet) + abs(Qm_inlet))/2
            Q = Q_m/rho
            norm_Q = (Q_m/norm_rho)
            
            Q_inlet = (Qm_inlet/rho_inlet)
            Q_outlet = (Qm_outlet/rho_outlet)
            
        else:
            
            p_kinematic_inlet = df_inlet["areaAverage(p)"]
            p_kinematic_outlet = df_outlet["areaAverage(p)"]
            dp_kinematic = p_kinematic_inlet - p_kinematic_outlet
            
            p_static_inlet = df_inlet["areaAverage(static(p))"]
            p_static_outlet = df_outlet["areaAverage(static(p))"]
            dp_static = p_static_inlet - p_static_outlet
            
            p_total_inlet = df_inlet["areaAverage(total(p))"]
            p_total_outlet = df_outlet["areaAverage(total(p))"]
            dp_total = p_total_inlet - p_total_outlet
            
            Q_inlet = df_Q_inlet["sum(phi)"]*sym 
            Q_outlet = df_Q_outlet["sum(phi)"]*sym 
            Q = (abs(Q_inlet) + abs(Q_inlet))/2
            
        U_inlet = df_inlet["areaAverage(mag(U))"]
        U_outlet = df_outlet["areaAverage(mag(U))"]
            
        dp_dynamic = dp_total - dp_static
        v = Q/((np.pi * DN**2)/4)
        zeta = (2 * dp_total) / (rho * v**2)
        Re = (v*DN) / nu
        
        if compressible == 1:
            print("p_total_inlet =", p_total_inlet.iloc[-1])
            print("p_total_outlet =", p_total_outlet.iloc[-1])
            print("dp_total =", dp_total.iloc[-1])
            
            print("p_static_inlet =", p_static_inlet.iloc[-1])
            print("p_static_outlet =", p_static_outlet.iloc[-1])
            print("dp_static =", dp_static.iloc[-1])
            
            print("rho_inlet =", rho_inlet.iloc[-1])
            print("rho_outlet =", rho_outlet.iloc[-1])
            print("rho =", rho.iloc[-1] )
            
            print("T_inlet =", T_inlet.iloc[-1])
            print("T_outlet =", T_outlet.iloc[-1])
            print("T =", T.iloc[-1] )
        
            print("Qm_inlet =", Qm_inlet.iloc[-1])
            print("Qm_outlet =", Qm_outlet.iloc[-1])
            print("Q_m =", Q_m.iloc[-1] )
            print("Q_norm =", norm_Q.iloc[-1] )
            
            print("Q_inlet =", Q_inlet.iloc[-1])
            print("Q_outlet =", Q_outlet.iloc[-1])
        else:
            
            print("p_kinematic_inlet =", p_kinematic_inlet.iloc[-1])
            print("p_kinematic_outlet =", p_kinematic_outlet.iloc[-1])
            print("dp_kinematic =", dp_kinematic.iloc[-1])
            
            print("p_total_inlet =", p_total_inlet.iloc[-1])
            print("p_total_outlet =", p_total_outlet.iloc[-1])
            print("dp_total =", dp_total.iloc[-1])
            
            print("p_static_inlet =", p_static_inlet.iloc[-1])
            print("p_static_outlet =", p_static_outlet.iloc[-1])
            print("dp_static =", dp_static.iloc[-1])
            
            print("Q_inlet =", Q_inlet.iloc[-1])
            print("Q_outlet =", Q_outlet.iloc[-1])
            
        print("U_inlet =", U_inlet.iloc[-1])
        print("U_outlet =", U_outlet.iloc[-1])    
        
        print("v =", v.iloc[-1] )
        print("zeta =", zeta.iloc[-1])
        print("Re =", Re.iloc[-1])
        print("")
        
        lambd = (2*np.log10(DN/K)+1.14)**(-2)
        zeta_pipe = (lambd * L) / DN
        # zeta_pipe = 0.10809745232093505
        
        if compressible == 1:
            dp_tot_pipe = (zeta_pipe * rho.iloc[-1] * (v.iloc[-1])**2)/2
        else: dp_tot_pipe = (zeta_pipe * rho * (v.iloc[-1])**2)/2 
        
        print("lambda =", lambd)
        print("zeta_pipe =", zeta_pipe)
        print("delta p_tot pipe =", dp_tot_pipe)
        print("")
        
        dp_total_valve = dp_total - dp_tot_pipe
        
        # zeta_valve = (2 * dp_total_valve) / (rho.iloc[-1] * v**2)
        # Kv = ((norm_Q*3600)/5141)*np.sqrt(abs((norm_rho*df_inlet["areaAverage(T)"])/((dp_total_valve*1e-6)*(df_outlet["areaAverage(total(p))"]*1e-6))))
        zeta_valve = (2 * dp_total_valve) / (rho * v**2)
        Kv = (3600*Q)*np.sqrt(abs(rho/(998.23*(dp_total_valve/1e5))))
        
        print("delta p_tot valve =", dp_total_valve.iloc[-1])
        print("zeta valve =", zeta_valve.iloc[-1])
        print("Kv =", Kv.iloc[-1])
        
        pi_M = M / ( dp_total_valve * DN**3 )
        pi_F_axial = F_axial / ( dp_total_valve * DN**2  )
        pi_F_tangential = F_tangential / ( dp_total_valve * DN**2 )
        
        print("pi_M =", pi_M.iloc[-1])
        print("pi_F_axial =", pi_F_axial.iloc[-1])
        print("pi_F_tangential =", pi_F_tangential.iloc[-1])
        
        if angles == []:
            fig = plt.figure(num=0, figsize=(14,10), dpi=80, facecolor='w', edgecolor='k')
            fig.canvas.manager.set_window_title("Hydrodynamic Coefficients")
            fig.clear()
            plt.title("Hydrodynamic Coefficients, Iteration = " + str("%.0f"%(Time.size-1))+", Time = "+str((Time.iloc[-1])), fontsize= 20)
        else:
            fig = plt.figure(num=angle+1, figsize=(14,10), dpi=80, facecolor='w', edgecolor='k')
            fig.canvas.manager.set_window_title("Hydrodynamic Coefficients for " + "Angle " + str(angle) + "°")
            fig.clear()
            plt.title("Hydrodynamic Coefficients for "+ "Angle " + str(angle) + "°"+", Iteration = " + str("%.0f"%(Time.size-1))+", Time = "+str((Time.iloc[-1])), fontsize= 20)
        
        plt.plot(Time, p_total_inlet, linewidth= 3, label="$p_{total,inlet}$ $[Pa]$"+" = "+str("%.3g"%((p_total_inlet.iloc[-1]))) )
        plt.plot(Time, p_total_outlet, linewidth= 3, label="$p_{total,outlet}$ $[Pa]$"+" = "+str("%.3g"%((p_total_outlet.iloc[-1]))) )
        plt.plot(Time, dp_total, linewidth= 3, label="$\Delta p_{total}$ $[Pa]$"+" = "+str("%.3g"%((dp_total.iloc[-1]))) )
        plt.text(Time.iloc[-1], dp_total.iloc[-1], "$\Delta p_{total}$ $[Pa]$" )
        
        plt.plot(Time, p_static_inlet, linewidth= 3, label="$p_{static,inlet}$ $[Pa]$"+" = "+str("%.3g"%((p_static_inlet.iloc[-1]))) )
        plt.plot(Time, p_static_outlet, linewidth= 3, label="$p_{static,outlet}$ $[Pa]$"+" = "+str("%.3g"%((p_static_outlet.iloc[-1]))) )
        plt.plot(Time, dp_static, linewidth= 3, label="$\Delta p_{static}$ $[Pa]$"+" = "+str("%.3g"%((dp_static.iloc[-1]))) )
        plt.text(Time.iloc[-1], dp_static.iloc[-1], "$\Delta p_{static}$ $[Pa]$" )
        
        plt.plot(Time, dp_dynamic, linewidth= 3, label="$\Delta p_{dynamic}$ $[Pa]$"+" = "+str("%.3g"%((dp_dynamic.iloc[-1]))) )
        
        plt.plot(Time, Q_inlet, linewidth= 3, label="$Q_{inlet}$ $[m^3/s]$"+" = "+str("%.3g"%((Q_inlet.iloc[-1]))) )
        plt.plot(Time, Q_outlet, linewidth= 3, label="$Q_{outlet}$ $[m^3/s]$"+" = "+str("%.3g"%((Q_outlet.iloc[-1]))) )
        plt.plot(Time, Q, linewidth= 3, label="$Q$ $[m^3/s]$"+" = "+str("%.3g"%((Q.iloc[-1]))) )
        
        plt.plot(Time, U_inlet, linewidth= 3, label="$U_{inlet}$ $[m/s]$"+" = "+str("%.3g"%((U_inlet.iloc[-1]))) )
        plt.plot(Time, U_outlet, linewidth= 3, label="$U_{outlet}$ $[m/s]$"+" = "+str("%.3g"%((U_outlet.iloc[-1]))) )
        
        plt.plot(Time, zeta, linewidth= 3, label="$\zeta$ $[-]$"+" = "+str("%.3g"%((zeta.iloc[-1]))) )
        plt.text(Time.iloc[-1], zeta.iloc[-1], "$\zeta$ $[-]$" )
        plt.plot(Time, zeta_valve, linewidth= 3, label="$\zeta_{valve}$ $[-]$"+" = "+str("%.3g"%((zeta_valve.iloc[-1]))) )
        
        plt.plot(Time, Kv, linewidth= 3, label="$Kv$ $[m^3/h]$"+" = "+str("%.3g"%((Kv.iloc[-1]))) )
        plt.plot(Time, Re, linewidth= 3, label="$Re$ $[-]$"+" = "+str("%.3g"%((Re.iloc[-1]))) )
        plt.plot(Time, v, linewidth= 3, label="$v_{inf}$ $[m/s]$"+" = "+str("%.3g"%((v.iloc[-1]))) )
                       
        plt.plot(Time, pi_M, linewidth= 3, label="$\pi_M$ $[-]$"+ " ("+surface+")" +" = "+str("%.3g"%((pi_M.iloc[-1]))) )
        plt.plot(Time, pi_F_axial, linewidth= 3, label="$\pi_{F,ax}$ $[-]$"+ " ("+surface+")" +" = "+str("%.3g"%((pi_F_axial.iloc[-1]))) )
        plt.plot(Time, pi_F_tangential, linewidth= 3, label="$\pi_{F,tan}$ $[-]$"+ " ("+surface+")" +" = "+str("%.3g"%((pi_F_tangential.iloc[-1]))) )
        
        if compressible == 0:
            
            plt.plot(Time, p_kinematic_inlet, linewidth= 3, label="$p_{kinematic,inlet}$ $[m^2/s^2]$"+" = "+str("%.3g"%((p_kinematic_inlet.iloc[-1]))) )
            plt.plot(Time, p_kinematic_outlet, linewidth= 3, label="$p_{kinematic,outlet}$ $[m^2/s^2]$"+" = "+str("%.3g"%((p_kinematic_outlet.iloc[-1]))) )
            plt.plot(Time, dp_kinematic, linewidth= 3, label="$\Delta p_{kinematic}$ $[m^2/s^2]$"+" = "+str("%.3g"%((dp_kinematic.iloc[-1]))) )
            plt.text(Time.iloc[-1], dp_kinematic.iloc[-1], "$\Delta p_{kinematic}$ $[m^2/s^2]$" )
        
        if compressible == 1:
            
            plt.plot(Time, T_inlet, linewidth= 3, label=r"$T_{inlet}$ $[K]$"+" = "+str("%.3g"%((T_inlet.iloc[-1]))) )
            plt.plot(Time, T_outlet, linewidth= 3, label=r"$T_{outlet}$ $[K]$"+" = "+str("%.3g"%((T_outlet.iloc[-1]))) )
            plt.plot(Time, T, linewidth= 3, label=r"$T$ $[K]$"+" = "+str("%.3g"%((T.iloc[-1]))) )
            
            plt.plot(Time, rho_inlet, linewidth= 3, label=r"$\rho_{inlet}$ $[kg/m^3]$"+" = "+str("%.3g"%((rho_inlet.iloc[-1]))) )
            plt.plot(Time, rho_outlet, linewidth= 3, label=r"$\rho_{outlet}$ $[kg/m^3]$"+" = "+str("%.3g"%((rho_outlet.iloc[-1]))) )
            plt.plot(Time, rho, linewidth= 3, label=r"$\rho$ $[kg/m^3]$"+" = "+str("%.3g"%((rho.iloc[-1]))) )
            
            plt.plot(Time, Qm_inlet, linewidth= 3, label="$Q_{m,inlet}$ $[kg/s]$"+" = "+str("%.3g"%((Qm_inlet.iloc[-1]))) )
            plt.plot(Time, Qm_outlet, linewidth= 3, label="$Q_{m,outlet}$ $[kg/s]$"+" = "+str("%.3g"%((Qm_outlet.iloc[-1]))) )
            plt.plot(Time, Q_m, linewidth= 3, label="$Q_m$ $[kg/s]$"+" = "+str("%.3g"%((Q_m.iloc[-1]))) )
            

        plt.rc('xtick', labelsize= 14)   
        plt.rc('ytick', labelsize= 14) 
        plt.xlabel(r' Time [s]', fontsize = 14)
        # plt.yscale('log')
        # plt.xscale('log')
        
        num_curves = len(plt.gca().get_lines())
        import matplotlib as mpl
        cmap = mpl.cm.get_cmap('turbo', num_curves)
        lines = plt.gca().get_lines()
        for ci, line in enumerate(lines):
            line.set_color(cmap(ci))
        plt.legend(loc='best',  ncol=4, shadow= True, fontsize= 11)
        plt.grid(linestyle= '-', linewidth= 1)
        # plt.ylim(-1, 40)
        plt.tight_layout()
        plt.show(block= False )  
        fig.canvas.draw() 
        
        dp_total_angles[i] = dp_total.iloc[-1]
        Q_angles[i] = Q.iloc[-1]
        zeta_angles[i] = zeta.iloc[-1]
        zeta_valve_angles[i] = zeta_valve.iloc[-1]
        pi_M_angles[i] = pi_M.iloc[-1]
        pi_F_axial_angles[i] = pi_F_axial.iloc[-1]
        pi_F_tangential_angles[i] = pi_F_tangential.iloc[-1]
        M_angles[i] = M.iloc[-1]
        M_pressure_angles[i] = M_pressure.iloc[-1]
        M_viscous_angles[i] = M_viscous.iloc[-1]
        
        i+=1

        df = pd.DataFrame({     
                                "zeta valve": zeta_valve_angles,
                                "pi_M": pi_M_angles,
                                "pi_F_axial": pi_F_axial_angles,
                                "pi_F_tangential": pi_F_tangential_angles,
                                "M": M_angles,
                                "M_pressure": M_pressure_angles,
                                "M_viscous": M_viscous_angles,
                                "dp_total": dp_total_angles,
                                "Q": Q_angles,
                                "zeta": zeta_angles,
                                                                    }, index=angles)
        df.index.name = 'Angles'
        df.to_csv("Flow_Coefficients.csv")
        # print(df)
        # print("zeta valve 0 = ",df.loc[40, "zeta valve"])
           
    # plt.close("all")
    if len(angles) > 1:
        fig = plt.figure(num=None, figsize=(15, 10), dpi=80 )
        fig.canvas.manager.set_window_title("Flow Coefficients")
        fig.canvas.manager.window.showMaximized()
        
        for kk in range(0,8+1):
            font = 15
            if kk == 0:
                plt.subplot(3, 3, 1)
                plt.title( "Pressure Drop - $\Delta p_{total}$ [Pa]"  , fontsize= font)
                clr = "r"
                phys_quant = dp_total_angles
                plt.grid(linestyle= '--', linewidth= 1)
                plt.xticks(np.arange(angles[0], angles[-1], 10 ))
            if kk == 1:
                plt.subplot(3, 3, 4)
                plt.title( "Pressure Drop Coefficient - $\zeta$ [-]"  , fontsize= font)    
                clr = "b"
                phys_quant = zeta_angles
                # plt.yscale('log')
                plt.grid(linestyle= '--', linewidth= 1)
                plt.xticks(np.arange(angles[0], angles[-1], 10 ))
                # plt.yscale('log')
            if kk == 2:
                plt.subplot(3, 3, 7)
                plt.title( "Pressure Drop Coefficient - $\zeta_{valve}$ for the valve [-]"  , fontsize= font)
                clr = "C0"
                phys_quant = zeta_valve_angles
                # plt.yscale('log')
                plt.grid(linestyle= '--', linewidth= 1)
                plt.xticks(np.arange(angles[0], angles[-1], 10 ))
                # plt.yscale('log')
            if kk == 3:
                plt.subplot(3, 3, 2)
                plt.title( "Hydrodynamic Torque Coefficient - "+"$\pi_M$" + " for the valve [-]" , fontsize= font)
                clr = "m"
                phys_quant = pi_M_angles
                plt.grid(linestyle= '--', linewidth= 1)
                plt.xticks(np.arange(angles[0], angles[-1], 10 ))
            if kk ==4 :
                plt.subplot(3, 3, 5)
                plt.title( "Hydrodynamic Axial Force Coefficient - "+ "$\pi_{F,ax}$" + " for the valve [-]"  , fontsize= font)
                clr = "#C8C416"
                phys_quant = pi_F_axial_angles
                plt.grid(linestyle= '--', linewidth= 1)
                plt.xticks(np.arange(angles[0], angles[-1], 10 ))
            if kk == 5:
                plt.subplot(3, 3, 8)
                plt.title( "Hydrodynamic Tangential Force Coefficient - "+"$\pi_{F,tan}$" + " for the valve [-]"  , fontsize= font) 
                clr = "#FF6600"
                phys_quant = pi_F_tangential_angles     
                plt.grid(linestyle= '--', linewidth= 1)
                plt.xticks(np.arange(angles[0], angles[-1], 10 ))
            if kk == 6:
                plt.subplot(3, 3, 3)
                plt.title( "Hydrodynamic Torque - "+"$M_{H}$" + " on the disk [Nm]"  , fontsize= font) 
                clr = "k"
                phys_quant = M_angles     
                plt.grid(linestyle= '--', linewidth= 1)
                plt.xticks(np.arange(angles[0], angles[-1], 10 ))
            if kk == 7:
                plt.subplot(3, 3, 6)
                plt.title( "Hydrodynamic Torque - pressure - "+"$M_{Hp}$" + " on the disk [Nm]"  , fontsize= font) 
                clr = "#1A9A1D"
                phys_quant = M_pressure_angles     
                plt.grid(linestyle= '--', linewidth= 1)
                plt.xticks(np.arange(angles[0], angles[-1], 10 ))
            if kk == 8:
                plt.subplot(3, 3, 9)
                plt.title( "Hydrodynamic Torque - viscous - "+"$M_{Hv}$" + " on the disk [Nm]"  , fontsize= font) 
                clr = "#8908AC"
                phys_quant = M_viscous_angles     
                plt.grid(linestyle= '--', linewidth= 1)
                plt.xticks(np.arange(angles[0], angles[-1], 10 ))
                       
            plt.plot(angles, phys_quant , linestyle='--', linewidth= 1, color=clr )
            plt.plot(angles, phys_quant , "s", color=clr, markersize=8 )
            
            for ii in range(0,len(angles)):
                plt.text(angles[ii], phys_quant[ii] , str("%.3E"%(phys_quant[ii])), fontsize= 12 , color=clr, bbox=dict(facecolor='white', edgecolor=clr, boxstyle='round') )
            
            xx = np.linspace(angles[0], angles[-1], 100)
            bspline = interpolate.make_interp_spline(angles, phys_quant, k=5 )
            aprox = bspline(xx)
            plt.plot( xx, aprox , color=clr, linestyle='-',  linewidth= 2 )
        
        plt.rc('xtick', labelsize= 10)   
        plt.rc('ytick', labelsize= 10) 
        fig.supxlabel(r' Angle [°]', fontsize = 14)
        plt.tight_layout()
        plt.show(block= False )  
        fig.canvas.draw() 
        plt.savefig("Flow_Coefficients.png")
                
        fig = plt.figure(num=None, figsize=(15, 10), dpi=80 )
        fig.canvas.manager.set_window_title("delta_p_total - Q")
        plt.plot(dp_total_angles, Q_angles , linestyle='-', linewidth= 3, color="k" )
        plt.plot(dp_total_angles, Q_angles , "s", color="k", markersize=8 )
        for ii in range(0,len(angles)):
            plt.text(dp_total_angles[ii], Q_angles[ii] , str("%.0f"%(angles[ii])) + "°" , fontsize= 14, bbox=dict(facecolor='white', edgecolor="k", boxstyle='round') )
        
        plt.rc('xtick', labelsize= 14)   
        plt.rc('ytick', labelsize= 14) 
        plt.ylabel("$Q$ $[m^3/s]$", fontsize = 14)
        plt.xlabel("$\Delta p_{total}$ $[Pa]$", fontsize = 14)
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
    
    
    
    case_name = r"C:\Users\trusinja\Desktop\FOAM_WORK\Pipe_Elbow\Hexahedral"
    case_name = r"C:\Users\trusinja\Desktop\FOAM_WORK\Pipe_Elbow\Hexcore"
    case_name = r"C:\Users\trusinja\Desktop\FOAM_WORK\Pipe_Elbow\Polyhedral"
    case_name = r"C:\Users\trusinja\Desktop\FOAM_WORK\Pipe_Elbow\Tetrahedral"
    
    angles = [  ]
    rho = 998.23
    compressible = 0
    
    
    flow_coefficients(case_name,angles,rho,compressible)








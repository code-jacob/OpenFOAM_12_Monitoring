# -*- coding: utf-8 -*-
"""
Created on Fri Mar  1 07:10:43 2024
Author: Jakub Trušina
Name: spyFoam_GUI.py.py
"""

update_after_default = 6000


case_name = "Y:/home/trusinja/FOAM_WORK_UBUNTU/Open_FOAM_12/DN3200_in_straight_pipe/all_fluid/case"

angles = [ 0 ]
rho = 998.23
if "incompressible" in case_name:
    compressible = 0
else:  compressible = 1

# =============================================================================================

import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt

from spyFoam_residuals import residuals
from spyFoam_flow_coefficients import flow_coefficients
from spyFoam_cellMinMax import cellMinMax
from spyFoam_forces import forces

def close_window(event=None):
    plt.close("all")
    window.destroy()

def run_residuals():
    case_name = str(directory_entry.get())
    residuals(case_name,angles,rho,compressible)
    update_after = int(update_after_entry.get())
    window.after( update_after*1000 , run_residuals )

def run_flow_coefficients():
    case_name = str(directory_entry.get())
    flow_coefficients(case_name,angles,rho,compressible)
    update_after = int(update_after_entry.get())
    window.after( update_after*1000 , run_flow_coefficients )
    
def run_cellMinMax():
    case_name = str(directory_entry.get())
    cellMinMax(case_name,angles,rho,compressible)
    update_after = int(update_after_entry.get())
    window.after( update_after*1000 , run_cellMinMax )

def run_forces():
    case_name = str(directory_entry.get())
    forces(case_name,angles,rho,compressible)
    update_after = int(update_after_entry.get())
    window.after( update_after*1000 , run_forces )


fnt_size = 15
fnt = "Century Gothic"

window = tk.Tk()
window.title("spyFoam_GUI")

wdth = 10
pdx = 0
row = 1
style = ttk.Style()
style.theme_use('vista')
style.configure('my.TButton', background="light blue", foreground = 'black', font=(fnt, fnt_size))

row = row 
run_button = ttk.Button(window, text="Residuals", width=10, style='my.TButton', command=lambda: run_residuals())
run_button.grid(row=row, column=0, columnspan=3, sticky="we", padx=10, pady=10)

row = row + 1
run_button = ttk.Button(window, text="Flow Coefficients", width=10, style='my.TButton', command=lambda: run_flow_coefficients())
run_button.grid(row=row, column=0, columnspan=3, sticky="we", padx=10, pady=10)  

row = row + 1
run_button = ttk.Button(window, text="min/max of Cells", width=10, style='my.TButton', command=lambda: run_cellMinMax())
run_button.grid(row=row, column=0, columnspan=3, sticky="we", padx=10, pady=10)  

row = row + 1
run_button = ttk.Button(window, text="Forces", width=10, style='my.TButton', command=lambda: run_forces())
run_button.grid(row=row, column=0, columnspan=3, sticky="we", padx=10, pady=10) 

row = row + 1
update_after_label = ttk.Label(window, text="update after", font=(fnt,fnt_size))
update_after_label.grid(row=row, column=0, padx=10, pady=10, sticky="we")
update_after_label = ttk.Label(window, text="[s]", font=(fnt,fnt_size))
update_after_label.grid(row=row, column=2, padx=10, pady=10, sticky="w")
update_after_entry = ttk.Entry(window, width=wdth, font=(fnt,fnt_size-3))
update_after_entry.grid(row=row, column=1, sticky="e", padx=10, pady=10)
update_after_entry.insert(0, update_after_default )

row = row + 1
directory_label = ttk.Label(window, text="Directory:", font=(fnt,fnt_size)  )
directory_label.grid(row=row, column=0, padx=10, pady=10, sticky="e")
directory_entry = ttk.Entry(window, width=wdth, font=(fnt,fnt_size-3))
directory_entry.grid(row=row, column=1, columnspan=5, sticky="we", padx=pdx, pady=10)
directory_entry.insert( 0, case_name )

window.bind("<Return>", lambda event: (run_residuals(), run_flow_coefficients(), run_cellMinMax(), run_forces() ))   
window.bind("<Escape>", close_window)
window.protocol("WM_DELETE_WINDOW", close_window)
window.mainloop()




















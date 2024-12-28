# -*- coding: utf-8 -*-
"""
Created on Fri Mar  1 07:10:43 2024
Author: Jakub Trušina
Name: spyFoam_CHT_GUI.py.py
"""

update_after_default = 30

case_name = r"Y:\home\trusinja\FOAM_WORK_UBUNTU\Open_FOAM_12\Cooling_Ikea_Mug"  
regions = [ "AIR" , "WATER" , "MUG" ]
# regions = [ "WATER" ]


# case_name = r"Y:\home\trusinja\FOAM_WORK_UBUNTU\Open_FOAM_12\Gate_Valve_steady_state"  
# regions = [ "AIR" , "FLUID" , "BODY" , "BOLT" , "COVER" , "GASKET" , "NUTS" , "WASHER" ]
# regions = [ "COVER" ]

# case_name = r"Y:\home\trusinja\FOAM_WORK_UBUNTU\Open_FOAM_12\groud_air\transient_closed"  
# regions = [ "AIR" , "GROUND" ]
# regions = [ "AIR" ]

# =============================================================================================

import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt

from spyFoam_CHT_residuals import residuals
from spyFoam_CHT_probe import probe
from spyFoam_CHT_cellMinMax import cellMinMax

def close_window(event=None):
    plt.close("all")
    window.destroy()

def run_residuals():
    case_name = str(directory_entry.get())
    residuals(case_name, regions)
    update_after = int(update_after_entry.get())
    window.after( update_after*1000 , run_residuals )

def run_cellMinMax():
    case_name = str(directory_entry.get())
    cellMinMax(case_name, regions)
    update_after = int(update_after_entry.get())
    window.after( update_after*1000 , run_cellMinMax )

def run_probe():
    case_name = str(directory_entry.get())
    probe(case_name, regions)
    update_after = int(update_after_entry.get())
    window.after( update_after*1000 , run_probe )

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
run_button = ttk.Button(window, text="min/max of Cells", width=10, style='my.TButton', command=lambda: run_cellMinMax())
run_button.grid(row=row, column=0, columnspan=3, sticky="we", padx=10, pady=10)  

row = row + 1
run_button = ttk.Button(window, text="Probe", width=10, style='my.TButton', command=lambda: run_probe())
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

window.bind("<Return>", lambda event: ( run_residuals(), run_cellMinMax(),  run_probe(),  ))   
window.bind("<Escape>", close_window)
window.protocol("WM_DELETE_WINDOW", close_window)
window.mainloop()











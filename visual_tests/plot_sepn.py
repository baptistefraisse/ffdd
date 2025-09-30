""" Visual test : plot neutron separation energy """

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
from mpl_toolkits.axes_grid1 import make_axes_locatable
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ffdd.sepn import sepn

# plot function

def plot_sepn():
    """
    Plot neutron separation energy (MeV).

    Returns:
        str: plot file name.
    """
    
    # nuclei loop

    n_list, z_list, sepn_list = [], [], []

    for a in range(300):
        for z in range(150):
            try:
                sepn_list.append(sepn(a,z))
                n_list.append(a-z)
                z_list.append(z)
            except KeyError:
                continue

    # figure design

    fig, ax = plt.subplots(figsize=(8, 6))
    gs = gridspec.GridSpec(2, 1, height_ratios=[1, 4], hspace=0.05)

    scatter = ax.scatter(n_list, z_list, c=sepn_list, marker='s', cmap='coolwarm')

    ax.set_xlabel('N (Neutron number)', fontsize=14)
    ax.set_ylabel('Z (Proton number)', fontsize=14)
    ax.set_title(f'Neutron separation energy (MeV)', fontsize=16)
    
    ax.tick_params(axis='x', labelsize=14)
    ax.tick_params(axis='y', labelsize=14)
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="4%", pad=0.05) 
    cbar = fig.colorbar(scatter, cax=cax)
    cbar.set_label('Neutron separation energy (MeV)', fontsize=14)
    cbar.ax.tick_params(labelsize=14)

    ax.grid(True, linestyle='--', alpha=0.3)
    ax.set_aspect('auto')
    plt.tight_layout()

    # saving

    figure_file_name = f'plot_sepn.png'
    plt.savefig(figure_file_name)

    # return figure file name 

    return(figure_file_name)

# visual test

if __name__ == '__main__':
    _ = plot_sepn()



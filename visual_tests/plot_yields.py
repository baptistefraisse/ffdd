""" Visual test : plot yields """

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
from mpl_toolkits.axes_grid1 import make_axes_locatable
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ffdd.yields import read_fission_yields, fission_fragments
from ffdd.utils import z_to_name
plt.rcParams['font.family'] = 'Times New Roman'

# plot function

def plot_yields(a_target, z_target):
    """
    Plot fission yields at the highest available incident energy.

    Args:
        a_target (int): Mass number of the target nucleus.
        z_target (int): Charge number of the target nucleus.

    Returns:
        str: plot file name.
    """

    # fission yields file reading

    energy_list, nfy_list = read_fission_yields(a_target, z_target)

    # highest available incident energy selection

    energy = energy_list[-1]
    nfy = nfy_list[-1]

    # plot lists filling

    a_list, z_list, p_list = [], [], []
    ff_list = fission_fragments(nfy)
    for ff in ff_list:
        a_list.append(ff[0])
        z_list.append(ff[1])
        p_list.append(ff[2])
    a_list = np.array(a_list, dtype=int)
    z_list = np.array(z_list, dtype=int)
    p_list = np.array(p_list)

    a_list = a_list[p_list>0]
    z_list = z_list[p_list>0]
    p_list = p_list[p_list>0]
    logp_list = np.log(p_list)

    a_unique = np.unique(a_list)
    yield_a = np.array([np.sum(p_list[a_list == a]) for a in a_unique])
    z_unique = np.unique(z_list)
    yield_z = np.array([np.sum(p_list[z_list == z]) for z in z_unique])

    # figure design

    fig, ax = plt.subplots(figsize=(8, 6))
    gs = gridspec.GridSpec(2, 1, height_ratios=[1, 4], hspace=0.05)

    scatter = ax.scatter(a_list, z_list, c=logp_list, marker='s', cmap='coolwarm')

    yield_a_scaled = yield_a / np.max(yield_a) * 20 + 10  # arbitrary scale
    ax.plot(a_unique, yield_a_scaled, color='black', lw=2, alpha=0.6)
    yield_z_scaled = yield_z / np.max(yield_z) * 30 + 40  # arbitrary scale
    ax.plot(yield_z_scaled, z_unique, color='black', lw=2, alpha=0.6)

    ax.set_xlabel('A (Mass number)', fontsize=14)
    ax.set_ylabel('Z (Charge number)', fontsize=14)
    ax.set_title(f'Independent fission yields of n+{a_target}{z_to_name[z_target]} at {energy} MeV'
                + '\n' + f'with arbitrary scaled projections on A and Z', fontsize=16)
    
    ax.tick_params(axis='x', labelsize=14)
    ax.tick_params(axis='y', labelsize=14)
    divider = make_axes_locatable(ax)
    cax = divider.append_axes('right', size='4%', pad=0.05) 
    cbar = fig.colorbar(scatter, cax=cax)
    cbar.set_label('Probability (log)', fontsize=14)
    cbar.ax.tick_params(labelsize=14)

    ax.grid(True, linestyle='--', alpha=0.3)
    ax.set_aspect('auto')
    plt.tight_layout()

    # saving

    figure_file_name = f'plot_yields_{a_target}{z_to_name[z_target]}.png'
    plt.savefig(figure_file_name)

    # return figure file name 

    return(figure_file_name)

# visual test

if __name__ == '__main__':
    a_target = 238
    z_target = 92 
    _ = plot_yields(a_target, z_target)



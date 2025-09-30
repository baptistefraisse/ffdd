""" Visual test : plot mass """

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
from mpl_toolkits.axes_grid1 import make_axes_locatable
import sys
import os
from collections import defaultdict
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ffdd.tke import tke
from ffdd.utils import z_to_name
from ffdd.yields import read_fission_yields, fission_fragments

# plot function

def plot_tke(a_target, z_target, beta):
    """
    Plot Total Kinetic Energy (MeV) vs. fragments mass.

    Args:
        a_target (int): Mass number of the target nucleus.
        z_target (int): Charge number of the target nucleus.
        beta (float): Quadrupole deformation coefficient.

    Returns:
        str: plot file name.
    """

    # yields at lower available incident energy

    energy_list, nfy_list = read_fission_yields(a_target, z_target)
    energy = energy_list[0] 
    nfy = nfy_list[0]

    ff_list = fission_fragments(nfy)
    a_list, z_list, p_list, tke_list = [], [], [], []

    # fission fragments loop

    for ff in ff_list:

        a_list.append(ff[0])
        z_list.append(ff[1])
        p_list.append(ff[2])

        # heavy fragment 

        if ff[0] >= a_target//2:
            tke_list.append(tke(ff[0], ff[1], a_target-ff[0], z_target-ff[1], beta))

        # light fragment

        else:
            tke_list.append(tke(a_target-ff[0], z_target-ff[1], ff[0], ff[1], beta))
            
    a_list = np.array(a_list, dtype=int)
    z_list = np.array(z_list, dtype=int)
    p_list = np.array(p_list)
    tke_list = np.array(tke_list)

    # TKE vs. fragment mass

    tke_sum_by_a = defaultdict(float)
    proba_sum_by_a = defaultdict(float)

    for a, tke_val, p in zip(a_list, tke_list, p_list):
        tke_sum_by_a[a] += tke_val * p
        proba_sum_by_a[a] += p

    a_unique = sorted(tke_sum_by_a.keys())
    tke_avg = [tke_sum_by_a[a] / proba_sum_by_a[a] for a in a_unique]

    # figure design

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(a_unique, tke_avg, color='black')
    ax.set_xlabel('A (Mass number)', fontsize=14)
    ax.set_ylabel('TKE (MeV)', fontsize=14)
    ax.set_title(f'Total Kinetic Energy averaged on fragment mass for {a_target}{z_to_name[z_target]}+n at {energy} MeV',
                  fontsize=16)
    ax.tick_params(axis='x', labelsize=14)
    ax.tick_params(axis='y', labelsize=14)
    ax.grid(True, linestyle='--', alpha=0.3)
    ax.set_aspect('auto')
    plt.tight_layout()

    # saving

    figure_file_name = f'plot_tke.png'
    plt.savefig(figure_file_name)

    # return figure file name 

    return(figure_file_name)

# visual test

if __name__ == '__main__':
    a_target = 238
    z_target = 92
    beta = 0.2
    _ = plot_tke(a_target, z_target, beta)



""" Total Kinetic Energy (TKE) simulation for fission fragments """

# nuclear radius function


def nuclear_radius(a):
    """
    Compute nuclear radius with the incompressible model (r0 = 1.2 fm)

    Args:
        a (int): Mass number of the nucleus.

    Returns:
        float: Radius of the nucleus (fm).
    """

    r0 = 1.2  # fm
    return r0 * pow(a, 1 / 3)


# kinetic energy function


def tke(ah, zh, al, zl, beta = 0.2):
    """
    Compute total kinetic energy (TKE) of fission fragments
    with the simple model of two charged spheres in contact

    Args:
        Ah (int): Mass number of the heavy fragment.
        Zh (int): Charge number of the heavy fragment.
        Al (int): Mass number of the light fragment.
        Zl (int): Charge number of the light fragment.
        beta (float): Quadrupolar deformation coefficient.

    Returns:
        float: Total kinetic energy (MeV).
    """

    # nuclear radii (fm)

    rh = nuclear_radius(ah)
    rl = nuclear_radius(al)
    initial_distance = (rh + rl) * (1 + 2 * beta)

    # Coulomb constant (MeV.fm)

    k = 1.44

    # Total kinetic energy (MeV)

    return k * zh * zl / initial_distance

# visual test : plot TKE uranium 238

"""
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
from mpl_toolkits.axes_grid1 import make_axes_locatable
plt.rcParams["font.family"] = "Times New Roman"

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from yields.yields import read_fission_yields, fission_fragments_coupled, z_to_name

A_target = 238
Z_target = 92 
beta = 0.2

energy_list, nfy_list = read_fission_yields(238, 92)
energy = energy_list[1]
nfy = nfy_list[1]
tke_test = []
ah_list = []
ff_list = fission_fragments_coupled(A_target, Z_target, nfy)

for ff in ff_list:
    ah, zh, al, zl, _ = ff
    tke_test.append(tke(ah, zh, al, zl))

ah_list = [ff[0] for ff in ff_list]
zh_list = [ff[1] for ff in ff_list]

fig, ax = plt.subplots(figsize=(8, 6))
gs = gridspec.GridSpec(2, 1, height_ratios=[1, 4], hspace=0.05)
sc = plt.scatter(ah_list, zh_list, c=tke_test, cmap='coolwarm', s=60)
cbar = fig.colorbar(sc, ax=ax, pad=0.0)
cbar.set_label("Total kinetic energy (MeV)", fontsize=14)
cbar.ax.tick_params(labelsize=14)
ax.set_xlabel(r'Mass number of the heavy fragment', fontsize=14)
ax.set_ylabel(r'Charge number of the heavy fragment', fontsize=14)
ax.set_title(f"Total kinetic energy of n+{A_target}{z_to_name[Z_target]} fission at {energy} MeV"
             + "\n" + f"Model: two charged and deformed spheres in contact (beta = {beta})",
             fontsize=16)
ax.tick_params(axis='x', labelsize=14)
ax.tick_params(axis='y', labelsize=14)

plt.tight_layout()
plt.show()
"""
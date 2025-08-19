""" Reader of neutron-induced independent fission yields (ENDF-BVIII) """

# librairies

import os
import re
import openmc
from ffdd.utils import z_to_name, periodic_table

# reader of fission yields (via openmc)


def read_fission_yields(a, z):
    """
    Reader of evaluated neutron-induced fission yield (NFYs)
    before deexcitation (independent) at each available
    incident energies.

    Args:
        a (int): Mass number of the target nucleus.
        z (int): Charge number of the target nucleus.

    Returns:
        list: Incident energies (MeV).
        dict: Independent yields with (string format)
    """

    if z in z_to_name:
        atom_name = z_to_name[z]
    else:
        raise ValueError(f"ERROR: Target nucleus Z={z} unavailable in NFY data.")

    filename = f"data/yields/nfy-{z:03d}_{atom_name}_{a}.endf"
    filepath = os.path.join(os.path.dirname(__file__), filename)
    if not os.path.exists(filepath):
        raise FileNotFoundError(
            f"ERROR: Target nucleus (A={a},Z={z}) unavailable in NFY data."
        )

    nfy_eval = openmc.data.FissionProductYields(filepath)
    energy_list = nfy_eval.energies
    nfy_list = nfy_eval.independent
    energy_list = [e*1e-6 for e in energy_list] # eV to MeV

    return energy_list, nfy_list


# converter of fission yields into numbers : A, Z, probability


def fission_fragments(nfy):
    """
    Convert NFYs read in str format into lists of three
    floats: mass, charge and probability of each fragment.

    Args:
        nfy (dict): Neutron fission yields at a given energy.

    Returns:
        list: Fragments 5-uples [Ah,Zh,Al,Zl,P],
        Ah (int): Heavy fragment mass number, 
        Zh (int): Heavy fragment charge number,
        Al (int): Light fragment mass number,
        Zl (int): Light fragment charge number,
        P (float): Fragmentation probability.
    """

    # list of fission fragments and associated probability

    ff = []

    for nucleus, value in nfy.items():

        match = re.match(r"([A-Za-z]+)(\d+)", nucleus)

        if match:
            print(nucleus)
            element, a = match.groups()
            a = int(a)
            z = int(periodic_table[element])
            proba_str = str(value)

            if proba_str.startswith("(") and "e" in proba_str:
                # read format : "(X+/-Y)e-Z"
                base, exposant = proba_str.split("e")
                base = base.strip("()")
                x_str, _ = base.split("+/-")
                proba_float = float(x_str) * 10 ** int(exposant)
            else:
                # read format: "X+/-Y"
                x_str, _ = proba_str.split("+/-")
                proba_float = float(x_str)

            ff.append([a, z, proba_float]) # fusionner (sommer probq) les memes a et z (isomeres!!!)

    return ff


# fission fragments coupling


def fission_fragments_coupled(a, z, nfy):
    """
    Coupling of fission fragments by mass and charge conservation

    Args:
        a (int): Mass number of the target.
        z (int): Charge number of the target.
        nfy (list): Neutron fission yields at a given energy.

    Returns:
        list: coupled fission fragments 5-uples [Ah,Zh,Al,Zl,P],
              Ah (int): Heavy fragment mass number, 
              Zh (int): Heavy fragment charge number,
              Al (int): Light fragment mass number,
              Zl (int): Light fragment charge number,
              P (float): Fragmentation probability.
    """

    ff = fission_fragments(nfy)
    ff_coupled = []

    for k in range(len(ff) // 2):
        al, zl, p = ff[k]
        ah = a - al
        zh = z - zl
        ff_coupled.append([ah, zh, al, zl, p])

    return ff_coupled

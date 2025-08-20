""" Reader of neutron-induced independent fission yields (ENDF-BVIII.0) """

# librairies

import os
import re
import openmc
import numpy as np
from collections import defaultdict
from ffdd.utils import fiss_z_to_name, periodic_table

# OpenMC warning for missing uncertainties

import warnings
warnings.filterwarnings("ignore", "Using UFloat objects with std_dev==0")

# reader of fission yields (via openmc)


def read_fission_yields(a, z):
    """
    Reader of indepentend neutron-induced fission yield
    from nuclear data librairy ENDF/BVIII.0 for all available
    incident energies.

    Args:
        a (int): Mass number of the target nucleus.
        z (int): Charge number of the target nucleus.

    Returns:
        energy_list (list): Incident energies (MeV).
        nfy_list (dict): Independent yields with (string format)
    """

    if z in fiss_z_to_name:
        atom_name = fiss_z_to_name[z]
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
    Convert yields read from ENDF/BVIII.0 into lists of three
    floats: mass, charge and probability for each fragment.

    Args:
        nfy (dict): Neutron fission yields at a given energy.

    Returns:
        ff (array): Fragments 5-uples [A,Z,P] with
        A (int): Mass number of the fragment, 
        Z (int): Charge number of the fragment,
        P (float): Fragmentation probability.
    """

    # list of fission fragments and associated probability

    ff = []

    for nucleus, value in nfy.items():

        match = re.match(r"([A-Za-z]+)(\d+)", nucleus)

        if match:

            element, a = match.groups()
            a = int(a)
            z = int(periodic_table[element])
            proba_float = value.n if hasattr(value, "nominal_value") else float(value)
            ff.append([a, z, proba_float])
    
    # merging isomeric (metastables) states

    ff_isom_merged_dict = defaultdict(float)

    for A, Z, p in ff:
        ff_isom_merged_dict[(A, Z)] += p

    ff_isom_merged_list = [(A, Z, p) for (A, Z), p in sorted(ff_isom_merged_dict.items())]

    return ff_isom_merged_list


# fission fragments coupling


def fission_fragments_coupled(a, z, nfy):
    """
    Coupling of fission fragments by mass and charge conservation.

    Args:
        a (int): Mass number of the target.
        z (int): Charge number of the target.
        nfy (list): Neutron fission yields at a given energy.

    Returns:
        ff (array): Coupled fission fragments 5-uples [Ah,Zh,Al,Zl,P] with
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
        ah = a + 1 - al # incident neutron: +1
        zh = z - zl
        ff_coupled.append([ah, zh, al, zl, p])

    return ff_coupled

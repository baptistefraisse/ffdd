""" Average decay of fission fragments """

# librairies

import numpy as np
from ffdd.sepn import sepn
from ffdd.yields import read_fission_yields, fission_fragments_coupled
from ffdd.tke import tke
from ffdd.energy import q_value, txe_sharing

# decay of a fission fragment

def decay(a, z, xe, ekin):
    """
    Decay of an excited nucleus by neutron emissions.

    Args:
        a (int): Mass number of the nucleus.
        z (int): Charge number of the nucleus.
        xe (float): Excitation energy of the nucleus (MeV). 
        ekin (float): Average kinetic energy of emitted neutrons (MeV).
    
    Returns:
        nu (int): Number of emitted neutrons.
        xe (float): Residual excitation energy (MeV).
    """

    # init

    nu = 0
    sn = sepn(a, z)

    # sequential neutron evaporation

    while xe > sn:
        nu += 1
        a -= 1
        xe -= sn + ekin
        sn = sepn(a, z)

    return nu, xe

# average neutron emissions in fission

def nubar(a_target, z_target, ekin = 2.0, beta = 0.2, model = 'fong', rt = 1):
    """
    Average neutron multiplicity in fission.

    Args:
        a_target (int): Mass number of the target fissile nucleus.
        z_target (int): Charge number of the target fissile nucleus.
        ekin (float): Average kinetic energy of emitted neutrons (MeV).
        beta (float): Average quadrupolar deformation of fragments. 
        model (str): Energy sharing model ('fong' or 'edigy'). 
        rt (float): Anisothermal coefficient. 
    
    Returns:
        energies (float list): incident energies available in the literature (MeV).
        nubar_vs_energy (float list): average total number of emitted neutrons for each energy.
    """

    # scan of available incident energies

    energies, nfys = read_fission_yields(a_target, z_target)
    nubar_vs_energy = []

    # loop on available incident energies

    for k in range(len(energies)):

        total_proba = 0
        nu_list, proba_list = [], []
        energy = energies[k]
        nfy = nfys[k]

        # scan of fragmentations for one given incident energy
        
        for ah, zh, al, zl, proba in fission_fragments_coupled(a_target, z_target, nfy):

            # fragments masses and separation energies from data

            try:
                q = q_value(a_target, z_target, ah, zh, al, zl, energy)
                total_proba += proba

            except KeyError:
                continue

            # energy balance for this fragmentation
            
            tke_ff = tke(ah, zh, al, zl, beta)
            txe = q - tke_ff

            # excitation energy sharing between fragments

            try:   
                xeh, xel = txe_sharing(txe, ah, zh, al, zl, model=model, rt=rt)

            except KeyError:
                continue

            # neutron decay cascade of the excited fragments

            nuh, _ = decay(ah, zh, xeh, ekin=ekin)
            nul, _ = decay(al, zl, xel, ekin=ekin)

            # total emissions by the two fragments

            nu = nuh + nul
            nu_list.append(nu)
            proba_list.append(proba)
            
        # average decay of fission over all fragmentations

        proba_list = np.array(proba_list) / total_proba
        nubar_vs_energy.append(np.average(nu_list, weights = proba_list))

    return energies, nubar_vs_energy

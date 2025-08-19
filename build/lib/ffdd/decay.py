""" Average decay of fission fragments """

# librairies

import numpy as np
from ffdd.mass import nuclear_mass
from ffdd.sepn import sepn
from ffdd.yields import read_fission_yields, fission_fragments_coupled
from ffdd.tke import tke

# decay function of fission fragments

def decay(a_target = 235, z_target = 92, ekin = 0.8, beta = 0.22):
    """
    Deterministic simulation fission fragments decay 

    Args:
        a_target (int): Mass number of the target fissile nucleus.
        z_target (int): Charge number of the target fissile nucleus.
        ekin (float): Average kinetic energy of emitted neutrons (MeV).
        beta (float): Average quadrupolar deformation of fragments. 
    
    Returns:
        list: incident energies available in the literature (MeV).
        list: average total number of emitted neutrons for each energy.
        list: average total gamma-rays energy released (MeV) for each energy.
    """

    # target fissile nucleus properties
    
    m_target = nuclear_mass(a_target, z_target) 
    sn_target = sepn(a_target, z_target)

    # scan of available incident energies

    energies, nfys = read_fission_yields(a_target, z_target)
    nubar_vs_energy, egtot_vs_energy = [], []

    # loop on available incident energies

    for k in range(len(energies)):

        total_proba = 0
        nu_list, egtot_list, proba_list = [], [], []
        energy = energies[k]
        nfy = nfys[k]

        # scan of fragmentations for one given incident energy

        for ah, zh, al, zl, proba in fission_fragments_coupled(a_target, z_target, nfy):

            nu, egtot = 0, 0

            # fragments masses and separation energies from data

            try:
                mh, ml = nuclear_mass(ah, zh), nuclear_mass(al, zl)
                snh, snl = sepn(al,zl), sepn(ah, zh)
                total_proba += proba

            except KeyError:
                continue

            # energy balance for this fragmentation
            
            tke_ff = tke(ah, zh, al, zl, beta)
            q_value = m_target + sn_target + energy - mh - ml
            txe = q_value - tke_ff

            # excitation energy partition between fragments

            x = al/(al+ah)
            xel = x * txe
            xeh = (1-x) * txe

            # neutron decay cascade of the light fragment

            while xel > snl:
                nu += 1
                al -= 1
                xel -= snl + ekin
                snl = sepn(al, zl)

            # neutron decay cascade of the heavy fragment

            while xeh > snh:
                nu += 1
                ah -= 1
                xeh -= snh + ekin
                snh = sepn(ah, zh)

            # remaining energy for gamma-rays

            egtot += xel + xeh

            # final results for this fragmentation

            nu_list.append(nu)
            egtot_list.append(egtot)
            proba_list.append(proba)
    
        # average decay of fission over all fragmentations

        proba_list = np.array(proba_list)/total_proba
        nubar = np.average(nu_list, weights = proba_list)
        egbar = np.average(egtot_list, weights= proba_list)
        nubar_vs_energy.append(nubar)
        egtot_vs_energy.append(egbar)

    return(energies, nubar_vs_energy, egtot_vs_energy)

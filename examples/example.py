""" Example: Influence of deformation and incident energy on neutron emission of 235U """

# libraries

import sys
import os
import matplotlib.pyplot as plt
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from ffdd.decay import nubar

# study function


def example():
    """
    Influence of deformation and incident energy on neutron emission of 235U.

    Returns:
        str: PNG file name.
    """

    # uranium-235

    a_target = 235
    z_target = 92

    # average neutron energy

    ekin = 2.0  # MeV

    # quadrupole deformations exploration

    beta_list = [0.15, 0.20, 0.25]

    _, ax = plt.subplots(figsize=(8, 6))

    for beta in beta_list:

        energy, nu = nubar(a_target, z_target, ekin, beta=beta, model='fong', rt=1)
        plt.scatter(
            energy, nu, marker="s", linestyle="-", label=f"FFDD with β = {beta}"
        )

    # evaluated data for comparison (ENDF/BVIII.0)

    endf_energy = [2e-8, 0.3, 0.4, 0.6, 3.5, 6, 8, 10, 13, 14.5, 16]  # MeV
    endf_nubar = [2.41, 2.46, 2.46, 2.47, 2.83, 3.22, 3.54, 3.89, 4.23, 4.45, 4.68]
    plt.scatter(endf_energy, endf_nubar, marker="s", label="ENDF/BVIII.0")

    # figure design

    ax.set_xlabel("Incident neutron energy (MeV)", fontsize=14)
    ax.set_ylabel("Nubar (average number of emitted neutrons)", fontsize=14)
    ax.set_title("Neutron-induced fission of uranium-235", fontsize=16)
    ax.tick_params(axis="x", labelsize=14)
    ax.tick_params(axis="y", labelsize=14)
    plt.legend(frameon=False, fontsize=14)
    plt.tight_layout()

    # save

    figname = "example.png"
    plt.savefig(figname)
    return figname


# run

if __name__ == "__main__":
    _ = example()

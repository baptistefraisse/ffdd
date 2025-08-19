""" Reader of nuclear masses (AME2020) """

# librairies

import os
import pandas as pd

# parameters

KEV_TO_MEV = 1e-3
U_MEV = 931.49402823  # MeV/c^2

# ASCII file parameters

HEADER = 39

col_widths = [
    1,  # a1     → ctrl
    3,  # i3     → N-Z
    5,  # i5     → N
    5,  # i5     → Z
    5,  # i5     → A
    1,  # 1x     → space
    3,  # a3     → el
    4,  # a4     → o
    1,  # 1x     → space
    14,  # f14.6 → mass excess (keV)
    12,  # f12.6 → mass excess unc
    13,  # f13.5 → binding energy
    1,  # 1x     → space
    10,  # f10.5 → binding unc
    1,  # 1x     → espace
    2,  # a2     → beta type
    13,  # f13.5 → beta decay energy
    11,  # f11.5 → beta decay unc
    1,  # 1x     → space
    3,  # i3     → dummy
    1,  # 1x     → space
    13,  # f13.6 → atomic mass
    12,  # f12.6 → atomic mass unc
]

col_names = [
    "ctrl",
    "N-Z",
    "N",
    "Z",
    "A",
    "space1",
    "el",
    "o",
    "space2",
    "mass_excess",
    "mass_excess_unc",
    "binding_energy",
    "space3",
    "binding_unc",
    "space4",
    "beta_type",
    "beta_decay_energy",
    "beta_decay_unc",
    "space5",
    "dummy",
    "space6",
    "atomic_mass",
    "atomic_mass_unc",
]

# reading and filtering

_datafile = os.path.join(os.path.dirname(__file__), 'data/mass.txt')
_df = pd.read_fwf(
    _datafile,
    skiprows=HEADER,
    widths=col_widths,
    names=col_names,
    usecols=['Z', 'A', 'mass_excess'],
)
_df = _df[pd.to_numeric(_df['mass_excess'], errors='coerce').notnull()]
_df['mass_excess'] = pd.to_numeric(_df['mass_excess'])

# dict

mass_dict = {(int(row.Z), int(row.A)): row.mass_excess for _, row in _df.iterrows()}

# nuclear masses function


def nuclear_mass(a, z):
    """ Reader of tabulated nuclear masses.

    Args:
        a (int): Mass number.
        z (int): Charge number.

    Returns:
        m (float): Nuclear mass (MeV/c^2).

    Raises:
        KeyError: If nucleus was not found in the mass table.
    """

    try:
        mass_excess = mass_dict[(z, a)] * KEV_TO_MEV
    except KeyError:
        raise KeyError(f'Mass for nucleus (Z={z}, A={a}) not available.')

    return mass_excess + a*U_MEV

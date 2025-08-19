""" Reader of neutron energy separation files (LANL) """

# librairies

import os
import pandas as pd

# neutron separation file

_datafile = os.path.join(os.path.dirname(__file__), 'data/sepn.dat')
_df = pd.read_csv(_datafile,  sep=r'\s+', names=['Z', 'N', 'S1n', 'S2n'])
_df.set_index(['Z', 'N'], inplace=True)
_df = _df[_df['S1n'] > -2000.0]  # filter unknown values (tagged by -2000.)
_s1n_dict = {(Z, N): S1n for (Z, N), S1n in _df['S1n'].items()}

# single neutron separation energy function

def sepn(a, z):
    """Single neutron separation energy.

    Args:
        a (int): Mass number.
        z (int): Charge number

    Returns:
        sn (float): Single neutron separation energy (MeV).
    """
    n = a - z
    sn = _s1n_dict.get((z, n), float("nan"))
    return sn

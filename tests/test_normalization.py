""" Unitary test : yields normalization """

import pytest
import warnings
import os
import re
from ffdd.yields import read_fission_yields, fission_fragments_coupled

# test

def test_normalization():
    """Check that the probabilities of coupled fission fragments sum to 1 (5%)"""

    # available target nuclei

    nuclei = []
    yields_dir = "./ffdd/data/yields/"
    files = [f for f in os.listdir(yields_dir) if f.endswith(".endf")]
    pattern = re.compile(r"nfy-(\d+)_([A-Za-z]+)_(\d+)\.endf")
    for f in files:
        match = pattern.match(f)
        if match:
            z_str, _, a_str = match.groups()
            z = int(z_str)
            a = int(a_str)
            nuclei.append([a,z])

    # loop over all available nuclei yields

    for a_target, z_target in nuclei:

        # ignore openmc warning if no uncertainties

        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", "Using UFloat objects with std_dev==0")
            _, nfy_list = read_fission_yields(a_target, z_target)

        # probabilities sum

        for nfy in nfy_list:

            ff = fission_fragments_coupled(a_target, z_target, nfy)
            sum_p = sum(p for _, _, _, _, p in ff)

            # assert

            assert sum_p == pytest.approx(1.0, rel=5e-2)

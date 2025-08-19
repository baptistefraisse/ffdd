""" Energy balance in nuclear fission """

# librairies

from ffdd.mass import nuclear_mass
from ffdd.sepn import sepn
from ffdd.utils import NEUTRON_MASS

# Q-value for neutron-induced fission


def q_value(a, z, ah, zh, al, zl, energy):
    """
    Q-value of neutron-induced fission.

    Args:
        a (int): Mass number of the target nucleus.
        z (int): Charge number of the target nucleus.
        ah (int): Mass number of the heavy fragment.
        zh (int): Charge number of the heavy fragment.
        al (int): Mass number of the light fragment.
        zl (int): Charge number of the lighe fragment.
        energy (float): Incident neutron energy (MeV).

    Returns:
        q (float): Q-value (MeV).
    """

    # fission properties

    m = nuclear_mass(a, z)
    sn = sepn(a, z)
    mh = nuclear_mass(ah, zh)
    ml = nuclear_mass(al, zl)

    # q-value definition

    q = m + NEUTRON_MASS + sn + energy - mh - ml

    return q


# Fong model for excitation energy sharing between fragments


def fong(ah, al):
    """
    Fong model for excitation energy sharing between fragments
    (nucleons gas at thermal equilibrium).

    Args:
        ah (int): Mass number of the heavy fragment.
        al (int): Mass number of the light fragment.

    Returns:
        x (float): Excitation energy sharing factor (0<x<1).
    """

    x = al / (al + ah)
    return x


# von Edigy model for excitation energy sharing between fragments


def edigy(ah, zh, al, zl):
    """
    Von Edigy (BSGF) model for excitation energy sharing between fragments.
    See: T. von Edigy and D. Bucurescu, Phys. Rev. C 72, 044311 (2005).

    Args:
        ah (int): Mass number of the heavy fragment.
        zh (int): Charge number of the heavy fragment.
        al (int): Mass number of the light fragment.
        zl (int): Charge number of the lighe fragment.

    Returns:
        x (float): Excitation energy sharing factor.
    """

    # von Edigy/BSGF model parameters

    p = 0.1271
    q = 4.9813e-3
    r = -8.9553e-5

    # heavy fragment

    pdh = (
        0.5
        * pow(-1, zh)
        * (
            -nuclear_mass(ah + 2, zh + 1)
            + 2 * nuclear_mass(ah, zh)
            - nuclear_mass(ah - 2, zh - 1)
        )
    )
    if ah % 2 == 0 and zh % 2 == 0:  # even-even nucleus
        deltah = 0.5 * pdh
    elif ah % 2 == 1 and zh % 2 == 1:  # odd-odd nucleus
        deltah = - 0.5 * pdh
    else:
        deltah = 0
    sh = sepn(ah, zh) - deltah
    dh = ah * (p + q * sh + r * ah)

    # light fragment

    pdl = (
        0.5
        * pow(-1, zl)
        * (
            -nuclear_mass(al + 2, zl + 1)
            + 2 * nuclear_mass(al, zl)
            - nuclear_mass(al - 2, zl - 1)
        )
    )
    if al % 2 == 0 and zl % 2 == 0:  # even-even nucleus
        deltal = 0.5 * pdl
    elif ah % 2 == 1 and zh % 2 == 1:  # odd-odd nucleus
        deltal = - 0.5 * pdl
    else:
        deltal = 0
    sl = sepn(al, zl) - deltal
    dl = al * (p + q * sl + r * al)

    # sharing factor

    x = dl / (dl + dh)
    return x


# excitation energy sharing between fragments


def txe_sharing(txe, ah, zh, al, zl, model="fong", rt=1.0):
    """
    Sharing of the Total Excitation Energy between the two fission fragments.

    Args:
        txe (float): Total Excitation Energy (MeV).
        ah (int): Mass number of the heavy fragment.
        zh (int): Charge number of the heavy fragment.
        al (int): Mass number of the light fragment.
        zl (int): Charge number of the lighe fragment.
        model (str): Model for excitation energy sharing ('fong' or 'edigy').
        rt (float): Anisothermal factor.

    Returns:
        xeh (float): Excitation energy of the heavy fragment (MeV).
        xel (float): Excitation energy of the light fragment (MeV).
    """

    # energy partition factor

    if model == "fong":
        x = fong(ah, al)

    elif model == "edigy":
        x = edigy(ah, zh, al, zl)

    # thermal equilibrium

    x = pow(rt, 2) * x

    # excitation energy partition

    xel = x * txe
    xeh = (1 - x) * txe

    return xeh, xel

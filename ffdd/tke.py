""" Total Kinetic Energy (TKE) simulation for fission fragments """

from ffdd.utils import COULOMB_CST, NUCLEAR_RADIUS_R0

# nuclear radius function


def nuclear_radius(a):
    """
    Nuclear radius from the incompressible model (r0 = 1.2 fm).

    Args:
        a (int): Mass number of the nucleus.

    Returns:
        r (float): Radius of the nucleus (fm).
    """
    
    return NUCLEAR_RADIUS_R0 * pow(a, 1 / 3)


# kinetic energy function


def tke(ah, zh, al, zl, beta = 0.2):
    """
    Compute total kinetic energy (TKE) of fission fragments
    with the simple model of two charged spheres in contact.

    Args:
        Ah (int): Mass number of the heavy fragment.
        Zh (int): Charge number of the heavy fragment.
        Al (int): Mass number of the light fragment.
        Zl (int): Charge number of the light fragment.
        beta (float): Quadrupolar deformation coefficient.

    Returns:
        tke (float): Total kinetic energy (MeV).
    """

    # nuclear radii (fm)

    rh = nuclear_radius(ah)
    rl = nuclear_radius(al)
    initial_distance = (rh + rl) * (1 + 2 * beta)

    # Total kinetic energy (MeV)

    tke = COULOMB_CST * zh * zl / initial_distance

    return tke

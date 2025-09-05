import numpy as np
from numpy import linalg as LA
import matplotlib.pyplot as plt

import Geodesic_Parameters as GP
import Rep_Rotation as RR

def control_sequence_SU2(comp: np.ndarray, steps: int = 1000):
    """
    Calculate the control sequence for the geodesic
    Input:
        Vector Representing U: comp = [k_0,k_1,k_2,k_3], U = k_0 1 + k_i sigma_i
        Number of Points: steps
    Output:
        t: [0,T]
        Controls: cx(t) and cz(t) for t=[0,T] with number of time points
    """
    phi0, beta, T = GP.geodesic_parameters_SU2(comp)
    t: np.ndarray = np.linspace(0,T,steps)
    control_X: np.ndarray = np.real(np.cos(beta*t + phi0))
    control_Z: np.ndarray = np.real(np.sin(beta*t + phi0))
    return [t,control_X, control_Z]

def geodesic_SU2(comp: np.ndarray, steps: int = 1000):
    """
    Calculate the geodesic curve in the comp Representation
    Input:
        Vector Representing U: comp = [k_0,k_1,k_2,k_3], U = k_0 1 + k_i sigma_i
    Output:
        Geodesic Components of U(t): k_i(t) i=0,1,2,3  U(t) = k_0 1 + k_i sigma_i, t=[0,T] with number of time points
    """
    phi0,beta,T = GP.geodesic_parameters_SU2(comp)
    t: np.ndarray = np.linspace(0,T,steps)
    cphi: float = np.cos(phi0)
    sphi: float = np.sin(phi0)
    b: float = np.sqrt(1.+beta**2)
    cb: np.ndarray = np.cos(t*b/2.)
    cbeta: np.ndarray = np.cos(t*beta/2.)
    sb: np.ndarray = np.sin(t*b/2.)
    sbeta: np.ndarray = np.sin(t*beta/2.)
    unit: np.ndarray = cb*cbeta + beta/b * sb*sbeta
    alpha: np.ndarray = np.arccos(unit)
    sigx: np.ndarray = cphi/b*sb*cbeta - sphi/b*sb*sbeta
    sigy: np.ndarray = beta/b*sb*cbeta - cb*sbeta
    sigz: np.ndarray = sphi/b*sb*cbeta + cphi/b*sb*sbeta
    comp: np.ndarray = np.transpose(np.array([unit,sigx,sigy,sigz]))
    return [t,comp]

def geodesic_SU2_rot(comp: np.ndarray, steps: int = 1000):
    """
    Calculate the geodesic curve in the rot Representation
    Input:
        comp: comp Representation of target
    Output:
        list: [alpha(t),k(t)] rot Representation 
    """
    t,geodesic_comp = geodesic_SU2(comp,steps)
    geodesic_rot = np.array([RR.rot_calc(comp) for comp in geodesic_comp])
    return geodesic_rot

def test_geodesic_SU2(comp: np.ndarray, eps: float = 10**(-5)):
    """
    Input:
        Vector representing U: comp = [k_0,k_1,k_2,k_3,k_4], U = k_0 1 + k_i sigma_i
        Tolerance: eps
    Output:
        Boolean: If U(T) = U with the geodesic
    """
    comp_geodesic = geodesic_SU2(comp)[1][-1]
    print(f"Test Geodesic: {comp},{comp_geodesic}")
    return (np.abs(comp - comp_geodesic) < eps)

test_angle = 0.3*np.pi
test_comp: np.ndarray = np.array([np.cos(test_angle),0,np.sin(test_angle),0])

if __name__ == "__main__":
    print(f"Test Geodesic: {test_geodesic_SU2(test_comp)}")
    print(f"Geodesic Comp: {geodesic_SU2_rot(test_comp)}")


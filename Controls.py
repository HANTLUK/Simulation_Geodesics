import numpy as np
from numpy import linalg as LA

import Geodesic_Parameters as GP

def controls_SU2(comp: np.ndarray, sites: int):
    """
    Calculate the controls to be implemented via the Lie-Trotter-Suzuki prouct formula
    Input:
        comp: Target unitary
        sites: number of sites
    Output:
        t: times
        controls: rotations to implement on site, convention (X Z X)
    """
    phi0,beta,T = GP.geodesic_parameters_SU2(comp)
    lie_trotter_steps: int = int((sites+1)/2)
    t: np.ndarray = np.array([T/(lie_trotter_steps-1)*(0.5 + i) for i in range(lie_trotter_steps)])
    delta: float = T/2/(lie_trotter_steps-1)
    ts = t[:-1]
    control_X: np.ndarray = np.real(np.cos(beta*ts + phi0))
    control_Z: np.ndarray = np.real(np.sin(beta*ts + phi0))
    x: list = []
    z: list = []
    for i,(cX,cZ) in enumerate(zip(control_X,control_Z)):
        if i == 0:
            x.append(delta*cX/2)
        else:
            x[-1] += delta*cX/2
        z.append(delta*cZ)
        x.append(delta*cX/2)
    z.append(0)
    return [t,np.array(x),np.array(z)]

def controls_trotter_XZ(alphaX: float, alphaZ: float, sites: int):
    """
    Calculate the Controls to implement the X + Z rotation via the Trotter formula
    Input:
        alphaX: X angle
        alphaZ: Z angle
        sites: number of sites
    Output:
        t: times
        cx, cz: controls
    """
    trotter_steps: int = int(sites/2)
    t: np.ndarray = np.array([i/trotter_steps for i in range(trotter_steps)])
    cx: np.ndarray = alphaX/trotter_steps*np.ones(trotter_steps)
    cz: np.ndarray = alphaZ/trotter_steps*np.ones(trotter_steps)
    return [t,cx,cz]


def controls_trotter_XZ_random(alphaX: float, alphaZ: float, sites: int):
    """
    Calculate the Controls to implement the X + Z rotation via the Trotter formula but with random weighting of the angles
    Input:
        alphaX: X angle
        alphaZ: Z angle
        sites: number of sites
    Output:
        t: times
        cx, cz: controls
    """
    trotter_steps: int = int(sites/2)
    rng = np.random.default_rng()
    rx: np.ndarray = rng.random(trotter_steps) + 0.5
    rz: np.ndarray = rng.random(trotter_steps) + 0.5
    totx = np.sum(rx)
    totz = np.sum(rz)
    t: np.ndarray = np.array([i/trotter_steps for i in range(trotter_steps)])
    cx: np.ndarray = alphaX/totx*rx
    cz: np.ndarray = alphaZ/totz*rz
    return [t,cx,cz]

if __name__ == "__main__":
    alpha: float = 0.3*np.pi
    comp: np.ndarray = np.array([np.cos(alpha),0.,np.sin(alpha),0.])
    sites: int = 20
    print(f"Controls {controls_SU2(comp,sites)[1]}")
    print(f"Controls {controls_trotter_XZ(alpha,0.,sites)[1]}")

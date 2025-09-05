import numpy as np
from numpy import linalg as LA

import Controls as C
import Rep_Rotation as RR

EX = np.array([1.,0.,0.])
EZ = np.array([0.,0.,1.])

def rot_rep(rot: list):
    """
    Rotation representation only from rot Representation
    Input:
        rot: rot Representation
    Output:
        rotation_rep: as in Rep_Rotation
    """
    return RR.rotation_rep(rot=rot)

def control_curve_SU2(controls: list):
    """
    Calculate the curve from the controls in (X Z X) convention
    Input:
        t,x,z: output from controls
    Output:
        curve_comp: U(t)
    """
    t,x,z = controls
    m: int = len(x)
    x = x.tolist()
    z = z.tolist()
    rot: list = rot_rep([x.pop(0),EX])
    curve_comp: list[np.ndarray] = [rot.comp]
    for i in range(m-1):
        rotZ = rot_rep([z.pop(0),EZ])
        rot = rot*rotZ
        curve_comp.append(rot.comp)
        rotX = rot_rep([x.pop(0),EX])
        rot = rot*rotX
        curve_comp.append(rot.comp)
    return np.array(curve_comp)

if __name__ == "__main__":
    alpha: float = 0.3*np.pi
    comp: np.ndarray = np.array([np.cos(alpha),0.,np.sin(alpha),0.])
    sites: int = 100
    controls_geodesic: list = C.controls_SU2(comp,sites) 
    print(f"Controlled Curve: {control_curve_SU2(controls_geodesic)[-1]}")
    alphaX, alphaZ = [0.1*np.pi,0.3*np.pi]
    controls_trotter: list = C.controls_trotter_XZ(alphaX,alphaZ,sites) 
    print(f"Controlled Curve: {control_curve_SU2(controls_trotter)[-1]}")

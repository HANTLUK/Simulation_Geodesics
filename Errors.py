import numpy as np
import matplotlib.pyplot as plt
from numpy import linalg as LA
import qiskit.quantum_info as qi

# import forest.benchmarking.distance_measures as dm

import Rep_Rotation as RR
import Implementation as I
import Controls as C

import warnings
warnings.filterwarnings("ignore")

def error_implementation(controls: list, k: float, ord = "fro"):
    """
    Calculates the diamond norm, frobenius norm and one norm of the error
    Input:
        controls: controls [t,x,z]
        k: parameter
        ord: diamond/frobenius/1
    Output:
        error: diamond,frobenius,one
    """
    imp_gate = I.implemented_gate(controls,k)
    des_gate = I.desired_gate(controls)
    if ord == 1:
        one_norm = LA.norm(imp_gate-des_gate,ord=1)
        return one_norm
    elif ord == "fro":
        error_mat = (imp_gate - des_gate)[1:4,1:4]
        fro_norm = LA.norm(error_mat,ord="fro")
        return fro_norm
    elif ord == "dia":
        des_choi = qi.Choi(qi.PTM(imp_gate))
        imp_choi = qi.Choi(qi.PTM(des_gate))
        dia_norm = qi.diamond_norm(des_choi - imp_choi)
        # dia_norm = dm.diamond_norm_distance(des_choi.data,imp_choi.data)
        return dia_norm

def error_approx(controls: list, k: float, ord = "fro"):
    """
    Calculates the approximations to the error norm
    Input:
        controls: controls [t,x,z]
        ord: diamond/frobenius/1
    Output:
        error: error approximation
    """
    t,cx,cz = controls
    sites = len(t)
    gammaX = 0.5*(1-k**2)*(cx/k)**2
    gammaZ = 0.5*(1-k**2)*(cz/k)**2
    if ord == "dia":
        return np.sum(gammaX + gammaZ)
    elif ord == "fro":
        gammaX_alt = 0.5*(1-k**2)*(np.sum(np.abs(cx))/k)**2/sites
        gammaZ_alt = 0.5*(1-k**2)*(np.sum(np.abs(cz))/k)**2/sites
        alt = np.sqrt(2)*np.sqrt(gammaX_alt**2 + gammaZ_alt**2 + gammaX_alt*gammaZ_alt)
        local = np.sqrt(2)*np.sum(np.sqrt(gammaX**2 + gammaZ**2 + gammaX*gammaZ))
        return local
    else:
        return None

if __name__ == "__main__":
    alpha: float = 0.0
    comp: np.ndarray = np.array([np.cos(alpha),0.,np.sin(alpha),0.])
    sites: int = 10
    k: float = 0.9
    controls = C.controls_SU2(comp,sites)
    target = RR.rotation_rep(comp = comp)
    print(f"Error: {error_implementation(controls,k)}")
    print(f"Error: {error_approx(controls,k)}")

    # Test_Trotter
    sites: int = 20
    alphas = np.array([0.99*np.pi,0.,0.])
    alphaX, Y, alphaZ = alphas
    target = RR.rotation_rep(exp = alphas)
    controls = C.controls_trotter_XZ(alphaX,alphaZ,sites)
    print(f"Controls: {controls}")
    print(f"Error: {error_implementation(controls,k)}")
    print(f"Error: {error_approx(controls,k)}")

import numpy as np
from numpy import linalg as LA
import matplotlib.pyplot as plt
import io
from itertools import zip_longest

import Rep_Rotation as RR
import Controls as C
import Control_Curves as CC
import Geodesic_Curves as GC

def plot_control_curve_SU2(comp: np.ndarray, sites: int, name: str = ""):
    """
    Plots the control curve in comparison to the geodesic curve
    Input:
        comp: target unitary
        sites: number of sites
        name: file name
    """
    filename: str = f"Plots/plot_curve_comp{name}.png"
    t, geodesic_comp = GC.geodesic_SU2(comp)
    comp1, compX, compY, compZ = np.transpose(geodesic_comp)
    controls_geodesic: list = C.controls_SU2(comp,sites)
    curve_comp: np.ndarray = CC.control_curve_SU2(controls_geodesic)
    ccomp1, ccompX, ccompY, ccompZ = np.transpose(curve_comp)
    fig = plt.figure()
    ax = fig.add_subplot(projection="3d")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")
    ax.plot(compX, compY, compZ, color='#F33333')
    ax.plot(ccompX, ccompY, ccompZ, color='#33F333')
    ax.plot(comp[1],comp[2],comp[3], "ro")
    ax.set_title(f"Geodesic Comparison {name}")
    plt.savefig(filename,dpi=150)

def tab_control_curve_SU2(comp: np.ndarray, sites: int, name: str = ""):
    """
    Plots the control curve in comparison to the geodesic curve
    Input:
        comp: target unitary
        sites: number of sites
        name: file name
    """
    filename: str = f"Tabs/tab_curve_comp{name}.dat"
    t, geodesic_comp = GC.geodesic_SU2(comp)
    comp1, compX, compY, compZ = np.transpose(geodesic_comp)
    controls_geodesic: list = C.controls_SU2(comp,sites)
    curve_comp: np.ndarray = CC.control_curve_SU2(controls_geodesic)
    ccomp1, ccompX, ccompY, ccompZ = np.transpose(curve_comp)
    with io.open(filename,"w") as file:
        for x in zip_longest(compX,compY,compZ,ccompX,ccompY,ccompZ,fillvalue=None):
            file.write("\t".join([str(_) for _ in x])+"\n")
        file.write("\t".join([str(_) for _ in comp[1:]]))

def plot_control_curve_trotter_XZ(alphaX: float, alphaZ: float, sites: int, name: str = ""):
    """
    Plots the curve for the trotter formula
    Input:
        alphaX: X angle
        alphaZ: Z angle
        sites: number of sites
        name: file name
    """
    filename: str = f"Plots/plot_curve_trott{name}.png"
    alphas = np.array([alphaX,0.,alphaZ])
    rot_rep = RR.rotation_rep(rot=[LA.norm(alphas),alphas/LA.norm(alphas)])
    comp = rot_rep.comp
    controls_trotter: list = C.controls_trotter_XZ(alphaX,alphaZ,sites)
    curve_comp: np.ndarray = CC.control_curve_SU2(controls_trotter)
    ccomp1, ccompX, ccompY, ccompZ = np.transpose(curve_comp)
    fig = plt.figure()
    ax = fig.add_subplot(projection="3d")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")
    ax.plot(ccompX, ccompY, ccompZ, color='#33F333')
    ax.plot(comp[1],comp[2],comp[3], "ro")
    ax.set_title(f"Curve Trotter {name}")
    plt.savefig(filename,dpi=150)


if __name__ == "__main__":
    alpha: float = 0.3*np.pi
    comp: np.ndarray = np.array([np.cos(alpha),0.,np.sin(alpha),0.])
    sites: int = 100
    plot_control_curve_SU2(comp,sites,"pi_3")
    tab_control_curve_SU2(comp,sites,"pi_3")
    alphaX, alphaZ = [0.1*np.pi,0.3*np.pi]
    sites: int = 10
    plot_control_curve_trotter_XZ(alphaX,alphaZ,sites,"pi_1pi_3")


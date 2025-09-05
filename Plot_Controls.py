import numpy as np
import matplotlib.pyplot as plt
import io

import Controls as C
import Geodesic_Curves as GC

def plot_controls_SU2(comp: np.ndarray, sites: int, name: str = ""):
    """
    Plot the implemented controls in comparison to the smooth controls
    Input:
        comp: Target unitary
        sites: number of sites
    """
    filename: str = f"Plots/plot_controls_comp{name}.png"
    t,x,z = C.controls_SU2(comp,sites)
    fig = plt.figure()
    ax = fig.add_subplot()
    ax.set_xlabel("t")
    ax.set_ylabel("c")
    ax.plot(t,x*sites,color="#F33333")
    ax.plot(t,z*sites,color="#D33333")
    t,x,z = GC.control_sequence_SU2(comp)
    ax.plot(t,x,color="#33F333")
    ax.plot(t,z,color="#33D333")
    ax.set_title(f"Control Comparison {name}")
    plt.savefig(filename,dpi=150)

def tab_controls_SU2(comp: np.ndarray, sites: int):
    """
    Plots the controls
    Input:
        comp: target unitary
        sites: number of sites
    """
    filename: str = f"Tabs/tab_curve_controls.dat"
    t, geodesic_comp = GC.geodesic_SU2(comp)
    comp1, compX, compY, compZ = np.transpose(geodesic_comp)
    controls_geodesic: list = C.controls_SU2(comp,sites)
    t,x,z = controls_geodesic
    with io.open(filename,"w") as file:
        for tuple_output in zip(t,x,z):
            file.write("\t".join([str(_) for _ in tuple_output])+"\n")

if __name__ == "__main__":
    alpha: float = 0.3*np.pi
    comp: np.ndarray = np.array([np.cos(alpha),0.,np.sin(alpha),0.])
    sites: int = 1000
    plot_controls_SU2(comp,sites,"pi_3")
    tab_controls_SU2(comp,sites)

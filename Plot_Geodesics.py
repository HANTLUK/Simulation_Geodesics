import numpy as np
from numpy import linalg as LA
import matplotlib.pyplot as plt

import Geodesic_Curves as GC

def plot_geodesic_comp(comp: np.ndarray, name: str = ""):
    """
    Plots the geodesic curve in the comp representation
    Input:
        comp: comp Representation of Rotation
    """
    filename: str = f"Plots/plot_Geodesic{name}.png"
    print(f"{GC.geodesic_SU2(comp)}")
    t, geodesic_comp = GC.geodesic_SU2(comp)
    comp1, compX, compY, compZ = np.transpose(geodesic_comp)
    fig = plt.figure()
    ax = fig.add_subplot(projection="3d")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")
    ax.plot(compX, compY, compZ, color='#F33333')
    ax.plot(comp[1],comp[2],comp[3], "ro")
    ax.set_title(f"Geodesic {name}")
    plt.savefig(filename,dpi=150)

if __name__ == "__main__":
    alpha: float = 0.3*np.pi
    plot_geodesic_comp([np.cos(alpha),0.,np.sin(alpha),0.],"pi_3")

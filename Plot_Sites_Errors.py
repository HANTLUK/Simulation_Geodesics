import numpy as np
import matplotlib.pyplot as plt
from numpy import linalg as LA

import Test_Scenarios as TS
import Rep_Rotation as RR
import Controls as C
import Errors as E
import Geodesic_Parameters as GP
import Plot_Errors as PE

def plots_x_sites_fro():
    alpha = 0.5*np.pi
    sitess: int = [2**n for n in range(1,13)]
    k: float = 0.9
    controls = [C.controls_trotter_XZ(alpha,0,sites) for sites in sitess]
    PE.plot_errors_sites(controls,sitess,k,"fro","x")

def plots_x_sites_dia():
    alpha = 0.5*np.pi
    sitess: int = [2**n for n in range(1,13)]
    k: float = 0.9
    controls = [C.controls_trotter_XZ(alpha,0,sites) for sites in sitess]
    PE.plot_errors_sites(controls,sitess,k,"dia","x")

def plots_xz_sites_fro():
    alphaX = 0.5*np.pi
    alphaZ = 0.8*np.pi
    sitess: int = [2**n for n in range(1,13)]
    k: float = 0.9
    controls = [C.controls_trotter_XZ(alphaX,alphaZ,sites) for sites in sitess]
    PE.plot_errors_sites(controls,sitess,k,"fro","xz")

def plots_xz_sites_dia():
    alphaX = 0.5*np.pi
    alphaZ = 0.8*np.pi
    sitess: int = [2**n for n in range(1,13)]
    k: float = 0.9
    controls = [C.controls_trotter_XZ(alphaX,alphaZ,sites) for sites in sitess]
    PE.plot_errors_sites(controls,sitess,k,"dia","xz")

if __name__ == "__main__":
    # Trotter
    plots_xz_sites_fro()
    plots_xz_sites_dia()
    plots_x_sites_fro()
    plots_x_sites_dia()


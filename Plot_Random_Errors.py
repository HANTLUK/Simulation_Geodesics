import numpy as np

import Plot_Errors as PE
import Test_Scenarios as TS
import Controls as C

"""
Random Geodesics and random xz sequences plot error in terms of arclength.
"""

def plots_x_rand_fro():
    factor: float = 0.
    alphas, angles = TS.scenario_xz(factor)
    sitess: int = [1000,10000]
    k: float = 0.9
    controlss = [[C.controls_trotter_XZ_random(aX,aZ,sites) for aX,aY,aZ in angles] for sites in sitess]
    PE.plot_errors(alphas,controlss,sitess,k,"fro","x_rand")

def plots_x_rand_dia():
    factor: float = 0.
    alphas, angles = TS.scenario_xz(factor)
    sitess: int = [5000,10000]
    k: float = 0.9
    controlss = [[C.controls_trotter_XZ_random(aX,aZ,sites) for aX,aY,aZ in angles] for sites in sitess]
    PE.plot_errors(alphas,controlss,sitess,k,"dia","x_rand")

if __name__ == "__main__":
    # Trotter
    plots_x_rand_fro()
    plots_x_rand_dia()


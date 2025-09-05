import numpy as np
import matplotlib.pyplot as plt
from numpy import linalg as LA
import io

import Test_Scenarios as TS
import Rep_Rotation as RR
import Controls as C
import Errors as E
import Geodesic_Parameters as GP

def plot_errors(alphas: np.ndarray, controlss: np.ndarray, sitess: list, k: float, ord = "fro", name: str = ""):
    """
    Plot the numerical errors of controls to target
    Input:
        alphas: parameter for target unitaries
        controlss: array of controls
        sitess: list of numbers of sites
        k: float
        ord: "fro", "dia" or 1
        name: plot name
    """
    filename: str = f"Plots/plot_error_{ord}_{name}.png"
    fig = plt.figure()
    ax = fig.add_subplot()
    ax.set_xlabel("angle")
    ax.set_ylabel(f"error {ord}")
    for controls,sites in zip(controlss,sitess):
        errors = np.array([sites*E.error_implementation(control,k,ord) for control in controls])
        error_approxs = np.array([sites*E.error_approx(control,k,ord) for control in controls])
        ax.scatter(alphas,errors, color="#F33333",marker=".")
        ax.scatter(alphas,error_approxs, color="#33F333",marker=".")
    plt.savefig(filename,dpi=150)

def tab_errors(alphas: np.ndarray, controlss: np.ndarray, sitess: list, k: float, ord = "fro", name: str = ""):
    """
    Table to plot numerical errors of controls to target
    Input:
        alphas: parameter for target unitaries
        controlss: array of controls
        sitess: list of numbers of sites
        k: float
        ord: "fro", "dia" or 1
        name: plot name
    """
    filename: str = f"Tabs/tab_error_{ord}_{name}.dat"
    with io.open(filename, "w") as file:
        for controls,sites in zip(controlss,sitess):
            errors = np.array([sites*E.error_implementation(control,k,ord) for control in controls])
            error_approxs = np.array([sites*E.error_approx(control,k,ord) for control in controls])
            for alpha,error,error_approx in zip(alphas,errors,error_approxs):
                file.write("\t".join([str(_) for _ in [alpha,error,error_approx]])+"\n")

def plot_errors_arclength(alphas: np.ndarray, controlss: np.ndarray, comps: list, sitess: list, k: float, ord = "fro", name: str = ""):
    """
    Plot the approximated and numerical errors of the controls, w.r.t arclength
    Input:
        alphas: parameter for target unitary
        controlss: array of controls
        sitess: list of numbers of sites
        k: float
        ord: "fro", "dia" or 1
        name: plot name
    """
    filename: str = f"Plots/plot_error_arclength_{ord}_{name}.png"
    arclengths = np.array([GP.geodesic_parameters_SU2(comp)[2] for comp in comps])
    fig = plt.figure()
    ax = fig.add_subplot()
    ax.set_xlabel("arclength")
    ax.set_ylabel(f"error {ord}")
    for controls,sites in zip(controlss,sitess):
        errors = [sites*E.error_implementation(control,k,ord) for control in controls]
        error_approxs = [sites*E.error_approx(control,k,ord) for control in controls]
        a,b = np.polyfit(arclengths**2,errors,1)
        error_fit = a*arclengths**2 + b
        # ax.plot(arclengths,error_fit, color="#F33333")
        ax.scatter(arclengths,error_approxs, color="#33F333",marker=".")
        ax.scatter(arclengths,errors, color="#F33333",marker=".")
    plt.savefig(filename,dpi=150)


def tab_errors_arclength(alphas: np.ndarray, controlss: np.ndarray, comps: list, sitess: list, k: float, ord = "fro", name: str = ""):
    """
    Table to plot numerical errors of controls to target
    Input:
        alphas: parameter for target unitaries
        controlss: array of controls
        sitess: list of numbers of sites
        k: float
        ord: "fro", "dia" or 1
        name: plot name
    """
    filename: str = f"Tabs/tab_error_{ord}_{name}.dat"
    arclengths = np.array([GP.geodesic_parameters_SU2(comp)[2] for comp in comps])
    with io.open(filename, "w") as file:
        for controls,sites in zip(controlss,sitess):
            errors = np.array([sites*E.error_implementation(control,k,ord) for control in controls])
            error_approxs = np.array([sites*E.error_approx(control,k,ord) for control in controls])
            for arclength,error,error_approx in zip(arclengths,errors,error_approxs):
                file.write("\t".join([str(_) for _ in [arclength,error,error_approx]])+"\n")

def plot_errors_sites(controls: np.ndarray, sitess: list, k: float, ord = "fro", name: str = ""):
    """
    Plot the numerical errors and approximation of controls to target
    Input:
        controlss: array of controls
        sitess: list of numbers of sites
        k: float
        ord: "fro", "dia" or 1
        name: plot name
    """
    filename: str = f"Plots/plot_error_sites_{ord}_{name}.png"
    fig = plt.figure()
    ax = fig.add_subplot()
    ax.set_xlabel("sites")
    ax.set_ylabel(f"error {ord}")
    errors = np.array([sites*E.error_implementation(control,k,ord) for control,sites in zip(controls,sitess)])
    error_approxs = np.array([sites*E.error_approx(control,k,ord) for control,sites in zip(controls,sitess)])
    ax.scatter(sitess,errors, color="#F33333",marker=".")
    ax.scatter(sitess,error_approxs, color="#33F333",marker=".")
    plt.savefig(filename,dpi=150)

def plots_y_fro():
    alphas, comps = TS.scenario_y()
    sitess: int = [1000,10000]
    k: float = 0.9
    controlss = [[C.controls_SU2(comp,sites) for comp in comps] for sites in sitess]
    plot_errors(alphas,controlss,sitess,k,"fro","y")
    plot_errors_arclength(alphas,controlss,comps,sitess,k,"fro","y")

def plots_y_dia():
    alphas, comps = TS.scenario_y()
    sitess: int = [5000,10000]
    k: float = 0.9
    controlss = [[C.controls_SU2(comp,sites) for comp in comps] for sites in sitess]
    plot_errors(alphas,controlss,sitess,k,"dia","y")
    plot_errors_arclength(alphas,controlss,comps,sitess,k,"dia","y")

def tab_y_dia():
    alphas, comps = TS.scenario_y()
    sitess: int = [1000,2000]
    k: float = 0.9
    controlss = [[C.controls_SU2(comp,sites) for comp in comps] for sites in sitess]
    tab_errors_arclength(alphas,controlss,comps,sitess,k,"dia","y")

def plots_x_fro():
    factor: float = 0.
    alphas, angles = TS.scenario_xz(factor)
    sitess: int = [1000,10000]
    k: float = 0.9
    controlss = [[C.controls_trotter_XZ(aX,aZ,sites) for aX,aY,aZ in angles] for sites in sitess]
    # targets = [[RR.rotation_rep(exp = angle) for angle in angles] for sites in sitess]
    plot_errors(alphas,controlss,sitess,k,"fro","x")

def plots_x_dia():
    factor: float = 0.
    alphas, angles = TS.scenario_xz(factor)
    sitess: int = [5000,10000]
    k: float = 0.9
    controlss = [[C.controls_trotter_XZ(aX,aZ,sites) for aX,aY,aZ in angles] for sites in sitess]
    plot_errors(alphas,controlss,sitess,k,"dia","x")

def tab_x_dia():
    factor: float = 0.
    alphas, angles = TS.scenario_xz(factor)
    sitess: int = [500,1000]
    k: float = 0.9
    controlss = [[C.controls_trotter_XZ(aX,aZ,sites) for aX,aY,aZ in angles] for sites in sitess]
    tab_errors(alphas,controlss,sitess,k,"dia","x")

def plots_xz_fro():
    factor: float = 0.5
    alphas, angles = TS.scenario_xz(factor)
    sitess: int = [1000,10000]
    k: float = 0.9
    controlss = [[C.controls_trotter_XZ(aX,aZ,sites) for aX,aY,aZ in angles] for sites in sitess]
    # targets = [[RR.rotation_rep(exp = angle) for angle in angles] for sites in sitess]
    plot_errors(alphas,controlss,sitess,k,"fro","xz")

def plots_xz_dia():
    factor: float = 0.5
    alphas, angles = TS.scenario_xz(factor)
    sitess: int = [5000,10000]
    k: float = 0.9
    controlss = [[C.controls_trotter_XZ(aX,aZ,sites) for aX,aY,aZ in angles] for sites in sitess]
    plot_errors(alphas,controlss,sitess,k,"dia","xz")

if __name__ == "__main__":
    # Geodesic
    # plots_y_dia()
    # plots_y_fro()
    # Trotter
    # plots_x_fro()
    # plots_x_dia()
    tab_y_dia()
    tab_x_dia()
    # Trotter XZ
    # plots_xz_fro()
    # plots_xz_dia()

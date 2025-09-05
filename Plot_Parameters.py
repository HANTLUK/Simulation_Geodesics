import numpy as np
import matplotlib.pyplot as plt

import io

import Test_Scenarios as TS
import Geodesic_Parameters as GP

def plot_parameters(alphas: np.ndarray, comps: np.ndarray, name: str = ""):
    """
    Plot the arclength of comps
    Input:
        alphas: angles
        comps: Unitaries
        name: plot name
    """
    filename: str = f"Plots/plot_arclength_{name}"
    fig = plt.figure()
    ax = fig.add_subplot()
    ax.set_xlabel("angle")
    ax.set_ylabel("arclength")
    ax.set_xlim([0,np.pi])
    ax.set_ylim([0,2*np.pi])
    ax.set_title(f"Arclengths for {name}")
    Ts: np.ndarray = np.array([GP.geodesic_parameters_SU2(comp)[2] for comp in comps])
    ax.plot(2*alphas,Ts,color="#F33333")
    ax.plot(alphas,alphas)
    ax.plot(alphas,alphas+np.pi)
    ax.plot(alphas,3.5*np.sqrt(alphas))
    ax.plot(alphas,2.6*np.sqrt(alphas))
    plt.savefig(filename,dpi=150)

def tab_parameters(alphas: np.ndarray, comps: np.ndarray, name: str = ""):
    """
    Tabs to plot the arclength of comps
    Input:
        alphas: angles
        comps: Unitaries
        name: plot name
    """
    filename: str = f"Tabs/tab_arclength_{name}.dat"
    Ts: np.ndarray = np.array([GP.geodesic_parameters_SU2(comp)[2] for comp in comps])
    with io.open(filename,"w") as file:
        for T,alpha in zip(Ts,alphas):
            file.write("\t".join([str(_) for _ in [alpha,alpha,2*alpha,alpha+np.pi,3.5*np.sqrt(alpha),2.6*np.sqrt(alpha),T]])+"\n")

if __name__ == "__main__":
    alphas, comps = TS.scenario_y()
    plot_parameters(alphas,comps,"y")
    tab_parameters(alphas,comps,"y")

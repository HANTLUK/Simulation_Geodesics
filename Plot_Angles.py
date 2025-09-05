import numpy as np
import matplotlib.pyplot as plt

ks = np.array([0.1,0.5,0.9])

def lambdas(alpha: float):
    test = False
    """
    Calculates the parameter for the ellipse projection
    Input:
        alpha: angle on ellipse
    Output:
        lp,lm: parameters for both extrema
    """
    ca = np.cos(alpha)
    sa = np.sin(alpha)
    rc = (k**2*ca**2+sa**2)
    rs = (k**2*sa**2+ca**2)
    bracket = -(rs-1.)*rc+k**2
    lp = (-k+np.sqrt(bracket))/rc
    lm = (-k-np.sqrt(bracket))/rc
    corr = (k*sa+lp*sa)**2 + (ca+lp*k*ca)**2
    if test: print("Test Lambdas",corr)
    min_distl = lp
    if np.abs(lp) > np.abs(lm):
        min_distl = lm
    return [min_distl,lp,lm]

def plot_distance_circle():
    fig = plt.figure()
    ax = fig.add_subplot()
    ax.set_xlabel("alpha")
    ax.set_ylabel("lambdas")

    for k in ks:
        alpha = np.linspace(0,np.pi,100)
        ca = np.cos(alpha)
        sa = np.sin(alpha)
        rc = (k**2*ca**2+sa**2)
        rs = (k**2*sa**2+ca**2)
        bracket = -(rs-1.)*rc+k**2
        lp = (-k+np.sqrt(bracket))/rc
        lm = (-k-np.sqrt(bracket))/rc
        corr = (k*sa+lp*sa)**2 + (ca+lp*k*ca)**2
        ax.plot(alpha,lp, linewidth=1, antialiased=True)
        ax.plot(alpha,lm, linewidth=1, antialiased=True)
    ax.set_title(f'Parameter to Circle')
    plt.savefig(f"ParameterProjection.png",dpi=150)

def plot_optimal_angle():
    fig = plt.figure()
    ax = fig.add_subplot()
    ax.set_xlabel("beta")
    ax.set_ylabel("alpha")
    ax.set_xlim([0,0.5*np.pi])
    ax.set_ylim([0,0.5*np.pi])

    for k in ks:
        beta = np.linspace(0,0.5*np.pi,100)
        alpha = np.linspace(0,0.5*np.pi,100)
        cb = np.cos(beta)
        sb = np.sin(beta)
        ca = np.cos(alpha)
        sa = np.sin(alpha)
        rc = (k**2*ca**2+sa**2)
        rs = (k**2*sa**2+ca**2)
        bracket = -(rs-1.)*rc+k**2
        lp = (-k+np.sqrt(bracket))/rc
        lm = (-k-np.sqrt(bracket))/rc
        l_min = lp
        for i,(lp,lm) in enumerate(zip(lp,lm)):
            if np.abs(lp) > np.abs(lm): l_min[i] = lm
        beta1 = np.arctan2(k*sa+l_min*sa,ca+l_min*k*ca)
        alpha2 = np.arctan2(sb,k*cb)
        ax.plot(beta1,beta, linewidth=1, antialiased=True,color="red")
        ax.plot(beta,1/k*beta, linewidth=1, antialiased=True,color="green")
        ax.plot(beta,alpha2, linewidth=1, antialiased=True,color="blue")
        ax.plot(beta,beta, linewidth=1, antialiased=True,color="black")
    ax.set_title(f'Optimal Angle')
    plt.savefig(f"plot_Angle_Optimal.png",dpi=150)

if __name__ == "__main__":
    plot_optimal_angle()
    plot_distance_circle()

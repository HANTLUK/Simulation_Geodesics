import numpy as np

def scenario_y(steps: int = 100):
    """
    Creates the family of y-Rotations
    Input:
        steps: number of angles
    Output:
        comps: array of comps
    """
    alphas = np.linspace(-np.pi,np.pi,steps)
    comps = np.array([[np.cos(alpha),0.,np.sin(alpha),0.] for alpha in alphas])
    return [alphas,comps]

def scenario_xz(factor: float = 0., steps: int = 100):
    alphas = np.linspace(-np.pi,np.pi,steps)
    angles = np.array([[alpha,0.,alpha*factor] for alpha in alphas])
    return [alphas,angles]

if __name__ == "__main__":
    print(f"Comps: {scenario_y()}") 

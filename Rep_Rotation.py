import numpy as np
from numpy import linalg as LA
import matplotlib.pyplot as plt

I: np.ndarray = np.eye(2)
SIGMA_X: np.ndarray = np.array([[0.,1.],[1.,0.]])
SIGMA_Y: np.ndarray = np.array([[0.,-1.j],[1.j,0.]])
SIGMA_Z: np.ndarray = np.array([[1.,0.],[0.,-1.]])
SIGMAS: list = [I,1.j*SIGMA_X,1.j*SIGMA_Y,1.j*SIGMA_Z]

def rot_calc(comp: np.ndarray, debug: bool = False):
    """
    Change of conventions from calc to rot
    Input:
        comp: Rotation in comp Representation
    Output:
        rot: Rotation in rot Representation
    """
    eps: float = 10**(-5)
    norm_comp: float = LA.norm(comp)
    if debug: print(f"Norm Comp: {norm_comp}\n")
    comps: np.ndarray = np.array(comp[1:4])
    sine: float = LA.norm(comps)
    cos: float = comps[0]
    if sine > eps and sine <= 1.:
        alpha = np.arctan2(sine,cos)
        if debug: print(f"Sine: {sine},{np.sin(alpha)}\n")
        k = comps/sine
    else:
        alpha = 0.
        k = np.array([1.,0.,0.])
    return [alpha,k]

def comp_rot_exp(exp: np.ndarray, eps: float = 10**(-5)):
    """
    Change conventions from exp to calc
    Input:
        exp: exp representation
    Output:
        comp: comp representation
    """
    alpha: float = LA.norm(exp)
    if alpha > eps:
        vec = exp/alpha
    else:
        vec = np.array([0.,0.,0.])
        alpha = 0.
    return [alpha,vec]


def comp_calc(rot: list, eps: float = 10**(-5), debug: bool = False):
    """
    Change of Conventions from rot to comp
    Input:
        rot: Rotation in rot representation
    Output:
        comp: Rotation in component representation
    """
    alpha,k = rot
    if debug: print(f"rot: {alpha},{k}")
    if np.sin(alpha) > eps:
        vec = k*np.sin(alpha)
    else:
        vec = k*eps
    if debug: print(f"Vector: {vec}")
    comp = np.array([np.cos(alpha),vec[0],vec[1],vec[2]])
    if debug: print(f"Components from rotation: {comp}")
    return comp


def product(a_rot: list, b_rot: list, eps: float = 10**(-5), debug: bool = False):
    """
    Calculate the Product of two rotations
    Input:
        a,b: Rotation in rot Representation
    Output:
        c: Rotation in rot Representation, a x b
    """
    a_alpha,a_k = a_rot
    b_alpha,b_k = b_rot
    cos_alpha = np.cos(a_alpha)*np.cos(b_alpha)-np.dot(a_k,b_k)*np.sin(a_alpha)*np.sin(b_alpha)
    if debug: print(f"Cos(alpha): {cos_alpha}")
    alpha = np.arccos(cos_alpha)
    k = a_k*np.sin(a_alpha)*np.cos(b_alpha) + b_k*np.sin(b_alpha)*np.cos(a_alpha) - np.cross(a_k,b_k)*np.sin(a_alpha)*np.sin(b_alpha)
    norm_k = LA.norm(k)
    if debug: print(f"Sin(k) {norm_k},{np.sin(alpha)}")
    k /= np.sin(alpha)
    if debug: print(f"Product: {alpha},{k}")
    return [alpha,k]

def matrix_calc(comp: np.ndarray):
    """
    Calculate the matrix Representation
    Input:
        comp: Rotation in the comp Representation
    Output:
        mat: Rotation in the mat Representation
    """
    matrix = np.zeros((2,2),dtype=np.complex64)
    for com,sigma in zip(comp,SIGMAS):
        matrix += com*sigma
    return matrix

class rotation_rep:
    """
    Class for representations of rotations.
    variables:
        comp: components of U = k_0 1 + k_i sigma_i
        rot: angle alpha and rotation vector [alpha,np.ndarray] e(i alpha k.sigma)
        mat: matrix representation
    funtions:
        multiplication: product of two rotations
    """
    def __init__(self,comp = None, rot = None, exp = None):
        if comp is not None:
            self.comp = comp
            self.rot = rot_calc(comp)
        elif rot is not None:
            self.rot = rot
            self.comp = comp_calc(rot)
        elif exp is not None:
            self.rot = comp_rot_exp(exp)
            self.comp = comp_calc(self.rot)
        else:
            self.comp = np.array([1.,0.,0.,0.])
            self.rot = [0.,np.array([0.,0.,0.])]

    def __str__(self):
        return f"\nRotation:\n{self.rot}\n{self.comp}\n{self.mat()}"

    def __rmul__(self,other):
        rot = product(self.rot,other.rot)
        return rotation_rep(rot = rot) 
    
    def __mul__(self,other):
        rot = product(self.rot,other.rot)
        return rotation_rep(rot = rot) 

    def mat(self):
        """Matrix Representation"""
        return matrix_calc(self.comp)

# Test scenarios
comp_1 = np.array([np.cos(np.pi/4),np.sin(np.pi/4),0.,0.])
rot_2 = [0.7,np.array([1.,0.,0.])]

if __name__ == "__main__":
    print(f"\nTest representations")
    rot_1 = rot_calc(comp_1)
    comp_c1 = comp_calc(rot_1)
    print(f"Test Comp Rot Comp: {comp_1},{rot_1},{comp_c1}")
    comp_2 = comp_calc(rot_2)
    rot_c2 = rot_calc(comp_2)
    print(f"Test Rot Comp Rot: {rot_2},{comp_2},{rot_c2}")

    print(f"\nTest product")
    rot_A = [np.pi/4,np.array([1.,0.,0.])]
    rot_B = [0.7,np.array([0.,0.,1.])]
    rot_C = [-np.pi/4,np.array([1.,0.,0.])]
    rot_AB = product(rot_A,rot_B)
    rot_ABC = product(rot_AB,rot_C)
    print(f"Test Product 2: {rot_A},{rot_B},{rot_AB},{rot_C},{rot_ABC}\n")

    print(f"Test class\n")
    rotation_1 = rotation_rep(comp = comp_1)
    rotation_2 = rotation_rep(comp = comp_calc(rot_2))
    rotation_3 = rotation_1 * rotation_2
    print(f"Test Classes: {rotation_1},{rotation_2},{rotation_3}")

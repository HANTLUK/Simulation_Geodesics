import numpy as np
import qiskit.quantum_info as qi
from numpy import linalg as LA

import Controls as C
import Rep_Rotation as RR

def desired_x(angle: float):
    """
    Calculates the desired gate for a single X rotation
    Input:
        angle: target angle
    Output:
       ptm: PTM representation of the desired gate 
    """
    angle = angle
    cangle = np.cos(angle)
    sangle = np.sin(angle)
    ptm: np.ndarray = np.array([[1.,0.,0.,0.],[0.,1.,0.,0.],[0.,0.,cangle,-sangle],[0.,0.,sangle,cangle]],dtype=np.float128)
    return ptm

def desired_z(angle: float):
    """
    Calculates the desired gate for a single Z rotation
    Input:
        angle: target angle
    Output:
       ptm: PTM representation of the desired gate 
    """
    angle = angle
    cangle = np.cos(angle)
    sangle = np.sin(angle)
    ptm: np.ndarray = np.array([[1.,0.,0.,0.],[0.,cangle,-sangle,0.],[0.,sangle,cangle,0.],[0.,0.,0.,1.]],dtype=np.float128)
    return ptm

def implementation_x(angle: float, k: float):
    """
    Calculates the implemented gate for a single X rotation
    Input:
        angle: target angle
        k: order parameter
    Output:
       ptm: PTM representation of the implemented gate 
    """
    angle = angle
    cangle = np.cos(angle)
    sangle = k*np.sin(angle)
    ptm: np.ndarray = np.array([[1.,0.,0.,0.],[0.,1.,0.,0.],[0.,0.,cangle,-sangle],[0.,0.,sangle,cangle]],dtype=np.float128)
    return ptm

def implementation_z(angle: float, k: float):
    """
    Calculates the implemented gate for a single Z rotation
    Input:
        angle: target angle
        k: order parameter
    Output:
       ptm: PTM representation of the implemented gate 
    """
    angle = angle
    cangle = np.cos(angle)
    sangle = k*np.sin(angle)
    ptm: np.ndarray = np.array([[1.,0.,0.,0.],[0.,cangle,-sangle,0.],[0.,sangle,cangle,0.],[0.,0.,0.,1.]],dtype=np.float128)
    return ptm

def desired_gate(controls: list):
    """
    Calculates the PTM for the desired gate
    Input:
        rot_rep: Representation of the rotation
    Output:
        ptm: PTM representation of the desired gate
    """
    t,x,z = controls
    m: int = len(x)
    x = x.tolist()
    z = z.tolist()
    gate: np.ndarray = np.eye(4,dtype=np.float128)
    for i in range(m):
        des_X = desired_x(x.pop(0))
        gate = gate @ des_X
        des_Z = desired_z(z.pop(0))
        gate = gate @ des_Z
    return gate


def implemented_gate(controls: list, k: float):
    """
    Calculates the implemented gate for the rotation sequence
    Input:
        controls: output of controls
        sites: number of sites
    Output:
        matrix: np.ndarray PTM representation of the implemented gate
    """
    t,x,z = controls
    m: int = len(x)
    x = (x/k).tolist()
    z = (z/k).tolist()
    gate: np.ndarray = np.eye(4,dtype=np.float128)
    for i in range(m):
        impl_X = implementation_x(x.pop(0),k)
        gate = gate @ impl_X
        impl_Z = implementation_z(z.pop(0),k)
        gate = gate @ impl_Z
    return gate

def impl_x_test(alpha: float, sites: int, k: float):
    """
    Calculates the difference in the implementation of x directly
    Input:
        alpha: X angle
        sites: number of sites
        k: parameter
    Output:
        impl_gate: Implemented Gate
    """
    rot_sites = int(sites/2)
    alpha_impl = alpha/k/rot_sites
    impl_single = np.array([[1.,0.,0.,0.],[0.,1.,0.,0.],[0.,0.,np.cos(alpha_impl),-k*np.sin(alpha_impl)],[0.,0.,k*np.sin(alpha_impl),np.cos(alpha_impl)]])
    return LA.matrix_power(impl_single,rot_sites)

def des_x_test(alpha: float):
    """
    The desired operation for only X rotation
    Input:
        alpha: X angle
    Output:
        des_gate: Desired Gate
    """
    alpha = alpha
    gate = np.array([[1.,0.,0.,0.],[0.,1.,0.,0.],[0.,0.,np.cos(alpha),-np.sin(alpha)],[0.,0.,np.sin(alpha),np.cos(alpha)]])
    return gate

if __name__ == "__main__":
    alpha: float = 0.3*np.pi
    comp: np.ndarray = np.array([np.cos(alpha/2),0.,np.sin(alpha/2),0.])
    sites: int = 20
    k: float = 0.9
    rot_rep = RR.rotation_rep(comp = comp)
    controls = C.controls_SU2(comp,sites)
    print(f"Controls: {controls}")
    print(f"Implemented gate: {implemented_gate(controls,k)}")
    print(f"Desired gate: {desired_gate(controls)}")
    # Test_Trotter
    alphaX = 0.99*np.pi
    alphas = np.array([alphaX,0.,0.])
    alphaX, Y, alphaZ = alphas
    rot_rep = RR.rotation_rep(exp = alphas/2)
    controls = C.controls_trotter_XZ(alphaX,alphaZ,sites)
    print(f"Params: {alphaX}, {sites}, {k}")
    print(f"Controls: {controls}")
    print(f"Implemented Gate (Direct): {impl_x_test(alphaX,sites,k)}")
    print(f"Implemented gate: {implemented_gate(controls,k)}")
    print(f"Desired Gate (Direct): {des_x_test(alphaX)}")
    print(f"Desired gate: {desired_gate(controls)}")

import numpy as np
import numpy.linalg as LA
import scipy.optimize as opt
import matplotlib.pyplot as plt

def geodesic_parameters_SU2(comp: np.ndarray):
    """
    Calculate the parameters for the geodesic on SU(2)
    Input: 
        Vector Representing U: comp = [k_0,k_1,k_2,k_3], U = k_0 1 + k_i sigma_i
    Output: 
        Parameters for the geodesic: phi0, beta, T
    Hint:
        Only Y-Rotations so far, [cos(alpha), 0, sin(alpha), 0]
    """
    phi0: float = 0.
    g: float = np.arcsin(np.abs(comp[2]))
    T: float = np.sqrt(8.*np.pi*g - 4.*g**2)
    if T > 0:
        beta: float = -np.sign(comp[2])*(2.*g-2.*np.pi)/T
    else: beta = 0
    return [phi0, beta, T]

def parametersBetaT(c1,cy):
	debug = True
	eps = 10**(-3)
	A = c1 + 1.j*cy
	absA = np.abs(A)
	if absA > 1.:
		if debug: print("Large Parameters") 
		absA = 1.		
	argA = np.abs(np.angle(A))
	if A == 0.:
		T = np.pi
		beta = 0.
	elif absA == 1.:
		T = 2.*np.sqrt(argA*(2.*np.pi - argA))
		beta = np.sign(cy)*np.sqrt(4.*np.pi**2 - T**2)/T
	elif np.abs(c1-absA*np.sin(np.pi/2.*absA)) < eps:
		T = np.pi*np.sqrt(1. - absA**2)
		beta = absA/np.sqrt(1. - absA**2)
		signBeta = c1/absA/np.sin(beta*T)
		beta = signBeta*beta
	elif c1 > absA*np.sin(np.pi/2.*absA):
		func1 = lambda beta : -beta/np.sqrt(1. + beta**2)*np.arcsin(np.sqrt((1. - absA**2)*(1. + beta**2))) + np.arcsin(beta*np.sqrt(1. - absA**2)/absA) - np.arctan2(cy/absA,c1/absA)
		beta_initial = absA/np.sqrt(1. - absA**2)
		beta = opt.fsolve(func1,beta_initial)[0]
		T = 2./np.sqrt(1.+beta**2)*np.arcsin(np.sqrt((1. - absA**2)*(1. + beta**2)))
	elif c1 < absA*np.sin(np.pi/2.*absA):
		func1 = lambda beta : beta/np.sqrt(1. + beta**2)*(np.pi - np.arcsin(np.sqrt((1. - absA**2)*(1. + beta**2)))) + np.arcsin(beta*np.sqrt(1. - absA**2)/absA) - np.arctan2(cy/absA,-c1/absA)
		beta_initial = absA/np.sqrt(1. - absA**2)
		beta = opt.fsolve(func1,beta_initial)[0]
		T = 2./np.sqrt(1.+beta**2)*np.arcsin(np.sqrt((1. - absA**2)*(1. + beta**2)))
	else:
		print("Error")
		return None
	return [beta,T]

	
def parameters(c):
	debug = True
	cx,cy,cz = c
	if debug: print("Norm",LA.norm(c)**2)
	c1 = np.sqrt(1. - LA.norm(c)**2)
	if debug: print("c1",c1,c1**2+LA.norm(c)**2)
	beta,T = parametersBetaT(c1,cy)
	phi0 = np.arctan2(cz,cx) - beta*T/2.
	return [phi0,beta,T]

def parameters_1(c):
	debug = False
	c1,cx,cy,cz = c
	beta,T = parametersBetaT(c1,cy)
	phi0 = np.arctan2(cz,cx) - beta*T/2.
	return [phi0,beta,T]

def test_Parameters(c):
	params = parameters(c)
	phi0,beta,T = params
	Rot = SG.optimal_rotation(params,T)
	print("cs\n",c,"\n",Rot)

def plot_Arclength(title, filename):
	debug = False
	samples = 300
	fig = plt.figure()
	ax = fig.add_subplot(projection="3d")
	ax.set_xlabel("y-Comp sin(angle)")
	ax.set_ylabel("x-z-Comp sin(angle)")
	ax.set_zlabel("Arclength")
	ys = np.linspace(.01,np.pi,samples)
	xzs = np.linspace(.01,np.pi-.01,samples)
	YY,XZ = np.meshgrid(ys,xzs)
	Ts = np.array([[parameters_1([np.cos(y)*np.cos(xz),0.,np.sin(y),np.cos(y)*np.sin(xz)])[2] for y in ys] for xz in xzs])
	ax.plot_surface(YY,XZ,Ts.reshape(samples,samples), color='#F33333')
	ax.set_title(title)
	plt.savefig(filename,dpi=150)
	plt.close()

def plot_Arclength_Y(title, filename):
	debug = False
	samples = 300
	fig = plt.figure()
	ax = fig.add_subplot()
	ax.set_xlabel("y-Comp sin(angle)")
	ax.set_ylabel("Arclength")
	ys = np.linspace(0.,np.pi,samples)
	# Ts = np.array([parameters_1([np.cos(y),0.,np.sin(y),0.])[2] for y in ys])
	Tns = np.array([np.sqrt(8.*np.pi*g - 4.*g**2) for g in ys])
	# ax.plot(ys,Ts, color='#F33333')
	ax.plot(ys,Tns)
	ax.set_title(title)
	plt.savefig(filename,dpi=150)
	plt.close()
	

if __name__ == "__main__":
	comps = [np.array([0.,-0.5,0.]), np.array([0.,0.,1.]), np.array([.1,.1,.1]), np.array([0.1,0.2,0.5])]
	for comp in comps:
		test_Parameters(comp)
	print("Plot")
	plot_Arclength("Arclength","Plots/Arclengths.png")
	plot_Arclength_Y("Arclength Y","Plots/ArclengthY.png")
	


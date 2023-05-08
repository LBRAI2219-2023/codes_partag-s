#%%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pynverse import inversefunc

# define useful functions
def vanGenuchten(psi, unit='cm'):
    ''' 
    Computes the water retention, theta, for a given value of psi using the van Genuchten model.
    The type of soil considered is a loam soil.
    
    Args:
        psi:   The soil suction/soil water potential (psi_m) expressed in [cm] or in [hPa]. Default is [cm].
        unit:  Specifies the unit of the value of psi. If unit is hPa then it is first converted into cm.
        
    Returns:
        Theta, the water retention corresponding to the given psi and is expressed in [cm^3/cm^3].
    '''
    # function parameters for loam soil (from HYDRUS)
    theta_s = 0.3991   # [cm^3/cm^3]
    theta_r = 0.0609   # [cm^3/cm^3]
    alpha = 0.0111     # [cm^-1]
    n = 1.4737         # [-]
    m = 1-1/n          # [-]
    # convert units of psi : hPa -> cm 
    if unit=='hPa':
        psi = 10*psi/9.81
    if unit != 'hPa' and unit != 'cm':
        print(('\033[31;1;4mWrong unit provided; the only untis accepted are `cm` or `hPa`\033[0m')) # print error in red and underlined text
    # compute water retention using the van Genuchten model
    water_retention = theta_r + (theta_s - theta_r)/(((1 + (alpha*abs(psi))**n))**m)
    return water_retention

def analytical_inv_vanGenuchten(theta, unit='cm'):
    '''
    Computes the soil suction/soil water potential for a given water content, theta, expressed in [cm^3/cm^3].
    The computation is done using the analitycal solution of the inverse of the van Genuchten model.
    The type of soil considered is a loam soil.
    
    Args:
        theta : Water content in cm^3/cm^3.
        unit:   Specifies the unit of the value returned. Defaulf is cm.
    
    Returns:
        Psi, the soil water potential in [cm of water].
    '''
    # function parameters for loam soil (from HYDRUS)
    theta_s = 0.3991   # [cm^3/cm^3]
    theta_r = 0.0609   # [cm^3/cm^3]
    alpha = 0.0111     # [cm^-1]
    n = 1.4737         # [-]
    m = 1-1/n          # [-]
    # compute psi using inverse van Genuchten
    psi = 1/alpha * (((theta-theta_r)/(theta_s-theta_r))**(-1/m) - 1)**(1/n) 
    # convert unit if necessary
    if unit == 'hPa':
        return psi*9.81/10
    else:
        return psi 

# declare buffers & dummy points for graphs
psi = [1, 10, 30, 100, 1000, 1500, 10000, 15000, 100000]
thetas = []
inv_thetas = []
inv_analytical = [] 

# compute theta's - direct function
for i in psi:
    thetas.append(vanGenuchten(i, unit='cm'))

# compute inverse function - numerically
inv_vanGenuchten = inversefunc(vanGenuchten)
for i in thetas:
    inv_thetas.append(inv_vanGenuchten(i))

# compute inverse function - analytically
for i in thetas:
    inv_analytical.append(analytical_inv_vanGenuchten(i))

# sanity check - make subplots with all 3 graphs
fig, axs = plt.subplots(1, 2, figsize=(10,5))
axs[0].plot(psi, thetas, 'b-')
axs[0].set_xscale('log')
axs[0].set_title('van Genuchten')
axs[0].grid(linestyle=':')
axs[0].set_xlabel('Log $\psi_m \quad [cm]$')
axs[0].set_ylabel('Water retention$ \quad [cm^3/cm^3]$')

axs[1].plot(thetas, inv_thetas, 'b-', label='numerique')
axs[1].plot(thetas, inv_analytical, 'r--', label='analitique')
axs[1].set_title('inverse van Genuchten')
axs[1].set_yscale('log')
axs[1].grid(linestyle=':')
axs[1].set_ylabel('Log $\psi_{m} \quad [cm]$')
axs[1].set_xlabel('Water retention$ \quad [cm^3/cm^3]$')
axs[1].legend(loc='best')

plt.savefig('./img/vanGenuchten_subplots.png', dpi=500)
plt.tight_layout()
plt.show()

#%%
# compute initial soil water content based on default values
# of MARSHAL soil.csv file
psi0 = [-15000, -300, -300, -300]
thetas0 = []
thetas_avg = []

for i in psi0:
    thetas0.append(vanGenuchten(i, unit='hPa'))
np.array(thetas0)

for i in range(3):
    theta_avg = (thetas0[i+1]+thetas0[i])/2
    thetas_avg.append(theta_avg)
    
np.array(thetas_avg)
print(thetas_avg)
water_content = sum(thetas_avg*40)
print(water_content)
# %%

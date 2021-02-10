import matplotlib.pyplot as plt
import numpy as np

"""
This code computes and plots the efficacy of contact tracing
as a function of app uptake among Android and iOS users.
The model for tracing efficacy is outline in the Corona
paper draft, and the probabilities of detecting a contact
are taken from Smittestopp data.
"""

#probabilities of detecting a contact, i = iOS, a = Android:
#p_ii = 0.54; p_ai = 0.53; p_ia = 0.53; p_aa = 0.74
p_ii = 0.54; p_ai = 0.53; p_ia = 0.53; p_aa = 0.74

#p_ia = prob. that a contact between iOS and Android is detected by iOS

n = 31

a_i = np.linspace(0,1,n)
a_a = np.linspace(0,1,n)

#market share iOS, should be replaced with real data:
phi = 0.5

#create 2D arrays with identical rows/columns:
c_ii = np.outer(a_i*a_i*phi**2,np.ones(n))
c_ai = np.outer(a_i,a_a)*phi*(1-phi)
c_ia = c_ai
c_aa = np.outer(np.ones(n),a_a*a_a*(1-phi)**2)

#probability that a contact is detected by at least one phone:
E = (2*p_ii-p_ii**2)*c_ii + (2*p_ia-p_ia**2)*c_ai + (2*p_ai-p_ai**2)*c_ia + (2*p_aa-p_aa**2)*c_aa

#save resulting efficacy matrix, used as input to other models:
np.savetxt('eff.txt',E)

data =  np.transpose(E) #[1:,1:])
x = np.linspace(0,1,31)#data[:,0]
#print(x)
fig, ax = plt.subplots()
im = ax.imshow(data,extent=[0, 1, 0, 1]) #,vmin=-1,vmax=1)
cs = plt.contour(x[0:],x[0:],np.flip(data,0),[0.25,0.5,0.75],colors='black',linestyles='dashed',linewidths=0.5)
labels = ax.clabel(cs, inline=1,fontsize=10)
for l in labels:
    l.set_rotation(l.get_rotation()-80)
    l.set_text(l.get_text()[:-1])
#plt.contour(data)

ticks = np.linspace(0,1,11)
ax.set_xticks(ticks)
ax.set_yticks(ticks)
# ... and label them with the respective list entries
labels = [f"{x_*100:.0f}" for x_ in ticks]
ax.set_xticklabels(labels,fontsize=14)
#print(labels)
labels.reverse()
ax.set_yticklabels(labels,fontsize=14)
#plt.setp(ax.get_xticklabels(), rotation=90,rotation_mode="default")
ax.invert_yaxis()
ax.set_xlabel("App uptake iOS (%)",fontsize=18)
ax.set_ylabel("App uptake Android (%)",fontsize=18)
#ax.set_title("Sporingseffektivitet som funksjon av andel app-brukere.")

plt.colorbar(im)
plt.tight_layout()
plt.savefig("efficacy_ios_android_2D.pdf")
#plt.savefig("efficacy_ios_android_2D.png")

plt.show()

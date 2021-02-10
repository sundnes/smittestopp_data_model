import matplotlib.pyplot as plt
import numpy as np

"""
This code computes and plots the efficacy of contact tracing
as a function of app uptake, assuming that the
uptake is the same for Android and iOS users.
The model for tracing efficacy is outline in the Corona
paper draft, and the probabilities of detecting a contact
are taken from Smittestopp data.
"""

#probabilities of detecting a contact, i = iOS, a = Android:
p_ii = 0.54; p_ai = 0.53; p_ia = 0.53; p_aa = 0.74
#p_ia = prob. that a contact between iOS and Android is detected by iOS

n = 101

a_i = np.linspace(0,1,n)
a_a = a_i

#market share iOS, should be replaced with real data:
phi = 0.5

#create 2D arrays from the 1D arrays
c_ii = a_i*a_i*phi**2
c_ai = a_i*a_a*phi*(1-phi)
c_ia = c_ai
c_aa = a_a*a_a*(1-phi)**2

#probability that a contact is detected by at least one phone:
#E = (2*p_ii-p_ii**2)*c_ii + (2*p_ia-p_ia**2)*c_ai + (2*p_ai-p_ai**2)*c_ia + (2*p_aa-p_aa**2)*c_aa
E = (2*p_ii-p_ii**2)*c_ii + (c_ia+c_ai)*(p_ia+p_ai - p_ia*p_ai) + (2*p_aa-p_aa**2)*c_aa

print(plt.rcParams)

print(plt.rcParams['font.family'])
print(plt.rcParams['font.sans-serif'])
#from matplotlib.font_manager import findfont, FontProperties
#font = findfont(FontProperties(family=['sans-serif']))
#print(font)

exit()


fig, ax = plt.subplots()
plt.plot(a_i,E,color='k')
plt.grid(linewidth=0.25)
#plt.axis('equal')
plt.axis([0,1,0,1])
ticks = np.linspace(0,1,11)
ax.set_xticks(ticks)
ax.set_yticks(ticks)
# ... and label them with the respective list entries
labels = [f"{x_*100:.0f}" for x_ in ticks]
ax.set_xticklabels(labels,fontsize=14)
ax.set_yticklabels(labels,fontsize=14)
ax.set_ylabel("Tracing efficacy (%)",fontsize=18)
ax.set_xlabel("App uptake (%)",fontsize=18)
#ax.set_title("Sporingseffektivitet som funksjon av andel app-brukere.")
plt.tight_layout()

outfile = "efficacy_ios_android_1D.pdf"
plt.savefig(outfile)
plt.show()

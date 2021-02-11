import matplotlib.pyplot as plt
import numpy as np

def read_file(filename):
    matrix = np.loadtxt(filename,skiprows=1)
    matrix = matrix[:,1:]
    matrix = np.transpose(matrix)
    return matrix

files = ['eff_iso_70/growthrate_matrix_ae_1.5_4.txt','eff_iso_70/growthrate_matrix_ae_2.7_4.txt']

fig, ax = plt.subplots() #figsize=(5,5))

styles = ['-','--']

for filename,s in zip(files,styles):
    data = read_file(filename)
    x = np.linspace(0,1,data.shape[0])

    plt.plot(x,np.diagonal(data),color = 'k',linestyle=s)

plt.plot([0,1],[0,0],color='k',linestyle = ':',linewidth=0.5)

#plt.axis()

plt.legend(['$R0$=1.5','$R0$=2.7'],fontsize=14)
xticks = np.linspace(0,1,11)
yticks = np.linspace(-0.15,0.1,6)
ax.set_xticks(xticks)
ax.set_yticks(yticks)
# ... and label them with the respective list entries
xlabels = [f"{x_*100:.0f}" for x_ in xticks]
ax.set_xticklabels(xlabels,fontsize=14)
#plt.setp(ax.get_xticklabels(), rotation=90,rotation_mode="default",fontsize=14)
ylabels = [f"{r:.2f}" for r in np.linspace(-0.15,0.10,6)]
ax.set_yticklabels(ylabels,fontsize=14)

ax.set_ylabel("Growth rate (days$^{-1}$)",fontsize=18)
ax.set_xlabel("App uptake (%)",fontsize=18)
#plt.title("Vekstrate som funksjon av app-opptak, $R0=1.7$ and $R0=2.7$.")

plt.tight_layout()

plt.savefig("growthrate_uptake_1D.pdf")
plt.show()

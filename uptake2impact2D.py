import matplotlib.pyplot as plt
import numpy as np
import sys

#filename = 'growthrate_matrix_ae_1.4_4.txt'
#filename = 'maxR0controlled_matrix_ae_uptake4-0iso.txt'

try:
    filename = sys.argv[1]
except:
    filename = 'growthrate_matrix_ae_1.4_4.txt'

matrix = np.loadtxt(filename,skiprows=1)
matrix = matrix[:,1:]


#x = matrix[:,0]
#print(x)
data =  np.transpose(matrix) #[1:,1:])


"""
print(x[7],x[20])

print(data[5,:]) #,data[20,5])
y = data[:,7]
x = np.linspace(4,96,len(y))

plt.plot(x,y)
plt.show()
exit()
"""
x = np.linspace(0.02,0.98,data.shape[0])
#print(x)
#print(data.shape)
#exit()

fig, ax = plt.subplots()
im = ax.imshow(data,extent=[0, 1, 0, 1],vmin=-0.1,vmax=0.1)
ax.contour(x,x,np.flip(data,0),[0.0],colors='k')
#ax.contour(x,x,data,[0.0])

#plt.plot([0.7],[0.8],'rx',markersize=10,linewidth=4)

# We want to show all ticks...
ticks = np.linspace(0,1,11)
ax.set_xticks(ticks)
ax.set_yticks(ticks)
# ... and label them with the respective list entries
labels = [f"{x_*100:.0f}" for x_ in ticks]
ax.set_xticklabels(labels,fontsize=14)
#print(labels)
labels.reverse()
ax.set_yticklabels(labels,fontsize=14)
#plt.setp(ax.get_xticklabels(), rotation=90,rotation_mode="default",fontsize=14)
ax.invert_yaxis()
ax.set_ylabel("App uptake Android (%)",fontsize=18)
ax.set_xlabel("App uptake iOS (%)",fontsize=18)
#ax.set_title("Plot shows r, for R0 = 1.7 and delay = 4hrs")
#ax.set_title("Vekstrate $r$, for $R0$ = 2.7")

plt.colorbar(im)
plt.tight_layout()

outfile = filename.replace('txt','pdf')
plt.savefig(outfile)
#plt.show()

#print(plt.rcParams.get('figure.figsize'))


"""
plt.figure(2)
x = np.linspace(0,1,data.shape[0])

plt.plot(x,np.diagonal(data))
plt.show()
"""

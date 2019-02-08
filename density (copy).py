import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def getdensity():
	path ='data/Hangzhou_Edgelist.csv'

	#load row data
	I=[]
	df=pd.read_csv(path,sep=',')#,nrows=1000
	for i,row in df.iterrows():
		x=row['XCoord']
		y=row['YCoord']
		I.append([x,y])

	xy=np.asarray(I)
	print "num of intersections:",len(xy)

	#build density
	dsize=[400,400]
	d=np.zeros(dsize)

	dstep=(xy.max(0)-xy.min(0))/(np.asarray(dsize)-1)
	print dstep
	dij=np.floor((xy-xy.min(0))/dstep)
	for[i,j] in dij:
		i,j=int(i),int(j)
		d[i][j]=d[i][j]+1
	print "map grid size:",dsize

	#show heatmap
	#dd=d+1                  #original
	#dd=(np.log(d+1))**2     #peak
	#dd=np.log(d+1)          #off-peak
	dd=np.sqrt(d+1)          #transit


	coef_peak=250
	coef_offpeak=150
	coef_transient=200

	dd=dd*coef_transient/np.max(dd) #normalize 0~255
	print np.max(dd)

	plt.imshow(dd,cmap='hot',vmin=0,vmax=255,interpolation='spline36')
	plt.xlabel("longtitude")
	plt.ylabel("latitude")
	plt.title('Roadmap intersection distribution')
	plt.tick_params(axis='both',left=False,top=False,right=False,bottom=False,labelleft=False,labeltop=False,labelright=False,labelbottom=False)
	plt.savefig("intersect_density_200x200_sqrt.png")
	plt.show()
	return

getdensity()
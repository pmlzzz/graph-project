import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random

global dij

def plot(id2prob):
	global dij
	#print dij
	dsize=[200,200]
	d=np.zeros(dsize)
	for idx,pair in enumerate(id2prob):
		xx= int(dij[idx][0])
		yy= int(dij[idx][1])
		d[xx][yy]=pair[1]
	plt.imshow(d,cmap='hot',vmin=0,vmax=255,interpolation='spline36')
	plt.xlabel("longtitude")
	plt.ylabel("latitude")
	plt.title('Roadmap intersection distribution')
	plt.tick_params(axis='both',left=False,top=False,right=False,bottom=False,labelleft=False,labeltop=False,labelright=False,labelbottom=False)
	plt.savefig("intersect_density_200x200_sqrt.png")
	plt.show()

def getdensity():
	path ='data/Hangzhou_Edgelist.csv'

	#load row data
	I=[]
	id2den=[]
	df=pd.read_csv(path,sep=',')#,nrows=1000
	for i,row in df.iterrows():
		x=row['XCoord']
		y=row['YCoord']
		idx=row['START_NODE']
		I.append([x,y])
		id2den.append([idx,0])
	xy=np.asarray(I)
	print "num of intersections:",len(xy)

	#build density
	dsize=[200,200]
	d=np.zeros(dsize)
	dstep=(xy.max(0)-xy.min(0))/(np.asarray(dsize)-1)
	global dij#coordinate of grid
	dij=np.floor((xy-xy.min(0))/dstep)
	for[i,j] in dij:
		i,j=int(i),int(j)
		d[i][j]=d[i][j]+1
	print len(dij)
	for idx,pair in enumerate(id2den):
		xx= int(dij[idx][0])
		yy= int(dij[idx][1])
		pair[1]=d[xx][yy]
	
	

	return id2den#id,density

def getprobability(timeperiod,id2den):
	coef_time=[250,250,150]#original,peak,off-peak
	tmp=np.zeros(len(id2den));
	id2prop=[]
	for idx,pair in enumerate(id2den):
		tmp[idx]=pair[1]
	d=np.sqrt(tmp+1)
	PO=d*coef_time[timeperiod]/np.max(d)#probablity of O
	PD=d*coef_time[timeperiod]/np.max(d)#probablity of O
	for idx,pair in enumerate(id2den):
		id2prop.append([pair[0],PO[idx],PD[idx]])
	return id2prop#id,probability

def normalizaion(id2prob):
	SumO=0;SumD=0;
	for pair in id2prob:
		SumO+=pair[1];
		SumD+=pair[2];
	for pair in id2prob:
		pair[1]=pair[1]/SumO
		pair[2]=pair[2]/SumD
	return id2prob
	#print id2prop
def buildgraph():
	path ='data/Hangzhou_Edgelist.csv'
	df=pd.read_csv(path,sep=',')#,nrows=1000
	graph={}
	VC={}
	EC={}
	for i,row in df.iterrows():
		node1=row['START_NODE']
		node2=row['END_NODE']
		length=row['LENGTH']
		if node1 not in graph:
			graph[node1]={}
			EC[node1]={}
		graph[node1][node2]=length
		EC[node1][node2]=0
		if node2 not in graph:
			graph[node2]={}
			EC[node1]={}
		graph[node2][node1]=length
		EC[node1][node2]=0
		VC[node1]=0
		VC[node2]=0
	return [graph,EC,VC]
	
def buildOD(numofOD,id2prob):
	ODpair=[]
	CPO=[]#cumulative_probability_O
	CPD=[]#cumulative_probability_O
	tmp1=0
	tmp2=0
	l=len(id2prob)
	for pair in id2prob:
		tmp1+=pair[1]
		tmp2+=pair[2]
		CPO.append(tmp1)
		CPD.append(tmp2)
	for i in range(numofOD):
		pair=[]
		p1=random.random()
		for j in range(l):
			if p1<CPO[j]:
				pair.append(id2prob[j][0])
				break
		p2=random.random()
		for j in range(l):
			if p2<CPD[j]:
				pair.append(id2prob[j][0])
				break
		ODpair.append(pair)
	return ODpair
	#for i in range(numofOD):

def updateweight(graph,node1,node2):
	graph[node1][node2]+=5

def findpath(graph,O,D):#return shortest distance and shortest path
	nodes=[]
	visited=[]
	dist={O:0}
	parent={O:O}
	path=[D]
	for i in graph:
		nodes.append(i)
		if i!=O: dist[i]=float('inf')
	visited.append(O)
	nodes.remove(O)
	cur=pre=O
	while nodes:
		mindist=float('inf')
		for v in visited:
			for n in nodes:
				if n in graph[v]:
					dist[n]=min(dist[n],dist[v]+graph[v][n])
					if dist[n]<mindist:
						mindist=dist[n]
						cur=n
						pre=v
						parent[cur]=pre
		visited.append(cur)
		nodes.remove(cur)
	node=D
	while node!=O:
		node=parent[node]
		path.append(node)
	path.reverse()
	return [dist[D],path]

def buildpath(graph,ODpair,VC,EC):
	parents={}
	for pair in ODpair:
		parent={}
		O=pair[0]
		D=pair[1]
		path=findpath(graph,O,D)[1]
		pre=O
		for node in path:
			VC[node]+=1
			if node!=O:
				EC[pre][node]+=1
				updateweight(graph,pre,node)
				if node not in parents:
					parents[node]=[]
				parents[node].append(pre)
			pre=node

	return [VC,EC,parents]

def relation(VC,EC,parents,k,a):# target node:k, 
	queue=[k]
	dist=0
	while queue:
		size=len(queue)
		for i in range(size):
			cur=queue.front()
			queue.popleft()
			for p in parents[cur]:
				alpha_p=pow(EC[p][cur]/VC[p],dist)
				if alpha_p>a:
					pi=(EC[p][cur]/VC[k])*alpha_p
					queue.append(p)
		dist+=1





id2den=getdensity()
id2prob=getprobability(0,id2den)
plot(id2prob)
id2prob=normalizaion(id2prob)
graphstruct=buildgraph()#graph,VC,EC
graph=graphstruct[0]
VC=graphstruct[1]
EC=graphstruct[2]
print graph[1][2]
updateweight(graph,1,2)
ODpair=buildOD(100,id2prob)
#pathinfo=buildpath(graph,ODpair,VC,EC)
#VC=pathinfo[0]
#EC=pathinfo[1]
#parents=pathinfo[2]
testgraph={0:{1:2,3:1},1:{3:3,4:10},2:{0:4,5:5},3:{2:2,4:2,5:8,6:4},4:{6:6},5:{},6:{5:1}}
print findpath(testgraph,0,1)
print findpath(testgraph,0,2)
print findpath(testgraph,0,3)
print findpath(testgraph,0,4)
print findpath(testgraph,0,5)
print findpath(testgraph,0,6)[1]
#print id2prop
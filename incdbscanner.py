import matplotlib
from cluster import *
import numpy as np
import matplotlib.pyplot as plt 
from numpy import inf
from numpy import sqrt 


class incdbscanner:

    dataSet = []
    count = 0
    visited = []
    curCores = []
    newCores = []
    Clusters = []
    potentialCLusters = []
    Outlier = 0
    num = 0

    def __init__(self):
        self.Outlier = cluster('Outlier')

    def incdbscan(
        self,
        D,
        eps,
        MinPts,
        K,
        ):


        Outlierpoints = []
        plt.figure(1)
        plt.title(r'INCREMENTAL DBSCAN Algorithm', fontsize=18)
        plt.xlabel(r'Dim 1', fontsize=17)
        plt.ylabel(r'Dim 2', fontsize=17)
        auxK = 0
        for point in D:
            self.dataSet.append(point)
            auxK += 1
            name = 'Cluster' + str(self.count)
            C = cluster(name)
            self.count += 1
            C.addPoint(point)
            self.curCores.append(point)
            self.Clusters.append(C)
            if(auxK == K):
                break
        D = D[K:]
        for point in D:
            self.dataSet.append(point)
            self.incrementalAdd(point, eps, MinPts)
            for core in self.newCores:
                if core not in self.curCores:
                    self.curCores.append(core)
        for clust in self.Clusters:
            plt.plot(clust.getX(), clust.getY(), 'o', label=clust.name)
        print ('Outlier \n')
        print (self.Outlier.getPoints())
        for Outlierp in self.Outlier.getPoints():
            Outlierpoints.append(Outlierp)
        for pts in Outlierpoints:
            print ('\nOutlier:' + str(Outlierpoints))
            print ('\nPoint:' + str(pts))
            for clust in self.Clusters:
                print ('Cluster Points ')
                clust.printPoints()
                if clust.has(pts) and self.Outlier.has(pts):
                    print ('\n Point to REMOVE' + str(pts))
                    self.Outlier.remPoint(pts)    
        print ('Outlier 2 \n')
        print (self.Outlier.getPoints())
        if len(self.Outlier.getPoints()) > 0:
            plt.plot(self.Outlier.getX(), self.Outlier.getY(), 'o',
                 label='Outlier')
        print(self.count)         



        plt.grid(True)
        plt.margins(0.05)
        plt.show()
        while True:
            plt.figure(2)
            plt.clf()
            plt.title(r'INCREMENTAL DBSCAN with k-control After Deletion', fontsize=18)
            plt.xlabel(r'Dim 1', fontsize=17)
            plt.ylabel(r'Dim 2', fontsize=17)
            for clust in self.Clusters:
                clust.printPoints()
                plt.plot(clust.getX(), clust.getY(), 'o', label=clust.name)
       
            if len(self.Outlier.getPoints()) > 0:
                self.Outlier.printPoints()
                plt.plot(self.Outlier.getX(), self.Outlier.getY(), 'o',
                     label='Outlier')

            plt.legend(loc='lower left')
            plt.grid(True)
            plt.margins(0.05)
            plt.show()
    #___________________________________________________________________________________________________________________________________________________________________________________--
    def expandCluster(
        self,
        point,
        NeighbourPoints,
        C,
        eps,
        MinPts,
        ):
        self.visited = []

        C.addPoint(point)

        for p in NeighbourPoints:
            if p not in self.visited:
                self.visited.append(p)
                np = self.regionQuery(p, eps)
                if len(np) >= MinPts:
                    for n in np:
                        if n not in NeighbourPoints:
                            NeighbourPoints.append(n)

            for c in self.Clusters:
                if not c.has(p):
                    if not C.has(p):
                        C.addPoint(p)

            if len(self.Clusters) == 0:
                if not C.has(p):
                    C.addPoint(p)

        self.Clusters.append(C)
        print ('\n' + C.name + '\n')
        C.printPoints()
    #_________________________________________________________________________________________________________________________

    def expandCluster2(
        self,
        point,
        NeighbourPoints,
        C,
        eps,
        MinPts,
        ):
        self.visited = []

        C.addPoint(point)

        for p in NeighbourPoints:
            if p not in self.visited:
                self.visited.append(p)
                np = self.regionQuery(p, eps)
                if len(np) >= MinPts:
                    for n in np:
                        if n not in NeighbourPoints:
                            NeighbourPoints.append(n)

            for c in self.potentialCLusters:
                if not c.has(p):
                    if not C.has(p):
                        C.addPoint(p)

            if len(self.potentialCLusters) == 0:
                if not C.has(p):
                    C.addPoint(p)

        self.potentialCLusters.append(C)
        print ('\n' + C.name + '\n')
        C.printPoints() 
        

    #____________________________________________________________________________________________________________________________________________________________________________________
    def regionQuery(self, P, eps):
        result = []
        for d in self.dataSet:
            if float(((float(d[0]) - float(P[0])) ** 2 + (float(d[1]) - float(P[1])) ** 2) ** 0.5) <= float(eps):
                result.append(d)
        return result
    #_________________________________________________________________________________________________________________________________________________________________________________________
    def findNearestCluster(self, p):
        closest = self.curCores[0]
        for core in self.curCores:
            if(np.linalg.norm(core-p)< np.linalg.norm(closest-p)):
                closest = core
        return closest
    #___________________________________________________________________________________________________________________________________________________
    def incrementalAdd(
        self,
        p,
        eps,
        Minpts,
        ):
        self.num = self.num + 1
        print ('\nADDING point ' + str(self.num))
        self.visited = []
        self.newCores = []
        UpdSeedIns = []
        foundClusters = []
        potentialSize = 1
        NeighbourPoints = self.regionQuery(p, eps)
        #if the p has enough points in its neighborhood had it to the new core record 
        if len(NeighbourPoints) >= Minpts:
            self.newCores.append(p)
        self.visited.append(p)
        potentialSize += len(NeighbourPoints)
        #visit the neighbors of p
        for pt in NeighbourPoints:
            #if the neighbor of the neighbor hasnt been visited before add it to the visited
            
            if pt not in self.visited:
                self.visited.append(pt)
                np = self.regionQuery(pt, eps)
                if len(np) >= Minpts:
                    #if the neighborhood of the neighbor is big enough add each of said neighbor of neighbors to the neighborhood of p
                    for n in np:
                        if n not in NeighbourPoints:
                            NeighbourPoints.append(n)
                    #if p neighbor with a big enough neighborhood isnt in the Core record add to the new core record        
                    if pt not in self.curCores:
                        self.newCores.append(pt)
                    potentialSize += len(np)    
        #for each pof these new cores                
        for core in self.newCores:
            corehood = self.regionQuery(core, eps)
            print ('the corehood is:', corehood)
            for elem in corehood:
                print ('The Minpts are:', Minpts)
                print (self.regionQuery(elem, eps))
                if len(self.regionQuery(elem, eps)) >= Minpts:
                    #had these new cores to the updateSeedList
                    if elem not in UpdSeedIns:
                        UpdSeedIns.append(elem)

        #if there are no points in UpdateSeedList p is an outlier
        if len(UpdSeedIns) < 1:
            self.Outlier.addPoint(p)
        else:
            #there are Seeds for the update
            findCount = 0
            #If any of the seed is in an already existate cluster update findcount, if said cluster isnt in found clusters add
            for seed in UpdSeedIns:
                for clust in self.Clusters:
                    if clust.has(seed):
                        findCount += 1
                        if clust.name not in foundClusters:
                            foundClusters.append(clust.name)
                            break
            #Creating a new cluster
            # if the seeds werent found in any existing cluster we need to create a new one          
            if len(foundClusters) == 0:
                flag = 0
                for clust in self.Clusters:
                    if(clust.size() < Minpts):
                        for pt in clust.getPoints():
                            self.Outlier.addPoint(pt)
                        self.Clusters.remove(clust)
                        self.count += 1
                        name = "Cluster" + str(self.count)
                        C = cluster(name)
                        self.expandCluster(UpdSeedIns[0],self.regionQuery(UpdSeedIns[0],eps), C, eps, Minpts)
                        flag = 1
                        print("Deleting CLuster thats too small and expanding P")
                        break
                if(flag == 0) :
                    smallest = self.Clusters[0]
                    #First look for the smallest cluster already created
                    for clust in self.Clusters:
                        if(clust.size() < smallest.size()):
                            smallest=clust 
                    if(potentialSize > smallest.size()):
                        closest = self.Clusters[0]
                        #original = self.Clusters[0]
                        min_dist = inf
                        for pt in smallest.getPoints():
                            for clust in self.Clusters:
                                for point in clust.getPoints():
                                    if( sqrt((pt[0]-point[0])**2 + (pt[1]-point[1])**2) <min_dist and clust != smallest):
                                        closest = clust
                                        original = clust
                                        min_dist = sqrt((pt[0]-point[0])**2 + (pt[1]-point[1])**2)                  
                        if(min_dist <= eps):
                            #merge them
                            master = closest
                            print('close')
                            closest.printPoints()
                            print('small')
                            smallest.printPoints()
                            for pt in smallest.getPoints():
                                if not master.has(pt):
                                 master.addPoint(pt)   
                            self.Clusters.remove(smallest)
                            self.Clusters.remove(original)
                            self.Clusters.append(master)
                            self.count += 1
                            name = "Cluster" + str(self.count)
                            C = cluster(name)
                            self.expandCluster(UpdSeedIns[0],self.regionQuery(UpdSeedIns[0],eps), C, eps, Minpts)
                            print("Merging smallest with closest and expanding p")
                        else:
                            self.potentialCLusters.append(smallest)
                            for pt in smallest.getPoints():
                                self.Outlier.addPoint(pt)
                            self.Clusters.remove(smallest)
                            self.count += 1
                            name = "Cluster" + str(self.count)
                            C = cluster(name)
                            self.expandCluster(UpdSeedIns[0],self.regionQuery(UpdSeedIns[0],eps), C, eps, Minpts)
                            print("Deleting smallest and expanding p")
                    else:
                        self.count +=1
                        name = "Cluster" + str(self.count)
                        C = cluster(name)
                        self.expandCluster2(UpdSeedIns[0],self.regionQuery(UpdSeedIns[0],eps), C, eps, Minpts)
                        self.Outlier.addPoint(p)
                        print("p becomes outlier")
            #Adding a Point P to already existing cluster                      
            elif len(foundClusters) == 1:
                originalCluster = -1
                newCluster = -1
                for c in self.Clusters:
                    if c.name == foundClusters[0]:
                        originalCluster = c
                        newCluster = c
                newCluster.addPoint(p)
                #Replace with a need freshly made cluster
                if len(UpdSeedIns) > findCount:
                    for seed in UpdSeedIns:
                        if not newCluster.has(seed):
                            newCluster.addPoint(seed)
                self.Clusters.remove(originalCluster)
                self.Clusters.append(newCluster)
            else:
                if len(self.potentialCLusters) > 0 :
                    master_name = foundClusters[0]
                    master = self.Clusters[0]
                    original = self.Clusters[0]
                    foundClusters.pop(0)
                    for clust in self.Clusters:
                        if clust.name == master_name:
                            master = clust
                            original = clust
                    while(len(foundClusters)>0 and len(self.potentialCLusters)>0):
                        merge_name = foundClusters[0]
                        foundClusters.pop(0)
                        original_merge = self.Clusters[0]
                        merge = self.Clusters[0]
                        for clust in self.Clusters:
                            if clust.name == merge_name:
                                original_merge = clust
                                merge = clust
                        for pt in merge:
                            if not master.has(pt):
                                master.addPoint(pt)
                        toadd = self.potentialCLusters[0]
                        self.Clusters.append(toadd)        
                        self.potentialCLusters.remove(toadd)
                        self.Clusters.remove(original_merge)
                                       

                    for seed in UpdSeedIns:
                        if not master.has(seed):
                            master.addPoint(seed)
                    master.addPoint(p)
                    self.Clusters.remove(original)
                    self.Clusters.append(master) 


                
                else:
                    smallest1_name = foundClusters[0]
                    for clust in self.Clusters:
                        if clust.name == smallest1_name:
                            smallest1 = clust
                    minsize = smallest1.size()
                    for clust in foundClusters:
                        for c in self.Clusters:
                            if c.name == clust:
                                size = c.size()
                                if size < minsize:
                                    smallest1 = c
                                    minsize = size
                    master = smallest1        
                    for seed in UpdSeedIns:
                        if not master.has(seed):
                            master.addPoint(seed)    
                    master.addPoint(p)  
                    self.Clusters.remove(smallest1)
                    self.Clusters.append(master)


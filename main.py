from incdbscanner import *
import csv
import re
import sys
sys.path.append('./')
configPath = 'config'
dataPath = 'ppf2.csv'
def main():
    [Data,eps,MinPts,K]= getData()
    print(len(Data))
    indbc= incdbscanner()
    indbc.incdbscan(Data, eps, MinPts, K)
def getData():
    Data = []
    with open(dataPath, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            Data.append([float(row[0]),float(row[1])])
           
    f = open(configPath,'r')
   
    [eps,MinPts,K] = parse(f.readline())
   
    print(eps,MinPts,K)
   
    return [Data,eps,MinPts,K]
def parse(line):
    data = line.split(" ")
    return [int(data[0]),int(data[1]), int(data[2])]
   
           
   
main()
import os
import datetime
from tomlinCostDistance import *


def main():
    nRow = 20  # number of rows
    nCol = 20  # number of columns
    HowFar = 10000.0  # maximum travel-cost distance to be calculated

    InitialCost = [[-1 for i in range(nCol)] for i in range(nRow)]
    InitialCost[9][9] = 0  # set the value of sources to a non-negative number

    IncrementalCost = [[-1 for i in range(nCol)] for i in range(nRow)]
    # read the friction data from the file
    frictionFile = "IncrementalCost2.txt"
    try:
        f=open(frictionFile)
        for i in range(0,nRow,1):
             line = f.readline()
             tempValues = line.split(' ')
             for j in range(0,nCol,1):
                 IncrementalCost[i][j] = int(tempValues[j])
        f.close()
    except:
        print("%S opening failed" % frictionFile)

    # set the source of each cell to itself
    ShiftNorth = [[0 for i in range(nCol)] for i in range(nRow)]
    ShiftEast = [[0 for i in range(nCol)] for i in range(nRow)]

    print ("Start calculating.")
    starttime = datetime.datetime.now()
    CostDistance = spread(nRow,nCol,HowFar,InitialCost,IncrementalCost,ShiftNorth,ShiftEast)
    endtime = datetime.datetime.now()
    print ("Running time: " + str((endtime-starttime).seconds) )
    print ("Calculating completed.")

    # save the results
    f1=open('CostDistance.txt','w')
    f2=open('shiftNorth.txt','w')
    f3=open('shiftEast.txt','w')
    for i in range(0,nRow,1):
        for j in range(0,nCol,1):
            f1.write(str(CostDistance[i][j]))
            f1.write(' ')
            f2.write(str(int(ShiftNorth[i][j])))
            f2.write(' ')
            f3.write(str(int(ShiftEast[i][j])))
            f3.write(' ')
        f1.write('\n')
        f2.write('\n')
        f3.write('\n')
    f1.close()
    f2.close()
    f3.close()

    print ("Data saving completed.")

if __name__ == '__main__':
    main()


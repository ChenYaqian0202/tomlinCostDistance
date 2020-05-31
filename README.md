# tomlinCostDistance
The 2D cost distance algorithm proposed by Tomlin implemented in Python.

-------------------------
Core file and parameter settings
-------------------------
tomlinCostDistance.py is the core file.
The input parameters can be modified in the main.py.
main.py and tomlinCostDistance.py should be put in the same dictionary.


-------------------------
Example data
-------------------------
IncrementalCost1.txt and IncrementalCost2.txt are two example input friction data files.


-------------------------
Output
-------------------------
The algorithm generates three arrays:
(1) CostDistance.txt------recording the least accumulative cost from each cell to its nearest source
(2) ShiftNorth.txt--------recording each cell's row distance from its SourceCell
(3) ShiftEast.txt---------recording each cell's column distance from its SourceCell
v:(i,j)
v's nearest source s: (i + ShiftNorth[i][j], j - ShiftEast[i][j])


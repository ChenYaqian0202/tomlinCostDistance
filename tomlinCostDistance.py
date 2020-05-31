import math


def blocked (ActiveRow,ActiveColumn,InwardShiftNorth,InwardShiftEast,NeighborRow,NeighborColumn,IncrementalCost):
    # RETURN 1 IF TRAVEL PATH FROM SOURCE TO NEIGHBOR
    # IS BLOCKED BY HIGHER INCREMENTAL COST
    SourceRow = int(ActiveRow + InwardShiftNorth)
    SourceColumn = int(ActiveColumn - InwardShiftEast)
    Blockage = 0
    if abs(NeighborRow-SourceRow) >= abs(NeighborColumn-SourceColumn):
        if NeighborRow <> SourceRow:
            if NeighborRow < SourceRow: RowStep = 1
            else: RowStep = -1
            if NeighborRow + RowStep <> SourceRow:
                Cshift = float(SourceColumn-NeighborColumn) / float(abs(SourceRow-NeighborRow))
                C = float(NeighborColumn)
                for NextRow in range(NeighborRow + RowStep,SourceRow,RowStep):
                    C = C + Cshift
                    NextCol = int(C + 0.5)
                    if IncrementalCost[NextRow][NextCol] > IncrementalCost[NeighborRow][NeighborColumn]:
                            Blockage = 1
                            break
    elif NeighborColumn <> SourceColumn:
        if NeighborColumn < SourceColumn : ColStep = 1
        else: ColStep = -1
        if NeighborColumn + ColStep <> SourceColumn:
            Rshift = float(SourceRow-NeighborRow) / float(abs(SourceColumn-NeighborColumn))
            R = float(NeighborRow)
            for NextCol in range(NeighborColumn + ColStep,SourceColumn,ColStep):
                R = R + Rshift
                NextRow = int(R + 0.5)
                if IncrementalCost[NextRow][NextCol] > IncrementalCost[NeighborRow][NeighborColumn]:
                        Blockage = 1
                        break
    return Blockage

def getSideCell (NextNeighbor,ActiveRow,ActiveColumn,InwardShiftNorth,InwardShiftEast,OutwardShiftNorth,OutwardShiftEast):
        # IDENTIFY SIDE CELL AROUND WHICH TRAVEL PATH
        # FROM SOURCE TO NEIGHBOR PIVOTS
        global SideRow, SideColumn
        SideRow = ActiveRow
        SideColumn = ActiveColumn
        if InwardShiftEast == 0: IncomingSlope = 99999999.9
        else: IncomingSlope = float(InwardShiftNorth)/float(InwardShiftEast)
        if InwardShiftNorth > 0 and InwardShiftEast == 0:
            if OutwardShiftEast == 1: SideColumn = ActiveColumn + 1
            elif OutwardShiftEast == -1: SideColumn = ActiveColumn - 1
        elif InwardShiftNorth < 0 and InwardShiftEast == 0:
            if OutwardShiftEast == 1: SideColumn = ActiveColumn + 1
            elif OutwardShiftEast == -1: SideColumn = ActiveColumn - 1
        elif InwardShiftNorth == 0 and InwardShiftEast > 0:
            if OutwardShiftNorth == 1: SideRow = ActiveRow - 1
            elif OutwardShiftNorth == -1: SideRow = ActiveRow + 1
        elif InwardShiftNorth == 0 and InwardShiftEast < 0:
            if OutwardShiftNorth == 1: SideRow = ActiveRow - 1
            elif OutwardShiftNorth == -1: SideRow = ActiveRow + 1
        elif InwardShiftNorth > 0 and InwardShiftEast > 0:
            if NextNeighbor == 0 or NextNeighbor == 4: SideColumn = ActiveColumn - 1
            elif NextNeighbor == 1 or NextNeighbor == 6: SideRow = ActiveRow + 1
            elif NextNeighbor == 5:
                if IncomingSlope < 1.0: SideRow = ActiveRow - 1
                elif IncomingSlope > 1.0: SideColumn = ActiveColumn + 1
        elif InwardShiftNorth < 0 and InwardShiftEast > 0:
            if NextNeighbor == 1 or NextNeighbor == 5: SideRow = ActiveRow - 1
            elif NextNeighbor == 2 or NextNeighbor == 10: SideColumn = ActiveColumn - 1
            elif NextNeighbor == 6:
                if IncomingSlope < -1.0: SideColumn = ActiveColumn + 1
                elif IncomingSlope > -1.0: SideRow = ActiveRow + 1
        elif InwardShiftNorth < 0 and InwardShiftEast < 0:
            if NextNeighbor == 2 or NextNeighbor == 6: SideColumn = ActiveColumn + 1
            elif NextNeighbor == 3 or NextNeighbor == 4: SideRow = ActiveRow - 1
            elif NextNeighbor == 10:
                if IncomingSlope < 1.0: SideRow = ActiveRow + 1
                elif IncomingSlope > 1.0: SideColumn = ActiveColumn - 1
        elif InwardShiftNorth > 0 and InwardShiftEast < 0:
            if NextNeighbor == 3 or NextNeighbor == 10: SideRow = ActiveRow + 1
            elif NextNeighbor == 0 or NextNeighbor == 5: SideColumn = ActiveColumn + 1
            elif NextNeighbor == 4:
                if IncomingSlope < -1.0: SideColumn = ActiveColumn - 1
                elif IncomingSlope > -1.0: SideRow = ActiveRow - 1


def spread(HowManyRows,HowManyColumns,HowFar,InitialCost,IncrementalCost,ShiftNorth,ShiftEast):
    # RETURN A REAL-NUMBER ARRAY REPRESENTING A GRID OF ACCUMULATED TRAVEL COSTS
    # HowManyRows         is an integer indicating number of rows in input and output grids
    # HowManyColumns      is an integer indicating number of columns in input and output grids
    # HowFar              is an integer indicating maximum travel-cost distance to be calculated
    # InitialCost         is an integer or real-number array representing an input grid on which
    #                     StartingCells from which travel-cost distances are to be measured
    #                     are set to 0 (or greater to apply an initial "headstart" distance),
    #                     while others are below 0
    # IncrementalCost     is a real-number array representing an input grid on which
    #                     each cell's value indicates its side-to-side dimension in travel cost
    # ShiftNorth          is an integer array recording each cell's row distance from its SourceCell
    # ShiftEast           is an integer array recording each cell's column distance from its SourceCell
    # CumulativeCost      is a real-number array representing the output grid of accumulated travel costs
    # INITIALIZE
    SqRtOf2 = math.sqrt(2)
    OctagonalShift = [ 1, 1, 1, 1,SqRtOf2,SqRtOf2,SqRtOf2,SqRtOf2]
    RowShift = [-1, 0, 1, 0,-1,-1, 1, 1]
    ColumnShift = [ 0, 1, 0,-1,-1, 1, 1,-1]
    InwardShiftNorth = 0
    InwardShiftEast = 0
    ActiveCost = 1.0
    NewDistance = 1.0
    ActiveList = [[0,0,0]]
    CumulativeCost = [[0 for i in range(HowManyColumns)] for i in range(HowManyRows)]
    for ThisRow in range(HowManyRows):
        for ThisColumn in range(HowManyColumns):
            if IncrementalCost[ThisRow][ThisColumn]<1:
                IncrementalCost[ThisRow][ThisColumn] = 1.0
            if InitialCost[ThisRow][ThisColumn] >= 0:
                ActiveList.append([InitialCost[ThisRow][ThisColumn],ThisRow,ThisColumn])
                CumulativeCost[ThisRow][ThisColumn] = InitialCost[ThisRow][ThisColumn]
            else: CumulativeCost[ThisRow][ThisColumn] = HowFar
    ActiveList[0:1] = []
    ActiveList.sort()
    # LOOP THROUGH LIST OF ACTIVE CELLS
    for NextActiveCell in ActiveList:
        if NextActiveCell[0] > HowFar: break
        ActiveDistance = NextActiveCell[0]
        ActiveRow = NextActiveCell[1]
        ActiveColumn = NextActiveCell[2]
        ActivePosition = ActiveList.index(NextActiveCell)
        ActiveCost = IncrementalCost[ActiveRow][ActiveColumn]
        InwardShiftNorth = ShiftNorth[ActiveRow][ActiveColumn]
        InwardShiftEast = ShiftEast[ActiveRow][ActiveColumn]
       
        # LOOP THROUGH ACTIVE CELL'S ADJACENT NEIGHBORS
        for NextNeighbor in range(8):
            OutwardShiftNorth = -RowShift[NextNeighbor]
            OutwardShiftEast = ColumnShift[NextNeighbor]
            NeighborRow = ActiveRow + RowShift[NextNeighbor]
            if NeighborRow < 0 or NeighborRow >= HowManyRows: continue
            NeighborColumn = ActiveColumn + OutwardShiftEast 
            if NeighborColumn < 0 or NeighborColumn >= HowManyColumns: continue
            if IncrementalCost[NeighborRow][NeighborColumn] > HowFar:continue
         
            # CALCULATE DISTANCE FROM ACTIVE CELL TO NEIGHBOR CELL
            NewDistance = ((ActiveCost + IncrementalCost[NeighborRow][NeighborColumn])/2.0 )* OctagonalShift[NextNeighbor]
           
            # IF TRAVEL PATH FROM SOURCE TO NEIGHBOR REFRACTS,
            # CALCULATE NEIGHBOR'S DISTANCE
            # AND MAKE ACTIVE CELL A NEW SOURCE
            if IncrementalCost[NeighborRow][NeighborColumn] < IncrementalCost[ActiveRow][ActiveColumn]:
                NeighborShiftNorth = OutwardShiftNorth
                NeighborShiftEast = OutwardShiftEast
                NeighborDistance = ActiveDistance + NewDistance

            # IF PATH DOESN'T REFRACT BUT DOES DIFFRACT
            # CALCULATE NEIGHBOR'S DISTANCE
            else:
                getSideCell (NextNeighbor,ActiveRow,ActiveColumn,InwardShiftNorth,InwardShiftEast,OutwardShiftNorth,OutwardShiftEast)
                if IncrementalCost[SideRow][SideColumn] > ActiveCost:
                    NeighborShiftNorth = OutwardShiftNorth
                    NeighborShiftEast = OutwardShiftEast
                    NeighborDistance = ActiveDistance + NewDistance

                # IF PATH DOESN'T REFRACT OR DIFFRACT
                # BUT IS BLOCKED BY HIGHER INCREMENTAL COST
                # SKIP THIS NEIGHBOR
                elif blocked(ActiveRow,ActiveColumn,InwardShiftNorth,InwardShiftEast,NeighborRow,NeighborColumn,IncrementalCost): 
                    continue

                # IF PATH IS UNREFRACTED, UNDIFFRACTED, AND UNBLOCKED,
                # CALCULATE NEIGHBOR'S DISTANCE FROM ACTIVE CELL'S SOURCE CELL
                else:
                    NeighborShiftNorth = OutwardShiftNorth + InwardShiftNorth
                    NeighborShiftEast = OutwardShiftEast + InwardShiftEast
                    SourceToNeighbor = math.sqrt(math.pow((InwardShiftNorth + OutwardShiftNorth),2) + math.pow((InwardShiftEast + OutwardShiftEast), 2))
                    SourceToActive = math.sqrt(math.pow(InwardShiftNorth,2) + math.pow(InwardShiftEast,2))
                    ActiveToNeighbor = math.sqrt(math.pow(OutwardShiftNorth,2) + math.pow(OutwardShiftEast,2))
                    OctangularFix = (SourceToNeighbor-SourceToActive) / ActiveToNeighbor
                    NeighborDistance = ActiveDistance + (NewDistance * OctangularFix)

            # IF NEIGHBOR'S NEW DISTANCE EXCEEDS ITS CURRENT DISTANCE
            # OR THE MAXIMUM DISTANCE LIMIT, SKIP THIS NEIGHBOR
            if (NeighborDistance * 1.00001) >= CumulativeCost[NeighborRow][NeighborColumn] or NeighborDistance > HowFar: 
                    continue

            # IF NEIGHBOT HAD ALREADY BEEN REACHED,
            # REMOVE IT FROM THE ACTIVE LIST
            if ShiftNorth[NeighborRow][NeighborColumn] <> 0 or ShiftEast[NeighborRow][NeighborColumn] <> 0:
                for OldActiveCell in ActiveList[ActivePosition:]:
                     if OldActiveCell[1] == NeighborRow and OldActiveCell[2] == NeighborColumn:
                         del ActiveList[ActiveList.index(OldActiveCell)]
                         break
            # ADD NEIGHBOR TO THE ACTIVE LIST, THE CUMULATIVE COST GRID,
            # THE SHIFTNORTH GRID, AND THE SHIFTEAST GRID       
            for OldActiveCell in ActiveList[ActivePosition:]:
                if NeighborDistance >= OldActiveCell[0]: continue
                ActiveList.insert(ActiveList.index(OldActiveCell),[NeighborDistance,NeighborRow,NeighborColumn])
                break            
            else:
                ActiveList.append([NeighborDistance,NeighborRow,NeighborColumn])
            CumulativeCost[NeighborRow][NeighborColumn] = NeighborDistance
            ShiftNorth[NeighborRow][NeighborColumn] = NeighborShiftNorth
            ShiftEast[NeighborRow][NeighborColumn] = NeighborShiftEast
    # RETURN THE CUMULATIVE COST GRID
    return CumulativeCost



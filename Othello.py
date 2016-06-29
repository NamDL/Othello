#!/usr/bin/python

import sys
import Queue
import heapq
import copy

values=[[0 for x in range(5)] for x in range (5)]
currentState=[[0 for x in range(5)] for x in range (5)]
charArray=[['A1','B1','C1','D1','E1'],['A2','B2','C2','D2','E2'],['A3','B3','C3','D3','E3'],['A4','B4','C4','D4','E4'],['A5','B5','C5','D5','E5']]

class Square:
   'Defines each square in the board'
   def __init__(self,explored,row,col):
      self.cellValue=0
      self.explored = explored
      self.row = row
      self.col=col
      self.a=-9999
      self.b=9999
   def isExplored():
       return self.explored
   def __cmp__(self, other):
        return cmp(self.cellValue, other.cellValue)
      
def printToFile(row,col,curDepth,value,alpha,beta,bo):
   if alpha>=9999:
      alpha="Infinity"
   if value>=9999:
      value="Infinity"
   if beta>=9999:
      beta="Infinity"                                                                                                                        
   if alpha<=-9999:
      alpha="-Infinity"
   if value<=-9999:
      value="-Infinity"
   if beta<=-9999:
      beta="-Infinity"                                                                                                                        
   string=charArray[row][col]+","+str(curDepth)+","+str(value)+","+str(alpha)+","+str(beta)                                                                                                                 
   bo.write(string)
   bo.write("\n")

def printToFile2(row,col,curDepth,value,bo):
   if value>=9999:
      value="Infinity"
   if value<=-9999:
      value="-Infinity"
   string=charArray[row][col]+","+str(curDepth)+","+str(value)
   bo.write(string)
   bo.write("\n")

def raidCell(row,col,player):
    if player=='X':
        opponent='O'
    else:
        opponent='X'
    raidValue=values[row][col]
    for i in row-1, row, row+1:
        if i < 0 or i == len(currentState): continue
        for j in col-1, col, col+1:
            if j < 0 or j == len(currentState[i]): continue
            if i == row and j == col: continue
            if i==row-1 and j==col-1: continue
            if i==row+1 and j==col+1: continue
            if i==row+1 and j==col-1: continue
            if i==row-1 and j==col+1: continue
            if currentState[i][j]==opponent:
               raidValue=raidValue+values[i][j]
    return raidValue

def raidCellMM(row,col,player):
    if player=='X':
        opponent='O'
    else:
        opponent='X'
    raidValue=0
    for i in row-1, row, row+1:
        if i < 0 or i == len(currentState): continue
        for j in col-1, col, col+1:
            if j < 0 or j == len(currentState[i]): continue
            if i == row and j == col: continue
            if i==row-1 and j==col-1: continue
            if i==row+1 and j==col+1: continue
            if i==row+1 and j==col-1: continue
            if i==row-1 and j==col+1: continue
            if currentState[i][j]==opponent:
               raidValue=raidValue+values[i][j]
    return raidValue

#check if the particular square can be raided( aka adjacent to an existing piece of the player) or not
def checkRaidValidity(row,col,player):
    raid=False
    for i in row-1, row, row+1:
        if i < 0 or i == len(currentState): continue
        for j in col-1, col, col+1:
            if j < 0 or j == len(currentState[i]): continue
            if i == row and j == col: continue
            if i==row-1 and j==col-1: continue
            if i==row+1 and j==col+1: continue
            if i==row+1 and j==col-1: continue
            if i==row-1 and j==col+1: continue
            if(currentState[i][j]==player):
                raid=True
                return raid
    return raid

#check if the heap contains another entry with vaue as much as the highest value. if so compare the two and return the one that occurs earliest.
def checkForDuplicates(square,h):
    for val in h:
        if square.cellValue==val.cellValue:
            if(val.row<square.row):
                return val
            elif(val.row==square.row):
                if(val.col==square.col):
                    return val
    return square            

def upDateCurrentState(row,col,player):
   if player=='X':
        opponent='O'
   else:
        opponent='X'
   for i in row-1, row, row+1:
        if i < 0 or i == len(currentState): continue
        for j in col-1, col, col+1:
            if j < 0 or j == len(currentState[i]): continue
            if i == row and j == col: continue
            if i==row-1 and j==col-1: continue
            if i==row+1 and j==col+1: continue
            if i==row+1 and j==col-1: continue
            if i==row-1 and j==col+1: continue
            if(currentState[i][j]==opponent):
               currentState[i][j]=player

#predict the next state by making use of the greedy best first search.
def nextStateGBFS(squareList,player,opponentValue,myValue,fo):
    h = []
    nodeLarge=None
    value=-9999
    op=opponentValue
    for val in squareList:
        if(val.explored == False):
            opponentValue=op
            cellGain=0
            isRaid=checkRaidValidity(val.row,val.col,player)
            if isRaid:
                cellGain=raidCellMM(val.row,val.col,player)
                opponentValue=opponentValue-cellGain
            cellGain=myValue+cellGain-opponentValue+values[val.row][val.col]
            setattr(val, 'cellValue', cellGain)
            heapq.heappush(h, val)
            if(cellGain>value):
               value=cellGain
               nodeLarge=copy.deepcopy(val)
    return nodeLarge


def getRaidSet(row,col,player):
   global currentState
   if player=='X':
        opponent='O'
   else:
        opponent='X'
   raidValue=[[0 for x in range(5)] for x in range (5)]
   for i in row-1, row, row+1:
        if i < 0 or i == len(currentState): continue
        for j in col-1, col, col+1:
            if j < 0 or j == len(currentState[i]): continue
            if i == row and j == col: continue
            if i==row-1 and j==col-1: continue
            if i==row+1 and j==col+1: continue
            if i==row+1 and j==col-1: continue
            if i==row-1 and j==col+1: continue
            if currentState[i][j]==opponent:
               raidValue[i][j]=1
   return raidValue


def nextStateFindMax(squareList,node,curDepth,depth,myValue,opponentValue,player,opponent,bo):
   if curDepth==depth:
      cellGain=0
      isRaid=checkRaidValidity(node.row,node.col,player)
      if isRaid:
         cellGain=raidCellMM(node.row,node.col,player)
         opponentValue=opponentValue-cellGain
      cellGain=myValue+cellGain-opponentValue+values[node.row][node.col]
      node.cellValue=cellGain
      return node   
   else:
      h=[]
      global currentState
      nodeLarge=node
      valueNode=9999
      if(not (checkIfContinue(squareList))):
         return Square("None",-1,-1)
      for val in squareList:
         if(val.explored==False):
            val.explored=True
            printToFile2(node.row,node.col,curDepth,node.cellValue,bo)
            cellGain=0
            isRaid=checkRaidValidity(node.row,node.col,player)
            raidSet=[[0 for x in range(5)] for x in range (5)]
            if isRaid:
               cellGain=raidCellMM(node.row,node.col,player)
               raidSet=getRaidSet(node.row,node.col,player)
               for i in range(0,5):
                  for j in range(0,5):
                     if raidSet[i][j]==1:
                        currentState[i][j]=player
            currentState[node.row][node.col]=player
            val.cellValue=-9999
            endSquare=nextStateFindMin(squareList,val,curDepth+1,depth,myValue+values[node.row][node.col]+cellGain,opponentValue-cellGain,player,opponent,bo)
            printToFile2(val.row,val.col,curDepth+1,val.cellValue,bo)
            currentState[node.row][node.col]='*'
            for i in range(0,5):
                  for j in range(0,5):
                     if raidSet[i][j]==1:
                        currentState[i][j]=opponent
            val.explored=False
            if(endSquare.cellValue<valueNode):
               nodeLarge=copy.deepcopy(endSquare)
               valueNode=endSquare.cellValue
               node.cellValue=endSquare.cellValue
      return nodeLarge

def nextStateFindMin(squareList,node,curDepth,depth,myValue,opponentValue,player,opponent,bo):
   if curDepth==depth:
      cellGain=0
      isRaid=checkRaidValidity(node.row,node.col,opponent)
      if isRaid:
         cellGain=raidCellMM(node.row,node.col,opponent)
         myValue=myValue-cellGain
      cellGain=myValue-cellGain-opponentValue-values[node.row][node.col]
      node.cellValue=cellGain
      return node
   else:
      nodeLarge=node   
      valueNode=-9999
      if(not (checkIfContinue(squareList))):
         return Square("None",-1,-1)
      for val in squareList:
         if(val.explored==False):
            val.explored=True
            printToFile2(node.row,node.col,curDepth,node.cellValue,bo)
            raidSet=[[0 for x in range(5)] for x in range (5)]
            isRaid=checkRaidValidity(node.row,node.col,opponent)
            cellGain=0
            if isRaid:
               cellGain=raidCellMM(node.row,node.col,opponent)
               raidSet=getRaidSet(node.row,node.col,opponent)
               for i in range(0,5):
                  for j in range(0,5):
                     if raidSet[i][j]==1:
                        currentState[i][j]=opponent
            currentState[node.row][node.col]=opponent
            val.cellValue=9999
            endSquare=nextStateFindMax(squareList,val,curDepth+1,depth,myValue-cellGain,opponentValue+values[node.row][node.col]+cellGain,player,opponent,bo)
            currentState[node.row][node.col]='*'
            for i in range(0,5):
                  for j in range(0,5):
                     if raidSet[i][j]==1:
                        currentState[i][j]=player
            if(endSquare.cellValue>valueNode):
               nodeLarge=copy.deepcopy(endSquare)
               valueNode=endSquare.cellValue
               node.cellValue=endSquare.cellValue
            printToFile2(val.row,val.col,curDepth+1,val.cellValue,bo)
            val.explored=False
      return nodeLarge
      
       
def nextStateMinMax(squareList,depth,myValue,opponentValue,player,opponent,fo):
   value=-9999
   nodeLargest=None
   bo = open("traverse_log.txt", "a")
   bo.write("Node,Depth,Value")
   bo.write("\n")
   string="root,0,-Infinity"
   bo.write(string)
   bo.write("\n")
   for val in squareList:
      h=[]
      if(val.explored==False):
         val.explored=True
         val.cellValue=9999       
         square=nextStateFindMax(squareList,val,1,depth,myValue,opponentValue,player,opponent,bo)
         val.explored=False
         if square.explored=="None":
            return val
         if square.cellValue>value:
            nodeLargest=copy.deepcopy(val)
            value=square.cellValue
         printToFile2(val.row,val.col,1,val.cellValue,bo)
         string="root,0,"+str(nodeLargest.cellValue)
         bo.write(string)
         bo.write("\n")
   return nodeLargest

def nextStateMinAB(squareList,node,curDepth,depth,myValue,opponentValue,player,opponent,A,B,bo):
   if curDepth==depth:
      node.a=A
      node.b=B
      cellGain=0
      isRaid=checkRaidValidity(node.row,node.col,opponent)
      if isRaid:
         cellGain=raidCellMM(node.row,node.col,opponent)
         myValue=myValue-cellGain
      cellGain=myValue-cellGain-opponentValue-values[node.row][node.col]
      node.cellValue=cellGain
      return node
   else:
      node.a=A
      node.b=B
      nodeLarge=node
      valueNode=-9999
      nodeLarge=node
      if(not (checkIfContinue(squareList))):
         return Square("None",-1,-1)
      for val in squareList:
         if(val.explored==False):
            val.explored=True
            printToFile(node.row,node.col,curDepth,node.cellValue,node.a,node.b,bo)
            raidSet=[[0 for x in range(5)] for x in range (5)]
            isRaid=checkRaidValidity(node.row,node.col,opponent)
            cellGain=0
            if isRaid:
               cellGain=raidCellMM(node.row,node.col,opponent)
               raidSet=getRaidSet(node.row,node.col,opponent)
               for i in range(0,5):
                  for j in range(0,5):
                     if raidSet[i][j]==1:
                        currentState[i][j]=opponent
            currentState[node.row][node.col]=opponent
            prev=node.a
            val.cellValue=9999
            endSquare=nextStateMaxAB(squareList,val,curDepth+1,depth,myValue-cellGain,opponentValue+values[node.row][node.col]+cellGain,player,opponent,node.a,node.b,bo)
            currentState[node.row][node.col]='*'
            for i in range(0,5):
                  for j in range(0,5):
                     if raidSet[i][j]==1:
                        currentState[i][j]=player
            val.explored=False            
            if(endSquare.cellValue>valueNode):
               nodeLarge=copy.deepcopy(endSquare)
               valueNode=endSquare.cellValue
               node.cellValue=endSquare.cellValue
            node.a=max(node.a,endSquare.cellValue)
            printToFile(val.row,val.col,curDepth+1,val.cellValue,val.a,val.b,bo)
            if node.a>=node.b:
               node.a=prev
               return node
      return nodeLarge         


def nextStateMaxAB(squareList,node,curDepth,depth,myValue,opponentValue,player,opponent,A,B,bo):
   if curDepth==depth:
      node.a=A
      node.b=B
      cellGain=0
      isRaid=checkRaidValidity(node.row,node.col,player)
      if isRaid:
         cellGain=raidCellMM(node.row,node.col,player)
         opponentValue=opponentValue-cellGain
      cellGain=myValue+cellGain-opponentValue+values[node.row][node.col]
      node.cellValue=cellGain
      return node
   else:
      h=[]
      node.a=A
      node.b=B
      global currentState
      nodeLarge=node
      valueNode=9999
      if(not (checkIfContinue(squareList))):
         return Square("None",-1,-1)
      for val in squareList:
         if(val.explored==False):
            val.explored=True
            printToFile(node.row,node.col,curDepth,node.cellValue,node.a,node.b,bo)
            cellGain=0
            isRaid=checkRaidValidity(node.row,node.col,player)
            raidSet=[[0 for x in range(5)] for x in range (5)]
            if isRaid:
               cellGain=raidCellMM(node.row,node.col,player)
               raidSet=getRaidSet(node.row,node.col,player)
               for i in range(0,5):
                  for j in range(0,5):
                     if raidSet[i][j]==1:
                        currentState[i][j]=player               
            currentState[node.row][node.col]=player
            prev=node.b
            val.cellValue=-9999
            endSquare=nextStateMinAB(squareList,val,curDepth+1,depth,myValue+values[node.row][node.col]+cellGain,opponentValue-cellGain,player,opponent,node.a,node.b,bo)
            val.explored=False
            currentState[node.row][node.col]='*'
            for i in range(0,5):
                  for j in range(0,5):
                     if raidSet[i][j]==1:
                        currentState[i][j]=opponent            
            if(endSquare.cellValue<valueNode):
               nodeLarge=copy.deepcopy(endSquare)
               valueNode=endSquare.cellValue
               node.cellValue=endSquare.cellValue
            node.b=min(node.b,endSquare.cellValue)
            printToFile(val.row,val.col,curDepth+1,val.cellValue,val.a,val.b,bo)
            if(node.a>=node.b):
               node.b=prev
               return node
      return nodeLarge
   
def nextStateAB(squareList,depth,myValue,opponentValue,player,opponent,fo):
   value=-9999
   nodeLargest=None
   bo = open("traverse_log.txt", "a")
   bo.write("Node,Depth,Value,Alpha,Beta")
   bo.write("\n")
   string="root,0,-Infinity,-Infinity,Infinity"
   bo.write(string)
   bo.write("\n")
   alpha=-9999
   beta=9999
   for val in squareList:
      if val.explored==False:
         val.explored=True
         val.cellValue=9999
         square=nextStateMaxAB(squareList,val,1,depth,myValue,opponentValue,player,opponent,alpha,beta,bo)
         val.explored=False
         if square.explored=="None":
            return val
         retValue=square.cellValue
         if square.cellValue>value:
            nodeLargest=copy.deepcopy(val)
            value=square.cellValue
         alpha=max(alpha,retValue)
         nodeLargest.a=alpha
         printToFile(val.row,val.col,1,val.cellValue,val.a,val.b,bo)
         string="root,0,"+str(nodeLargest.cellValue)+","+str(alpha)+",Infinity"
         bo.write(string)
         bo.write("\n")
         if alpha>=beta:
            return nodeLargest         
   return nodeLargest   
      
         
def nextState(result):
    algo=result[0].strip()
    player=result[1].strip()
    depth=int(result[2].strip())
    count=0
    myValue=0
    opponentValue=0
    squareList=[]
    fo = open("next_state.txt", "a")
    #construct the 2D array for the values present in each box
    for i in range(3,8):
        values[count]=[int(i) for i in result[i].split()]
        count=count+1
    count=0
    for i in range(8,13):
        currentState[count]=list(result[i].strip())
        count=count+1    
    if player=='X':
        opponent='O'
    else:
        opponent='X'
    for i in range(0,5):
        for j in range(0,5):
            if(currentState[i][j] in ['O','X']):
                if currentState[i][j]==player:
                    myValue=myValue+values[i][j]
                elif currentState[i][j]==opponent:
                    opponentValue=opponentValue+values[i][j]
                square=Square(True,i,j)
                squareList.append(square)
            else:
                square=Square(False,i,j)
                squareList.append(square)
    if algo=='1':
       square=nextStateGBFS(squareList,player,opponentValue,myValue,fo)
       square.explored='True'
    if algo=='2':
       square=nextStateMinMax(squareList,depth,myValue,opponentValue,player,opponent,fo)
       square.explored='True'
    if algo=='3':
       square=nextStateAB(squareList,depth,myValue,opponentValue,player,opponent,fo)
       square.explored='True'
    currentState[square.row][square.col]=player
    if(checkRaidValidity(square.row,square.col,player)):
       upDateCurrentState(square.row,square.col,player)
    for i in range(0,5):
       for j in range(0,5):
          fo.write(currentState[i][j]);
       fo.write("\n")
       

def checkIfContinue(squareList):
   for val in squareList:
        if(not val.explored):
           return True
   return False

def updatValuePlay(row,col,player,fo):
   currentState[row][col]=player
   if(checkRaidValidity(row,col,player)):
      upDateCurrentState(row,col,player)
   for i in range(0,5):
      for j in range(0,5):
         fo.write(currentState[i][j]);
      fo.write("\n")

def getPlayerValue(player):
   sums=0
   for i in range(0,5):
      for j in range (0,5):
         if currentState[i][j]==player:
            sums=sums+values[i][j]
   return sums

def updateSquareList(row,col,squareList):
   for val in squareList:
      if val.row==row and val.col==col:
         val.explored=True
         return   
  
def playGame(result):
   player1=result[1].strip()
   algo1=result[2].strip()
   depth1=int(result[3].strip())
   player2=result[4].strip()
   algo2=result[5].strip()
   depth2=int(result[6].strip())
   value1=0 #stores the total number of points collected by first player
   value2=0 #stores the total number of points collected by second player
   squareList=[]
   count=0
   fo = open("trace_state.txt", "w")
   Ro = open("traacckin_log.txt", "w") 
   for i in range(7,12):
        values[count]=[int(i) for i in result[i].split()]
        count=count+1
   count=0
   for i in range(12,17):
        currentState[count]=list(result[i].strip())
        count=count+1
   for i in range(0,5):
        for j in range(0,5):
            if(currentState[i][j] in ['O','X']):
                if currentState[i][j]==player1:
                    value1=value1+values[i][j]
                elif currentState[i][j]==player2:
                    value2=value2+values[i][j]
                square=Square(True,i,j)
                squareList.append(square)
            else:
                square=Square(False,i,j)
                squareList.append(square)
   #check if there are any square left unexplored. Until no square is left unexplored go on playing the game
   turn=1
   while(checkIfContinue(squareList)):
      value1=getPlayerValue(player1)
      value2=getPlayerValue(player2)
      if(turn%2!=0): # player 1 turn
         if algo1=='1':
            square=nextStateGBFS(squareList,player1,value2,value1,fo)
            updatValuePlay(square.row,square.col,player1,fo)
            updateSquareList(square.row,square.col,squareList)                                                         
         if algo1=='2':
            square=nextStateMinMax(squareList,depth1,value1,value2,player1,player2,fo)
            square.explored=True
            updatValuePlay(square.row,square.col,player1,fo)
            updateSquareList(square.row,square.col,squareList)
         if algo1=='3':
            square=nextStateAB(squareList,depth1,value1,value2,player1,player2,fo)
            square.explored=True
            updatValuePlay(square.row,square.col,player1,fo)
            updateSquareList(square.row,square.col,squareList)
      else:
         if algo2=='1':
            square=nextStateGBFS(squareList,player2,value1,value2,fo)
            square.explored=True
            updatValuePlay(square.row,square.col,player2,fo)
            updateSquareList(square.row,square.col,squareList)
         if algo2=='2':
            square=nextStateMinMax(squareList,depth2,value2,value1,player2,player1,fo)
            square.explored=True
            updatValuePlay(square.row,square.col,player2,fo)
            updateSquareList(square.row,square.col,squareList)
         if algo2=='3':
            square=nextStateAB(squareList,depth2,value2,value1,player2,player1,fo)
            square.explored=True
            updatValuePlay(square.row,square.col,player2,fo)
            updateSquareList(square.row,square.col,squareList)
      turn=turn+1
      for val in squareList:
         val.cellValue=0
               
      
   
def main(fname):
    result=[]
    with open(fname) as f:
        for line in f:
            result.append(line)
    algo=result[0].strip()
    if algo in ['1','2','3']:
       nextState(result)
    else:
       playGame(result)    

main(sys.argv[2])

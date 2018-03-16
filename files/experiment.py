from __future__ import print_function
import sys
import time
import json
import random
import math
from operator import itemgetter
import os
from twisted.internet import reactor
from twisted.internet import task
import pickle


class fakeClient():
   def __init__(self,sid):
      self.peer="1.1.1.1"
      self.subjectID=sid

class experimentClass():
   def __init__(self):
      "do init stuff"
      self.setParameters()
      self.data['matchType']="regular"
      self.monitorTaskList=['startExperiment','startHypothetical']
   # - store data in self.data[subjectID] which is a Subject object (defined below)
   # - send messages like self.customMessage(subjectID,msg)
   # - list of all subjects at self.data['subjectIDs']
  

   def setParameters(self):

      self.nonPickleData={}
      print("setPreliminaries")
      self.data['stopTick']=0
      self.data['elapsed']=0
      #currentTime,startTime,totalTime,jsTime
      self.data['timer']=[0,0,0,0]
      self.data['payoffs']=[[0,0],[0,0],[0,0],[0,0]]
      self.data['choices']=["1","2"]
      self.data['instructionsRunning']=0
      self.data['videoRunning']=0
      self.data['defaultOnlyMatches']=-10
      self.data['ruleLockFixedCost']=250
      self.data['ruleLockMarginalCost']=0
      self.data['currentMatch']=-1
      self.data['matchStartTime']=0

      self.data['totalMatches']=5
      self.data['exchangeRate']=float(1)/1250
      self.data['showPayoffTime']=60
      self.data['hypotheticalPeriodLength']=600

      self.data['preStageLengths']=[60,60,120,120,120,120,120,120,120,120,120]
      self.data['freeStageLengths']=[20,22, 6, 6, 45, 16, 3, 24, 18, 12, 48]

      #testing
      self.data['showPayoffTime']=6
      self.data['hypotheticalPeriodLength']=3600
      self.data['totalMatches']=10#not including practice
      self.data['preStageLengths']=[20,5,60,60,60,60,60,60,60,60,60,60]
      self.data['freeStageLengths']=[30]+[46, 36, 52, 85, 60, 7, 68, 41, 44, 42]


      # #testing
      # self.data['showPayoffTime']=1
      # self.data['hypotheticalPeriodLength']=1
      # self.data['totalMatches']=10#not including practice
      # self.data['preStageLengths']=[20,10,60,60,60,60,60,60,60,60,60,60]
      # self.data['freeStageLengths']=[30]+[46, 36, 52, 85, 60, 7, 68, 41, 44, 42]


      #testing
      # self.data['showPayoffTime']=3
      # self.data['preStageLengths']=[10,20,20,20,20,20,20,20,20,10,10,10,10,10,10,10]
      # self.data['freeStageLengths']=[15,15,15,15,15,15,15,15, 70, 177, 132, 320, 15, 63, 135, 106]
      # self.data['lockStageLengths']=[2,11, 76, 0, 106, 0, 443, 0, 29, 161, 129, 269, 0, 47, 102, 0] 
      # self.data['postStageLengths']=[2,10,10,10,10,10,10,5,5,5,5,5,5,5,5,5]
      # self.data['totalMatches']=60
      # self.data['preStageLengths']=[60, 120, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10,10]
      # self.data['freeStageLengths']=[60,2, 6, 5, 10, 16, 9, 13, 5, 2, 12, 1, 3, 5, 1, 9, 12, 1, 7, 2, 2, 3, 2, 2, 3, 6, 4, 1, 3, 4, 4, 13, 2, 3, 1, 5, 11, 3, 2, 5, 2, 5, 3, 10, 4, 6, 3, 6, 1, 2, 9, 5, 1, 7, 4, 7, 4, 5, 2, 3, 4]
      # self.data['lockStageLengths']=[60,0, 7, 0, 2, 0, 8, 0, 12, 0, 9, 0, 0, 6, 0, 0, 5, 0, 0, 0, 14, 18, 29, 0, 0, 0, 0, 10, 0, 0, 32, 0, 8, 2, 15, 0, 15, 31, 0, 0, 0, 1, 0, 0, 0, 7, 0, 4, 3, 0, 11, 0, 4, 0, 0, 3, 0, 0, 0, 0, 0]
      # self.data['postStageLengths']=[10,10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10]

      filename=self.config['webServerRoot']+self.config['currentExperiment']+'files/quiz.pickle'
      file = open(filename,'rb')
      self.data['quizQuestions']=pickle.load(file)
      file.close() 

   def reversePays(self,p):
      paysOut=[[p[0][1],p[0][0]],[p[2][1],p[2][0]],[p[1][1],p[1][0]],[p[3][1],p[3][0]]]
      return paysOut

   def endTrial(self,message,client):
      self.taskDone(message)
      for sid in self.data['subjectIDs']:
         self.data[sid].lastRule=-1
         self.data[sid].lockCosts=0
         self.data[sid].resetAllRules()
         self.data[sid].status={"page":"generic","message":["Next there will be a quiz.<br>  You will get $10 if you answer all questions correctly.<br> You will earn $0 if you answer one question incorrectly."],"stage":"initializing"}
         #self.data[sid].status[0]=0
         self.updateStatus(sid)


   def setPairs(self,theseSubjects):
      random.shuffle(theseSubjects)
      for k in range(len(theseSubjects)/2):
         sub1=theseSubjects[2*k+0]
         sub2=theseSubjects[2*k+1]

         self.data[sub1].partners[self.data['currentMatch']]=sub2
         self.data[sub1].roles[self.data['currentMatch']]=0
         self.data[sub1].gameTable[self.data['currentMatch']]=self.data['payoffs']

         self.data[sub2].partners[self.data['currentMatch']]=sub1
         self.data[sub2].roles[self.data['currentMatch']]=1
         self.data[sub2].gameTable[self.data['currentMatch']]=self.reversePays(self.data['payoffs'])

   def notAcceptingClientsAnymore(self):
      self.setMatchingsByQuiz()
      print("setMatchings2 - do nothing")
   def setMatchings(self):
      print("setMatchings - do nothing")

   def setMatchingsByQuiz(self):
      goodQuiz=[]
      badQuiz=[]
      for sid in self.data['subjectIDs']:
         if self.data[sid].quizEarnings>-10:
            goodQuiz.append(sid)
         else:
            badQuiz.append(sid)

      if len(badQuiz)%2==0:#Even number of bad quiz folks
         "do nothing"
      else:
         random.shuffle(goodQuiz)
         thisSID=goodQuiz.pop()
         badQuiz.append(thisSID)

      self.data['groups']={}
      self.data['groups'][0]=goodQuiz
      self.data['groups'][1]=badQuiz


      for sid in self.data['groups'][0]:
         self.data[sid].group="high"
         self.data[sid].timePerQuestion=60
         self.data[sid].timeUntilWarning=50
      for sid in self.data['groups'][1]:
         self.data[sid].group="low"
         # self.data[sid].timePerQuestion=4
         # self.data[sid].timeUntilWarning=1
         self.data[sid].timePerQuestion=30
         self.data[sid].timeUntilWarning=10
      print("matching set!!!!!!!")


   def makeMatching(self):
      print("makeMatching")
      if self.data['matchType']=="trial":
         #trail - creat Dummy clients
         for sid in self.data['subjectIDs']:
            self.data[sid].partners[self.data['currentMatch']]='randomPlayer'
            self.data[sid].roles[self.data['currentMatch']]=0
            self.data[sid].gameTable[self.data['currentMatch']]=self.data['payoffs']
      elif self.data['matchType']=="regularDemo":
         #trail - creat Dummy clients
         for sid in self.data['subjectIDs']:
            self.data[sid].partners[self.data['currentMatch']]='randomPlayer'
      elif self.data['matchType']=="regular":
         for group in self.data['groups']:
            if len(self.data['groups'][group])>0:
               self.setPairs(self.data['groups'][group])
   

   def makeMyChoice(self,subjectID):
      history=self.getClientHistory(subjectID)
      ruleOut=self.data[subjectID].pickRule("regular",history)
      if len(history)==0:
         thisPlay=self.data[subjectID].firstPeriodRules[-1][0]
         ruleOut=Rule([[thisPlay]],-1)
      return ruleOut




   def gameOver(self):
      for sid in self.data['subjectIDs']:
         totalPay=(self.data[sid].totalPayoffs[0]-self.data[sid].lockCosts)*self.data['exchangeRate']+self.data[sid].quizEarnings
         self.data[sid].status={"page":"generic","message":["ID:"+sid,"<br>Game Pay: %.02f"%((self.data[sid].totalPayoffs[0]-self.data[sid].lockCosts)*self.data['exchangeRate']),"<br>Quiz Pay: %.02f"%(self.data[sid].quizEarnings),"<br>Total Pay: %.02f"%(totalPay)]}
         self.updateStatus(sid)




   def startPreMatch(self):
      self.data['matchStartTime']=time.time()
      self.data['currentMatch']=self.data['currentMatch']+1
      if self.data['currentMatch']>self.data['totalMatches']:
         self.gameOver()#game over
      else:
         self.initializeTimer("everyoneTimer",self.data['timer'][2],self.startMatch)
         self.makeMatching()
         for sid in self.data['subjectIDs']:
            self.sendParameters(sid)
            self.data[sid].newMatch(self.data['currentMatch'])
            if self.data['matchType']=="trial":
               self.data[sid].status={"page":"defaultNotSet","match":self.data['currentMatch']}
            else:
               self.data[sid].status={"page":"preMatch","match":self.data['currentMatch']}
            self.updateStatus(sid)
            self.updateRules(sid,"everything","regular")      



   def startMatch(self):
      allDefaultRulesSet=1
      for sid in self.data['subjectIDs']:
         if len(self.data[sid].currentRules)==0 or len(self.data[sid].firstPeriodRules)==0:
            allDefaultRulesSet=0
      if allDefaultRulesSet==0:
         print("not all default Rules Set")
         self.initializeTimer("everyoneTimer",2,self.startMatch)
      else:
         self.data['startTime']=time.time()
         for sid in self.data['subjectIDs']:
            if self.data['matchType']=="trial":
               self.data[sid].status={"page":"game","confirmed":"no","locked":"yes","match":self.data['currentMatch']}
            else:
               self.data[sid].status={"page":"game","confirmed":"no","locked":"yes","match":self.data['currentMatch']}
            self.data[sid].matchRunning=1
            self.initializePeriodTimer(sid)
            self.updateStatus(sid)
            self.sendChoices(sid,'regular')
            #self.data[sid].freeLock=1
            #self.unlockRules({},self.clientsById[sid])
            #self.sendChoices(sid,'regular')

         #print "start Play Tick"
         #self.tick()


   def initializePeriodTimer(self,sid):
      warningTime=self.data[sid].timeUntilWarning
      self.initializeTimer(sid,warningTime,self.showWarning,sid)
      self.data[sid].status['warning']="no"
      self.updateStatus(sid)

   def showWarning(self,sid):
      remainingTime=self.data[sid].timePerQuestion-self.data[sid].timeUntilWarning
      self.initializeTimer(sid,remainingTime,self.confirmChoiceFromPython,sid)
      self.data[sid].status['warning']="yes"
      self.updateStatus(sid)
      self.sendChoices(sid,'regular')



   def getClientHistory(self,subjectID):
      myHistory=self.data[subjectID].history[self.data['currentMatch']]
      theirHistory=self.data[subjectID].opponentHistory[self.data['currentMatch']]
      history=[]
      for a,b in zip(myHistory,theirHistory):
         history.append([a,b])
      return history
   
   def getClientPayoffHistory(self,subjectID):
      myHistory=self.data[subjectID].history[self.data['currentMatch']]
      theirHistory=self.data[subjectID].opponentHistory[self.data['currentMatch']]
      history=[]
      for a,b in zip(myHistory,theirHistory):
         index=2*a+b
         thisPayoff=self.data[subjectID].gameTable[self.data['currentMatch']][index]
         history.append(thisPayoff)
      return history

   def confirmedMatchOver(self,message,client):
      print("confirmed Match Over")
      subjectID=client.subjectID
      self.data[subjectID].matchRunning=0
      moveToNextMatch=1
      for sid in self.data['subjectIDs']:
         if self.data[sid].matchRunning==1:
            moveToNextMatch=0
      if moveToNextMatch==1:
         if self.data['matchType']=="trial":
            msg={}
            msg['type']='endTrial'
            msg['title']='End Trial'
            msg['status']=''
            taskList.append(msg)
            self.endTrial(message,client)
         else:
            self.startPreMatch()



   def confirmChoiceFromPython(self,sid):
      thisClient=fakeClient(sid)
      self.confirmChoice({},thisClient)

   def confirmChoice(self,message,client):
      #print "Confi Choice",client.subjectID
      subjectID=client.subjectID
      if self.data[subjectID].status['locked']=="no":
         self.data[subjectID].status['animate']="no";
         self.data[subjectID].status['locked']="yes";
         self.lockRules(message,client)
      self.data[subjectID].status['warning']="no"
      self.cancelTimerFunction(subjectID)


      self.data[subjectID].currentPeriod=len(self.data[subjectID].history[self.data['currentMatch']])
      if self.data[subjectID].currentPeriod==0:
         #use first period rule
         self.data[subjectID].history[self.data['currentMatch']].append(self.data[subjectID].firstPeriodRules[-1][0])
         self.data[subjectID].lastRule=-1
         self.data[subjectID].lastRuleLength=0
      else:
         #use other rule
         myRule=self.makeMyChoice(subjectID)
         myRule.ruleUsed(self.data['currentMatch'],self.data[subjectID].currentPeriod)
         self.data[subjectID].history[self.data['currentMatch']].append(myRule.output)
         self.data[subjectID].lastRule=myRule.number
         self.data[subjectID].lastRuleLength=myRule.length
         self.data[subjectID].currentPeriod=len(self.data[subjectID].history[self.data['currentMatch']])
      self.data[subjectID].status["confirmed"]="yes"
      self.updateStatus(subjectID)
      self.checkPartner(subjectID)
      self.sendChoices(subjectID,'regular')


   def checkPartner(self,subjectID):
      myPartner=self.data[subjectID].partners[self.data['currentMatch']]
      if myPartner=="randomPlayer":
         self.finishPeriod(subjectID)
      else:
         myHistory=self.data[subjectID].history[self.data['currentMatch']]
         thierHistory=self.data[myPartner].history[self.data['currentMatch']]
         if len(myHistory)==len(thierHistory):
            self.finishPeriod(subjectID)
            self.finishPeriod(myPartner)
         else:
            "sdf"
            #send message to confirm that you are waiting now.

   def finishPeriod(self,subjectID):
      #Get opponents choices and payoffs
      myPartner=self.data[subjectID].partners[self.data['currentMatch']]
      myChoice=self.data[subjectID].history[self.data['currentMatch']][-1]
      if myPartner=="randomPlayer":
         theirChoice=random.choice([0,1])
      else:
         theirChoice=self.data[myPartner].history[self.data['currentMatch']][-1]
      self.data[subjectID].opponentHistory[self.data['currentMatch']].append(theirChoice)
      index=2*myChoice+theirChoice
      thisPayoff=self.data[subjectID].gameTable[self.data['currentMatch']][index]
      print("Finish PEriod Choice %s,%s,%s,%s"%(subjectID,self.data[subjectID].currentPeriod,[myChoice,theirChoice],thisPayoff))
      if self.data['matchType']=="regular" or self.data['matchType']=="regularDemo":
         self.data[subjectID].matchPayoffs[self.data['currentMatch']]=[x+y for x,y in zip(self.data[subjectID].matchPayoffs[self.data['currentMatch']],thisPayoff)]
         self.data[subjectID].totalPayoffs=[x+y for x,y in zip(self.data[subjectID].totalPayoffs,thisPayoff)]
      self.data[subjectID].actionProfileFrequencies[self.data['currentMatch']][index]=self.data[subjectID].actionProfileFrequencies[self.data['currentMatch']][index]+1
      self.data[subjectID].lastPlay=index

      #print "HERE",self.data[subjectID].currentPeriod,self.data['freeStageLengths'][self.data['currentMatch']]
      if self.data[subjectID].currentPeriod<self.data['freeStageLengths'][self.data['currentMatch']]:
         #start next period
         self.data[subjectID].status["confirmed"]="no"
         self.data[subjectID].status["animate"]="no"
         self.sendChoices(subjectID,'regular')
         #MOVE FORWARD HERE
         self.initializePeriodTimer(subjectID)
         #self.data[subjectID].status["locked"]="yes"
         self.updateStatus(subjectID)
         self.sendChoices(subjectID,'regular')
      else:
         #end of match
         # if len(self.data[subjectID].lockPeriods)>0:
         #    if self.data[sid].lockPeriods[-1][1]==-1:
         #       self.lockRules("",self.clientsById[sid])
         self.data[subjectID].status["page"]="postMatch"
         self.updateStatus(subjectID)
         self.sendChoices(subjectID,'regular')
      self.monitorMessage()

   def sendWarning(self,subjectID):
      msg={}
      msg['type']="warningMessage"
      msg['waitingTime']=1000*(self.data[subjectID].timePerQuestion-self.data[subjectID].timeUntilWarning)
      self.customMessage(subjectID,msg)
      self.updateStatus(subjectID)
      self.sendChoices(subjectID,'regular')

   def sendChoices(self,sid,sendType):     
      msg={}
      msg['type']="newHistory"
      thisHistory=self.getClientHistory(sid)
      thisPayoffHistory=self.getClientPayoffHistory(sid)
      msg['history']=thisHistory[-25:]
      msg['payoffHistory']=thisPayoffHistory[-25:]
      myRule=self.makeMyChoice(sid)
      msg['nextPeriodPlay']=myRule.output
      msg['period']=len(thisHistory)
      msg['lastPlay']=self.data[sid].lastPlay
      msg['matchPayoff']=self.data[sid].matchPayoffs[self.data['currentMatch']]
      msg['unlockCosts']=self.data[sid].lockCosts
      msg['totalPayoff']=self.data[sid].totalPayoffs[0]
      msg['lockCosts']=self.data[sid].lockCosts
      msg['elapsed']=self.data['elapsed']
      msg['actionProfileFrequencies']=self.data[sid].actionProfileFrequencies[self.data['currentMatch']]
      msg['lastRule']=self.data[sid].lastRule
      msg['lastRuleLength']=self.data[sid].lastRuleLength
      self.customMessage(sid,msg)
      self.updateRules(sid,"onlyStats","regular")



   def startTrial(self,message,client):
      self.data['monitorTasks'][message['index']]['status']='Done'
      self.monitorMessage()
      self.data['matchType']="trial"
      self.data['choices']=["W","Y"]
      self.data['payoffs']=[[0,0],[0,0],[0,0],[0,0]]
      #self.preMatch()
      self.startPreMatch()

   def startExperiment(self,message,client):
      self.taskDone(message)
      self.data['currentMatch']=0
      self.data['matchType']="regular"
      self.data['choices']=["W","Y"]
      self.data['payoffs']=[[3,3],[1,5],[4,1],[2,2]]
      self.data['payoffs']=[[1,5],[2,6],[3,7],[4,8]]
      self.data['payoffs']=[[48,48],[12,50],[50,12],[25,25]]
      self.data['payoffs']=[[38,38],[12,50],[50,12],[25,25]]
      # self.showPayoffs()
      reactor.callLater(.1,self.tester)

   def tester(self):
      msg={}
      for sid in self.data['subjectIDs']:
         self.data[sid].status={"page":"defaultNotSet","match":1}
         self.updateStatus(sid)
      for sid in self.data['subjectIDs']:
         thisClient=self.clientsById[sid]
         msg['thisRule']=['firstPeriod',0]
         self.setRulesBeginning(msg,thisClient)
         msg['thisRule']=['default',0]
         self.setRulesBeginning(msg,thisClient)
         #self.setFirstPeriod(msg,thisClient)
      reactor.callLater(.2,self.startPreMatch)


   def addHypHistory(self,message,client):
      message={}
      message['number']=len(self.data[client.subjectID].hypHistories)+1
      self.data[client.subjectID].hypHistories[message['number']]=[[-1,-1] for x in range(17)]
      self.getHypHistory(message,client)

   def getHypHistory(self,message,client):
      subjectID=client.subjectID
      msg={}
      msg['type']="hypHistory"
      thisNumber=message['number']
      if thisNumber==-1:
         thisNumber=1
      #self.data[subjectID].currentHypotheticalHistoryNumber=thisNumber

      if len(self.data[subjectID].hypHistories)==0:
         self.data[subjectID].hypHistories[1]=[[-1,-1] for x in range(17)]
         thisNumber=1

      msg['hypHistory']=self.data[subjectID].hypHistories[thisNumber]
      msg['totalHypHistories']=len(self.data[subjectID].hypHistories)
      msg['hypHistoryNumber']=thisNumber
      hypHistoryComplete=1
      for k in range(15):
         if self.data[subjectID].hypHistories[thisNumber][k][0]==-1:
            hypHistoryComplete=0
            break
         if self.data[subjectID].hypHistories[thisNumber][k][1]==-1:
            hypHistoryComplete=0
            break
      msg['hypHistoryComplete']=hypHistoryComplete
      self.customMessage(subjectID,msg)
      self.makeHypotheticalChoice(thisNumber,subjectID)

   def hypotheticalHistory(self,message,client):
      subjectID=client.subjectID
      historyNumber=message['historyNumber']
      history=message['history']
      self.data[subjectID].hypHistories[historyNumber]=history
      self.makeHypotheticalChoice(historyNumber,subjectID)

   def makeHypotheticalChoice(self,historyNumber,subjectID):

      msg={}
      msg['type']="hypotheticalChoice"
      history=self.data[subjectID].hypHistories[historyNumber]

      longestHypRule=max([x.length for x in self.data[subjectID].currentHypRules])
      complete=1
      for k in range(15-longestHypRule+1,15):
         if history[k][0]==-1 or history[k][1]==-1:
            complete=0
            break
      if complete>-1:
         hypRuleOut=self.data[subjectID].pickRule("hyp",history[0:15])
         msg['hypRuleNumber']=hypRuleOut.number
         msg['hypRuleOutput']=hypRuleOut.output
         msg['hypRuleLength']=hypRuleOut.length


      longestRegRule=max([x.length for x in self.data[subjectID].currentRules])
      for k in range(15-longestRegRule+1,15):
         if history[k][0]==-1 or history[k][1]==-1:
            complete=0
            break
      if complete>-1:
         regularRuleOut=self.data[subjectID].pickRule("regular",history[0:15])
         msg['regularRuleNumber']=regularRuleOut.number
         msg['regularRuleOutput']=regularRuleOut.output
         msg['regularRuleLength']=regularRuleOut.length
      
      if len(msg)>2:
         msg['hypHistories']=self.data[subjectID].hypHistories
         self.customMessage(subjectID,msg)



   def showPayoffs(self):
      self.initializeTimer("everyoneTimer",self.data['showPayoffTime'],self.showHypothetical)
      for sid in self.data['subjectIDs']:
         self.sendParameters(sid)
         self.data[sid].status={"page":"payoffsOnly"}
         self.updateStatus(sid)

   def startHypothetical(self,message,client):
      self.showHypothetical()

   def showHypothetical(self):
      self.initializeTimer("everyoneTimer",self.data['hypotheticalPeriodLength'],self.startPreMatch)
      for sid in self.data['subjectIDs']:
         self.data[sid].status={"page":"defaultNotSet","match":1}
         self.updateStatus(sid)


   def unlockRules(self,message,client):
      sid=client.subjectID
      self.data[sid].status['locked']="no";
      self.data[sid].status['animate']="no";
      self.data[sid].lockPeriods.append([time.time(),-1,self.data['currentMatch']])
      if self.data[sid].freeLock==0:
         if self.data['matchType']=="trial":
            self.data[sid].lockCosts=self.data[sid].lockCosts+0
         else:
            self.data[sid].lockCosts=self.data[sid].lockCosts+self.data['ruleLockFixedCost']
         self.data[sid].status['animate']="yes";
      self.data[sid].freeLock=0
      self.sendChoices(sid,'regular')
      self.updateStatus(sid)
      self.sendChoices(sid,'regular')
      self.data[sid].status['animate']="no";

   def lockRules(self,message,client):
      sid=client.subjectID
      self.data[sid].lockPeriods[-1][1]=time.time()
      unlockedSeconds=self.data[sid].lockPeriods[-1][1]-self.data[sid].lockPeriods[-1][0]
      self.sendChoices(sid,'regular')
      self.data[sid].status['locked']="yes";
      self.updateStatus(sid)
      self.sendChoices(sid,'regular')



   def startNewGame(self,message,client):
      #unregister all clients
      self.setPreliminaries()

   def sendParameters(self,subjectID):
      msg={}
      msg['type']="parameters"
      msg['ruleLockFixedCost']=self.data['ruleLockFixedCost']
      msg['ruleLockMarginalCost']=self.data['ruleLockMarginalCost']
      this=self.data['payoffs']
      if self.data['currentMatch'] in self.data[subjectID].roles:
         if self.data[subjectID].roles[self.data['currentMatch']]==1:
            this=self.reversePays(this)
      msg['payoffs']=this
      msg['choices']=self.data['choices']
      self.customMessage(subjectID,msg)


   def reconnectServer(self):
      if self.data['serverPage']=="quiz":
         startQuiz(self,"message","client",restart=1)

   def finishQuiz(self,message,client):
      self.taskDone(message)
      self.setMatchingsByQuiz()
      for sid in self.data['subjectIDs']:
         if self.data[sid].group=="high":
            self.data[sid].status={"page":"generic","message":["There are %s participants in your group (including yourself).<br> Everyone in your group earned $10.00 on the quiz."%(len(self.data['groups'][0]))]}
         else:
            self.data[sid].status={"page":"generic","message":["There are %s participants in your group (including yourself)."%(len(self.data['groups'][1]))]}
         self.updateStatus(sid)



   def startQuizOLD(self,message,client):
      self.data['serverPage']="quiz"
      self.taskDone(message)
      for sid in self.data['subjectIDs']:
         self.data[sid].resetAllRules()
      self.data['quizStartTime']=time.time()
      self.data['payoffs']=[[8,7],[6,5],[4,3],[2,1]]
      self.data['choices']=["W","Y"]
      for sid in self.data['subjectIDs']:
         self.sendParameters(sid)
         #[quizNow,QuestionNumber,0 question and 1 solution,tryNumber]
         # if restart==0:
         self.data[sid].status={"page":"quiz","questionNumber":1,"stage":"question","tries":0}
         self.sendQuizQuestion(sid)


   def checkAnswer(self,thisProb,thisProbType,thisAnswer):
      out="incorrect"
      if thisProbType!=3:#Action
         if thisAnswer==self.data['quizQuestions']['questions'][thisProb-1]['answer']:
            out="correct"
      elif thisProbType==3:#Add
         messageIndex=thisProb-1
         thisMessage=self.data['quizQuestions']['questions'][messageIndex]
         if thisAnswer in self.data['quizQuestions']['questions'][thisProb-1]['answer']:
            out="correct"
      return out

   def nextQuestion(self,message,client):
      subjectID=client.subjectID
      currentQuestion=self.data[subjectID].status['questionNumber']+1
      if currentQuestion>10:#10:#Number of quiz problems
         if self.data[subjectID].quizEarnings>0:
            self.data[subjectID].quizEarnings=10
         self.data[subjectID].status={"page":"quizSummary","summary":"$%.02f"%(self.data[subjectID].quizEarnings)}
         self.updateStatus(subjectID)
      else:
         self.data[subjectID].status={"page":"quiz","questionNumber":currentQuestion,"stage":"question","tries":0}
         self.sendQuizQuestion(subjectID)
   def tryAgain(self,message,client):
      subjectID=client.subjectID
      self.data[subjectID].status["stage"]="question"
      self.data[subjectID].status["tries"]=self.data[subjectID].status["tries"]+1
      self.sendQuizQuestion(subjectID)


   def getQuizProblem(self,message,client):
      subjectID=client.subjectID
      self.sendQuizQuestion(subjectID)


   def sendQuizQuestion(self,subjectID):
      self.monitorMessage()
      msg=self.data['quizQuestions']['questions'][self.data[subjectID].status['questionNumber']-1]
      msg['tries']=self.data[subjectID].status['tries']+1
      if self.data[subjectID].status['tries']==0:
         msg['price']="$0.50"
      elif self.data[subjectID].status['tries']==1:
         msg['price']="$0.25"
      else:
         msg['price']="$0.00"
      msg['quizEarnings']="$%.02f"%(self.data[subjectID].quizEarnings)
      self.customMessage(subjectID,msg)


   def quizAnswer(self,message,client):
      subjectID=client.subjectID
      thisProb=self.data[subjectID].status['questionNumber']
      thisProbType=message['questionType']
      thisAnswer=message['answer']
      if thisProb not in self.data[subjectID].quizAnswers:
         self.data[subjectID].quizAnswers[thisProb]=[]
      self.data[subjectID].quizAnswers[thisProb].append([time.time()-self.data['quizStartTime'],thisAnswer])
      answer=self.checkAnswer(thisProb,thisProbType,thisAnswer)
      if answer=="correct":
         if self.data[subjectID].status['tries']==0:
            price=.5
         elif self.data[subjectID].status['tries']==1:
            price=.25
         else:
            price=0
         self.data[subjectID].quizEarnings=self.data[subjectID].quizEarnings+price
         self.data[subjectID].status["stage"]="correct"
      elif answer=="incorrect":
         self.data[subjectID].status["stage"]="incorrect"
      self.getAnswerText(subjectID)

   def getAnswerText(self,subjectID):
      msg={}
      msg['type']='answerSolution'
      msg['quizEarnings']="$%.02f"%(self.data[subjectID].quizEarnings)
      if self.data[subjectID].status["stage"]=="correct":
         msg['solution']="correct"
         msg['solutionText']="The answer is correct."
         msg['buttonText']="Next Question."
         self.customMessage(subjectID,msg)
      elif self.data[subjectID].status["stage"]=="incorrect":
         self.data[subjectID].quizEarnings=0
         self.data[subjectID].status={"page":"generic","message":["That answer was incorrect. <br> Your earnings on the quiz are $0.00.<br> Please wait for other subjects to finish quiz."]}
         self.updateStatus(subjectID)


   def reconnectingClient(self,client):
      sid=client.subjectID
      self.sendParameters(sid)
      msg={}
      msg['type']='reconnecting'
      msg['currentUnlockedTime']=0
      if len(self.data[sid].lockPeriods)>0:
         if self.data[sid].lockPeriods[-1][1]==-1:
            msg['currentUnlockedTime']=time.time()-self.data[sid].lockPeriods[-1][0]
      self.customMessage(sid,msg)

      if self.data[sid].status["page"] in ["game","postMatch"]:
         self.sendChoices(sid,'regular')
         self.updateRules(sid,"everything","regular")
      elif self.data[sid].status["page"]=="hypothetical":
         self.updateRules(sid,"everything","hyp")
         self.updateRules(sid,"everything","regular")
      elif self.data[sid].status["page"]=="quiz":
         self.sendQuizQuestion(sid)
         if self.data[sid].status["stage"] in ["correct","incorrect"]:
            self.getAnswerText(sid)


      if self.data['videoRunning']==1:
         self.reconnectVideo(client)
      if self.data['instructionsRunning']==1:
         self.reconnectInstructions(client)

   def checkForDefaultAndFirstPeriod(self,subjectID):
      if len(self.data[subjectID].firstPeriodRules)>0 and len(self.data[subjectID].currentRules)>0:
         return True
      else:
         return False

   def updateRules(self,subjectID,updateType,ruleType):
      #print "updating rules "+ruleType

      allRules=self.data[subjectID].allRules
      msg={}
      msg['type']='updateRules'
      msg['ruleType']=ruleType
      msg['updateType']=updateType
      if ruleType=="regular":
         msg['currentRules']=[x.rule for x in self.data[subjectID].currentRules]
         msg['currentRuleNumbers']=[x.number for x in self.data[subjectID].currentRules]
         msg['lastUsed']=[x.lastUsed[self.data['currentMatch']] if self.data['currentMatch'] in x.lastUsed else -1 for x in self.data[subjectID].currentRules]
         msg['ruleFrequency']=[x.frequency[self.data['currentMatch']] if self.data['currentMatch'] in x.frequency else 0 for x in self.data[subjectID].currentRules]
         if len(self.data[subjectID].firstPeriodRules)>0:
            firstPeriod=self.data[subjectID].firstPeriodRules[-1][0]
         else:
            firstPeriod=-1
         msg['firstPeriodRule']=firstPeriod
      elif ruleType=="hyp":
         msg['currentRules']=[x.rule for x in self.data[subjectID].currentHypRules]
         msg['currentRuleNumbers']=[x.number for x in self.data[subjectID].currentHypRules]
         msg['lastUsed']=[x.lastUsed[self.data['currentMatch']] if self.data['currentMatch'] in x.lastUsed else -1 for x in self.data[subjectID].currentHypRules]
         msg['ruleFrequency']=[x.frequency[self.data['currentMatch']] if self.data['currentMatch'] in x.frequency else 0 for x in self.data[subjectID].currentHypRules]
         if len(self.data[subjectID].firstPeriodRulesHyp)>0:
            firstPeriod=self.data[subjectID].firstPeriodRulesHyp[-1][0]
         else:
            firstPeriod=-1
         msg['firstPeriodRule']=firstPeriod
      msg['lastRuleNumber']=self.data[subjectID].lastRule
      if self.data[subjectID].lastRule==-1:
         msg['lastRuleLastUsed']=0
         msg['lastRuleFrequency']=0
      else:
         msg['lastRuleLastUsed']=self.data[subjectID].allRules[self.data[subjectID].lastRule].lastUsed[self.data['currentMatch']]
         msg['lastRuleFrequency']=self.data[subjectID].allRules[self.data[subjectID].lastRule].frequency[self.data['currentMatch']]

      if len(self.data[subjectID].currentRules)==0 or self.data[subjectID].status['page']=="hypothetical":
         msg['nextPeriodPlay']=0
         msg['nextPeriodRule']=0
         msg['nextPeriodRuleLength']=0
      else:
         myRule=self.makeMyChoice(subjectID)
         msg['nextPeriodPlay']=myRule.output
         msg['nextPeriodRule']=myRule.number
         msg['nextPeriodRuleLength']=myRule.length
         if 'confirmed' in self.data[subjectID].status:
            if self.data[subjectID].status['confirmed']=="yes":
               #print "CONFIRMED"
               msg['nextPeriodPlay']=self.data[subjectID].history[self.data['currentMatch']][-1]
               msg['nextPeriodRule']=self.data[subjectID].lastRule
               msg['nextPeriodRuleLength']=self.data[subjectID].lastRuleLength

      self.customMessage(subjectID,msg)

   def findRuleClassByList(self,ruleIN,subjectID):
      out=-1
      for r in self.data[subjectID].allRules:
         if r.rule==ruleIN:
            out=r
         break
      return out

   def switchRuleOutput(self,message,client):
      subjectID=client.subjectID
      newRuleList=message['thisRule']
      rulesType=message['rulesType']
      self.data[subjectID].switchRules(newRuleList,self.data['currentMatch'],time.time()-self.data['matchStartTime'],rulesType)
      self.updateRules(subjectID,"everything",rulesType)

   def addRule(self,message,client):
      subjectID=client.subjectID
      thisRule=message['thisRule']
      rulesType=message['rulesType']
      self.data[subjectID].addRule(thisRule,self.data['currentMatch'],time.time()-self.data['matchStartTime'],rulesType)
      self.updateRules(subjectID,"everything",rulesType)

   def setRulesBeginning(self,message,client):
      sid=client.subjectID
      ruleType=message['thisRule'][0]
      thisRule=message['thisRule'][1]
      if ruleType=="firstPeriod":
         for rulesType in ["hyp","regular"]:
            self.data[sid].setFirstPeriodRule(thisRule,self.data['currentMatch'],time.time()-self.data['matchStartTime'],rulesType)
      elif ruleType=="default":
         for rulesType in ["hyp","regular"]:
            self.data[sid].setDefaultRule(thisRule,self.data['currentMatch'],time.time()-self.data['matchStartTime'],rulesType)

      if self.checkForDefaultAndFirstPeriod(sid):
         if self.data['matchType']=="trial":
            self.data[sid].status={"page":"preMatch","match":self.data['currentMatch']}
            self.updateRules(sid,"everything","regular")
         else:
            self.data[sid].status["page"]="hypothetical"
            self.updateRules(sid,"everything","hyp")
            self.updateRules(sid,"everything","regular")
         self.updateStatus(sid)
      else:
         msg={}
         msg['type']="beginRules"
         msg['defaultRule']=-1  
         msg['firstPeriodRule']=-1
         if len(self.data[sid].firstPeriodRules)>0:
            msg['firstPeriodRule']=self.data[sid].firstPeriodRules[-1][0]
         if len(self.data[sid].currentRules)>0:
            msg['defaultRule']=self.data[sid].currentRules[-1].rule[0][0]
         self.customMessage(sid,msg)


   def setDefault(self,message,client):
      subjectID=client.subjectID
      thisRule=message['thisRule']#either 0 or 1
      rulesType=message['rulesType']
      self.data[subjectID].setDefaultRule(thisRule,self.data['currentMatch'],time.time()-self.data['matchStartTime'],rulesType)
      self.updateRules(subjectID,"everything",rulesType)


   def setFirstPeriod(self,message,client):
      subjectID=client.subjectID
      thisRule=message['thisRule']#either 0 or 1
      rulesType=message['rulesType']
      self.data[subjectID].setFirstPeriodRule(thisRule,self.data['currentMatch'],time.time()-self.data['matchStartTime'],rulesType)
      self.updateRules(subjectID,"everything",rulesType)

   def deleteRule(self,message,client):
      subjectID=client.subjectID
      ruleList=message['rule']
      rulesType=message['rulesType']
      self.data[subjectID].deleteRule(ruleList,self.data['currentMatch'],time.time()-self.data['matchStartTime'],rulesType)
      self.updateRules(subjectID,"everything",rulesType)


   def experimentDemo(self,sid,viewType):
      if viewType=="firstMatch" or viewType=="regular":
         self.data['matchType']="regularDemo"
         thisClient=self.clientsById[sid]
         self.data[sid].setFirstPeriodRule(random.choice([0,1]),0,0,'regular')
         self.data[sid].setDefaultRule(random.choice([0,1]),0,0,'regular')
         self.data['currentMatch']=0
         self.data['payoffs']=[[38,38],[12,50],[50,12],[25,25]]
         self.data['preStageLengths']=[20,20,60,60,60,60,60,60,60,60,60,60]
         for k in range(20):
            self.data[sid].gameTable[k]=self.data['payoffs']

         try:
            self.nextPeriodCall.cancel()
         except:
            pass

         try:
            self.nonPickleData[sid]['makeChoiceAutomatic'].cancel()
         except:
            pass

         try:
            self.nonPickleData[sid]['sendAutomaticWarning'].cancel()
         except:
            pass

         self.startPreMatch()


      # msg={}
      # msg['type']='startExperiment'
      # msg['title']='Start Experiment'
      # msg['status']=''
      # msg['index']=0


      # if 'pays' not in self.data:
      #    self.data['pays']={}
      #    self.data['matching']={}
      #    self.data['supergameLengths']={}
      #    self.data['order']={}
      #    self.data['roles']={}
      #    for match in range(10):
      #       self.data['pays'][match]={}
      #       self.data['matching'][match]={}
      #       self.data['order'][match]={}
      #       self.data['roles'][match]={}
      #       self.data['order'][match]["randomPlayer"]=["U","D"]
      #       self.data['roles'][match]["randomPlayer"]=1
      #       self.data['supergameLengths'][match]=30

      # for match in range(10):
      #    self.data['pays'][match][sid]={1:{1:[30,30],2:[10,40]},2:{1:[40,10],2:[20,20]}}
      #    self.data['matching'][match][sid]=["randomPlayer"]
      #    # self.data['matching'][match]["randomPlayer"]=[sid]
      #    self.data['order'][match][sid]=["U","D"]
      #    self.data['roles'][match][sid]=0

      # self.data['currentMatch']=1
      # self.data[sid].newMatch(1)
      # self.sendParameters(sid)
      # self.data[sid].getStatus()
      # self.updateStatus(sid)

   def displayDemo(self,viewType,subjectID):
      if viewType=="quiz":
         msg={}
         msg['type']='startQuizOLD'
         msg['title']='Start Quiz'
         msg['status']=''
         msg['index']=0
         self.startQuizOLD(msg,{})
      elif viewType=="trial":
         msg={}
         msg['type']='startTrial'
         msg['title']='Practice'
         msg['status']=''
         msg['index']=0
         self.startTrial(msg,{})
      elif viewType=="hypothetical":
         # msg={}
         # msg['type']='startExperiment'
         # msg['title']='Practice'
         # msg['status']=''
         # msg['index']=0
         # self.startExperiment(msg,{})
         self.data['matchType']="regular"
         self.showHypothetical()
      elif viewType=="firstMatch" or viewType=="regular":
         self.data['matchType']="regularDemo"
         thisClient=self.clientsById[subjectID]
         self.data[subjectID].setFirstPeriodRule(random.choice([0,1]),0,0,'regular')
         self.data[subjectID].setDefaultRule(random.choice([0,1]),0,0,'regular')
         self.data['currentMatch']=0
         self.data['payoffs']=[[38,38],[12,50],[50,12],[25,25]]
         self.data['preStageLengths']=[20,20,60,60,60,60,60,60,60,60,60,60]
         for k in range(20):
            self.data[subjectID].gameTable[k]=self.data['payoffs']

         try:
            self.nextPeriodCall.cancel()
         except:
            pass

         try:
            self.nonPickleData[subjectID]['makeChoiceAutomatic'].cancel()
         except:
            pass

         try:
            self.nonPickleData[subjectID]['sendAutomaticWarning'].cancel()
         except:
            pass

         self.startPreMatch()


class subjectClass():
   def __init__(self):
      self.history={}
      self.hypHistories={}
      self.opponentHistory={}
      self.actionProfileFrequencies={}
      self.allRules=[]
      self.firstPeriodRules=[]
      self.firstPeriodRulesHyp=[]
      self.currentRules=[]
      self.currentHypRules=[]
      self.lockPeriods=[]
      self.lockCosts=0
      self.gameTable={}
      self.partners={}
      self.roles={}
      self.matchPayoffs={}#Me,You
      self.totalPayoffs=[0,0]#Me,You
      self.quizEarnings=0
      self.quizAnswers={}
      # self.quizAnswers=[]
      self.lastPlay=-1
      self.lastRule=-1
      self.lastRuleLength=-1
      self.freeLock=0
      self.oldRules=[]
      self.resetAllRules()
      self.timePerQuestion=60
      self.timeUntilWarning=50
      self.status={"page":"generic","message":["Please read, sign, and date your consent form. <br> You may read over the instructions as we wait to begin."]}

   def resetAllRules(self):
      self.oldRules.append(self.allRules)
      self.oldRules.append(self.firstPeriodRules)
      self.oldRules.append(self.firstPeriodRulesHyp)
      self.allRules=[]
      self.currentRules=[]
      self.currentHypRules=[]
      self.firstPeriodRules=[]
      self.firstPeriodRulesHyp=[]
      allC=Rule([[0]],0)
      self.allRules.append(allC)
      allD=Rule([[1]],1)
      self.allRules.append(allD)

   def newMatch(self,match):
      self.lastPlay=-1
      self.history[match]=[]
      self.opponentHistory[match]=[]
      self.actionProfileFrequencies[match]=[0,0,0,0]
      self.matchPayoffs[match]=[0,0]
      self.currentPeriod=0
      self.matchRunning=0
      for rule in self.allRules:
         rule.lastUsed[match]=-1
         rule.frequency[match]=0

   def getRuleByList(self,ruleList):
      thisRule=[x for x in self.allRules if x.rule==ruleList]
      if len(thisRule)==0:
         out=-1
      elif len(thisRule)==1:
         out=thisRule[0]
      else:
         print("something weird is happening.  Apparently there are two of the same rules in the set?!?!?!?!?!?!?!?!")
      return out

   def deleteRule(self,ruleList,match,time,updateType):
      thisRule=self.getRuleByList(ruleList)
      if updateType=="regular":
         if thisRule in self.currentRules:
            self.currentRules.remove(thisRule)
            thisRule.deletedTimes.append([match,time])
         else:
            print("TRYING TO DELETE RULE NOT IN LIST!!!!!!!!!")
      elif updateType=="hyp":
         if thisRule in self.currentHypRules:
            self.currentHypRules.remove(thisRule)
            thisRule.hypDeletedTimes.append([match,time])
         else:
            print("TRYING TO DELETE RULE NOT IN LIST!!!!!!!!!")

   def addRule(self,ruleList,match,time,updateType):
      thisRule=self.getRuleByList(ruleList)
      if thisRule==-1:
         newRule=Rule(ruleList,len(self.allRules))
         self.allRules.append(newRule)
      else:
         newRule=thisRule

      if updateType=="regular":
         if newRule not in self.currentRules:
            newRule.addedTimes.append([match,time])
            self.currentRules.append(newRule)
         else:
            print("TRYING TO ADD RULE ALREADY IN LIST!!!!!!!!!")
      elif updateType=="hyp":
         if newRule not in self.currentHypRules:
            newRule.hypAddedTimes.append([match,time])
            self.currentHypRules.append(newRule)
         else:
            print("TRYING TO ADD RULE ALREADY IN LIST!!!!!!!!!")

   def setDefaultRule(self,rule,match,time,updateType):
      thisRule=self.getRuleByList([[rule]])#either 0 or 1
      if updateType=="regular":
         thisRule.addedTimes.append([match,time])
         if len(self.currentRules)>0:
            self.currentRules[0]=thisRule
         else:
            self.currentRules.append(thisRule)
      elif updateType=="hyp":
         thisRule.hypAddedTimes.append([match,time])
         if len(self.currentHypRules)>0:
            self.currentHypRules[0]=thisRule
         else:
            self.currentHypRules.append(thisRule)

   def setFirstPeriodRule(self,rule,match,time,updateType):
      if updateType=="regular":
         self.firstPeriodRules.append([rule,match,time])
      if updateType=="hyp":
         self.firstPeriodRulesHyp.append([rule,match,time])

   def switchRules(self,newRuleList,match,time,updateType):
      oldRule=[x if len(x)>1 else [1-x[0]] for x in newRuleList]
      newRule=[x if len(x)>1 else [x[0]] for x in newRuleList]
      self.addRule(newRule,match,time,updateType)
      self.deleteRule(oldRule,match,time,updateType)

   def pickRule(self,ruleListType,history):
      rulesThatFit=[]
      if ruleListType=="regular":
         for k in self.currentRules:
            if k.fitHistory(history):
               rulesThatFit.append(k)
      elif ruleListType=="hyp":
         for k in self.currentHypRules:
            if k.fitHistory(history):
               rulesThatFit.append(k)
      if len(rulesThatFit)>0:
         ruleOut=max(rulesThatFit,key= lambda x: x.length)
      else:
         ruleOut=self.allRules[0]
      return ruleOut


class Rule:
   def __init__(self,rule,number):
      self.rule=rule
      self.input=rule[:-1]
      self.length=len(self.input)
      self.output=rule[-1][0]
      self.number=number
      self.lastUsed={}
      self.frequency={}
      self.addedTimes=[]
      self.deletedTimes=[]

      self.hypAddedTimes=[]
      self.hypDeletedTimes=[]

      self.periodsUsed={}


   def fitHistory(self,history):
      if self.length>0:
         lastN=history[-self.length:]
      else:
         lastN=[]
      if lastN==self.input:
         out=True
      else:
         out=False
      return out

   def ruleUsed(self,match,period):
      if match not in self.periodsUsed:
         self.frequency[match]=0
         self.lastUsed[match]=-1
         self.periodsUsed[match]=[]
      self.frequency[match]=self.frequency[match]+1
      self.lastUsed[match]=period+1
      self.periodsUsed[match].append(period)




class monitorClass():
   def __init__(self):
      "do init stuff"
      self.monitorTasks()

   def getMonitorTable(self):
      table=[]
      titles=['#','subjectID','Rejoin',"Connection","Status","Quiz","Choices","Total"]
      try:
         for subjectID in self.data['subjectIDs']:
            this=[]
            refreshLink="<a href='javascript:void(0)' onclick='refreshClient(\"%s\");'>%s</a>"%(subjectID,subjectID)
            this.append(refreshLink)
            this.append("<a href='game.html?subjectID=%s'>Rejoin</a>"%(subjectID))
            this.append(self.data[subjectID].connectionStatus)
            this.append("%s"%(self.data[subjectID].status))
            this.append("$%.02f"%(self.data[subjectID].quizEarnings))
            this.append("%s"%(self.data[subjectID].totalPayoffs[0]))
            totalPoints=self.data[subjectID].totalPayoffs[0]
            totalPay=totalPoints*self.data['exchangeRate']+self.data[subjectID].quizEarnings
            this.append("$%.02f"%(totalPay))
            table.append(this)
      except Exception as thisExept: 
         print("can't get table at this time because:")
         print(thisExept)
      return table,titles
   
   def monitorTasks(self):
      taskList=[]

      msg={}
      msg['type']='loadInstructions'
      msg['title']='Load Instructions'
      msg['source']=self.config['domain']+self.config['currentExperiment']+self.config['instructionsFolder']+"/audio/output.m4a"
      msg['status']=''
      taskList.append(msg)

      filename=self.config['webServerRoot']+self.config['currentExperiment']+self.config['instructionsFolder']+"/audio/output.duration"
      file = open(filename,'r')
      fileData=file.read()
      file.close() 

      msg={}
      msg['type']='startInstructions'
      msg['title']='Start Instructions'
      msg['totalTime']=float(fileData)
      msg['status']=''
      taskList.append(msg)


      msg={}
      msg['type']='startTrial'
      msg['title']='Practice'
      msg['status']=''
      taskList.append(msg)

      msg={}
      msg['type']='endTrial'
      msg['title']='End Trial'
      msg['status']=''
      taskList.append(msg)

      msg={}
      msg['type']='startQuizOLD'
      msg['title']='Start Quiz'
      msg['status']=''
      taskList.append(msg)

      msg={}
      msg['type']='finishQuiz'
      msg['title']='Finish Quiz'
      msg['status']=''
      taskList.append(msg)

      msg={}
      msg['type']='startExperiment'
      msg['title']='Start Experiment'
      msg['status']=''
      taskList.append(msg)

      for k in range(len(taskList)):
         taskList[k]['index']=k

      self.data['monitorTasks']=taskList


if __name__ == "__main__":
   import imp
   filename="../../steep/code/python/server.py"
   completePathToServerDotPyFile=os.path.abspath(filename) 
   server = imp.load_source('server',completePathToServerDotPyFile)
   #python experiment.py -l local -o True -s False



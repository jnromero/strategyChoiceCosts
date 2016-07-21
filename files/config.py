#!/usr/bin/python

import pickle
import os
scriptPath=os.path.dirname(os.path.realpath(__file__))

def defaultSettings(location,configFile,serverStartString):
	config={}
	config['favicon']="common/"

	config['packageFolder']="/common/"
	config['currentExperiment']="/strategyChoice/20160712_costs/"
	config['instructionsFolder']="/files/instructions/instructions250/"
	config['instructionsTexFile']="/latex/instructions_Costs250_Apr2016.tex"
	config["location"]=location
	config["quiz"]="True"
	config['screenServerPort']=15374

	if location=="local":
		config['webServerRoot']="/Users/jnr/Dropbox/Sites/jnromero.com/Experiments/"
		config['serverType']="regularExperiment"	
		config['serverPort']=24921
		config['webSocketPort']=13557
		ip="localhost"
		config["domain"]="http://"+ip+":"+str(config['serverPort'])
		config["websocketURL"]="ws://"+ip+":"+str(config['webSocketPort'])
		config["screenServer"]="http://"+ip+":"+str(config['screenServerPort'])
	elif location=="esl":
		config['webServerRoot']="/Users/jnr/Dropbox/Sites/jnromero.com/Experiments/"
		config['serverType']="regularExperiment"	
		config['serverPort']=24921
		config['webSocketPort']=13557
		ip="10.128.228.70"
		config["domain"]="http://"+ip+":"+str(config['serverPort'])
		config["websocketURL"]="ws://"+ip+":"+str(config['webSocketPort'])
		config["screenServer"]="http://"+ip+":"+str(config['screenServerPort'])
	elif location=="webf":
		config['webServerRoot']="/home/jnromero/Sites/jnromero.com/Experiments/"
		config['serverType']="regularExperiment"	
		config['serverPort']=24921
		config['webSocketPort']=13557
		config["domain"]="http://jnromero.com/experiment"
		config["websocketURL"]='ws://jnromero.com/webSockets/mainExperiment'
		config["screenServer"]="http://jnromero.com/screenServer/"
	elif location=="localDemo":
		config['webServerRoot']="/Users/jnr/Dropbox/Sites/jnromero.com/Experiments/"
		config['serverType']="demoExperiment"	
		config['serverPort']=28641
		config['webSocketPort']=10374
		ip="localhost"
		config["domain"]="http://"+ip+":"+str(config['serverPort'])
		config["websocketURL"]="ws://"+ip+":"+str(config['webSocketPort'])
		config["screenServer"]="http://"+ip+":"+str(config['screenServerPort'])
	elif location=="webfDemo":
		config['webServerRoot']="/home/jnromero/Sites/jnromero.com/Experiments/"
		config['serverType']="demoExperiment"	
		config['serverPort']=28641
		config['webSocketPort']=10374
		config["domain"]="http://jnromero.com/experiments/demos/costlyStrategyAdjustment"
		config["websocketURL"]='ws://jnromero.com/webSockets/demos/costlyStrategyAdjustment'
		config["screenServer"]="http://jnromero.com/screenServer/"

	config=setOtherFileLocations(config,serverStartString)
	writeJavascriptConfigFile(config,configFile)
	return config

def setOtherFileLocations(config,serverStartString):
	config['dataFolder']=config['currentExperiment']+"/data/"+serverStartString+"/"
	if not os.path.exists(config['webServerRoot']+config['dataFolder']):
		os.makedirs(config['webServerRoot']+config['dataFolder'])

	config['configJsURL']=config['domain']+config['dataFolder']+"/config.js"
	config['configJsPath']=config['webServerRoot']+config['dataFolder']+"/config.js"

	config['dataFileURL']=config['domain']+config['dataFolder']+"/%s.pickle"%(serverStartString)
	config['dataFilePath']=config['webServerRoot']+config['dataFolder']+"/%s.pickle"%(serverStartString)
	return config

def writeJavascriptConfigFile(config,configFile):
	string="//Config File Location: %s\n"%(configFile)
	string=string+"window.config=%s;"%(config)
	file = open(config['configJsPath'],'w')
	file.writelines(string)
	file.close() 


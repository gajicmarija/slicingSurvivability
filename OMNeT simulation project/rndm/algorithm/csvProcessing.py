import numpy as np
import pandas as pd
import re



#v1500l20000d36000f42000s500_195_VID49_LVD39_FDO41_SSH31_VIP35

def csvProcessing(fileName):
	df = pd.read_csv (fileName)
	#nVIP is number of VoIP clients, bVIP is bandwidth for VoIP clients
	dfnVIP,dfbVIP,dfnVID,dfbVID,dfnLVD,dfbLVD,dfnSSH,dfbSSH,dfnFD,dfbFD = [],[],[],[],[],[],[],[],[],[]
	for index, row in df.iterrows():
		scenarioName=row["scenario"]
		print(scenarioName)
		pattern = "D(.*?)_L"
		VID =  re.search(pattern, scenarioName).group(1)
		dfnVID.append(VID)
		pattern = "LVD(.*?)_F"
		LVD =  re.search(pattern, scenarioName).group(1)
		dfnLVD.append(LVD)
		pattern = "O(.*?)_S"
		FD =  re.search(pattern, scenarioName).group(1)
		dfnFD.append(FD)
		pattern = "H(.*?)_V"
		SSH =  re.search(pattern, scenarioName).group(1)
		dfnSSH.append(SSH)
		pattern = "VIP(.*?)$"
		VIP =  re.search(pattern, scenarioName).group(1)
		dfnVIP.append(VIP)

		pattern = "v(.*?)l"
		VIP =  re.search(pattern, scenarioName).group(1)
		dfbVIP.append(VIP)
		pattern = "l(.*?)d"
		LVD =  re.search(pattern, scenarioName).group(1)
		dfbLVD.append(LVD)
		pattern = "d(.*?)f"
		VID =  re.search(pattern, scenarioName).group(1)
		dfbVID.append(VID)
		print(VID)
		pattern = "f(.*?)s"
		FD =  re.search(pattern, scenarioName).group(1)
		dfbFD.append(FD)
		print(FD)
		pattern = "s(.*?)_"
		SSH =  re.search(pattern, scenarioName).group(1)
		dfbSSH.append(SSH)
		print(SSH)		

	df["bVIP"]=dfbVIP	
	df["bLVD"]=dfbLVD
	df["bVID"]=dfbVID
	df["bFD"]=dfbFD
	df["bSSH"]=dfbSSH
	df["nVIP"]=dfnVIP	
	df["nLVD"]=dfnLVD
	df["nVID"]=dfnVID
	df["nFD"]=dfnFD
	df["nSSH"]=dfnSSH

	df = df[['scenario',"nVIP","nLVD","nVID","nFD","nSSH","bVIP","bLVD","bVID","bFD","bSSH","hostVID","hostLVD","hostFDO","hostSSH","hostVIP","total"]]
	print(df)


csvProcessing("../analysis/exports/ml_data/output.csv")

import re

fullScenarioName = "disaster2S50_1455_VID485_LVD260_FDO50_SSH100_VIP400_cVP100_cF50_cLV10"
pattern = "v(.*?)l"    
print(re.search(pattern, fullScenarioName))
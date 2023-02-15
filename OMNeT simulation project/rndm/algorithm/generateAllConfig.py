from cfgGenLibAllConfig import *
import numpy as np
import math
import itertools, operator

#function for generation of all combinations for RA, assuming voip and ssh take 2mbps this means 98 for rest pr 97*96/2 total combinations
def genCombinations(num):
    combo=set()
    for cuts in itertools.combinations_with_replacement(range(1,num), 3):
        if(sum(cuts)==num):
            for i in set(itertools.permutations(cuts)):
                combo.add(i)
    return combo

# REMINDER: if app A has priority 0 and app B has priority 1, app A will get preferential treatment.

def gen_cfg(cfgName, useTwoLevelHTB):

    # IP settings don't change from scenario to scenario.
    hostIPs = OrderedDict([('VIP', '10.0.x.x'), ('LVD', '10.1.x.x'), ('VID', '10.2.x.x'), ('FDO', '10.3.x.x'), ('SSH', '10.4.x.x'),('cVP', '10.5.x.x'),('cF', '10.6.x.x'),('cLV', '10.7.x.x')])
    serverIPs = OrderedDict([('VIP', '10.10.0.0'), ('LVD', '10.11.0.0'), ('VID', '10.12.0.0'), ('FDO', '10.13.0.0'), ('SSH', '10.14.0.0'),('cVP', '10.15.x.x'),('cF', '10.16.x.x'),('cLV', '10.17.x.x')])

    
    # myCfg-001 -- VIP + LVD, no prio
    if cfgName == 'myCfg-001':
        hostPrios = OrderedDict([('VIP', 0), ('LVD', 0), ('VID', 0), ('FDO', 0), ('SSH', 0)])
        hostNumbers = OrderedDict([('VIP', 400), ('LVD', 10), ('VID', 0), ('FDO', 0), ('SSH', 0)])
        rate = 15e6
        bwSplits = [OrderedDict([('VIP', round(p * .01 * rate)), ('LVD', round((100 - p) * .01 * rate)), ('VID', 0), ('FDO', 0), ('SSH', 0)]) for p in range(10, 100, 10)]
        baseCfgName = 'liteCbaselineTestTokenQoS_base'
    elif cfgName=="S1NoDis":
        bwSplits = []
        ceilSplits = []
        bwSplits.append(OrderedDict([('VIP', 17500000), ('LVD',150000000), ('VID',540000000), ('FDO',156000000), ('SSH',700000),('cVP', 5000000),('cF', 52000000),('cLV', 75000000)]))
        ceilSplits=bwSplits
        hostPrios = OrderedDict([('VIP', 1), ('LVD', 1), ('VID', 1), ('FDO', 1), ('SSH', 1),('cVP', 0),('cF', 0),('cLV', 0)])
        hostNumbers = OrderedDict([('VIP', 350), ('LVD', 37), ('VID', 135), ('FDO', 60), ('SSH', 100),('cVP', 100),('cF', 20),('cLV', 18)])
        baseCfgName = 'liteCbaselineTestTokenQoS_base'  
        generate_all_config_files1(cfgName, baseCfgName, hostNumbers, hostPrios, hostIPs, serverIPs, bwSplits, ceilSplits) 
    elif cfgName=="S2sli8withGuarantees":
        baseCfgName = 'liteCbaselineTestTokenQoS_base'  
        hostPrios = OrderedDict([('VIP', 1), ('LVD', 1), ('VID', 1), ('FDO', 1), ('SSH', 1),('cVP', 0),('cF', 0),('cLV', 0)])
        hostNumbers = OrderedDict([('VIP', 350), ('LVD', 37), ('VID', 135), ('FDO', 60), ('SSH', 100),('cVP', 100),('cF', 20),('cLV', 18)])
        percentage = [1,2]
        for i in percentage:
            bwSplits = []
            ceilSplits = []
            cfgName="S2sli8withGuarantees"
            bwSplits.append(OrderedDict([('VIP', 17500000*(i/100)), ('LVD',150000000*(i/100)), ('VID',540000000*(i/100)), ('FDO',156000000*(i/100)), ('SSH',700000*(i/100)),('cVP', 5000000*(i/100)),('cF', 52000000*(i/100)),('cLV', 75000000*(i/100))]))
            ceilSplits=bwSplits
           #bwSplits.append(OrderedDict([('VIP', 0), ('LVD',0), ('VID',0), ('FDO',0), ('SSH',0),('cVP', 2*19000000*(i/100)),('cF', 2*896000000*(i/100)),('cLV', 2*85000000*(i/100))]))
           #ceiling.append(OrderedDict([('VIP', 2*9600000), ('LVD',2*286000000*(i/100)), ('VID',2*461000000*(i/100)), ('FDO',2*224000000*(i/100)), ('SSH',2*500000*(i/100)),('cVP', 2*1000e6*(i/100)),('cF', 2*1000e6*(i/100)),('cLV', 2*1000e6*(i/100))]))
            cfgName+="%s" % (i)
            generate_all_config_files1(cfgName, baseCfgName, hostNumbers, hostPrios, hostIPs, serverIPs, bwSplits, ceilSplits) 
    elif cfgName=="S3sli8noGuarantees":
        baseCfgName = 'liteCbaselineTestTokenQoS_base'  
        hostPrios = OrderedDict([('VIP', 1), ('LVD', 1), ('VID', 1), ('FDO', 1), ('SSH', 1),('cVP', 0),('cF', 0),('cLV', 0)])
        hostNumbers = OrderedDict([('VIP', 350), ('LVD', 37), ('VID', 135), ('FDO', 60), ('SSH', 100),('cVP', 100),('cF', 20),('cLV', 18)])
        percentage = [1,2,20,50,80,100]
        for i in percentage:
            bwSplits = []
            ceilSplits = []
            cfgName="S3sli8noGuarantees"
            bwSplits.append(OrderedDict([('VIP', 0), ('LVD',0), ('VID',0), ('FDO',0), ('SSH',0),('cVP', 39000000*(i/100)),('cF', 403000000*(i/100)),('cLV', 558000000*(i/100))]))
            ceilSplits.append(OrderedDict([('VIP', 17500000*(i/100)), ('LVD',150000000*(i/100)), ('VID',540000000*(i/100)), ('FDO',156000000*(i/100)), ('SSH',700000*(i/100)),('cVP', 1000000000*(i/100)),('cF', 1000000000*(i/100)),('cLV', 1000000000*(i/100))]))
           #bwSplits.append(OrderedDict([('VIP', 0), ('LVD',0), ('VID',0), ('FDO',0), ('SSH',0),('cVP', 2*19000000*(i/100)),('cF', 2*896000000*(i/100)),('cLV', 2*85000000*(i/100))]))
           #ceiling.append(OrderedDict([('VIP', 2*9600000), ('LVD',2*286000000*(i/100)), ('VID',2*461000000*(i/100)), ('FDO',2*224000000*(i/100)), ('SSH',2*500000*(i/100)),('cVP', 2*1000e6*(i/100)),('cF', 2*1000e6*(i/100)),('cLV', 2*1000e6*(i/100))]))
            cfgName+="%s" % (i)
            generate_all_config_files1(cfgName, baseCfgName, hostNumbers, hostPrios, hostIPs, serverIPs, bwSplits, ceilSplits) 
    elif cfgName=="S3sli8noGuaranteesV2":
        baseCfgName = 'liteCbaselineTestTokenQoS_base'  
        hostPrios = OrderedDict([('VIP', 1), ('LVD', 1), ('VID', 1), ('FDO', 1), ('SSH', 1),('cVP', 0),('cF', 0),('cLV', 0)])
        hostNumbers = OrderedDict([('VIP', 350), ('LVD', 37), ('VID', 135), ('FDO', 60), ('SSH', 100),('cVP', 100),('cF', 20),('cLV', 18)])
        percentage = [5]
        for i in percentage:
            bwSplits = []
            ceilSplits = []
            cfgName="S3sli8noGuaranteesV2"
            rate = 996200000*(i/100)
            if rate >= 132000000:
            	bwSplits.append(OrderedDict([('VIP', 0), ('LVD',0), ('VID',0), ('FDO',0), ('SSH',0),('cVP', 5000000),('cF', 52000000),('cLV', 75000000)]))
            	ceilSplits.append(OrderedDict([('VIP', 17500000*(i/100)), ('LVD',150000000*(i/100)), ('VID',540000000*(i/100)), ('FDO',156000000*(i/100)), ('SSH',700000*(i/100)), ('cVP', 5000000),('cF', 52000000),('cLV', 75000000)]))
            else:
            	bwSplits.append(OrderedDict([('VIP', 0), ('LVD',0), ('VID',0), ('FDO',0), ('SSH',0),('cVP', math.floor((rate/129)*5)),('cF', math.floor((rate/129)*52)),('cLV', math.floor((rate/129)*72))]))
            	ceilSplits.append(OrderedDict([('VIP', 17500000*(i/100)), ('LVD',150000000*(i/100)), ('VID',540000000*(i/100)), ('FDO',156000000*(i/100)), ('SSH',700000*(i/100)), ('cVP', rate),('cF', rate),('cLV', rate)]))
           

           #bwSplits.append(OrderedDict([('VIP', 0), ('LVD',0), ('VID',0), ('FDO',0), ('SSH',0),('cVP', 2*19000000*(i/100)),('cF', 2*896000000*(i/100)),('cLV', 2*85000000*(i/100))]))
           #ceiling.append(OrderedDict([('VIP', 2*9600000), ('LVD',2*286000000*(i/100)), ('VID',2*461000000*(i/100)), ('FDO',2*224000000*(i/100)), ('SSH',2*500000*(i/100)),('cVP', 2*1000e6*(i/100)),('cF', 2*1000e6*(i/100)),('cLV', 2*1000e6*(i/100))]))
            cfgName+="%s" % (i)
            generate_all_config_files1(cfgName, baseCfgName, hostNumbers, hostPrios, hostIPs, serverIPs, bwSplits, ceilSplits,rate) 
    elif cfgName=="S4sli2noGuaranteesV2Fix":
        baseCfgName = 'liteCbaselineTestTokenQoS_base'  
        hostPrios = OrderedDict([('critical', 0), ('nonCritical',1)])
        flowNumbers = OrderedDict([('VIP', 350), ('LVD', 37), ('VID', 135), ('FDO', 60), ('SSH', 100),('cVP', 100),('cF', 20),('cLV', 18)])
        hostNumbers = OrderedDict([('critical', 1), ('nonCritical',1)])
        percentage = [20,30,40,80]
        for i in percentage:
            rate = 996200000*(i/100)
            bwSplits = []
            ceilSplits = []
            cfgName="S4sli2noGuaranteesV2Fix"
            if rate >= 132000000:
                bwSplits.append(OrderedDict([('critical', 132000000), ('nonCritical',0)]))
                ceilSplits.append(OrderedDict([('critical',132000000 ), ('nonCritical',864200000*(i/100))])) #FIXME: noncritical BW *(i/100)
            else:
            	bwSplits.append(OrderedDict([('critical', rate), ('nonCritical',0)]))
            	ceilSplits.append(OrderedDict([('critical',996200000*(i/100) ), ('nonCritical',864200000*(i/100))])) #FIXME same as above *(i/100)

           #bwSplits.append(OrderedDict([('VIP', 0), ('LVD',0), ('VID',0), ('FDO',0), ('SSH',0),('cVP', 2*19000000*(i/100)),('cF', 2*896000000*(i/100)),('cLV', 2*85000000*(i/100))]))
           #ceiling.append(OrderedDict([('VIP', 2*9600000), ('LVD',2*286000000*(i/100)), ('VID',2*461000000*(i/100)), ('FDO',2*224000000*(i/100)), ('SSH',2*500000*(i/100)),('cVP', 2*1000e6*(i/100)),('cF', 2*1000e6*(i/100)),('cLV', 2*1000e6*(i/100))]))
            cfgName+="%s" % (i)
            generate_all_config_files2(cfgName, baseCfgName, hostNumbers, hostPrios, hostIPs, serverIPs, bwSplits, ceilSplits, flowNumbers, rate) 
    elif cfgName=="S5sli4noGuaranteesNew":
        baseCfgName = 'liteCbaselineTestTokenQoS_base'  
        hostPrios = OrderedDict([('cVP', 0),('cF', 0),('cLV', 0),('nonCritical',1)])
        flowNumbers = OrderedDict([('VIP', 350), ('LVD', 37), ('VID', 135), ('FDO', 60), ('SSH', 100),('cVP', 100),('cF', 20),('cLV', 18)])
        hostNumbers = OrderedDict([('cVP', 100),('cF', 20),('cLV', 18),('nonCritical',1)])
        percentage = [5,10,100]
        for i in percentage:
            rate = 996200000*(i/100)
            bwSplits = []
            ceilSplits = []
            cfgName="S5sli4noGuaranteesNew"
            if rate >= 132000000:
                bwSplits.append(OrderedDict([('cVP', 5000000),('cF', 52000000),('cLV', 75000000),('nonCritical',0)]))
                ceilSplits.append(OrderedDict([('cVP', 5000000),('cF', 52000000),('cLV', 75000000),('nonCritical',864200000*(i/100))]))
            else:
                bwSplits.append(OrderedDict([('cVP', math.floor((rate/129)*5)),('cF', math.floor((rate/129)*52)),('cLV', math.floor((rate/129)*72)),('nonCritical',0)]))
                ceilSplits.append(OrderedDict([ ('cVP', rate),('cF', rate),('cLV', rate),('nonCritical',864200000*(i/100))]))
           

           #bwSplits.append(OrderedDict([('VIP', 0), ('LVD',0), ('VID',0), ('FDO',0), ('SSH',0),('cVP', 2*19000000*(i/100)),('cF', 2*896000000*(i/100)),('cLV', 2*85000000*(i/100))]))
           #ceiling.append(OrderedDict([('VIP', 2*9600000), ('LVD',2*286000000*(i/100)), ('VID',2*461000000*(i/100)), ('FDO',2*224000000*(i/100)), ('SSH',2*500000*(i/100)),('cVP', 2*1000e6*(i/100)),('cF', 2*1000e6*(i/100)),('cLV', 2*1000e6*(i/100))]))
            cfgName+="%s" % (i)
            generate_all_config_files3(cfgName, baseCfgName, hostNumbers, hostPrios, hostIPs, serverIPs, bwSplits, ceilSplits, flowNumbers, rate) 
   
    elif cfgName=="Ddisaster8S":
        baseCfgName = 'liteCbaselineTestTokenQoS_base'
        hostPrios = OrderedDict([('VIP', 1), ('LVD', 1), ('VID', 1), ('FDO', 1), ('SSH', 1),('cVP', 0),('cF', 0),('cLV', 0)])
        hostNumbers = OrderedDict([('VIP', 400), ('LVD', 260), ('VID', 485), ('FDO', 100), ('SSH', 100),('cVP', 100),('cF', 50),('cLV', 10)])
        percentage = [20,50,80]
        for i in percentage:
            bwSplits = []
            ceiling = []
            cfgName="Ddisaster8S"
            bwSplits.append(OrderedDict([('VIP', 0), ('LVD',0), ('VID',0), ('FDO',0), ('SSH',0),('cVP', 2*19000000*(i/100)),('cF', 2*896000000*(i/100)),('cLV', 2*85000000*(i/100))]))
            ceiling.append(OrderedDict([('VIP', 2*9600000), ('LVD',2*286000000*(i/100)), ('VID',2*461000000*(i/100)), ('FDO',2*224000000*(i/100)), ('SSH',2*500000*(i/100)),('cVP', 2*1000e6*(i/100)),('cF', 2*1000e6*(i/100)),('cLV', 2*1000e6*(i/100))]))
            rate = 2*1000*(i/100) #rate is in bytes
            cfgName+="%s" % (i)
            generate_all_config_files_ceil(cfgName, baseCfgName, hostNumbers, hostPrios, hostIPs, serverIPs, bwSplits, ceiling, rate, useTwoLevelHTB)
    elif cfgName=="scenario1ND":
        bwSplits = []
        #bwSplits.append(OrderedDict([('VIP', 17500000), ('LVD',150000000), ('VID',540000000), ('FDO',52000000), ('SSH',700000),('cVP', 5000000),('cF', 156000000),('cLV', 75000000)]))
        bwSplits.append(OrderedDict([('VIP', 17500000), ('LVD',150000000), ('VID',540000000), ('FDO',52000000), ('SSH',700000),('cVP', 5000000),('cF', 156000000),('cLV', 97300)]))
        hostPrios = OrderedDict([('VIP', 1), ('LVD', 1), ('VID', 1), ('FDO', 1), ('SSH', 1),('cVP', 0),('cF', 0),('cLV', 0)])
        hostNumbers = OrderedDict([('VIP', 350), ('LVD', 50), ('VID', 225), ('FDO', 20), ('SSH', 100),('cVP', 100),('cF', 60),('cLV', 25)])
        rate = 1000 
        baseCfgName = 'liteCbaselineTestTokenQoS_base'  
        generate_all_config_files(cfgName, baseCfgName, hostNumbers, hostPrios, hostIPs, serverIPs, bwSplits,rate, useTwoLevelHTB) 
    elif cfgName=="S6sli2noGuaranteesV2":
        baseCfgName = 'liteCbaselineTestTokenQoS_base'  
        hostPrios = OrderedDict([('delay', 0), ('bandwidth',1)])
        flowNumbers = OrderedDict([('VIP', 350), ('LVD', 37), ('VID', 135), ('FDO', 60), ('SSH', 100),('cVP', 100),('cF', 20),('cLV', 18)])
        hostNumbers = OrderedDict([('delay', 1), ('bandwidth',1)])
        percentage = [5]
        for i in percentage:
            rate = 996200000*(i/100)
            bwSplits = []
            ceilSplits = []
            cfgName="S6sli2noGuaranteesV2"
            
            bwSplits.append(OrderedDict([('delay', 23200000*(i/100)), ('bandwidth',973000000*(i/100))]))
            ceilSplits.append(OrderedDict([('delay',23200000*(i/100)), ('bandwidth',973000000*(i/100))]))
           

           #bwSplits.append(OrderedDict([('VIP', 0), ('LVD',0), ('VID',0), ('FDO',0), ('SSH',0),('cVP', 2*19000000*(i/100)),('cF', 2*896000000*(i/100)),('cLV', 2*85000000*(i/100))]))
           #ceiling.append(OrderedDict([('VIP', 2*9600000), ('LVD',2*286000000*(i/100)), ('VID',2*461000000*(i/100)), ('FDO',2*224000000*(i/100)), ('SSH',2*500000*(i/100)),('cVP', 2*1000e6*(i/100)),('cF', 2*1000e6*(i/100)),('cLV', 2*1000e6*(i/100))]))
            cfgName+="%s" % (i)
            generate_all_config_files2(cfgName, baseCfgName, hostNumbers, hostPrios, hostIPs, serverIPs, bwSplits, ceilSplits, flowNumbers, rate) 
    elif cfgName=="S7sli4noGuaranteesNew":
        baseCfgName = 'liteCbaselineTestTokenQoS_base'  
        hostPrios = OrderedDict([('delCritical', 0),('delNonCrtical', 2),('bwCritical', 1),('bwNonCritical',3)])
        flowNumbers = OrderedDict([('VIP', 350), ('LVD', 37), ('VID', 135), ('FDO', 60), ('SSH', 100),('cVP', 100),('cF', 20),('cLV', 18)])
        hostNumbers = OrderedDict([('delCritical', 1),('delNonCrtical', 1),('bwCritical', 1),('bwNonCritical',1)])
        percentage = [5]
        for i in percentage:
            rate = 996200000*(i/100)
            bwSplits = []
            ceilSplits = []
            cfgName="S7sli4noGuaranteesNew"
            if rate >= 132000000:
                bwSplits.append(OrderedDict([('delCritical', 5000000),('delNonCrtical', 0),('bwCritical',127000000),('bwNonCritical',0)]))
                ceilSplits.append(OrderedDict([('delCritical', 5000000),('delNonCrtical', 18200000*(i/100)),('bwCritical',127000000),('bwNonCritical',846000000*(i/100))]))
            else:
                bwSplits.append(OrderedDict([('delCritical', math.floor((rate/132)*5)),('delNonCrtical', 0),('bwCritical',math.floor((rate/132)*127)),('bwNonCritical',0)]))
                ceilSplits.append(OrderedDict([('delCritical', rate),('delNonCrtical', 18200000*(i/100)),('bwCritical',rate),('bwNonCritical',846000000*(i/100))]))
           

           #bwSplits.append(OrderedDict([('VIP', 0), ('LVD',0), ('VID',0), ('FDO',0), ('SSH',0),('cVP', 2*19000000*(i/100)),('cF', 2*896000000*(i/100)),('cLV', 2*85000000*(i/100))]))
           #ceiling.append(OrderedDict([('VIP', 2*9600000), ('LVD',2*286000000*(i/100)), ('VID',2*461000000*(i/100)), ('FDO',2*224000000*(i/100)), ('SSH',2*500000*(i/100)),('cVP', 2*1000e6*(i/100)),('cF', 2*1000e6*(i/100)),('cLV', 2*1000e6*(i/100))]))
            cfgName+="%s" % (i)
            generate_all_config_files3(cfgName, baseCfgName, hostNumbers, hostPrios, hostIPs, serverIPs, bwSplits, ceilSplits, flowNumbers, rate) 
    elif cfgName=="S8sli8_4prio":
        baseCfgName = 'liteCbaselineTestTokenQoS_base'  
        hostPrios = OrderedDict([('VIP', 2), ('LVD', 3), ('VID', 3), ('FDO', 3), ('SSH', 2),('cVP', 0),('cF', 1),('cLV', 1)])
        hostNumbers = OrderedDict([('VIP', 350), ('LVD', 37), ('VID', 135), ('FDO', 60), ('SSH', 100),('cVP', 100),('cF', 20),('cLV', 18)])
        percentage = [5,10,20,30,40,80,100]
        for i in percentage:
            bwSplits = []
            ceilSplits = []
            cfgName="S8sli8_4prio"
            rate = 996200000*(i/100)
            if rate >= 132000000:
                bwSplits.append(OrderedDict([('VIP', 0), ('LVD',0), ('VID',0), ('FDO',0), ('SSH',0),('cVP', 5000000),('cF', 52000000),('cLV', 75000000)]))
                ceilSplits.append(OrderedDict([('VIP', 17500000*(i/100)), ('LVD',150000000*(i/100)), ('VID',540000000*(i/100)), ('FDO',156000000*(i/100)), ('SSH',700000*(i/100)), ('cVP', 5000000),('cF', 52000000),('cLV', 75000000)]))
            else:
                bwSplits.append(OrderedDict([('VIP', 0), ('LVD',0), ('VID',0), ('FDO',0), ('SSH',0),('cVP', math.floor((rate/129)*5)),('cF', math.floor((rate/129)*52)),('cLV', math.floor((rate/129)*72))]))
                ceilSplits.append(OrderedDict([('VIP', 17500000*(i/100)), ('LVD',150000000*(i/100)), ('VID',540000000*(i/100)), ('FDO',156000000*(i/100)), ('SSH',700000*(i/100)), ('cVP', rate),('cF', rate),('cLV', rate)]))
           

           #bwSplits.append(OrderedDict([('VIP', 0), ('LVD',0), ('VID',0), ('FDO',0), ('SSH',0),('cVP', 2*19000000*(i/100)),('cF', 2*896000000*(i/100)),('cLV', 2*85000000*(i/100))]))
           #ceiling.append(OrderedDict([('VIP', 2*9600000), ('LVD',2*286000000*(i/100)), ('VID',2*461000000*(i/100)), ('FDO',2*224000000*(i/100)), ('SSH',2*500000*(i/100)),('cVP', 2*1000e6*(i/100)),('cF', 2*1000e6*(i/100)),('cLV', 2*1000e6*(i/100))]))
            cfgName+="%s" % (i)
            generate_all_config_files1(cfgName, baseCfgName, hostNumbers, hostPrios, hostIPs, serverIPs, bwSplits, ceilSplits,rate) 
    elif cfgName=="S9sli4_3prio":
        baseCfgName = 'liteCbaselineTestTokenQoS_base'  
        hostPrios = OrderedDict([('cVP', 0),('cF', 1),('cLV', 1),('nonCritical',2)])
        flowNumbers = OrderedDict([('VIP', 350), ('LVD', 37), ('VID', 135), ('FDO', 60), ('SSH', 100),('cVP', 100),('cF', 20),('cLV', 18)])
        hostNumbers = OrderedDict([('cVP', 100),('cF', 20),('cLV', 18),('nonCritical',1)])
        percentage = [5,10,20,30,40,80,100]
        for i in percentage:
            rate = 996200000*(i/100)
            bwSplits = []
            ceilSplits = []
            cfgName="S9sli4_3prio"
            if rate >= 132000000:
                bwSplits.append(OrderedDict([('cVP', 5000000),('cF', 52000000),('cLV', 75000000),('nonCritical',0)]))
                ceilSplits.append(OrderedDict([('cVP', 5000000),('cF', 52000000),('cLV', 75000000),('nonCritical',864200000*(i/100))]))
            else:
                bwSplits.append(OrderedDict([('cVP', math.floor((rate/129)*5)),('cF', math.floor((rate/129)*52)),('cLV', math.floor((rate/129)*72)),('nonCritical',0)]))
                ceilSplits.append(OrderedDict([ ('cVP', rate),('cF', rate),('cLV', rate),('nonCritical',864200000*(i/100))]))
            cfgName+="%s" % (i)
            generate_all_config_files3(cfgName, baseCfgName, hostNumbers, hostPrios, hostIPs, serverIPs, bwSplits, ceilSplits, flowNumbers, rate) 

    elif cfgName=="S10sli4_2prio":
        baseCfgName = 'liteCbaselineTestTokenQoS_base'  
        hostPrios = OrderedDict([('delCritical', 0),('delNonCrtical', 1),('bwCritical', 0),('bwNonCritical',1)])
        flowNumbers = OrderedDict([('VIP', 350), ('LVD', 37), ('VID', 135), ('FDO', 60), ('SSH', 100),('cVP', 100),('cF', 20),('cLV', 18)])
        hostNumbers = OrderedDict([('delCritical', 1),('delNonCrtical', 1),('bwCritical', 1),('bwNonCritical',1)])
        percentage = [5]
        for i in percentage:
            rate = 996200000*(i/100)
            bwSplits = []
            ceilSplits = []
            cfgName="S10sli4_2prio"
            if rate >= 132000000:
                bwSplits.append(OrderedDict([('delCritical', 5000000),('delNonCrtical', 0),('bwCritical',127000000),('bwNonCritical',0)]))
                ceilSplits.append(OrderedDict([('delCritical', 5000000),('delNonCrtical', 18200000*(i/100)),('bwCritical',127000000),('bwNonCritical',846000000*(i/100))]))
            else:
                bwSplits.append(OrderedDict([('delCritical', math.floor((rate/132)*5)),('delNonCrtical', 0),('bwCritical',math.floor((rate/132)*127)),('bwNonCritical',0)]))
                ceilSplits.append(OrderedDict([('delCritical', rate),('delNonCrtical', 18200000*(i/100)),('bwCritical',rate),('bwNonCritical',846000000*(i/100))]))
           #bwSplits.append(OrderedDict([('VIP', 0), ('LVD',0), ('VID',0), ('FDO',0), ('SSH',0),('cVP', 2*19000000*(i/100)),('cF', 2*896000000*(i/100)),('cLV', 2*85000000*(i/100))]))
           #ceiling.append(OrderedDict([('VIP', 2*9600000), ('LVD',2*286000000*(i/100)), ('VID',2*461000000*(i/100)), ('FDO',2*224000000*(i/100)), ('SSH',2*500000*(i/100)),('cVP', 2*1000e6*(i/100)),('cF', 2*1000e6*(i/100)),('cLV', 2*1000e6*(i/100))]))
            cfgName+="%s" % (i)
            generate_all_config_files3(cfgName, baseCfgName, hostNumbers, hostPrios, hostIPs, serverIPs, bwSplits, ceilSplits, flowNumbers, rate) 
    elif cfgName=="S11sli8_3prio":
        baseCfgName = 'liteCbaselineTestTokenQoS_base'  
        hostPrios = OrderedDict([('VIP', 2), ('LVD', 2), ('VID', 2), ('FDO', 2), ('SSH', 2),('cVP', 0),('cF', 1),('cLV', 1)])
        hostNumbers = OrderedDict([('VIP', 350), ('LVD', 37), ('VID', 135), ('FDO', 60), ('SSH', 100),('cVP', 100),('cF', 20),('cLV', 18)])
        percentage = [5,10,20,30,40,80,100]
        for i in percentage:
            bwSplits = []
            ceilSplits = []
            cfgName="S11sli8_3prio"
            rate = 996200000*(i/100)
            if rate >= 132000000:
                bwSplits.append(OrderedDict([('VIP', 0), ('LVD',0), ('VID',0), ('FDO',0), ('SSH',0),('cVP', 5000000),('cF', 52000000),('cLV', 75000000)]))
                ceilSplits.append(OrderedDict([('VIP', 17500000*(i/100)), ('LVD',150000000*(i/100)), ('VID',540000000*(i/100)), ('FDO',156000000*(i/100)), ('SSH',700000*(i/100)), ('cVP', 5000000),('cF', 52000000),('cLV', 75000000)]))
            else:
                bwSplits.append(OrderedDict([('VIP', 0), ('LVD',0), ('VID',0), ('FDO',0), ('SSH',0),('cVP', math.floor((rate/129)*5)),('cF', math.floor((rate/129)*52)),('cLV', math.floor((rate/129)*72))]))
                ceilSplits.append(OrderedDict([('VIP', 17500000*(i/100)), ('LVD',150000000*(i/100)), ('VID',540000000*(i/100)), ('FDO',156000000*(i/100)), ('SSH',700000*(i/100)), ('cVP', rate),('cF', rate),('cLV', rate)]))
           

           #bwSplits.append(OrderedDict([('VIP', 0), ('LVD',0), ('VID',0), ('FDO',0), ('SSH',0),('cVP', 2*19000000*(i/100)),('cF', 2*896000000*(i/100)),('cLV', 2*85000000*(i/100))]))
           #ceiling.append(OrderedDict([('VIP', 2*9600000), ('LVD',2*286000000*(i/100)), ('VID',2*461000000*(i/100)), ('FDO',2*224000000*(i/100)), ('SSH',2*500000*(i/100)),('cVP', 2*1000e6*(i/100)),('cF', 2*1000e6*(i/100)),('cLV', 2*1000e6*(i/100))]))
            cfgName+="%s" % (i)
            generate_all_config_files1(cfgName, baseCfgName, hostNumbers, hostPrios, hostIPs, serverIPs, bwSplits, ceilSplits,rate) 
    elif cfgName=="S12sli4_3prio":
        baseCfgName = 'liteCbaselineTestTokenQoS_base'  
        hostPrios = OrderedDict([('delCritical', 0),('delNonCrtical', 2),('bwCritical', 1),('bwNonCritical',2)])
        flowNumbers = OrderedDict([('VIP', 350), ('LVD', 37), ('VID', 135), ('FDO', 60), ('SSH', 100),('cVP', 100),('cF', 20),('cLV', 18)])
        hostNumbers = OrderedDict([('delCritical', 1),('delNonCrtical', 1),('bwCritical', 1),('bwNonCritical',1)])
        percentage = [100]
        for i in percentage:
            rate = 996200000*(i/100)
            bwSplits = []
            ceilSplits = []
            cfgName="S12sli4_3prio"
            if rate >= 132000000:
                bwSplits.append(OrderedDict([('delCritical', 5000000),('delNonCrtical', 0),('bwCritical',127000000),('bwNonCritical',0)]))
                ceilSplits.append(OrderedDict([('delCritical', 5000000),('delNonCrtical', 18200000*(i/100)),('bwCritical',127000000),('bwNonCritical',846000000*(i/100))]))
            else:
                bwSplits.append(OrderedDict([('delCritical', math.floor((rate/132)*5)),('delNonCrtical', 0),('bwCritical',math.floor((rate/132)*127)),('bwNonCritical',0)]))
                ceilSplits.append(OrderedDict([('delCritical', rate),('delNonCrtical', 18200000*(i/100)),('bwCritical',rate),('bwNonCritical',846000000*(i/100))]))
           

           #bwSplits.append(OrderedDict([('VIP', 0), ('LVD',0), ('VID',0), ('FDO',0), ('SSH',0),('cVP', 2*19000000*(i/100)),('cF', 2*896000000*(i/100)),('cLV', 2*85000000*(i/100))]))
           #ceiling.append(OrderedDict([('VIP', 2*9600000), ('LVD',2*286000000*(i/100)), ('VID',2*461000000*(i/100)), ('FDO',2*224000000*(i/100)), ('SSH',2*500000*(i/100)),('cVP', 2*1000e6*(i/100)),('cF', 2*1000e6*(i/100)),('cLV', 2*1000e6*(i/100))]))
            cfgName+="%s" % (i)
            generate_all_config_files3(cfgName, baseCfgName, hostNumbers, hostPrios, hostIPs, serverIPs, bwSplits, ceilSplits, flowNumbers, rate)
    

    # Default.
    else:
        print('Config name %s not found - doing nothing.' % cfgName)
        return
    
    

    # # ini - vector of bwSplits
    # generate_ini(cfgName, baseCfgName, hostNumbers, hostIPs, bwSplits)
    # generate_ini('%s' % cfgName, baseCfgName, hostNumbers, hostIPs, bwSplits, withoutHTB = True)
    # # routing.xml - skip types with number == 0?
    # generate_routing_xml(cfgName, hostNumbers, hostIPs, serverIPs)
    # # htb.xml (1 per bwSplit) - skip with number == 0
    # for bwSplit in bwSplits:
    #     longName = "%s_bw-%s" % (cfgName, "_".join(["%s_%02dk" % (k, round(v / 2)) for k, v in bwSplit.items()]))
    #     generate_htb_xml(longName, hostNumbers, hostPrios, bwSplit)


# cfgNames = [('myCfg-005', True), ('myCfg-006', False)]#, ('myCfg-005', True)]
# cfgNames = [('myCfg-007', True), ('myCfg-008', False)]
# cfgNames = [('cfg-voip-lvd-001', True), ('cfg-voip-lvd-002', False)]
# cfgNames = [('cfg-voip-vod-fdl-001', False)]
#cfgNames = [("Ddisaster2S", False),("DnoDisaster", False),("Ddisaster8S", False)]
cfgNames = [("S4sli2noGuaranteesV2Fix", False)]


for cfgName in cfgNames:
    gen_cfg(cfgName[0], cfgName[1])

# TODO: add anarcho edition as well
# TODO: maybe also a flag for cleaning files with the same prefix (and potentially even sim results with the same prefix)
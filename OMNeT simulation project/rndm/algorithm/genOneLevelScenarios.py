from cfgGenLib import *
import numpy as np
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
    hostIPs2S = OrderedDict([('VIP', '10.20.x.x'), ('LVD', '10.21.x.x'), ('VID', '10.22.x.x'), ('FDO', '10.23.x.x'), ('SSH', '10.24.x.x'),('cVP', '10.5.x.x'),('cF', '10.6.x.x'),('cLV', '10.7.x.x')])
    serverIPs2S = OrderedDict([('VIP', '10.220.0.0'), ('LVD', '10.221.0.0'), ('VID', '10.222.0.0'), ('FDO', '10.223.0.0'), ('SSH', '10.224.0.0'),('cVP', '10.15.x.x'),('cF', '10.16.x.x'),('cLV', '10.17.x.x')])    

    # myCfg-001 -- VIP + LVD, no prio
    if cfgName == 'myCfg-001':
        hostPrios = OrderedDict([('VIP', 0), ('LVD', 0), ('VID', 0), ('FDO', 0), ('SSH', 0)])
        hostNumbers = OrderedDict([('VIP', 400), ('LVD', 10), ('VID', 0), ('FDO', 0), ('SSH', 0)])
        rate = 15e6
        bwSplits = [OrderedDict([('VIP', round(p * .01 * rate)), ('LVD', round((100 - p) * .01 * rate)), ('VID', 0), ('FDO', 0), ('SSH', 0)]) for p in range(10, 100, 10)]
        baseCfgName = 'liteCbaselineTestTokenQoS_base'
    # myCfg-002 -- VIP + LVD, with prio
    elif cfgName == 'myCfg-002':
        hostPrios = OrderedDict([('VIP', 1), ('LVD', 0), ('VID', 0), ('FDO', 0), ('SSH', 0)])
        hostNumbers = OrderedDict([('VIP', 400), ('LVD', 10), ('VID', 0), ('FDO', 0), ('SSH', 0)])
        rate = 15e6
        bwSplits = [OrderedDict([('VIP', round(p * .01 * rate)), ('LVD', round((100 - p) * .01 * rate)), ('VID', 0), ('FDO', 0), ('SSH', 0)]) for p in range(10, 100, 10)]
        baseCfgName = 'liteCbaselineTestTokenQoS_base'
    # myCfg-003 -- LVD + VID scenario, no prio
    elif cfgName == 'myCfg-003':
        hostPrios = OrderedDict([('VIP', 0), ('LVD', 0), ('VID', 0), ('FDO', 0), ('SSH', 0)])
        hostNumbers = OrderedDict([('VIP', 0), ('LVD', 30), ('VID', 30), ('FDO', 0), ('SSH', 0)])
        rate = 50e6
        bwSplits = [OrderedDict([('VIP', 0), ('LVD', round((100 - p) * .01 * rate)), ('VID', round(p * .01 * rate)), ('FDO', 0), ('SSH', 0)]) for p in range(10, 100, 10)]
        baseCfgName = 'liteCbaselineTestTokenQoS_base'
    # myCfg-004 -- LVD + VID scenario, with prio
    elif cfgName == 'myCfg-004':
        hostPrios = OrderedDict([('VIP', 0), ('LVD', 1), ('VID', 0), ('FDO', 0), ('SSH', 0)])
        hostNumbers = OrderedDict([('VIP', 0), ('LVD', 30), ('VID', 30), ('FDO', 0), ('SSH', 0)])
        rate = 50e6
        bwSplits = [OrderedDict([('VIP', 0), ('LVD', round((100 - p) * .01 * rate)), ('VID', round(p * .01 * rate)), ('FDO', 0), ('SSH', 0)]) for p in range(10, 100, 10)]
        baseCfgName = 'liteCbaselineTestTokenQoS_base'
    # myCfg-005 -- LVD + VID scenario, with prio, but inverted
    elif cfgName == 'myCfg-005':
        hostPrios = OrderedDict([('VIP', 0), ('LVD', 0), ('VID', 1), ('FDO', 0), ('SSH', 0)])
        hostNumbers = OrderedDict([('VIP', 0), ('LVD', 30), ('VID', 30), ('FDO', 0), ('SSH', 0)])
        rate = 50e6
        bwSplits = [OrderedDict([('VIP', 0), ('LVD', round((100 - p) * .01 * rate)), ('VID', round(p * .01 * rate)), ('FDO', 0), ('SSH', 0)]) for p in range(10, 100, 10)]
        baseCfgName = 'liteCbaselineTestTokenQoS_base'
    # myCfg-006 -- LVD + VID scenario, with prio, but inverted -- copy of 005
    elif cfgName == 'myCfg-006':
        hostPrios = OrderedDict([('VIP', 0), ('LVD', 0), ('VID', 1), ('FDO', 0), ('SSH', 0)])
        hostNumbers = OrderedDict([('VIP', 0), ('LVD', 30), ('VID', 30), ('FDO', 0), ('SSH', 0)])
        rate = 50e6
        bwSplits = [OrderedDict([('VIP', 0), ('LVD', round((100 - p) * .01 * rate)), ('VID', round(p * .01 * rate)), ('FDO', 0), ('SSH', 0)]) for p in range(10, 100, 10)]
        baseCfgName = 'liteCbaselineTestTokenQoS_base'
    # myCfg-007 -- LVD + VID scenario, no prio
    elif cfgName == 'myCfg-007':
        hostPrios = OrderedDict([('VIP', 0), ('LVD', 0), ('VID', 0), ('FDO', 0), ('SSH', 0)])
        hostNumbers = OrderedDict([('VIP', 0), ('LVD', 30), ('VID', 30), ('FDO', 0), ('SSH', 0)])
        rate = 50e6
        bwSplits = [OrderedDict([('VIP', 0), ('LVD', round((100 - p) * .01 * rate)), ('VID', round(p * .01 * rate)), ('FDO', 0), ('SSH', 0)]) for p in range(10, 100, 10)]
        baseCfgName = 'liteCbaselineTestTokenQoS_base'
    # myCfg-008 -- LVD + VID scenario, no prio -- copy of 007 -- used for 2-level version
    elif cfgName == 'myCfg-008':
        hostPrios = OrderedDict([('VIP', 0), ('LVD', 0), ('VID', 0), ('FDO', 0), ('SSH', 0)])
        hostNumbers = OrderedDict([('VIP', 0), ('LVD', 30), ('VID', 30), ('FDO', 0), ('SSH', 0)])
        rate = 50e6
        bwSplits = [OrderedDict([('VIP', 0), ('LVD', round((100 - p) * .01 * rate)), ('VID', round(p * .01 * rate)), ('FDO', 0), ('SSH', 0)]) for p in range(10, 100, 10)]
        baseCfgName = 'liteCbaselineTestTokenQoS_base'
    # cfg-voip-lvd-001 -- LVD + VIP scenario, no prio
    elif cfgName == 'cfg-voip-lvd-001':
        hostPrios = OrderedDict([('VIP', 0), ('LVD', 0), ('VID', 0), ('FDO', 0), ('SSH', 0)])
        hostNumbers = OrderedDict([('VIP', 400), ('LVD', 10), ('VID', 0), ('FDO', 0), ('SSH', 0)])
        rate = 25e6
        bwSplits = [OrderedDict([('VIP', round(p * .01 * rate)), ('LVD', round((100 - p) * .01 * rate)), ('VID', 0), ('FDO', 0), ('SSH', 0)]) for p in range(10, 100, 10)]
        baseCfgName = 'liteCbaselineTestTokenQoS_base'
    # cfg-voip-lvd-002 -- LVD + VIP scenario, no prio -- copy of 001 -- used for 2-level version
    elif cfgName == 'cfg-voip-lvd-002':
        hostPrios = OrderedDict([('VIP', 0), ('LVD', 0), ('VID', 0), ('FDO', 0), ('SSH', 0)])
        hostNumbers = OrderedDict([('VIP', 400), ('LVD', 10), ('VID', 0), ('FDO', 0), ('SSH', 0)])
        rate = 25e6
        bwSplits = [OrderedDict([('VIP', round(p * .01 * rate)), ('LVD', round((100 - p) * .01 * rate)), ('VID', 0), ('FDO', 0), ('SSH', 0)]) for p in range(10, 100, 10)]
        baseCfgName = 'liteCbaselineTestTokenQoS_base'
    elif cfgName == 'cfg-voip-vod-fdl-001':
        hostPrios = OrderedDict([('VIP', 0), ('LVD', 0), ('VID', 0), ('FDO', 0), ('SSH', 0)])
        hostNumbers = OrderedDict([('VIP', 2), ('LVD', 0), ('VID', 2), ('FDO', 2), ('SSH', 0)])
        rate = 25e6
        bwSplits = [OrderedDict([('VIP', round(.33 * rate)), ('LVD', 0), ('VID', round(.33 * rate)), ('FDO', round(.33 * rate)), ('SSH', 0)])]
        baseCfgName = 'liteCbaselineTestTokenQoS_base'
    # 'cfg-fakevoip-vod-001' -- VoIP + VoD, 5% split steps, no prios.
    elif cfgName == 'cfg-fakevoip-vod-001':
        hostPrios = OrderedDict([('VIP', 0), ('LVD', 0), ('VID', 0), ('FDO', 0), ('SSH', 0)])
        hostNumbers = OrderedDict([('VIP', 20), ('LVD', 0), ('VID', 20), ('FDO', 0), ('SSH', 0)])
        rate = 25e6
        bwSplits = [OrderedDict([('VIP', round(p * .01 * rate)), ('LVD', 0), ('VID', round((100 - p) * .01 * rate)), ('FDO', 0), ('SSH', 0)]) for p in range(5, 100, 5)]
        baseCfgName = 'liteCbaselineTestTokenQoS_base'
    elif cfgName == '':
        bwSplits = []
        hostPrios = OrderedDict([('VIP', 0), ('LVD', 0), ('VID', 0), ('FDO', 0), ('SSH', 0)])
        hostNumbers = OrderedDict([('VIP', 35), ('LVD', 39), ('VID', 49), ('FDO', 41), ('SSH', 31)])
        rate = 100e6 #rate is in bytes
        baseCfgName = 'liteCbaselineTestTokenQoS_base'   
        setCombinations=genCombinations(98) 
        for i in setCombinations:
            cfgName=""
            bwSplits = []
            x = np.random.randint(0, 98, size=(3,))
            while sum(x) != 98: x = np.random.randint(10, 98, size=(3,))
            #x= x*1000000#because it is in bytes
            #bwSplits = [OrderedDict([('VIP', round(p * .01 * rate)), ('LVD', 0), ('VID', round((100 - p) * .01 * rate)), ('FDO', 0), ('SSH', 0)]) for p in range(5, 100, 5)]
            bwSplits.append(OrderedDict([('VIP', 1500000), ('LVD', i[0]*1000000), ('VID', i[1]*1000000), ('FDO', i[2]*1000000), ('SSH', 500000)]))
            cfgName+="v1500l%sd%sf%ss500" % (i[0],i[1],i[2])
            print(cfgName)
            generate_all_config_files(cfgName, baseCfgName, hostNumbers, hostPrios, hostIPs, serverIPs, bwSplits, useTwoLevelHTB)
    elif cfgName=="zeroNoDisaster":
        bwSplits = []
        bwSplits.append(OrderedDict([('VIP', 9600000), ('LVD',286000000), ('VID',462000000), ('FDO',224000000), ('SSH',500000),('cVP', 120000),('cF', 11200000),('cLV', 5500000)]))
        hostPrios = OrderedDict([('VIP', 1), ('LVD', 1), ('VID', 1), ('FDO', 1), ('SSH', 1),('cVP', 0),('cF', 0),('cLV', 0)])
        hostNumbers = OrderedDict([('VIP', 1), ('LVD', 1), ('VID', 242), ('FDO', 1), ('SSH', 1),('cVP', 1),('cF', 1),('cLV', 1)])
        rate = 1000 
        baseCfgName = 'liteCbaselineTestTokenQoS_base'  
        generate_all_config_files(cfgName, baseCfgName, hostNumbers, hostPrios, hostIPs, serverIPs, bwSplits,rate, useTwoLevelHTB) 
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
    elif cfgName=="Ddisaster2S":
        baseCfgName = 'liteCbaselineTestTokenQoS_base'
        hostPrios2S = OrderedDict([('nonCritical', 1),('critical', 0)])
        hostNumbers = OrderedDict([('VIP', 400), ('LVD', 260), ('VID', 485), ('FDO', 100), ('SSH', 100),('cVP', 100),('cF', 50),('cLV', 10)])
        percentage = [20,50,80]
        for i in percentage:
        #for i in range (10,100,10):
            bwSplits2S = []
            ceiling2S = []
            cfgName="Ddisaster2S"
            bwSplits2S.append(OrderedDict([('nonCritical', 0),('critical', 2*1000e6*(i/100))]))
            ceiling2S.append(OrderedDict([('nonCritical', 2*1000e6*(i/100)),('critical', 2*1000e6*(i/100))]))
            rate = 2*1000e6*(i/100) #rate is in bytes
            cfgName+="%s" % (i)
            generate_all_config_files_ceil2S(cfgName, baseCfgName, hostNumbers, hostPrios2S, hostIPs2S, serverIPs2S, bwSplits2S, ceiling2S,rate, useTwoLevelHTB) 
    elif cfgName=="cnsm":
        bwSplits = []
        bwSplits.append(OrderedDict([('VIP', 1750000), ('LVD',70000000), ('VID',54000000), ('FDO',5200000), ('SSH',70000),('cVP', 250000),('cF', 7800000),('cLV', 12500000)]))
        hostPrios = OrderedDict([('VIP', 1), ('LVD', 1), ('VID', 1), ('FDO', 1), ('SSH', 1),('cVP', 0),('cF', 0),('cLV', 0)])
        hostNumbers = OrderedDict([('VIP', 35), ('LVD', 28), ('VID', 45), ('FDO', 2), ('SSH', 10),('cVP', 5),('cF', 3),('cLV', 5)])
        rate = 1000 
        baseCfgName = 'liteCbaselineTestTokenQoS_base'  
        generate_all_config_files(cfgName, baseCfgName, hostNumbers, hostPrios, hostIPs, serverIPs, bwSplits,rate, useTwoLevelHTB)
    elif cfgName=="finalNoDisaster":
        bwSplits = []
        bwSplits.append(OrderedDict([('VIP', 17500000), ('LVD',700000000), ('VID',540000000), ('FDO',52000000), ('SSH',700000),('cVP', 5000000),('cF', 156000000),('cLV', 250000000)]))
        hostPrios = OrderedDict([('VIP', 1), ('LVD', 1), ('VID', 1), ('FDO', 1), ('SSH', 1),('cVP', 0),('cF', 0),('cLV', 0)])
        hostNumbers = OrderedDict([('VIP', 350), ('LVD', 280), ('VID', 450), ('FDO', 20), ('SSH', 100),('cVP', 100),('cF', 60),('cLV', 100)])
        rate = 1800 
        baseCfgName = 'liteCbaselineTestTokenQoS_base'  
        generate_all_config_files(cfgName, baseCfgName, hostNumbers, hostPrios, hostIPs, serverIPs, bwSplits,rate, useTwoLevelHTB)  
    
    elif cfgName=="scenario1ND":
        bwSplits = []
        bwSplits.append(OrderedDict([('VIP', 17500000), ('LVD',150000000), ('VID',540000000), ('FDO',52000000), ('SSH',700000),('cVP', 5000000),('cF', 156000000),('cLV', 75000000)]))
        hostPrios = OrderedDict([('VIP', 1), ('LVD', 1), ('VID', 1), ('FDO', 1), ('SSH', 1),('cVP', 0),('cF', 0),('cLV', 0)])
        hostNumbers = OrderedDict([('VIP', 350), ('LVD', 50), ('VID', 225), ('FDO', 20), ('SSH', 100),('cVP', 100),('cF', 60),('cLV', 25)])
        rate = 1000 
        baseCfgName = 'liteCbaselineTestTokenQoS_base'  
        generate_all_config_files(cfgName, baseCfgName, hostNumbers, hostPrios, hostIPs, serverIPs, bwSplits,rate, useTwoLevelHTB) 
    elif cfgName=="scenario2D8S":
        baseCfgName = 'liteCbaselineTestTokenQoS_base'
        hostPrios = OrderedDict([('VIP', 1), ('LVD', 1), ('VID', 1), ('FDO', 1), ('SSH', 1),('cVP', 0),('cF', 0),('cLV', 0)])
        hostNumbers = OrderedDict([('VIP', 350), ('LVD', 50), ('VID', 225), ('FDO', 20), ('SSH', 100),('cVP', 100),('cF', 60),('cLV', 25)])
        percentage = [1,5]
        for i in percentage:
            bwSplits = []
            ceiling = []
            cfgName="scenario2D8S"
            bwSplits.append(OrderedDict([('VIP', 0), ('LVD',0), ('VID',0), ('FDO',0), ('SSH',0),('cVP', 21105932*(i/100)),('cF', 658505086*(i/100)),('cLV',316588981*(i/100))]))
            ceiling.append(OrderedDict([('VIP', 17500000), ('LVD',150000000), ('VID',540000000), ('FDO',52000000), ('SSH',700000),('cVP', 9962e5*(i/100)),('cF', 9962e5*(i/100)),('cLV', 9962e5*(i/100))]))
            rate = 1000*(i/100) #rate is in bytes
            cfgName+="%s" % (i)
            generate_all_config_files_ceil(cfgName, baseCfgName, hostNumbers, hostPrios, hostIPs, serverIPs, bwSplits, ceiling, rate, useTwoLevelHTB)
    elif cfgName=="scenario3D8SG":
        baseCfgName = 'liteCbaselineTestTokenQoS_base'
        hostPrios = OrderedDict([('VIP', 1), ('LVD', 1), ('VID', 1), ('FDO', 1), ('SSH', 1),('cVP', 0),('cF', 0),('cLV', 0)])
        hostNumbers = OrderedDict([('VIP', 350), ('LVD', 50), ('VID', 225), ('FDO', 20), ('SSH', 100),('cVP', 100),('cF', 60),('cLV', 25)])
        percentage = [1,5,20,50,80]
        for i in percentage:
            bwSplits = []
            ceiling = []
            cfgName="scenario3D8SG"
            bwSplits.append(OrderedDict([('VIP', 17500000*(i/100)), ('LVD',150000000*(i/100)), ('VID',540000000*(i/100)), ('FDO',52000000*(i/100)), ('SSH',700000*(i/100)),('cVP', 5000000*(i/100)),('cF', 156000000*(i/100)),('cLV', 75000000*(i/100))]))
            #bwSplits.append(OrderedDict([('VIP', 0), ('LVD',0), ('VID',0), ('FDO',0), ('SSH',0),('cVP', 21105932*(i/100)),('cF', 658505086*(i/100)),('cLV',316588981*(i/100))]))
            ceiling.append(OrderedDict([('VIP', 17500000*(i/100)), ('LVD',150000000*(i/100)), ('VID',540000000*(i/100)), ('FDO',52000000*(i/100)), ('SSH',700000*(i/100)),('cVP', 5000000*(i/100)),('cF', 156000000*(i/100)),('cLV', 75000000*(i/100))]))
            rate = 1000*(i/100) #rate is in Mbytes
            cfgName+="%s" % (i)
            generate_all_config_files_ceil(cfgName, baseCfgName, hostNumbers, hostPrios, hostIPs, serverIPs, bwSplits, ceiling, rate, useTwoLevelHTB)
        bwSplits = []
       
        
        
        rate = 1000 
          
        generate_all_config_files(cfgName, baseCfgName, hostNumbers, hostPrios, hostIPs, serverIPs, bwSplits,rate, useTwoLevelHTB)
    

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
cfgNames = [("scenario3D8SG", False)]


for cfgName in cfgNames:
    gen_cfg(cfgName[0], cfgName[1])

# TODO: add anarcho edition as well
# TODO: maybe also a flag for cleaning files with the same prefix (and potentially even sim results with the same prefix)
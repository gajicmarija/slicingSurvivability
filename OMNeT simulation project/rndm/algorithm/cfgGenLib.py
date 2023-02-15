from collections import OrderedDict
import xml.etree.ElementTree as ET

# generate_ip_addresses('10.0.x.x', 410)
def generate_ip_addresses(ipRange, nIPs):
    ips = []
    oct3 = 0
    oct4 = 1
    for i in range(0, nIPs):
        ips.append(ipRange.replace('x.x', '%d.%d' %(oct3, oct4)))
        oct4 = oct4 + 4
        if oct4 >= 254:
            oct3 = oct3 + 1
            oct4 = 1
    return ips

# Generate INI file with configuration.
#   cfgName:        Name of the config.
#   baseCfgName:    Name of base config that is to be extended.
#   hostNumbers:    Dict with number of hosts per app type.
#   hostIPs:        Dict of host IPs per app type.
#   bwSplits:       List of dicts with bandwidth splits per app to consider.
#   withoutHTB:     Option to exclude HTB-related config for anarcho-version.
#   twoLevelHTB:    Option to use two-level HTB with leaf nodes per flow.
def generate_ini(cfgName, baseCfgName, hostNumbers, hostIPs, bwSplits, rate,withoutHTB = False, twoLevelHTB = False):
    # General config.

    for bwSplit in bwSplits:
        longName = "%s%s" % (cfgName, "".join(["%s%02d" % (k, round(v / 1e5)) for k, v in bwSplit.items()]))
        print(longName)

        if not withoutHTB:
            cfgString = '[Config %s]\n' % cfgName
        # else:
        #     cfgString = '[Config %s_anarcho]\n' % cfgName
            cfgString = cfgString + 'description = "Config %s"\n' % cfgName
            cfgString = cfgString + 'extends = %s\n\n' % baseCfgName
    
    # Recording-related extras.
    #cfgString = cfgString + '**.host*.app*.endToEndDelay:vector.vector-recording = false\n'
    #cfgString = cfgString + '**.router*.app*.txPk:vector.vector-recording = false\n'
    #cfgString = cfgString + '**.router*.app*.rxPkOk:vector.vector-recording = false\n\n'

    # Routing and hosts.
            cfgString = cfgString + '*.configurator.config = xmldoc("configs/baseQoS/%sroutingtest1.xml")\n' % cfgName
            for k, v in hostNumbers.items():
                cfgString = cfgString + '*.n%s = %d\n' % (k, v)
            cfgString = cfgString + '\n'
            
            if not withoutHTB:
                # HTB.
                activeHosts = [k for k in hostNumbers.keys() if hostNumbers[k] > 0]
                nActiveApps = len(activeHosts)
                cfgString = cfgString + '*.router*.ppp[0].queue.typename = "HtbQueue"\n'
                if twoLevelHTB:
                    nQueues = sum(hostNumbers.values())
                else:
                    nQueues = nActiveApps
                cfgString = cfgString + '*.router*.ppp[0].queue.numQueues = %d\n' % nQueues
                cfgString = cfgString + '*.router*.ppp[0].queue.queue[*].typename = "DropTailQueue"\n'
                # FIXME: rly?
                cfgString = cfgString + '*.router*.ppp[0].queue.packetCapacity = -1\n'
                cfgString = cfgString + '*.router*.ppp[0].queue.htbHysterisis = false\n'
                xmlNames = ""
                # for bwSplit in bwSplits:
                #     longName = "%s_bw-%s" % (cfgName, "_".join(["%s_%02dk" % (k, round(v / 1e3)) for k, v in bwSplit.items()]))
                xmlNames+='xmldoc("configs/htbTree/%s_htb.xml")' % cfgName
                cfgString = cfgString + '*.router*.ppp[0].queue.htbTreeConfig = %s\n' % xmlNames
                cfgString = cfgString + '*.router*.ppp[0].queue.classifier.defaultGateIndex = 0\n'
                #cfgString = cfgString + '*.router*.ppp[0].queue.classifier.packetFilters = "%s"\n' % ";".join(["*"] * nQueues)
                # Filters based on hostIPs.
                r0pdf = []
                r1pdf = []
                if not twoLevelHTB:
                    r0pdf.append('[')
                    r1pdf.append('[')
                    for h in activeHosts:
                        print(hostIPs[h])
                        if h == activeHosts[-1]:
                            r0pdf.append('expr(ipv4.srcAddress.str() =~ "%s")]' % hostIPs[h].replace('x', '*'))
                            r1pdf.append('expr(ipv4.destAddress.str() =~ "%s")]' % hostIPs[h].replace('x', '*'))
                        else:
                            r0pdf.append('expr(ipv4.srcAddress.str() =~ "%s"), ' % hostIPs[h].replace('x', '*'))
                            r1pdf.append('expr(ipv4.destAddress.str() =~ "%s"), ' % hostIPs[h].replace('x', '*'))

                    #r0pdf.append(']')
                    #r1pdf.append(']')    

                else:
                    for h in activeHosts:
                        ips = generate_ip_addresses(hostIPs[h], hostNumbers[h])
                        r0pdf.append('[')
                        r1pdf.append('[')
                        for i in range(0, hostNumbers[h]):
                            if i == hostNumbers[h]:
                                r0pdf.append('expr(ipv4.srcAddress.str() =~ "%s")]' % hostIPs[h].replace('x', '*'))
                                r1pdf.append('expr(ipv4.destAddress.str() =~ "%s")]' % hostIPs[h].replace('x', '*'))
                            else:
                                r0pdf.append('expr(ipv4.srcAddress.str() =~ "%s"), ' % ips[i])
                                r1pdf.append('expr(ipv4.destAddress.str() =~ "%s"), ' % ips[i])    
                cfgString = cfgString + '*.router0.ppp[0].queue.classifier.packetFilters = %s\n' % "".join(r0pdf)
                cfgString = cfgString + '*.router1.ppp[0].queue.classifier.packetFilters = %s\n\n' % "".join(r1pdf)
            
            # Rate and delay.
            cfgString = cfgString + '**.connFIX0.datarate = %de6 bps\n' % rate
            cfgString = cfgString + '**.connFIX0.delay = 10ms\n\n'

            # Write to file.
            if not withoutHTB:
                # myfile = open('../rndm/simulations/configs/baseQoS/%sroutingtest1.xml' % cfgName, 'wb')
                # runfile = open('../rndm/simulations/run.txt', 'a')
                # print(cfgName)
                f = open('/Users/marijagajic/omnetpp-6.0pre15/samples/rndm/simulations/omnetpp.ini', 'a')
            # else:
            #     f = open('%s_anarcho.txt' % cfgName, 'w')
            f.write(cfgString)
            #runfile.write("./runAndExportSimConfigWithCleanupSH.sh -i omnetpp.ini -c %s -s 5\n" % cfgName )
            f.close()
            #runfile.close()

# Generate XML file related to routing and IP address configuration.
def generate_routing_xml(cfgName, hostNumbers, hostIPs, serverIPs, twoLevelHTB = False):
    configElem = ET.Element('config')
    activeHosts = [k for k in hostNumbers.keys() if hostNumbers[k] > 0]
    # Host IPs.
    for h in activeHosts:
        ips = generate_ip_addresses(hostIPs[h], hostNumbers[h])
        if not twoLevelHTB:
            add_xml_subelement(
                configElem, 
                {'type': 'interface', 
                'address': hostIPs[h],
                'hosts': 'host%s[*]' % h,
                'names': 'ppp0',
                'netmask': '255.255.255.252'})
        else:
            for i in range(0, hostNumbers[h]):
                add_xml_subelement(
                    configElem, 
                    {'type': 'interface', 
                    'address': ips[i],
                    'hosts': 'host%s[%d]' % (h, i),
                    'names': 'ppp0',
                    'netmask': '255.255.255.252'})
    for h in activeHosts:
        # Router IPs.
        add_xml_subelement(
            configElem, 
            {'type': 'interface', 
            'address': hostIPs[h],
            'hosts': 'router0',
            'towards': 'host%s[*]' % h,
            'netmask': '255.255.255.252'})
    for h in activeHosts:
        # Server IPs.
        add_xml_subelement(
            configElem, 
            {'type': 'interface', 
            'address': serverIPs[h],
            'hosts': 'server%s' % h,
            'names': 'ppp0',
            'netmask': '255.255.255.252'})
    # Catch-all for router1.
    add_xml_subelement(
            configElem, 
            {'type': 'interface', 
            'address': '10.x.x.x',
            'hosts': '**',
            'netmask': '255.x.x.x'})
    xmldata = ET.tostring(configElem)
    print("opening file")
    myfile = open('/Users/marijagajic/omnetpp-6.0pre15/samples/rndm/simulations/configs/baseQoS/%sroutingtest1.xml' % cfgName, 'wb')
    myfile.write(xmldata)

# Generate an XML file with HTB structure.
# HTB tree consists of just root + individual node per app type, no per-flow nodes.
#   cfgName:        Name of the configuration, used as prefix for XML file name.
#   hostNumbers:    Dict holding number of hosts per app type.
#   hostPrios:      Dict holding priority for each app type.
#   bwSplit:        Dict holding assured rate in bps per app type.
def generate_htb_xml(cfgName, hostNumbers, hostPrios, bwSplit):
    totalRate = sum(bwSplit.values())
    configElem = ET.Element('config')
    # FIXME: from collections import OrderedDict?
    # Root node.
    add_xml_subelement(
        configElem, 
        {'type': 'class', 'id': 'root', 'fields': OrderedDict([
            ('parentId', ['NULL']), 
            ('rate', ['int', int(totalRate / 1000)]), 
            ('ceil', ['int', int(totalRate / 1000)]), 
            ('burst', ['int', 2000]), 
            ('cburst', ['int', 2000]), 
            ('level', ['int', 1]), 
            ('quantum', ['int', 1500]), 
            ('mbuffer', ['int', 60])])})
    activeHosts = [k for k in hostNumbers.keys() if hostNumbers[k] > 0]
    qNum = 0
    # Nodes per app type with corresponding rate and priority.
    for h in activeHosts:
        add_xml_subelement(
            configElem,
            {'type': 'class', 'id': 'leafhost' + h, 'fields': OrderedDict([
                ('parentId', ['root']), 
                ('rate', ['int', int(bwSplit[h] / 1000)]), 
                ('ceil', ['int', int(bwSplit[h] / 1000)]), 
                ('burst', ['int', 2000]), 
                ('cburst', ['int', 2000]), 
                ('level', ['int', 0]), 
                ('quantum', ['int', 1500]), 
                ('mbuffer', ['int', 60]),
                ('priority', [hostPrios[h]]),
                ('queueNum', ['int', qNum])])})
        qNum = qNum + 1
    xmldata = ET.tostring(configElem)
    myfile = open('/Users/marijagajic/omnetpp-6.0pre15/samples/rndm/simulations/configs/htbTree/%s_htb.xml' % cfgName, 'wb')
    myfile.write(xmldata)

# Same as generate_htb_xml, but with per-flow leaves.
def generate_htb_xml_two_level(cfgName, hostNumbers, hostPrios, bwSplit):
    totalRate = sum(bwSplit.values())
    configElem = ET.Element('config')
    # FIXME: from collections import OrderedDict?
    # Root node.
    add_xml_subelement(
        configElem, 
        {'type': 'class', 'id': 'root', 'fields': OrderedDict([
            ('parentId', ['NULL']), 
            ('rate', ['int', int(totalRate / 1000)]), 
            ('ceil', ['int', int(totalRate / 1000)]), 
            ('burst', ['int', 2000]), 
            ('cburst', ['int', 2000]), 
            ('level', ['int', 2]), 
            ('quantum', ['int', 1500]), 
            ('mbuffer', ['int', 60])])})
    activeHosts = [k for k in hostNumbers.keys() if hostNumbers[k] > 0]
    # Inner nodes per app type with corresponding rate and priority.
    for h in activeHosts:
        add_xml_subelement(
            configElem,
            {'type': 'class', 'id': 'innerconn' + h, 'fields': OrderedDict([
                ('parentId', ['root']), 
                ('rate', ['int', int(bwSplit[h] / 1000)]), 
                ('ceil', ['int', int(bwSplit[h] / 1000)]), 
                ('burst', ['int', 2000]), 
                ('cburst', ['int', 2000]), 
                ('level', ['int', 1]), 
                ('quantum', ['int', 1500]), 
                ('mbuffer', ['int', 60])])})
    # Leaf nodes per flow type with corresponding rate and priority.
    qNum = 0
    for h in activeHosts:
        for hostNum in range(0, hostNumbers[h]):
            add_xml_subelement(
                configElem,
                {'type': 'class', 'id': 'leafhost' + h + str(hostNum), 'fields': OrderedDict([
                    ('parentId', ['innerconn' + h]), 
                    # No guarantees, ceil = parent's rate.
                    ('rate', ['int', 0]),
                    ('ceil', ['int', int(bwSplit[h] / 1000)]), 
                    ('burst', ['int', 2000]), 
                    ('cburst', ['int', 2000]), 
                    ('level', ['int', 0]), 
                    ('quantum', ['int', 1500]), 
                    ('mbuffer', ['int', 60]),
                    ('priority', [hostPrios[h]]),
                    ('queueNum', ['int', qNum])])})
            qNum = qNum + 1
    xmldata = ET.tostring(configElem)
    myfile = open('../rndm/simulations/configs/htbTree/%s_htb.xml' % cfgName, 'wb')
    myfile.write(xmldata)

# Given an XML node, attach a child according to the provided specification.
#   parent: XML node to be attached to.
#   spec:   Specification of child node. 'type' defines the main tag, other keys define attributes,
#           and 'fields' contains children, i.e.,  <spec['type'] somekey="spec['somekey']"><spec['fields']['somename']>.
def add_xml_subelement(parent, spec):
    subElem = ET.SubElement(parent, spec['type'])
    for k in [k for k in spec if k != 'type' and k != 'fields']:
        subElem.set(k, spec[k])
    if 'fields' in spec:
        for k, v in spec['fields'].items():
            curField = ET.SubElement(subElem, k)
            if (len(v) == 2):
                # print("v0: %s, v1: %s" % (str(v[0]), str(v[1])))
                curField.set('type', v[0])
                curField.text = str(v[1])
            else:
                # print("v0: %s" % (str(v[0])))
                curField.text = str(v[0])

def generate_all_config_files(cfgName, baseCfgName, hostNumbers, hostPrios, hostIPs, serverIPs, bwSplits, rate,useTwoLevelHTB):
    if not useTwoLevelHTB:
        # ini - for regular and anarcho version.
        print("In generate_all_config_files")
        generate_ini(cfgName, baseCfgName, hostNumbers, hostIPs, bwSplits,rate)
        generate_ini('%s' % cfgName, baseCfgName, hostNumbers, hostIPs, bwSplits,rate, withoutHTB = True)
        # routing.xml - skip types with number == 0?
        # htb.xml (1 per bwSplit) - skip with number == 0
        for bwSplit in bwSplits:
            longName = "%s%s" % (cfgName, "".join(["%s%02d" % (k, round(v / 1e5)) for k, v in bwSplit.items()]))
            generate_htb_xml(cfgName, hostNumbers, hostPrios, bwSplit)
            generate_routing_xml(cfgName, hostNumbers, hostIPs, serverIPs)
    else:
        print("In generate_all_config_files")
        # ini - for regular and anarcho version.
        generate_ini(cfgName, baseCfgName, hostNumbers, hostIPs, bwSplits, ceiling,rate,twoLevelHTB = True)
        generate_ini('%s' % cfgName, baseCfgName, hostNumbers, hostIPs, bwSplits, ceiling, ratewithoutHTB = True)
        # routing.xml - skip types with number == 0?
        # htb.xml (1 per bwSplit) - skip with number == 0
        for bwSplit in bwSplits:
            longName = "%s%s" % (cfgName, "".join(["%s%02d" % (k, round(v / 1e5)) for k, v in bwSplit.items()]))
            generate_htb_xml_two_level(cfgName, hostNumbers, hostPrios, bwSplit)
            generate_routing_xml(cfgName, hostNumbers, hostIPs, serverIPs, twoLevelHTB = True)

def generate_all_config_files_ceil(cfgName, baseCfgName, hostNumbers, hostPrios, hostIPs, serverIPs, bwSplits, ceilings,rate, useTwoLevelHTB):
    if not useTwoLevelHTB:
        # ini - for regular and anarcho version.
        print("In generate_all_config_files")
        generate_ini_ceil(cfgName, baseCfgName, hostNumbers, hostIPs, bwSplits,ceilings,rate)
        generate_ini_ceil('%s' % cfgName, baseCfgName, hostNumbers, hostIPs, bwSplits,ceilings,rate, withoutHTB = True)
        # routing.xml - skip types with number == 0?
        # htb.xml (1 per bwSplit) - skip with number == 0
        for bwSplit,ceiling in zip(bwSplits,ceilings):
            longName = "%s%s" % (cfgName, "".join(["%s%02d" % (k, round(v / 1e5)) for k, v in bwSplit.items()]))
            generate_htb_xml_ceil(cfgName, hostNumbers, hostPrios, bwSplit,ceiling)
            generate_routing_xml(cfgName, hostNumbers, hostIPs, serverIPs)
    # else:
    #     print("In generate_all_config_files")
    #     # ini - for regular and anarcho version.
    #     generate_ini_ceill(cfgName, baseCfgName, hostNumbers, hostIPs, bwSplits, twoLevelHTB = True)
    #     generate_ini_ceil('%s' % cfgName, baseCfgName, hostNumbers, hostIPs, bwSplits, withoutHTB = True)
    #     # routing.xml - skip types with number == 0?
    #     # htb.xml (1 per bwSplit) - skip with number == 0
    #     for bwSplit in bwSplits:
    #         longName = "%s%s" % (cfgName, "".join(["%s%02d" % (k, round(v / 1e5)) for k, v in bwSplit.items()]))
    #         generate_htb_xml_two_level_ceil(cfgName, hostNumbers, hostPrios, bwSplit)
    #         generate_routing_xml(cfgName, hostNumbers, hostIPs, serverIPs, twoLevelHTB = True)

def generate_ini_ceil(cfgName, baseCfgName, hostNumbers, hostIPs, bwSplits, ceiling,rate, withoutHTB = False, twoLevelHTB = False):
    # General config.

    for bwSplit in bwSplits:
        #longName = "%s%s" % (cfgName, "".join(["%s%02d" % (k, round(v / 1e5)) for k, v in bwSplit.items()]))
        #print(longName)

        if not withoutHTB:
            cfgString = '[Config %s]\n' % cfgName
        # else:
        #     cfgString = '[Config %s_anarcho]\n' % cfgName
            cfgString = cfgString + 'description = "Config %s"\n' % cfgName
            cfgString = cfgString + 'extends = %s\n\n' % baseCfgName
    
    # Recording-related extras.
    #cfgString = cfgString + '**.host*.app*.endToEndDelay:vector.vector-recording = false\n'
    #cfgString = cfgString + '**.router*.app*.txPk:vector.vector-recording = false\n'
    #cfgString = cfgString + '**.router*.app*.rxPkOk:vector.vector-recording = false\n\n'

    # Routing and hosts.
            cfgString = cfgString + '*.configurator.config = xmldoc("configs/baseQoS/%sroutingtest1.xml")\n' % cfgName
            for k, v in hostNumbers.items():
                cfgString = cfgString + '*.n%s = %d\n' % (k, v)
            cfgString = cfgString + '\n'
            
            if not withoutHTB:
                # HTB.
                activeHosts = [k for k in hostNumbers.keys() if hostNumbers[k] > 0]
                nActiveApps = len(activeHosts)
                cfgString = cfgString + '*.router*.ppp[0].queue.typename = "HtbQueue"\n'
                if twoLevelHTB:
                    nQueues = sum(hostNumbers.values())
                else:
                    nQueues = nActiveApps
                cfgString = cfgString + '*.router*.ppp[0].queue.numQueues = %d\n' % nQueues
                cfgString = cfgString + '*.router*.ppp[0].queue.queue[*].typename = "DropTailQueue"\n'
                # FIXME: rly?
                cfgString = cfgString + '*.router*.ppp[0].queue.packetCapacity = -1\n'
                cfgString = cfgString + '*.router*.ppp[0].queue.htbHysterisis = false\n'
                xmlNames = ""
                # for bwSplit in bwSplits:
                #     longName = "%s_bw-%s" % (cfgName, "_".join(["%s_%02dk" % (k, round(v / 1e3)) for k, v in bwSplit.items()]))
                xmlNames+='xmldoc("configs/htbTree/%s_htb.xml")' % cfgName
                cfgString = cfgString + '*.router*.ppp[0].queue.htbTreeConfig = %s\n' % xmlNames
                cfgString = cfgString + '*.router*.ppp[0].queue.classifier.defaultGateIndex = 0\n'
                #cfgString = cfgString + '*.router*.ppp[0].queue.classifier.packetFilters = "%s"\n' % ";".join(["*"] * nQueues)
                # Filters based on hostIPs.
                r0pdf = []
                r1pdf = []
                if not twoLevelHTB:
                    r0pdf.append('[')
                    r1pdf.append('[')
                    for h in activeHosts:
                        print(hostIPs[h])
                        if h == activeHosts[-1]:
                            r0pdf.append('expr(ipv4.srcAddress.str() =~ "%s")]' % hostIPs[h].replace('x', '*'))
                            r1pdf.append('expr(ipv4.destAddress.str() =~ "%s")]' % hostIPs[h].replace('x', '*'))
                        else:
                            r0pdf.append('expr(ipv4.srcAddress.str() =~ "%s"), ' % hostIPs[h].replace('x', '*'))
                            r1pdf.append('expr(ipv4.destAddress.str() =~ "%s"), ' % hostIPs[h].replace('x', '*'))

                    #r0pdf.append(']')
                    #r1pdf.append(']')    

                else:
                    for h in activeHosts:
                        ips = generate_ip_addresses(hostIPs[h], hostNumbers[h])
                        r0pdf.append('[')
                        r1pdf.append('[')
                        for i in range(0, hostNumbers[h]):
                            if i == hostNumbers[h]:
                                r0pdf.append('expr(ipv4.srcAddress.str() =~ "%s")]' % hostIPs[h].replace('x', '*'))
                                r1pdf.append('expr(ipv4.destAddress.str() =~ "%s")]' % hostIPs[h].replace('x', '*'))
                            else:
                                r0pdf.append('expr(ipv4.srcAddress.str() =~ "%s"), ' % ips[i])
                                r1pdf.append('expr(ipv4.destAddress.str() =~ "%s"), ' % ips[i])    
                cfgString = cfgString + '*.router0.ppp[0].queue.classifier.packetFilters = %s\n' % "".join(r0pdf)
                cfgString = cfgString + '*.router1.ppp[0].queue.classifier.packetFilters = %s\n\n' % "".join(r1pdf)
            
            # Rate and delay.
            cfgString = cfgString + '**.connFIX0.datarate = %de6 bps\n' % rate
            cfgString = cfgString + '**.connFIX0.delay = 10ms\n\n'

            # Write to file.
            if not withoutHTB:
                # myfile = open('../rndm/simulations/configs/baseQoS/%sroutingtest1.xml' % cfgName, 'wb')
                # runfile = open('../rndm/simulations/run.txt', 'a')
                # print(cfgName)
                f = open('/Users/marijagajic/omnetpp-6.0pre15/samples/rndm/simulations/omnetpp.ini', 'a')
            # else:
            #     f = open('%s_anarcho.txt' % cfgName, 'w')
            f.write(cfgString)
            #runfile.write("./runAndExportSimConfigWithCleanupSH.sh -i omnetpp.ini -c %s -s 5\n" % cfgName )
            f.close()
            #runfile.close()

def generate_htb_xml_ceil(cfgName, hostNumbers, hostPrios, bwSplit,ceiling):
    totalRate = sum(bwSplit.values())
    configElem = ET.Element('config')
    # FIXME: from collections import OrderedDict?
    # Root node.
    add_xml_subelement(
        configElem, 
        {'type': 'class', 'id': 'root', 'fields': OrderedDict([
            ('parentId', ['NULL']), 
            ('rate', ['int', int(totalRate / 1000)]), 
            ('ceil', ['int', int(totalRate / 1000)]), 
            ('burst', ['int', 2000]), 
            ('cburst', ['int', 2000]), 
            ('level', ['int', 1]), 
            ('quantum', ['int', 1500]), 
            ('mbuffer', ['int', 60])])})
    activeHosts = [k for k in hostNumbers.keys() if hostNumbers[k] > 0]
    qNum = 0
    # Nodes per app type with corresponding rate and priority.
    for h in activeHosts:
        add_xml_subelement(
            configElem,
            {'type': 'class', 'id': 'leafhost' + h, 'fields': OrderedDict([
                ('parentId', ['root']), 
                ('rate', ['int', int(bwSplit[h] / 1000)]), 
                ('ceil', ['int', int(ceiling[h] / 1000)]), 
                ('burst', ['int', 2000]), 
                ('cburst', ['int', 2000]), 
                ('level', ['int', 0]), 
                ('quantum', ['int', 1500]), 
                ('mbuffer', ['int', 60]),
                ('priority', [hostPrios[h]]),
                ('queueNum', ['int', qNum])])})
        qNum = qNum + 1
    xmldata = ET.tostring(configElem)
    myfile = open('/Users/marijagajic/omnetpp-6.0pre15/samples/rndm/simulations/configs/htbTree/%s_htb.xml' % cfgName, 'wb')
    myfile.write(xmldata)


def generate_htb_xml_ceil2S(cfgName, hostPrios, bwSplit,ceiling):
    totalRate = sum(bwSplit.values())
    configElem = ET.Element('config')
    # FIXME: from collections import OrderedDict?
    # Root node.
    add_xml_subelement(
        configElem, 
        {'type': 'class', 'id': 'root', 'fields': OrderedDict([
            ('parentId', ['NULL']), 
            ('rate', ['int', int(totalRate / 1000)]), 
            ('ceil', ['int', int(totalRate / 1000)]), 
            ('burst', ['int', 2000]), 
            ('cburst', ['int', 2000]), 
            ('level', ['int', 1]), 
            ('quantum', ['int', 1500]), 
            ('mbuffer', ['int', 60])])})
    activeHosts = [k for k in bwSplit.keys()]
    qNum = 0
    # Nodes per app type with corresponding rate and priority.
    for h in activeHosts:
        add_xml_subelement(
            configElem,
            {'type': 'class', 'id': 'leafhost' + h, 'fields': OrderedDict([
                ('parentId', ['root']), 
                ('rate', ['int', int(bwSplit[h] / 1000)]), 
                ('ceil', ['int', int(ceiling[h] / 1000)]), 
                ('burst', ['int', 2000]), 
                ('cburst', ['int', 2000]), 
                ('level', ['int', 0]), 
                ('quantum', ['int', 1500]), 
                ('mbuffer', ['int', 60]),
                ('priority', [hostPrios[h]]),
                ('queueNum', ['int', qNum])])})
        qNum = qNum + 1
    xmldata = ET.tostring(configElem)
    myfile = open('/Users/marijagajic/omnetpp-6.0pre15/samples/rndm/simulations/configs/htbTree/%s_htb.xml' % cfgName, 'wb')
    myfile.write(xmldata)

def generate_all_config_files_ceil2S(cfgName, baseCfgName, hostNumbers, hostPrios, hostIPs, serverIPs, bwSplits, ceilings, rate,useTwoLevelHTB):
    if not useTwoLevelHTB:
        # ini - for regular and anarcho version.
        print("In generate_all_config_files")
        generate_ini_ceil(cfgName, baseCfgName, hostNumbers, hostIPs, bwSplits,ceilings,rate)
        generate_ini_ceil('%s' % cfgName, baseCfgName, hostNumbers, hostIPs, bwSplits,ceilings,rate, withoutHTB = True)
        # routing.xml - skip types with number == 0?
        # htb.xml (1 per bwSplit) - skip with number == 0
        for bwSplit,ceiling in zip(bwSplits,ceilings):
            longName = "%s%s" % (cfgName, "".join(["%s%02d" % (k, round(v / 1e5)) for k, v in bwSplit.items()]))
            generate_htb_xml_ceil2S(cfgName, hostPrios, bwSplit,ceiling)
            generate_routing_xml(cfgName, hostNumbers, hostIPs, serverIPs)

def generate_ini_ceil(cfgName, baseCfgName, hostNumbers, hostIPs, bwSplits, ceiling, rate,withoutHTB = False, twoLevelHTB = False):
    # General config.

    for bwSplit in bwSplits:
        #longName = "%s%s" % (cfgName, "".join(["%s%02d" % (k, round(v / 1e5)) for k, v in bwSplit.items()]))
        #print(longName)

        if not withoutHTB:
            cfgString = '[Config %s]\n' % cfgName
        # else:
        #     cfgString = '[Config %s_anarcho]\n' % cfgName
            cfgString = cfgString + 'description = "Config %s"\n' % cfgName
            cfgString = cfgString + 'extends = %s\n\n' % baseCfgName
    
    # Recording-related extras.
    #cfgString = cfgString + '**.host*.app*.endToEndDelay:vector.vector-recording = false\n'
    #cfgString = cfgString + '**.router*.app*.txPk:vector.vector-recording = false\n'
    #cfgString = cfgString + '**.router*.app*.rxPkOk:vector.vector-recording = false\n\n'

    # Routing and hosts.
            cfgString = cfgString + '*.configurator.config = xmldoc("configs/baseQoS/%sroutingtest1.xml")\n' % cfgName
            for k, v in hostNumbers.items():
                cfgString = cfgString + '*.n%s = %d\n' % (k, v)
            cfgString = cfgString + '\n'
            
            if not withoutHTB:
                # HTB.
                activeHosts = [k for k in hostNumbers.keys() if hostNumbers[k] > 0]
                nActiveApps = len(activeHosts)
                cfgString = cfgString + '*.router*.ppp[0].queue.typename = "HtbQueue"\n'
                if twoLevelHTB:
                    nQueues = sum(hostNumbers.values())
                else:
                    nQueues = nActiveApps
                cfgString = cfgString + '*.router*.ppp[0].queue.numQueues = 2 \n'
                cfgString = cfgString + '*.router*.ppp[0].queue.queue[*].typename = "DropTailQueue"\n'
                # FIXME: rly?
                cfgString = cfgString + '*.router*.ppp[0].queue.packetCapacity = -1\n'
                cfgString = cfgString + '*.router*.ppp[0].queue.htbHysterisis = false\n'
                xmlNames = ""
                # for bwSplit in bwSplits:
                #     longName = "%s_bw-%s" % (cfgName, "_".join(["%s_%02dk" % (k, round(v / 1e3)) for k, v in bwSplit.items()]))
                xmlNames+='xmldoc("configs/htbTree/%s_htb.xml")' % cfgName
                cfgString = cfgString + '*.router*.ppp[0].queue.htbTreeConfig = %s\n' % xmlNames
                cfgString = cfgString + '*.router*.ppp[0].queue.classifier.defaultGateIndex = 0\n'
                #cfgString = cfgString + '*.router*.ppp[0].queue.classifier.packetFilters = "%s"\n' % ";".join(["*"] * nQueues)
                # Filters based on hostIPs.
                # r0pdf = []
                # r1pdf = []
                # if not twoLevelHTB:
                #     r0pdf.append('[')
                #     r1pdf.append('[')
                #     for h in activeHosts:
                #         print(hostIPs[h])
                #         if h == activeHosts[-1]:
                #             r0pdf.append('expr(ipv4.srcAddress.str() =~ "%s")]' % hostIPs[h].replace('x', '*'))
                #             r1pdf.append('expr(ipv4.destAddress.str() =~ "%s")]' % hostIPs[h].replace('x', '*'))
                #         else:
                #             r0pdf.append('expr(ipv4.srcAddress.str() =~ "%s"), ' % hostIPs[h].replace('x', '*'))
                #             r1pdf.append('expr(ipv4.destAddress.str() =~ "%s"), ' % hostIPs[h].replace('x', '*'))

                #     #r0pdf.append(']')
                #     #r1pdf.append(']')    

                # else:
                #     for h in activeHosts:
                #         ips = generate_ip_addresses(hostIPs[h], hostNumbers[h])
                #         r0pdf.append('[')
                #         r1pdf.append('[')
                #         for i in range(0, hostNumbers[h]):
                #             if i == hostNumbers[h]:
                #                 r0pdf.append('expr(ipv4.srcAddress.str() =~ "%s")]' % hostIPs[h].replace('x', '*'))
                #                 r1pdf.append('expr(ipv4.destAddress.str() =~ "%s")]' % hostIPs[h].replace('x', '*'))
                #             else:
                #                 r0pdf.append('expr(ipv4.srcAddress.str() =~ "%s"), ' % ips[i])
                #                 r1pdf.append('expr(ipv4.destAddress.str() =~ "%s"), ' % ips[i])    
            cfgString = cfgString + '*.router0.ppp[0].queue.classifier.packetFilters = [expr(ipv4.srcAddress.str() =~ "10.0.*.*"), expr(ipv4.srcAddress.str() =~ "10.1.*.*"), expr(ipv4.srcAddress.str() =~ "10.2.*.*"), expr(ipv4.srcAddress.str() =~ "10.3.*.*"), expr(ipv4.srcAddress.str() =~ "10.4.*.*"), expr(ipv4.srcAddress.str() =~ "10.5.*.*"), expr(ipv4.srcAddress.str() =~ "10.6.*.*"), expr(ipv4.srcAddress.str() =~ "10.7.*.*")]\n'
            cfgString = cfgString + '*.router1.ppp[0].queue.classifier.packetFilters = [expr(ipv4.destAddress.str() =~ "10.0.*.*"), expr(ipv4.destAddress.str() =~ "10.1.*.*"), expr(ipv4.destAddress.str() =~ "10.2.*.*"), expr(ipv4.destAddress.str() =~ "10.3.*.*"), expr(ipv4.destAddress.str() =~ "10.4.*.*"), expr(ipv4.destAddress.str() =~ "10.5.*.*"), expr(ipv4.destAddress.str() =~ "10.6.*.*"), expr(ipv4.destAddress.str() =~ "10.7.*.*")]\n\n\n' 


            
            # Rate and delay.
            cfgString = cfgString + '**.connFIX0.datarate = %de6 bps\n' % rate
            cfgString = cfgString + '**.connFIX0.delay = 10ms\n\n'

            # Write to file.
            if not withoutHTB:
                # myfile = open('../rndm/simulations/configs/baseQoS/%sroutingtest1.xml' % cfgName, 'wb')
                # runfile = open('../rndm/simulations/run.txt', 'a')
                # print(cfgName)
                f = open('/Users/marijagajic/omnetpp-6.0pre15/samples/rndm/simulations/omnetpp.ini', 'a')
            # else:
            #     f = open('%s_anarcho.txt' % cfgName, 'w')
            f.write(cfgString)
            #runfile.write("./runAndExportSimConfigWithCleanupSH.sh -i omnetpp.ini -c %s -s 5\n" % cfgName )
            f.close()
            #runfile.close()



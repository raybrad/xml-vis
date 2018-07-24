import lxml.etree as ET
import argparse
import re
import os
import xmltodict
from pprint import pprint

def transform(args):
    tree = ET.parse(args.input_file)
    root = tree.getroot()
    # inspects=getInspect(root) 
    # detectors=getDetector(root)
    # layers=getLayer(root)
    # conditions=getCondition(root)
    # geometrys=getGeometry(root)
    # models=getModel(root)
    # variables=getVariable(root)
    sections=['section_variable','section_model','section_pwcondition','section_geometry','section_layer','section_inspect','section_advanced'] 
    jobxml=dict()
    for s in sections:
        jobxml[s]=getSection(root,s)
    pprint(jobxml)    
    # fo = open(args.output_file,"w")
    # fo.write(output)
    # fo.close()



def getInspect(root):
    # inspectTyps={"inspect1":['target1','contour1','geometry1','detgroup'],"inspect2":['target1','contour1','geometry1','target2','contour2','geometry2','detgroup']}
    # inspects=dict()
    # for k,v in inspectTyps.items(): 
    #     #inspect1
    #     inspect=dict()
    #     for anchor in root.xpath('./section_inspect/'+k):
    #         name= anchor.attrib['name']
    #         print name
    #         res=[getText(anchor, it) for it in v]
    #         for r in res:
    #             print r
    #         inspect[name]=dict(zip(v,res))
    #     inspects[k]=inspect
    # print inspects        
    for anchor in root.findall('./section_inspect/*'):
        print anchor.tag
        output=recursive_dict(anchor)
        pprint(output)
    print 'ok'
    types=["inspect1","inspect2"]
    inspects=dict()
    for t in types:
        inspect=dict()
        for anchor in root.xpath('./section_inspect/'+t):
            # print anchor.attrib['name']
            output=recursive_dict(anchor)
            # pprint(recursive_dict(anchor))
            inspect[output[0]]=output[1]
        inspects[t]=inspect
    pprint(inspects)
    return inspects
        #inspect2
def getText(anchor,ele):
    return anchor.find('./'+ele).text

def convert(xml_file, xml_attribs=True):
    with open(xml_file, "rb") as f:    # notice the "rb" mode
        d = xmltodict.parse(f, xml_attribs=xml_attribs)
        return d
def recursive_dict(element):
        return element.attrib['name'] if element.attrib else element.tag, dict(map(recursive_dict, element)) or element.text

def getDetector(root):
    # for anchor in root.xpath('./section_detector/'):
    #     <detgroup name="Det_ADI_Logic_NC">
    # for key in inspects['inspect1'].keys():
    #     print key
    # for book in root:
    #     print book
    detectors=dict()
    for anchor in root.xpath('./section_detector/detgroup'):
        # print anchor.attrib['name']
        # pprint(recursive_dict(anchor))
        output=recursive_dict(anchor)
        # pprint(recursive_dict(anchor))
        detectors[output[0]]=output[1]
    pprint(detectors) 
    return detectors

def getLayer(root):
    types=["layer_in","layer_simulate","layer_operation","layer_pvband","layer_out"]
    layers=dict()
    for t in types:
        layer=dict()
        for anchor in root.xpath('./section_layer/'+t):
            # print anchor.attrib['name']
            # pprint(recursive_dict(anchor))
            output=recursive_dict(anchor)
            # pprint(recursive_dict(anchor))
            layer[output[0]]=output[1]
        layers[t]=layer
    pprint(layers) 
    return layers

def getCondition(root):
    conditions=dict()
    for anchor in root.xpath('./section_pwcondition/pwcondition'):
        output=recursive_dict(anchor)
        conditions[output[0]]=output[1]
    pprint(conditions) 
    return conditions

def getModel(root):
    models=dict()
    for anchor in root.xpath('./section_model/model'):
        output=recursive_dict(anchor)
        models[output[0]]=output[1]
    pprint(models) 
    return models

def getGeometry(root):
    geos=dict()
    for anchor in root.xpath('./section_geometry/geometry'):
        output=recursive_dict(anchor)
        geos[output[0]]=output[1]
    pprint(geos) 
    return geos

def getVariable(root):
    types=["var","global_setting","external_file"]
    variables=dict()
    for t in types:
        variable=dict()
        for anchor in root.xpath('./section_variables/'+t):
            # print anchor.attrib['name']
            # pprint(recursive_dict(anchor))
            output=recursive_dict(anchor)
            # pprint(recursive_dict(anchor))
            variable[output[0]]=output[1]
        variables[t]=variable
    pprint(variables) 
    return variables

# def getSection(root,subs):
#     secInfos=dict()
#     for t in subs.values():
#         element=dict()
#         for anchor in root.xpath('./'+subs.keys()+'/'+t):
#             # print anchor.attrib['name']
#             # pprint(recursive_dict(anchor))
#             output=recursive_dict(anchor)
#             # pprint(recursive_dict(anchor))
#             element[output[0]]=output[1]
#         secInfos[t]=element
#     pprint(secInfos) 
#     return secInfos

def getSection(root,section):
    secInfos=dict()
    for anchor in root.findall('./'+section+'/*'):
        tag=anchor.tag
        # print tag
        # pprint(recursive_dict(anchor))
        output=recursive_dict(anchor)
        # pprint(recursive_dict(anchor))
        # pprint(output)
        element={output[0]:output[1]}
        # print element
        if tag not in secInfos.keys():
            secInfos[tag]=[]
            secInfos[tag]=[element]
        else:
            secInfos[tag].append(element)
    # pprint(secInfos) 
    return secInfos

def parse_options():
    parser = argparse.ArgumentParser(
        description="This script is used to reorgnize LMC+ xml into debug file one for later operation")
    parser.add_argument('-i', dest='input_file', required=True, help="input job xml", type=str)
    parser.add_argument('-o', dest='output_file', help="output job xml", type=str)
    return parser.parse_args()

def main():
    args = parse_options()
    transform(args)
if __name__ == '__main__':
    main()

    # for elem in root.findall('.//external_file/file'):
    #     text0=elem.text
    #     match=re.search(content,text0)
    #     if match:
    #         elem.text = 'recipe_template.xml'
    # return root

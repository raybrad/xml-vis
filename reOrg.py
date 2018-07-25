import lxml.etree as ET
import argparse
import re
import os
import copy
import json
from pprint import pprint

def transform(args):
    tree = ET.parse(args.input_file)
    root = tree.getroot()
    sections=['section_variable','section_model','section_pwcondition','section_geometry','section_layer','section_detector','section_inspect','section_advanced'] 
    jobxml=dict()
    for s in sections:
        jobxml[s]=getSection(root,s)
    # pprint(jobxml)    
    inspectTree=genInspectTree(jobxml)
    pprint(inspectTree)                        
    outDict=fixup(inspectTree)
    jsonFile=json.dumps(outDict, indent=4)
    outputfile = open("flare.json", 'w')
    outputfile.write(jsonFile)
    outputfile.close()   
    
    # fo = open(args.output_file,"w")
    # fo.write(output)
    # fo.close()

def recursive_dict(element):
    """recursive fetch subsections into dict"""
    return element.attrib['name'] if element.attrib else element.tag, dict(map(recursive_dict, element)) or element.text

def getSection(root,section):
    """parse each section info into dict"""
    secInfos=dict()
    for anchor in root.findall('./'+section+'/*'):
        tag=anchor.tag
        output=recursive_dict(anchor)
        element={output[0]:output[1]}
        if tag not in secInfos.keys():
            secInfos[tag]=dict(element)
        else:
            secInfos[tag].update(element)
    return secInfos

def nested_get_value(value, what):
    if isinstance(what, unicode):
        return 
    elif isinstance(what, list):
        for d in what:
            for result in nested_get_value(value, d):
                yield result
    elif isinstance(what, dict):
        for k, v in what.items():
            if v == value:
                yield k
            else:
                for result in nested_get_value(value, v):
                    yield result

def nested_get_key(key, what):
    if isinstance(what, unicode):
        return 
    elif isinstance(what, list):
        for d in what:
            for result in nested_get_key(key, d):
                yield result
    elif isinstance(what, dict):
        for k, v in what.items():
            if k == key:
                yield v
            else:
                for result in nested_get_key(key, v):
                    yield result

def genInspectTree(jobxml):
    """build inspection based expaneded tree"""
    woInspectXML=copy.deepcopy(jobxml)
    woInspectXML.pop('section_inspect')
    # inspectTree=copy.deepcopy(jobxml['section_inspect']) #use deep copy,otherwise generator will work on inspectTree/jobxml too
    inspectTree=expandTree(jobxml['section_inspect'],woInspectXML)    
    # for k1,v1 in expand[0].items():
    #         if match1:
    #           #<operation>SIZING(L_cafill,${Upsizefill},"O")</operation>
    #           expand2=list(nested_get_key(v1,jobxml))

    # manual method 
    # for inspectType,inspects in jobxml['section_inspect'].items():
    #     for inspectName, inspectInfo in inspects.items():
    #         for k, v in inspectInfo.items():
    #             v=v.strip('${}')
    #             expand=list(nested_get_key(v,jobxml))
    #             if expand:
    #                 inspectTree[inspectType][inspectName][k]={v:expand[0]}
    return inspectTree

def expandTree(inDict,jobxml):
    newDict=copy.deepcopy(inDict)
    if isinstance(inDict,dict):
        for k,v in inDict.items():
            if isinstance(v,str):
                v=v.strip('${}')
                if k == 'operation':
                    # opList=re.split('-|\+|\*|\^',v)
                    opList=re.split('\+|-|\*|^|\(|\)|{|}|\s+|,',v)
                    if len(opList)>1:
                        tmpDict=dict()
                        for op in set(opList):
                            expand=list(nested_get_key(op,jobxml))
                            if expand:
                                tmpDict.update({op:expand[0]})
                        if tmpDict:
                            newDict[k]={v:tmpDict}
                        return newDict
                                
            expand=list(nested_get_key(v,jobxml))
            if expand:
                # print 'expand',expand
                newDict[k]={v:expandTree(expand[0],jobxml)}
            else:
                newDict[k]=expandTree(v,jobxml)
    return newDict            

def genLayerTree(jobxml):
    """build layerTree"""
    return

def fixup(what):
    if isinstance(what, str):
        return [dict(name=what)]
    elif isinstance(what, list):
        return [dict(name=i,children=fixup(x)) for i,x in enumerate(what)]

    elif isinstance(what, dict):
        if len(what)==1:
            for x, y in sorted(what.items()):
                if isinstance(y,dict) and len(y)==1:
                    return dict(name=x, children=[fixup(y)])
                else:
                    return dict(name=x, children=fixup(y))
        else:
            dictList=list()
            for x, y in sorted(what.items()):
                if isinstance(y,dict) and len(y)==1:
                    dictList.append(dict(name=x, children=[fixup(y)]))
                else:
                    dictList.append(dict(name=x, children=fixup(y)))
            return dictList

    else:
        return None

def parse_options():
    """parse command option"""
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


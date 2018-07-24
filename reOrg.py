import lxml.etree as ET
import argparse
import re
import os
import xmltodict
from pprint import pprint
from itertools import tee
import copy

def transform(args):
    tree = ET.parse(args.input_file)
    root = tree.getroot()
    sections=['section_variable','section_model','section_pwcondition','section_geometry','section_layer','section_detector','section_inspect','section_advanced'] 
    jobxml=dict()
    for s in sections:
        jobxml[s]=getSection(root,s)
    # pprint(jobxml)    
    genTree(jobxml)
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
            secInfos[tag]=[element]
        else:
            secInfos[tag].append(element)
    return secInfos

def nested_get(key, what):
    if isinstance(what, unicode):
        return 
    elif isinstance(what, list):
        for d in what:
            for result in nested_get(key, d):
                yield result
    elif isinstance(what, dict):
        for k, v in what.items():
            if k == key:
                yield v
            else:
                for result in nested_get(key, v):
                    yield result

def genTree(jobxml):
    """build inspection based expaneded tree"""
    inspectTree=copy.deepcopy(jobxml['section_inspect']) #use deep copy,otherwise generator will work on inspectTree/jobxml too
    for inspectType,inspects in jobxml['section_inspect'].items():
        for i,inspect in enumerate(inspects):
            for inspectName, inspectInfo in inspect.items():
                for k, v in inspectInfo.items():
                    expand=list(nested_get(v,jobxml))
                    if expand:
                        inspectTree[inspectType][i][inspectName][k]={v:expand}
    pprint(inspectTree)                        

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


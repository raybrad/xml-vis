import lxml.etree as ET
import argparse
import re
import os
import xmltodict
from pprint import pprint

def transform(args):
    tree = ET.parse(args.input_file)
    root = tree.getroot()
    inspects=getInspect(root) 
    detectors=getDetector(root)
    # fo = open(args.output_file,"w")
    # fo.write(output)
    # fo.close()



def getInspect(root):
    inspectTyps={"inspect1":['target1','contour1','geometry1','detgroup'],"inspect2":['target1','contour1','geometry1','target2','contour2','geometry2','detgroup']}
    inspects=dict()
    for k,v in inspectTyps.items(): 
        #inspect1
        inspect=dict()
        for anchor in root.xpath('./section_inspect/'+k):
            name= anchor.attrib['name']
            print name
            res=[getText(anchor, it) for it in v]
            for r in res:
                print r
            inspect[name]=dict(zip(v,res))
        inspects[k]=inspect
    print inspects        
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
    for anchor in root.xpath('./section_detector/detgroup'):
        print anchor.attrib['name']
        pprint(recursive_dict(anchor))
    
    for anchor in root.xpath('./section_inspect/inspect1'):
        print anchor.attrib['name']
        pprint(recursive_dict(anchor))
    return

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

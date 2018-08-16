# -*- coding: utf-8 -*-
import json
import argparse
import xmltodict
 
def convert(xml_file, xml_attribs=True):
    with open(xml_file, "rb") as f:    # notice the "rb" mode
        d = xmltodict.parse(f, xml_attribs=xml_attribs)
        return json.dumps(d, indent=4)

def fixup(what):
    if isinstance(what, unicode):
        return [dict(name=what)]
    elif isinstance(what, list):
        return [dict(name=i,children=fixup(x)) for i,x in enumerate(what)]

    elif isinstance(what, dict):
        if len(what)==1:
            # return dict(name=what.items()[0][0], children=fixup(what.items()[0][1]))
            for x, y in sorted(what.items()):
                if isinstance(y,dict) and len(y)==1:
                    return dict(name=x, children=[fixup(y)])
                else:
                    return dict(name=x, children=fixup(y))
        else:
            # return [dict(name=x, children=[fixup(y)]) if isinstance(y,dict) else dict(name=x, children=fixup(y)) for x, y in sorted(what.items())]
            dictList=list()
            for x, y in sorted(what.items()):
                if isinstance(y,dict) and len(y)==1:
                    dictList.append(dict(name=x, children=[fixup(y)]))
                else:
                    dictList.append(dict(name=x, children=fixup(y)))
            return dictList

    else:
        return None

def main():
    parser=argparse.ArgumentParser(description='This script is used to convert xml to d3 flare.json')
    parser.add_argument('-i',dest='input_xml',required=True,help='input xml file',type=str)
    args,unknown=parser.parse_known_args()
    jsonFile=convert(args.input_xml)
    
    inDict=json.loads(jsonFile.encode('UTF-8'))
    outDict=fixup(inDict)
    jsonFile=json.dumps(outDict, indent=4)
    outputfile = open("flare.json", 'w')
    outputfile.write(jsonFile)
    outputfile.close()   





if __name__ == '__main__':
    main()

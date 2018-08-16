import json
from pprint import pprint
import xmltodict
 
def convert(xml_file, xml_attribs=True):
    with open(xml_file, "rb") as f:    # notice the "rb" mode
        d = xmltodict.parse(f, xml_attribs=xml_attribs)
        return d
jDict=convert('test.xml')
print('type',type(jDict))
# pprint(jDict)
# for k,v in jDict.items():
#     print k
#     print v

def nested_get(key, what):
    if isinstance(what, unicode):
        return
    else:
        for k, v in what.items():
            # print 'key',k
            # print 'value',v
            if k == key:
                yield v
            elif isinstance(v, dict):
                for result in nested_get(key, v):
                    yield result
            elif isinstance(v, list):
                for d in v:
                    for result in nested_get(key, d):
                        yield result
#result=nested_get("inspect1",jDict)
result=nested_get("CT_Combine_ADI_NC",jDict)
print(list(result))
# jsonFile=json.dumps(list(result), indent=4)
# outputfile = open("nest.json", 'w')
# outputfile.write(jsonFile)
# outputfile.close()   

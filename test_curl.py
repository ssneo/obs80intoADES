
import os
import requests
import xml.etree.ElementTree as ET




command = 'curl https://minorplanetcenter.net/submit_xml_test -F "ack=curl_test" -F "ac2=tlinder34@gmail.com" -F "source=<xml_output_2023_11_08_19_06_42.xml" '

#xml_filename = "xml_output_2023_11_14_12_24_01.xml"
#tree = ET.parse( xml_filename )
#root = tree.getroot()
#for child in root:
#    print( root.tag, root.attrib)
#print (root)
#stop

#req = requests.post( "https://minorplanetcenter.net/submit_xml_test", data=root )

#print (req)

res = os.system( command )

print ('res', res)

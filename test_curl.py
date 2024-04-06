
import os
import requests
import xml.etree.ElementTree as ET


#file_loc = "prep_xml_output_2024_02_18_22_39_26.xml"
#url = "https://minorplanetcenter.net/submit_xml_test"

file_loc = "prep_xml_output_2024_02_19_02_46_25.xml"
url = "https://minorplanetcenter.net/submit_xml"


#command = 'curl https://minorplanetcenter.net/submit_xml_test -F "ack=curl_test" -F "ac2=tlinder34@gmail.com" -F "source=<prep_xml_output_2024_02_18_22_39_26.xml" '

#res = os.system( command )
#print ('res', res)

files = {'source<': open(file_loc, 'r')}
values = {'ack': 'request_test', 'ac2': 'tlinder34@gmail.com'}


req = requests.post( url, files=files, data=values )

for key in req.headers:
    print (key, req.headers[key])
#print (req.headers)
print ('')
print (req.status_code)
#print (req.content)
#print (req.text)



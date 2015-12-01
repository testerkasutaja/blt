import xml.etree.ElementTree as ET
import re

tree = ET.parse('Eesti_ilukirjandus/ilukirjandus/Eesti_ilukirjandus_1990/ilu_ajalooilu.tasak.xml')
root = tree.getroot()
alls = root.findall(".//p")


for elem in root.findall('.//p'):
    s = elem.find('s').text
    print (s)
    


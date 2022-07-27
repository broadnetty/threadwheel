import requests
from lxml import etree as ET
import parser as ps


page = ''
with requests.Session() as s:
    p = s.get("https://sc.support2.veeam.local/dashboards/rnd-issues-vbr", verify=False)
    page = p.text

html_content = page
parsed_html = ET.HTML(html_content)
html_tables = parsed_html.findall("body/main/div/div/table/tbody")
first_table = html_tables[0]
rows_list = list(first_table)

threads = []

for row in rows_list:
    case = row[0][0].text  # case number
    status = row[1].text  # status
    topic = row[2].text  # topic
    engineer = row[3].text  # engineer
    assigned = row[4].text  # assigned
    created = row[5].text  # created
    modified = row[6].text  # modified
    threads.append({'case': case,'status':status, 'topic': topic, 'engineer': engineer, 'assigned' :assigned, 'created': created, 'modified': modified})

for thread in threads:
    if thread['status'] != 'Closed':
        print(thread)
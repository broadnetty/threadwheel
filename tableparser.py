import requests
from lxml import etree as ET


class parser:

    def __init__(self,
                 tracker_url="https://sc.support2.veeam.local/dashboards/rnd-issues-vbr",
                 table_path="body/main/div/div/table/tbody"):
        self.tracker_url = tracker_url
        self.table_path = table_path

    def get_data(self):
        with requests.Session() as s:
            p = s.get(self.tracker_url, verify=False)
            return p.text

    def parse_to_list(self):
        html_content = self.get_data()
        html_tables = ET.HTML(html_content).findall(self.table_path)
        rows_list = list(html_tables[0])

        threads = []

        for row in rows_list:
            '''
            case = row[0][0].text  # case number
            status = row[1].text  # status
            topic = row[2].text  # topic
            engineer = row[3].text  # engineer
            assigned = row[4].text  # assigned
            created = row[5].text  # created
            modified = row[6].text  # modified
            '''
            threads.append({
                'case': row[0][0].text,
                'status': row[1].text,
                'topic': row[2].text,
                'engineer': row[3].text,
                'assigned': row[4].text,
                'created': row[5].text,
                'modified': row[6].text
                            })

        return threads

import requests
from lxml import etree as ET
from operator import itemgetter
import numpy as np


class parser:


    def __init__(self,
                 tracker_url="https://sc.support2.veeam.local/dashboards/rnd-issues-vbr",
                 table_path="body/main/div/div/table/tbody"):
        self.tracker_url = tracker_url
        self.table_path = table_path
        self.table_data = self.parse_to_list()

    def get_raw_data(self):
        with requests.Session() as s:
            p = s.get(self.tracker_url, verify=False)
            return p.text

    def parse_to_list(self):
        html_content = self.get_raw_data()
        parsedhtml = ET.HTML(html_content)
        html_tables = parsedhtml.findall(self.table_path)
        rows_list = list(html_tables[0])

        threads = []

        for row in rows_list:

            case = row[0][0].text if len(row[0]) > 0 else None # case number

            threads.append({
                'case': case,
                'status': row[1].text,
                'topic': row[2].text,
                'engineer': row[3].text,
                'assigned': row[4].text,
                'created': row[5].text,
                'modified': row[6].text
                            })

        data = []
        for row in threads:
            set = []
            for key in row:
                set.append(row[key])
                set = ['' if i is None else i for i in set]
            data.append(set)

        return data

    def get_table_data(self):
        return self.table_data

    def refresh_data(self):
        self.table_data = self.parse_to_list()
        return self.table_data

    def sort_by_column(self, col_num=0, reverse=False):
        self.table_data = sorted(self.table_data, key=itemgetter(col_num), reverse=reverse)
        pass

    def get_engineers_list(self):
        engineers = []
        for row in self.table_data:
            if row[3] not in engineers:
                engineers.append(row[3])
        engineers.sort()
        engineers.insert(0,'All')
        return engineers

    def get_filtered_data(self, value, col_num=3):
        rows = []

        if value == 'All':
            return self.refresh_data()

        for row in self.table_data:
            if row[col_num] == value:
                rows.append(row)
        self.table_data = rows
        return self.table_data
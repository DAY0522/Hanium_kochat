import json
import pandas as pd
import requests
from tqdm import tqdm
import numpy as np
from haversine import haversine
from itertools import combinations

from kocrawl.searcher.course_searcher import CourseSearcher

class Coordinate(CourseSearcher):

    def request_geo(self, road):
        page = requests.get(self.url + self.params + self.road_type + self.address + road + self.keys + self.primary_key)
        json_data = page.json()
        return json_data


    def extraction_geo(self, test_data):
        geocode = pd.DataFrame(columns = ['name','address', 'x', 'y'])
        none = None
        for idx, road in tqdm(zip(test_data.index,test_data['address'])):
            name = str(test_data['name'][idx])
            if len(str(road)) <= 5:
                geocode = geocode.append(
                        pd.DataFrame({'name':name,
                        'address':road,
                        'x':none,
                        'y':none},
                        index=[idx]))
                continue

            json_data = self.request_geo(road)

            if json_data['response']['status'] == 'NOT_FOUND' or json_data['response']['status'] == 'ERROR':
                geocode = geocode.append(
                        pd.DataFrame({'name':name,
                        'address':road,
                        'x':none,
                        'y':none},
                        index=[idx]))
                continue

            x = json_data['response']['result']['point']['x']
            y = json_data['response']['result']['point']['y']

            geocode = geocode.append(
                pd.DataFrame({'name':name,
                        'address':road,
                        'x':float(x),
                        'y':float(y)},
                        index=[idx]))
        return geocode

    def extraction_geo(self, test_data):
        result = self.extraction_geo(test_data)

        a = (result.x[0], result.y[0])
        b = (result.x[1], result.y[1])
        c = (result.x[2], result.y[2])
        d = (result.x[3], result.y[3])

        items = [a, b, c, d]

        list_items = list(permutations(items, 2))

        list_length = []

        for i in range(12):
            xa = list_items[i][0]
            xb = list_items[i][1]
            length = haversine(xa, xb)
            list_length.append(length)
        return list_length
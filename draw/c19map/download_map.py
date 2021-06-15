#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import folium
import json
import pandas as pd
import requests
import webbrowser
from folium.plugins import HeatMap


def get_fymap_data(url_str):
    r = requests.get(url_str, timeout=5)
    """ to pandas dataframe """
    # load json
    df = pd.DataFrame(r.json())
    # find 'list'
    province_data_list = df.loc['list', 'data']
    heatmap_list = []
    # load xls
    geo_df = pd.read_excel("./area.xls")

    for data_list in province_data_list:
        # ignore empty list
        if len(data_list['city']) != 0:
            for city_dict in data_list['city']:
                # find city/area
                if city_dict['citycode'] != "" and city_dict['conNum'] != "0":
                    for index, row in geo_df.iterrows():
                        a = str(city_dict['citycode'])
                        b = str(row['area_code'])
                        if a.startswith('CN' + b):
                            # heatmap data : [lat, lon, range]
                            heat_data = [round(row['lat'], 3), round(row['lon'], 3), float(city_dict['econNum'])]
                            heatmap_list.append(heat_data)
                            break
    return heatmap_list


if __name__ == "__main__":
    map_data = get_fymap_data("https://interface.sina.cn/news/wap/fymap2020_data.d.json")
    map_osm = folium.Map(location=[35, 110], zoom_start=5)
    HeatMap(map_data, name="coronavirus", min_opacity=0.8).add_to(map_osm)
    file_path = r"./test.html"
    map_osm.save(file_path)

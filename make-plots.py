#!/usr/bin/env python3
import gmplot
import pandas as pd


data = pd.read_csv("data.csv")

gmap = gmplot.GoogleMapPlotter(0,0,4)
heat_latitudes, heat_longitudes =data["Latitude"], data["Longitude"]
latitudes, longitudes = zip(*list(set(zip(data["Latitude"], data["Longitude"]))))
gmap.heatmap(heat_latitudes, heat_longitudes, radius=40)
gmap.scatter(latitudes, longitudes, marker=True, color="#00FF00")
gmap.draw("failed_logins.html")


with open("failed_logins.html", "r") as f:
    html = f.read()
html = html.replace("/usr/local/lib/python3.6/dist-packages/gmplot/markers/00FF00.png", "00FF00.png")
with open("failed_logins.html", "w") as f:
    f.write(html)
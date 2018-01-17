import gmplot
import pandas as pd


data = pd.read_csv("data.csv")

gmap = gmplot.GoogleMapPlotter(0,0,4)
heat_latitudes, heat_longitudes =data["Latitude"], data["Longitude"]
latitudes, longitudes = zip(*list(set(zip(data["Latitude"], data["Longitude"]))))
gmap.heatmap(heat_latitudes, heat_longitudes, radius=40)
gmap.scatter(latitudes, longitudes, marker=True, color="#00FF00")
gmap.draw("failed_logins.html")

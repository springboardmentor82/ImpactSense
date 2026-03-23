import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium

# Load dataset
data = pd.read_csv("Earthquakes_Dataset.csv")
print("First 5 Rows:")
print(data.head())

print("\nDataset Info:")
print(data.info())

print("\nMissing Values:")
print(data.isnull().sum())

# Remove duplicates
data = data.drop_duplicates()

print("\nStatistical Summary:")
print(data.describe())

# -----------------------------
# Magnitude Distribution
# -----------------------------
plt.figure()
sns.histplot(data["mag"], bins=30)
plt.title("Magnitude Distribution")
plt.show()

# -----------------------------
# Depth Distribution
# -----------------------------
plt.figure()
sns.histplot(data["depth_km"], bins=30)
plt.title("Depth Distribution")
plt.show()

# -----------------------------
# Map Visualization
# -----------------------------
map_center = [data["latitude"].mean(), data["longitude"].mean()]
earthquake_map = folium.Map(location=map_center, zoom_start=2)

for i in range(len(data)):
    folium.CircleMarker(
        location=[data.iloc[i]["latitude"], data.iloc[i]["longitude"]],
        radius=2,
        color="red",
        fill=True
    ).add_to(earthquake_map)

earthquake_map.save("earthquake_map.html")

print("Map saved as earthquake_map.html")

import folium

# Create base map
map_eq = folium.Map(
    location=[data['latitude'].mean(),
              data['longitude'].mean()],
    zoom_start=2
)

# Add earthquake points
for i in range(min(300, len(data))):
    folium.CircleMarker(
        location=[data.iloc[i]['latitude'],
                  data.iloc[i]['longitude']],
        radius=3,
        color='red',
        fill=True
    ).add_to(map_eq)

# Save map
map_eq.save("earthquake_map.html")

print("Map saved successfully!")

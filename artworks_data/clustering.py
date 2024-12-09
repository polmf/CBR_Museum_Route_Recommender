import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns

data = pd.read_csv("C:/Users/lolam/Desktop/SBC_2/artworks_data/artworks_final.csv") # no va a ser necesario _4clustering

features = ["Artist", "ConstituentID", "Date", "Medium", "Date", "Style"]

# codificar cols 
le_style = LabelEncoder()
data['Style_encoded'] = le_style.fit_transform(data['Style'])

le_artist = LabelEncoder()
data['Artist_encoded'] = le_artist.fit_transform(data['Artist'])

le_medium = LabelEncoder()
data['Medium_encoded'] = le_medium.fit_transform(data['Medium'])

clustering_data = data[['Dim_cm2', 'Date', 'Style_encoded', 'Artist_encoded', 'Medium_encoded']].dropna()

# normalitzem 
scaler = StandardScaler()
clustering_data_scaled = scaler.fit_transform(clustering_data)

kmeans = KMeans(n_clusters=5, random_state=42)  # Cambia n_clusters según el análisis
clustering_data['Cluster'] = kmeans.fit_predict(clustering_data_scaled)

plt.figure(figsize=(10, 6))
sns.scatterplot(
    x=clustering_data['Date'],
    y=clustering_data['Dim_cm2'],
    hue=clustering_data['Cluster'],
    palette='viridis'
)
plt.title("Clusters de Obras de Arte")
plt.xlabel("Año")
plt.ylabel("Área (cm^2)")
plt.legend(title="Cluster")
plt.show()


cluster_summary = clustering_data.groupby('Cluster').mean()
print(cluster_summary)

# clustering_data.to_csv("artworks_clustered.csv", index=False)

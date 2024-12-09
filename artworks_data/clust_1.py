import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA

data = pd.read_csv("C:/Users/lolam/Desktop/SBC_2/artworks_data/artworks_final.csv") # no va a ser necesario _4clustering

features = ["Artist", "ConstituentID", "Date", "Medium", "Style", "Dim_cm2"]

data['ConstituentID'] = data['ConstituentID'].str.split(',').str[0].astype(float)


le_style = LabelEncoder()
data['Style_encoded'] = le_style.fit_transform(data['Style'])

le_artist = LabelEncoder()
data['Artist_encoded'] = le_artist.fit_transform(data['Artist'])

le_medium = LabelEncoder()
data['Medium_encoded'] = le_medium.fit_transform(data['Medium'])

# Crear un nuevo dataframe con las características para clustering
clustering_data = data[['Dim_cm2', 'Date', 'Style_encoded', 'Artist_encoded', 'Medium_encoded', 'ConstituentID']].dropna()

# Normalizar las características
scaler = StandardScaler()
clustering_data_scaled = scaler.fit_transform(clustering_data)

# Determinar el número óptimo de clusters usando el método del codo
inertia = []
k_range = range(1, 11)
for k in k_range:
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(clustering_data_scaled)
    inertia.append(kmeans.inertia_)

# # descomentar para visualizar el método del codo
# plt.figure(figsize=(8, 5))
# plt.plot(k_range, inertia, marker='o')
# plt.title("Método del Codo para Determinar el Número de Clusters")
# plt.xlabel("Número de Clusters")
# plt.ylabel("Inercia")
# plt.show()

# número óptimo de clusters --> 5
kmeans = KMeans(n_clusters=5, random_state=42)  
clustering_data['Cluster'] = kmeans.fit_predict(clustering_data_scaled)

# Reducir a 2 dimensiones para la visualización con PCA
pca = PCA(n_components=2)
clustering_data_pca = pca.fit_transform(clustering_data_scaled)

# Añadir las dimensiones PCA al dataframe para graficar
clustering_data['PCA1'] = clustering_data_pca[:, 0]
clustering_data['PCA2'] = clustering_data_pca[:, 1]

# Visualizar los clusters
plt.figure(figsize=(10, 6))
sns.scatterplot(
    x=clustering_data['PCA1'],
    y=clustering_data['PCA2'],
    hue=clustering_data['Cluster'],
    palette='viridis'
)
plt.title("Clusters de Obras de Arte (PCA) y los mismos features que antes")
plt.xlabel("PCA1")
plt.ylabel("PCA2")
plt.legend(title="Cluster")
plt.show()

# Analizar los clusters resultantes
cluster_summary = clustering_data.groupby('Cluster').mean()
print(cluster_summary)

# Guardar los resultados
clustering_data.to_csv("artworks_clustered.csv", index=False)

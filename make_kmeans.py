import os
import json
import numpy as np
from sklearn.cluster import MiniBatchKMeans
import pickle

with open(os.path.join("training_data", "embeddings.json"), "r") as file:
    embeddings = json.load(file)
print("Starting KMEANS")
kmeans = MiniBatchKMeans(n_clusters=10000, verbose=2, batch_size=4096)
print("converting to numpy")
X = np.array(list(embeddings.values()))
print("fitting")
kmeans.fit(X)
print("DONE WITH KMEANS")
with open("kmeans.pickle", "wb") as file:
    pickle.dump(kmeans, file)

from email.policy import default
import json 
from sklearn.neighbors import KDTree
import numpy as np
from timeit import default_timer

def main():
    with open("training_data/embeddings.json", "r") as file:
        embeddings = json.load(file)
    data = np.array(list(embeddings.values()))
    start = default_timer()
    tree = KDTree(data)
    print("tree building: ", default_timer() - start, " seconds")

if __name__ == "__main__":
    main()
    
import json
from face_recognition import load_image_file, face_encodings
import numpy as np
import os
import pandas as pd
import tqdm
import multiprocessing as mp


def single(filename):
    image = load_image_file(os.path.join("training_data", "img_align_celeba", filename))
    encoding = face_encodings(image, model="large")
    return filename, encoding
    # if encoding:
    #     data[imageid] = encoding[0].tolist()



def main():
    filenames = os.listdir(os.path.join("training_data", "img_align_celeba"))
    data = {}
    with mp.Pool() as pool:
        mapped = pool.imap_unordered(single, filenames, chunksize=32)
        for filename, encoding in tqdm.tqdm(mapped, total=len(filenames)):
            if encoding:
                data[filename] = encoding[0].tolist()

    with open(os.path.join("training_data", "embeddings.json"), "w") as file:
        json.dump(data, file)


if __name__ == "__main__":
    main()

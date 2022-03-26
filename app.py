import flask
from flask import request
import os
import base64
import json
import cv2 as cv
import numpy as np
from face_recognition import face_distance, face_encodings, load_image_file
import pandas as pd
import pickle


list_attr = None
embeddings = None
user_embedding = None
gender = None
swiped = set()
last_embedding = None
kmeans = None
decision_tracker = []

def initialize_server():
    global list_attr
    global embeddings
    global kmeans
    list_attr = pd.read_csv("training_data/list_attr_celeba.txt", index_col="imageid")

    with open(os.path.join("training_data", "embeddings.json"), "r") as file:
        embeddings = json.load(file)
    with open("kmeans.pickle", "rb") as file:
        kmeans = pickle.load(file)


initialize_server()
app = flask.Flask(__name__)

@app.route("/reset")
def reset():
    global user_embedding, gender, swiped, last_embedding, decision_tracker
    user_embedding = None
    gender = None
    swiped = set()
    last_embedding = None
    decision_tracker = []
    return flask.redirect("/")

@app.route("/")
def index():
    global user_embedding
    if user_embedding is None:
        return flask.send_from_directory("static", "upload.html")
    else:
        return flask.send_from_directory("static", "swipe.html")


@app.route("/best_image/<yesno>", methods=("POST",))
def best_image(yesno):
    global list_attr
    global gender
    global swiped
    global user_embedding
    global last_embedding

    if user_embedding is None:
        return flask.redirect("/")

    yes_lr = 1e-2
    no_lr = 1e-3
    if yesno == "yes" and last_embedding is not None:
        decision_tracker.append(1)
        idx = kmeans.predict(last_embedding.reshape(1, -1))
        centroid = kmeans.cluster_centers_[idx]
        direction = np.linalg.norm(centroid - user_embedding)
        user_embedding += yes_lr * direction
    elif yesno == "no" and last_embedding is not None:
        decision_tracker.append(-1)
        idx = kmeans.predict(last_embedding.reshape(1, -1))
        centroid = kmeans.cluster_centers_[idx]
        direction = np.linalg.norm(centroid - user_embedding)
        user_embedding -= no_lr * direction
    with open("decisions.json", "w") as file:
        json.dump(decision_tracker, file)

    filtered_list_attr: pd.DataFrame = list_attr.query(f"Male == {1 if gender == 'male' else -1}")
    filtered_list_attr: pd.DataFrame = filtered_list_attr.query(f"Attractive == 1")
    filtered_list_attr: pd.DataFrame = filtered_list_attr.query(f"Blurry == -1")

    min_dist = np.inf
    max_dist = 0
    closest_image_id = filtered_list_attr.iloc[0].name
    for i in range(len(filtered_list_attr)):
        image_id = filtered_list_attr.iloc[i].name
        if image_id not in embeddings or image_id in swiped:
            continue
        embedding = np.array(embeddings[image_id])
        dist = face_distance([user_embedding], embedding)
        if dist < min_dist:
            min_dist = dist
            closest_image_id = image_id
        if dist > max_dist:
            max_dist = dist

    swiped.add(closest_image_id)
    last_embedding = np.array(embeddings[closest_image_id])

    percent = 100 * (1 - min_dist / max_dist)

    # image_key = os.path.splitext(closest_image_id)[0]

    image = load_image_file(os.path.join("training_data", "img_align_celeba", closest_image_id))
    retval, buffer = cv.imencode(".jpg", image[:,:,::-1])
    b64 = base64.b64encode(buffer).decode("utf-8")
    return {
        "image": b64,
        "distance": min_dist[0]
    }
    # return flask.redirect(f"/image/{image_key}", code=302)

@app.route("/upload", methods=("POST", ))
def upload():
    global user_embedding
    global gender
    file = request.files["user_image"]
    gender = request.form.get("gender", "male")
    image = load_image_file(file)
    embeddings = face_encodings(image)
    if embeddings:
        user_embedding = face_encodings(image)[0]
    return flask.redirect("/")

import os

from flask import Flask, redirect, render_template, request, url_for
from databaseAPI import *

UPLOAD_FOLDER = 'media'

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route("/", methods=["POST", "GET"])
def home():
    if(request.form.get("login") == "Login"):
        naam = request.form.get("naam").lower()
        if(type(download(naam)) == list):
            return redirect(f"/{naam}")
    if(request.form.get("create") == "Create"):
        naam = request.form.get("naam").lower()
        createUser(naam)
        return redirect(f"/{naam}")
    return render_template("index.html")

@app.route("/<naam>", methods=["POST", "GET"])
def user(naam):
    pics = download(naam)

    if(request.form.get("home") is not None):
        return redirect(f"/")

    if(request.form.get("upload") == "uploaden"):
        image = request.files["image"]
        imageName = image.filename

    
        image.save(os.path.join(app.config["UPLOAD_FOLDER"], imageName))

        path = os.path.join(app.config["UPLOAD_FOLDER"], imageName)        
        upload(path, naam)
        
        return redirect(f"/{naam}")
    
    if(request.form.get("delete") is not None):
        url = request.form.get("url")
        delete(url, naam)
        return redirect(f"/{naam}")
    return render_template("user.html", naam = naam , pics = pics)



if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)

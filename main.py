from flask import Flask, request, jsonify, send_file
from werkzeug.middleware.proxy_fix import ProxyFix
from PIL import Image
from io import BytesIO
import os, env, hashlib

app = Flask(__name__)
# comment the next line if in a dev environment. or don't. works either way.
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

@app.route("/")
def root():
  return "<p>This is a microservice to handle album cover uploading. There's nothing else here.</p>"

@app.route("/upload", methods=["POST"])
def uploadImage():
    if "image" not in request.files:
        return jsonify({"error":"No image uploaded"}), 400
    if "secret" not in request.form or request.form["secret"] != env.SECRET:
        return jsonify({"error":"Invalid secret"}), 401
    imageFile = request.files["image"]
    imageFile, imageHash = hashAndSize(imageFile.read())
    # i hate that i have to do this. please just save to jpeg, why do you need to complain
    if imageFile.mode in ["RGBA","P"]: 
        imageFile = imageFile.convert("RGB")
    imageFile.save("cover.jpg")
    return jsonify({"message":"Image uploaded successfully", "hash":imageHash}), 200

# This is in case we don't need to get around caching
@app.route("/cover.jpg")
def returnImage():
    if not os.path.exists("cover.jpg"):
        return jsonify({"error": "Image not found"}), 404
    else:
        return send_file("cover.jpg",mimetype="image/jpeg")

# And this is in case we DO need to get around caching (like in Discord)
@app.route("/<hashCover>.jpg")
def returnImageHashed(hashCover):
    if not os.path.exists("cover.jpg"):
        return jsonify({"error": "Image not found"}), 404
    else:
        return send_file("cover.jpg",mimetype="image/jpeg")

def hashAndSize(image):
    image = Image.open(BytesIO(image))
    pixelData = image.getdata()
    # this is ugly but it works!
    imageBytes =  b''.join(bytes([int(v) for v in x]) for x in pixelData)
    imageHash = hashlib.md5(imageBytes).hexdigest()[:6]
    image = image.resize((256, 256), Image.Resampling.BILINEAR)
    return image, imageHash

# comment first app.run and uncomment second IF in dev environment
# uncomment first app.run and comment second IF in prod environment
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=env.PORT)
    #app.run(debug=True, port=env.PORT)

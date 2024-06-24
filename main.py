from flask import Flask, request, jsonify, send_file
from werkzeug.middleware.proxy_fix import ProxyFix
import os, env

app = Flask(__name__)
# comment the next line if in a dev environment
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

@app.route("/")
def root():
  return "<p>This is a microservice to handle album cover uploading. There's nothing else here.</p>"

@app.route("/upload", methods=["POST"])
def upload_image():
    if "image" not in request.files:
        return jsonify({"error":"No image uploaded"}), 400
    if "secret" not in request.form or request.form["secret"] != env.SECRET:
        return jsonify({"error":"Invalid secret"}), 401
    image_file = request.files["image"]
    image_file.save("cover.jpg")
    return jsonify({"message":"Image uploaded successfully"}), 200

@app.route("/cover.jpg")
def return_image():
    if not os.path.exists("cover.jpg"):
        return jsonify({"error": "Image not found"}), 404
    else:
        return send_file("cover.jpg",mimetype="image/jpeg")

# comment first app.run and uncomment second IF in dev environment
# uncomment first app.run and comment second IF in prod environment
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=env.PORT)
#  app.run(debug=True, port=env.PORT)

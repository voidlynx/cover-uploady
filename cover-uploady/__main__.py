from flask import Flask, request, jsonify, send_file
import os, env

app = Flask(__name__)

@app.route("/")
def root():
  return "<p>This is a microservice to handle album cover uploading. There's nothing else here.</p>"

@app.route("/upload", methods=["POST"])
def upload_image():
  # Check if image file is uploaded
  if "image" not in request.files:
    return jsonify({"error":"No image uploaded"}), 400

  if "secret" not in request.form or request.form["secret"] != env.SECRET:
    return jsonify({"error":"Invalid secret"}), 401
  # Get image file
  image_file = request.files["image"]

  # Save the image to specified location and filename
  image_file.save("cover.jpg")

  return jsonify({"message":"Image uploaded successfully"}), 200

@app.route("/cover.jpg")
def return_image():
  if not os.path.exists("cover.jpg"):
    return jsonify({"error": "Image not found"}), 404
  else:
    return send_file("../cover.jpg",mimetype="image/jpeg")

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=env.PORT)
#  app.run(debug=True)

# CODE GENERATED USING GEMINI, LOL
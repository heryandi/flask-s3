from flask import Flask, render_template, request
app = Flask(__name__)

@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        file = request.files["img"]
        file.save("/home/user/Desktop/test.jpg")
        return render_template("index.html", success = "Successfully uploaded")
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)

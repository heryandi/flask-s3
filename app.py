from datetime import datetime, timedelta
import base64
import hmac, hashlib

from flask import Flask, json, jsonify, render_template, request

AWS_ACCESS_KEY_ID = ""
AWS_SECRET_ACCESS_KEY = ""
S3_BUCKET_NAME = ""
S3_BUCKET_URL = "//" + S3_BUCKET_NAME + ".s3.amazonaws.com" 

app = Flask(__name__)
@app.route("/", methods=["POST", "GET"])
def index():
    return render_template("index.html", AWS_ACCESS_KEY_ID = AWS_ACCESS_KEY_ID, S3_BUCKET_URL = S3_BUCKET_URL)

@app.route("/s3signature", methods=["GET"])
def s3signature():
    filename = request.args.get("name")

    policy_object = {
        "expiration": (datetime.utcnow() + timedelta(weeks=1)).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "conditions": [
            { "bucket": S3_BUCKET_NAME },
            { "acl": "public-read" },
            [ "starts-with", "$key", "" ],
            { "success_action_status": "200" },
        ]
    }
    policy = base64.b64encode(json.dumps(policy_object).replace("\n", "").replace("\r", ""))
    signature = base64.b64encode(hmac.new(AWS_SECRET_ACCESS_KEY, policy, hashlib.sha1).digest())

    return jsonify({
        "key": filename,
        "policy": policy,
        "signature": signature
    })

if __name__ == "__main__":
    app.run(debug=True)

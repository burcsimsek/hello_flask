# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START gae_python37_app]
import os
from flask import Flask, flash, redirect, render_template, request, \
    send_from_directory, url_for
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = 'uploads'

# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "super secret key"


@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    return render_template("main.html")


@app.route("/", methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        flash('Loading')
        f = request.files['file']
        f.save(secure_filename(f.filename))
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], f.filename))
        flash('File successfully uploaded')
        return redirect(url_for('uploaded_file', filename=f.filename))


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_python37_app]

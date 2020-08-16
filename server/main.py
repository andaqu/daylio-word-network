from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import parse as p
import formatter
import csv

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload", methods=["GET", "POST"])
def upload_file():
    ## code to save file: f.save(secure_filename(f.filename))
    if request.method == "POST":
        entries = p.read(request.files["file"])
        entries = p.clean(entries)
        p.init_stopwords(request.form.getlist("langs"))
        p.init_moods()
        formatter.init_network()
        nodes, edges, avg_moods = p.form_network(entries)
        network = formatter.build_network(
            nodes, edges, avg_moods, n=int(request.form["edge_count"])
        )
        return render_template("data.html", data=network)


if __name__ == "__main__":
    app.run(debug=True)


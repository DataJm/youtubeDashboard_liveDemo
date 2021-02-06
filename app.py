from flask import Flask, render_template
import pandas as pd
from sqlalchemy import create_engine

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api_views")
def api_views():
    connection_string = "postgres://postgres:gs@localhost/youtube"
    conn = create_engine(connection_string)
    data = pd.read_sql("select * from ratings",conn)

    resultado = data.groupby("channel_title")["views","likes"].sum()

    return (
        resultado
        .sort_values(by="views", ascending=False)
        .reset_index()
        .loc[:,["channel_title","views"]]
        .head()
        .to_json(orient="records")
    )

@app.route("/api_likes")
def api_likes():
    connection_string = "postgres://postgres:gs@localhost/youtube"
    conn = create_engine(connection_string)
    data = pd.read_sql("select * from ratings",conn)

    resultado = data.groupby("channel_title")["views","likes"].sum()

    return (
        resultado
        .sort_values(by="likes", ascending=False)
        .reset_index()
        .loc[:,["channel_title","likes"]]
        .head()
        .to_json(orient="records")
    )

if __name__=="__main__":
    app.run(debug=True)
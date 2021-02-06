from flask import Flask, render_template, jsonify
import pandas as pd
from sqlalchemy import create_engine
import os

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api_views")
def api_views():
    # connection_string = "postgres://efmgtzxggrgymw:1e8233447cc2f09d464fd438566302549997b6b8adedca294b966c257cdc8444@ec2-54-211-77-238.compute-1.amazonaws.com:5432/dch7pe82dhmbtc"
    connection_string = os.environ.get('DATABASE_URL', '')
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
    # connection_string = "postgres://postgres:gs@localhost/youtube"
    connection_string = os.environ.get('DATABASE_URL', '')
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
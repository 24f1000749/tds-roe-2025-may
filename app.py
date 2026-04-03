from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import re

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

df = pd.read_json("q-fastapi-llm-query.json")

@app.get("/query")
def query(q: str, response: Response):
    response.headers["X-Email"] = "24f1000749@ds.study.iitm.ac.in"

    # Total sales
    m = re.match(r"What is the total sales of (.+) in (.+)\?", q)
    if m:
        product = m.group(1)
        city = m.group(2)

        answer = df[
            (df["product"] == product) &
            (df["city"] == city)
        ]["sales"].sum()

        return {"answer": int(answer)}

    # Sales reps count
    m = re.match(r"How many sales reps are there in (.+)\?", q)
    if m:
        region = m.group(1)

        answer = df[df["region"] == region]["rep"].nunique()

        return {"answer": int(answer)}

    # Average sales
    m = re.match(r"What is the average sales for (.+) in (.+)\?", q)
    if m:
        product = m.group(1)
        region = m.group(2)

        answer = df[
            (df["product"] == product) &
            (df["region"] == region)
        ]["sales"].mean()

        return {"answer": round(float(answer), 2)}

    # Highest sale date
    m = re.match(r"On what date did (.+) make the highest sale in (.+)\?", q)
    if m:
        rep = m.group(1)
        city = m.group(2)

        filtered = df[
            (df["rep"] == rep) &
            (df["city"] == city)
        ]

        best_row = filtered.loc[filtered["sales"].idxmax()]

        return {"answer": best_row["date"]}

    return {"answer": "Question not supported"}

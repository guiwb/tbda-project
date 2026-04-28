from pymongo import MongoClient
import pandas as pd

client = MongoClient("mongodb://localhost:27017")
db = client["atividade02"]

def list_by_date(date):
    query = {
      "mensuracao": str(date)
    }

    result = list(db.provedores.find(query))
    df = pd.DataFrame(result)

    return df.drop(columns=["_id"], errors="ignore")

def get_available_dates():
    return sorted(db.provedores.distinct("mensuracao"))

def list_all():
    result = list(db.provedores.find())
    
    df = pd.DataFrame(result)
    df["mensuracao"] = pd.to_datetime(df["mensuracao"])
    df["ano"] = df["mensuracao"].dt.year.astype(str)
    
    return df.drop(columns=["_id"], errors="ignore")
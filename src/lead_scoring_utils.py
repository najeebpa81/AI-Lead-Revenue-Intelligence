
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline

BASE = Path(__file__).resolve().parent.parent
SOURCE = BASE / "data" / "raw" / "Lead_Scoring_dataset.csv"
CAT = ["Lead Origin","Lead Source","Country","City","Specialization","What is your current occupation"]
NUM = ["TotalVisits","Total Time Spent on Website","Page Views Per Visit","Source_Quality","Is_Senior","Has_Specialization","Has_City"]
FEATURES = CAT + NUM

def prepare(raw):
    d=raw.copy()
    # Pre-contact status fields (e.g. Last Activity, Tags, Lead Quality) deliberately excluded.
    for col in CAT:
        d[col]=d[col].replace("Select",np.nan)
    d["Source_Quality"]=d["Lead Source"].isin(["Google","Direct Traffic","Organic Search","Reference"]).astype(int)
    d["Is_Senior"]=d["What is your current occupation"].isin(["Working Professional","Businessman"]).astype(int)
    d["Has_Specialization"]=d["Specialization"].notna().astype(int)
    d["Has_City"]=d["City"].notna().astype(int)
    return d[FEATURES]

def load_split():
    d=pd.read_csv(SOURCE).drop_duplicates()
    d=d.dropna(subset=["Converted"])
    train,temp=train_test_split(d,test_size=.30,random_state=42,stratify=d["Converted"])
    val,test=train_test_split(temp,test_size=.50,random_state=42,stratify=temp["Converted"])
    return train,val,test

def preprocessing():
    return ColumnTransformer([
        ("cat",Pipeline([("imputer",SimpleImputer(strategy="constant",fill_value="Unknown")),
                         ("encode",OneHotEncoder(handle_unknown="ignore",sparse_output=False))]),CAT),
        ("num",Pipeline([("imputer",SimpleImputer(strategy="median")),("scale",StandardScaler())]),NUM)
    ],sparse_threshold=0)

def tiers(prob):
    return np.where(prob>=.70,"Hot",np.where(prob>=.40,"Warm","Cold"))

def lift_at_k(y,p,k=.2):
    n=max(1,int(np.ceil(len(y)*k)))
    top=np.argsort(p)[-n:]
    return float(np.mean(np.asarray(y)[top])/np.mean(y))

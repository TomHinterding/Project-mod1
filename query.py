import pandas as pd
import pandasql as ps
import os

csv_path = os.path.join("data/", "table/", "dataset_56_vote.csv")
Data = pd.read_csv(csv_path)

FEATURE_NAME_MAP = {
    "handicapped-infants": "Handicapped infants",
    "water-project-cost-sharing": "Water project cost sharing",
    "adoption-of-the-budget-resolution": "Adoption of the budget resolution",
    "physician-fee-freeze": "Physician fee freeze",
    "el-salvador-aid": "El Salvador aid",
    "religious-groups-in-schools": "Religious groups in schools",
    "anti-satellite-test-ban": "Anti satellite test ban",
    "aid-to-nicaraguan-contras": "Aid to Nicaraguan contras",
    "mx-missile": "MX missile",
    "immigration": "Immigration",
    "synfuels-corporation-cutback": "Synfuels corporation cutback",
    "education-spending": "Education spending",
    "superfund-right-to-sue": "Superfund right to sue",
    "crime": "Crime",
    "duty-free-exports": "Duty free exports",
    "export-administration-act-south-africa": "Export Administration Act (South Africa)"
}

VOTE_LABEL_MAP = {"y": "Yes", "n": "No", "?": "Unknown"}

def query(sql):
    return ps.sqldf(sql, globals())

def raw_readable():
    df = Data.copy()
    df = df.rename(columns=FEATURE_NAME_MAP)
    for c in df.columns:
        if c != "Class":
            df[c] = df[c].map(VOTE_LABEL_MAP)
    return df

def feature_options():
    return FEATURE_NAME_MAP.copy()


#query feature is probably needed, everything else maybe not depending on how we want to proceed with the diagrams
def queryfeature(feature):
        q = query(f"""
        SELECT df.Party,
        df.feature,
        df."?count",
        df.ncount,
        df.ycount,
        ROUND(100 * (CAST(df."?count" AS FLOAT) / (df."?count" + df.ycount + df.ncount)), 2) as "?%",
        ROUND(100 * (CAST(df.ncount AS FLOAT) / (df."?count" + df.ycount + df.ncount)), 2) as "n%",
        ROUND(100 * (CAST(df.ycount AS FLOAT) / (df."?count" + df.ycount + df.ncount)), 2) as "y%"
        FROM (SELECT d.Class AS Party, '{feature}' AS feature,
        COUNT(CASE WHEN d."{feature}" = '?' THEN d."{feature}" END) AS "?count",
        COUNT(CASE WHEN d."{feature}" = 'n' THEN d."{feature}" END) AS ycount,
        COUNT(CASE WHEN d."{feature}" = 'y' THEN d."{feature}" END) AS ncount
        FROM Data d
        GROUP BY d.Class) df
        GROUP BY df.Party
        ORDER BY df.Party ASC;
        """)
        q = q[["Party", "feature", "ycount", "?count", "ncount", "y%", "?%", "n%"]]
        return q





def querySelectedfeatures(featureList):
    selectionquery = pd.DataFrame()
    for col in featureList:
          selectionquery = pd.concat([selectionquery, queryfeature(col)], ignore_index=True)
    return selectionquery 

def queryall():
    usedData = Data.drop("Class", axis=1)
    allfeatureList = usedData.columns.tolist()
    totalquery = querySelectedfeatures(allfeatureList)
    return totalquery
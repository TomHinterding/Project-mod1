import pandas as pd
import pandasql as ps
import os

csv_path = os.path.join("data/", "table/", "dataset_56_vote.csv")
Data = pd.read_csv(csv_path)
def query(sql):
    return ps.sqldf(sql, globals())
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
import streamlit as st
import pandas as pd
import io
import csv
import os
import sys
from PIL import Image

def resolve_path(path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, path)

# Load the image file
icon_path = resolve_path("icon.png")
icon_image = Image.open(icon_path)

def days_worked(data, headers, factor = 1.5):
    keys = data.keys()
    days = {}

    for key in keys:
        if(key not in days):
            days[key] = 0
        for item in data[key]:
            try:
                time_ob = float(item["TOTAL %23 DAYS ON ON BOARD"])
                time_uw = float(item["TOTAL %23 OF DAYS UNDERWAY"])
                days[key] += time_uw * factor + (time_ob - time_uw)
            except:
                print(item)

    #listOut = sorted([(k,v) for k,v in days.items()], key = lambda x:x[1])

    dictOut = {}
    for key in keys:
        nuKey = f"{key[0]}, {key[1]}"
        dictOut[nuKey] = days[key]
    
    return dictOut

def read_once(path, *keys):
    data = {}
    keys = [k.upper() for k in keys]
    with io.TextIOWrapper(path) as file:
        lines = list(csv.reader(file))
        headers = [x.strip("\n").strip("\"") for x in lines[0]]
        for line in lines[1:]:
            splitLine = [x.strip("\"").strip().upper() for x in line]
            row = {}

            if splitLine[0] != "":

                for head, rowdata in zip(headers, splitLine):
                    row[head] = rowdata
                
                keyOut = tuple([row[k] for k in keys])
                dataOut = {k:v for k,v in row.items() if k not in keys}
                if( keyOut not in data):
                    data[keyOut] = []
                data[keyOut].append(dataOut)

        headout = [k for k in headers if k not in keys]

        return headout, data    

def runFunc(sp, iil):

    if sp is not None:

        headers, data = read_once(sp, "Last Name", "First Name")

        days = days_worked(data, headers)

        #print(days)

        df = pd.DataFrame(list(days.items()), columns=['Name', 'Days Worked'])

        st.dataframe(df, hide_index=True)

    if iil is not None:

        headers, data = read_once(iil, "SHIP NAME")

        df = pd.DataFrame(list(data.items()))

    return 0

if __name__ == "__main__":

    st.set_page_config(
        page_title="Analytics Afloat",
        layout="wide",
        page_icon=icon_image
    )

    sp = st.file_uploader("Sea Pay File", type="csv")
    iil = st.file_uploader("Inspector List", type="csv")    
    
    if st.button("RUN SCRIPT"):
        if sp is not None and iil is not None:
            runFunc(sp, iil)
        else:
            st.warning("Please upload both files")

    
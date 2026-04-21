import csv

def read_once(path, *keys):
    data = {}
    with open(path, "r") as file:
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
    
def getAll(data, key, value):
    dataOut = {}
    for k, v in data.items():
        for item in v:
            if key in item and item[key] == value:
                if k not in dataOut:
                    dataOut[k] = []
                
                dataOut[k].append(item)
    
    return dataOut
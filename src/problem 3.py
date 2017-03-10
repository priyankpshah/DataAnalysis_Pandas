import os.path as Path
import os
import pandas as pd
import matplotlib.pyplot as plot

NODATA = "-9,999.00"

class CompareData:
    def __init__(self, source, destination):
        self.destination = destination
        self.source = source
        self.extracteddata = None
        self.Years = None
        self.files = None
        self.keys = ["MaxAvg", "MinAvg", "PrecAvg"]

    def checkData(self,val):
        return (val!=NODATA)

    def readData(self):
        dataframe = pd.read_csv(self.source,delimiter='\t',header=None,
                                names = ["Filename", "Year", "MaxAvg","MinAvg", "PrecAvg"])
        self.extracteddata = dataframe.sort_values(by=["Filename","Year"])

        self.Years = list(self.extracteddata['Year'].drop_duplicates())
        self.files = list(self.extracteddata['Filename'].drop_duplicates())

        self.resultcount = {"MaxAvg": [0] * len(self.Years), "MinAvg": [0] * len(self.Years), "PrecAvg": [0] * len(self.Years)}

    def compareData(self):
        for key in self.keys:
            self.getCount(key)

    def getCount(self,key):
        # Function responsible for comparing years' record for Record Temp and Precipation
        offset = 0
        year = 1
        for file in range(len(self.files)):
            tmp = float(self.extracteddata[key][len(self.Years)*offset])
            while(year<len(self.Years)* (offset+1)):
                index = year - (len(self.Years) * offset)
                val = self.extracteddata[key][year]
                filter = self.checkData(val)
                if filter:
                   if(float(val)-tmp)>0:
                       self.resultcount[key][index] += 1
                       tmp = float(val)
                year += 1
            offset += 1

    def WriteResult(self):
        with open(self.destination,"w") as f_write:
            f_write.writelines(map("{}\t{}\t{}\t{}\t\n".format,self.Years,self.resultcount["MaxAvg"]
                                   ,self.resultcount["MinAvg"],self.resultcount["PrecAvg"]))

    def drawGraph(self):
        plot.hist([self.resultcount["MaxAvg"], self.resultcount["MinAvg"], self.resultcount["PrecAvg"]])
        plot.xlabel("Frequency")
        plot.title("Yearly Frequency Histogram")
        plot.show()

if __name__ == '__main__':
    # Source Path
    relpath = Path.join(Path.dirname(__file__), os.pardir, 'answers', 'YearlyAverages.out')
    sourcepath = Path.abspath(relpath)
    # Destination Path
    outputfile = "YearHistogram.out"
    destpath = os.path.join(os.path.dirname(__file__), os.pardir, 'answers', outputfile)
    destpath = Path.abspath(destpath)

    cd = CompareData(sourcepath, destpath)
    cd.readData()

    cd.compareData()
    cd.WriteResult()
    cd.drawGraph()
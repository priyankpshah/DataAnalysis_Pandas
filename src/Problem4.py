import os.path as Path
import os
import pandas as pd

class FindPearsonCR:
    def __init__(self,yeildsource, source, destination):
        self.destination = destination
        self.source = source
        self.yeildpath = yeildsource
        self.yeilddata = None
        self.extractedData = None
        self.fileData = {}
        self.corr_data = []
        self.Files = None
        self.currentdf = None
        self.keys = ["MaxAvg", "MinAvg", "PrecAvg"]

    def readYeildFile(self):
        self.yeilddata = pd.read_csv(self.yeildpath,delimiter='\t',header=None,names=["Year","Corn"])

    def readFile(self):
        self.extractedData = pd.read_csv(self.source, delimiter='\t', header=None,
                                names=["Filename", "Year", "MaxAvg", "MinAvg", "PrecAvg"])

        self.extractedData.groupby("Filename")
        self.Files = list(self.extractedData["Filename"].drop_duplicates())
        # processData will receive data for current file only.
        for file in self.Files:
            self.fileData[file] = self.extractedData["Filename"].apply(lambda x: (x==file))
            self.processData(file)

    def processData(self,file):
        # File is merging with Corn Yeild data
        self.currentdf = self.extractedData[self.fileData[file]]
        processingframe = pd.merge(self.currentdf,self.yeilddata,on="Year")
        # Current frame and filename passed to calculate Pearson Corr and to store results.
        file_corr = self.find_pearsoncr(processingframe,file)
        self.corr_data.append(file_corr)

    def find_pearsoncr(self,frame,file):
        result = {"MaxAvg": None, "MinAvg":None, "PrecAvg":None,"Filename": file}
        print frame
        # for key in self.keys:
        #     result[key] = frame[[key,"Corn"]].corr(method='pearson').iloc[0][1]
        # return result

    def WriteResult(self):
        finaldataframe = pd.DataFrame(self.corr_data)
        for key in self.keys:
            finaldataframe[key] = finaldataframe[key].map('{:,.2f}'.format)

        finaldataframe.sort_values(by='Filename')
        finaldataframe.to_csv(self.destination,sep='\t',index=False,header=None)

if __name__ == '__main__':
    relpath = Path.join(Path.dirname(__file__), os.pardir, 'answers', 'YearlyAverages.out')
    sourcepath = Path.abspath(relpath)

    yeildpath2 = Path.join(Path.dirname(__file__), os.pardir, 'yld_data/US_corn_grain_yield.txt')
    yeildpath = Path.abspath(yeildpath2)

    outputfile = "Correlations.out"
    destpath = os.path.join(os.path.dirname(__file__), os.pardir, 'answers', outputfile)
    destpath = Path.abspath(destpath)

    fp = FindPearsonCR(yeildpath,sourcepath, destpath)
    fp.readYeildFile()
    fp.readFile()
    # fp.WriteResult()


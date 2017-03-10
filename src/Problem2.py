import pandas as pd
import os.path as Path
import os
import glob
NODATA = -9999

class CalculateAverage:
    def __init__(self):
        self.years = [1985,1986,1987,1988,1989,1990,1991,1992,1993,1994,1995,1996,1997,1998,1999,
                      2000,2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014]
        self.extractedData = None
        self.sourcepath = None
        self.destinationpath = None
        self.yr_masks = None
        self.filename = None
        self.keylist = ['MaxTemp', 'MinTemp', 'Precipation']
        self.result = {'FileName':[], 'MaxTemp': [], 'MinTemp': [], 'Precipation':[], 'Year':[]}

    def checkData(self,val):
        return (val!=NODATA)

    def findMaskedYear(self):
        self.yr_masks = {}
        for yr in self.years:
            self.yr_masks[yr] = self.extractedData['Year'].apply(lambda val: (val == yr))

    def findMean(self,key):
        res=[]
        filterdata = self.extractedData[key].apply(lambda val: self.checkData(val))
        for yr in self.years:
            maskyear = self.yr_masks[yr]
            res.append(self.extractedData[key][filterdata & maskyear].mean())
            # function will be applied to the data of current year and valid data
        return [i/10 for i in res]

    def findSum(self,key):
        result = []
        filterdata = self.extractedData[key].apply(lambda val: self.checkData(val))

        for year in self.years:
            maskyear = self.yr_masks[year]
            result.append(self.extractedData[key][filterdata & maskyear].sum())
        # function will be applied to the data of current year and valid data
        return [i/100.0 for i in result]

    def readFiles(self,file):
        data = []
        df = pd.read_csv(file,delimiter='\t',header=None,names = ["Date", "MaxTemp", "MinTemp", "Precipation"])
        df['Date'] = pd.to_datetime(df['Date'].astype(str),format='%Y%m%d')
        self.filename = os.path.basename(file)
        df['Year'] = df['Date'].apply(lambda yyyymmdd: int(str(yyyymmdd)[:4]))
        # Contains individual file data
        data.append(df)
        # Contains Data of all the files .
        self.extractedData = pd.concat(data)

    def calculate(self):
        # Calculate Requirements for each column and append it to result.
        self.result['MaxTemp'].extend(self.findMean('MaxTemp'))
        self.result['MinTemp'].extend(self.findMean('MinTemp'))
        self.result['Precipation'].extend(self.findSum('Precipation'))
        self.result['Year'].extend(self.years)
        self.result['FileName'].extend([self.filename] * len(self.years))

    def Main(self):
        # Main function that process data and call functions
        relpath = Path.join(Path.dirname(__file__), os.pardir, "wx_data/*")
        self.sourcepath = Path.abspath(relpath)

        outputfile = "YearlyAverages.out"
        destpath = os.path.join(os.path.dirname(__file__), os.pardir, 'answers', outputfile)
        self.destinationpath = Path.abspath(destpath)
        # list of all the files(wx_data)
        allfiles = glob.glob(self.sourcepath)

        for file in allfiles:
            self.readFiles(file)
            self.findMaskedYear()
            self.calculate()

    def WriteResult(self):
        finaldataframe = pd.DataFrame(self.result, columns=self.result.keys())
        finaldataframe = finaldataframe.sort_values(by=['FileName','Year'],ascending=True).fillna(value=NODATA)
        finaldataframe['Precipation'] = finaldataframe['Precipation'].replace(0.0, NODATA)
        for key in self.keylist:
            finaldataframe[key] = finaldataframe[key].map('{:,.2f}'.format)
        # Write Data in files.
        with open(self.destinationpath, "w") as f_write:
            f_write.writelines(map("{}\t{}\t{}\t{}\t{}\n".format,finaldataframe['FileName'],finaldataframe['Year'],
                                   finaldataframe['MaxTemp'],finaldataframe['MinTemp'],finaldataframe['Precipation']))


ca = CalculateAverage()
ca.Main()
ca.WriteResult()













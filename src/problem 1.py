import os.path as path
import os
import glob

NODATA = -9999
class WeatherData:
    def __init__(self,destination,source):
        self.destination = destination
        self.source = source

    def countMissingValues(self):
        result,records = [],[]
        for file in glob.glob(self.source):
            count = 0
            f_read = open(file, "r")
            for i in f_read:
                i = i.rsplit()
                if(int(i[1]) != NODATA and int(i[2]) != NODATA and int(i[3])== NODATA):
                     count += 1
            '''result contains file name and records contains count'''
            result.append(path.basename(file))
            records.append(count)
            f_read.close()
        return result,records

    def WriteResult(self, file, records):
        with open(self.destination,"w") as f_write:
            f_write.writelines(map("{}\t{}\n".format,file,records))
        f_write.close()

if __name__ == '__main__':
    # Source Path
    relpath = path.join(path.dirname(__file__), os.pardir, "wx_data/*")
    sourcepath = path.abspath(relpath)
    # Destination Path
    outputfile = "MissingPrcpData.out"
    destpath = os.path.join(os.path.dirname(__file__), os.pardir, 'answers',outputfile)
    destpath = path.abspath(destpath)

    wd = WeatherData(destpath, sourcepath)
    # Count Missing Values
    file,records = wd.countMissingValues()
    # Write Result to file
    wd.WriteResult(file,records)















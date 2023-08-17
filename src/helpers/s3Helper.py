import s3fs
import pandas as pd
from io import StringIO

class s3Helper:
    def __init__(self,key,secret,endpoint,region,bucket):
        self.fs = s3fs.S3FileSystem(
            key=key,
            secret=secret,
            client_kwargs={'endpoint_url':endpoint,'region_name':region}
        )
        self._bucket = bucket
        pass

    def walkDirectory(self,additionalPath=''):
        return self.fs.walk("{0}{1}".format(self._bucket,additionalPath))
    
    def lsDirectory(self,additionalPath=''):
        return self.fs.ls("{0}{1}".format(self._bucket,additionalPath))
    
    def writeFile(self,filePath,df):
        csv_data = df.to_csv(index=False).encode() # Convert DataFrame to CSV bytes
        # bytes_to_write = df.to_csv(None).encode() #AttributeError: 'str' object has no attribute 'to_csv'
        with self.fs.open(filePath, 'wb') as f:
            f.write(csv_data)
        return
    
    def readFile(self,filePath):
        with self.fs.open(filePath, 'rb') as f:
            df = pd.read_csv(StringIO(f.read().decode()))
        return df
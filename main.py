from typing import Union
import pandas as pd
import sys
import os
import aiofiles
import calendar,time,datetime
from fastapi import FastAPI,UploadFile,File,status,HTTPException,Response
from fastapi.responses import FileResponse
from io import StringIO
from utils.formatting import *
from utils.validation import *
app = FastAPI()



@app.post("/upload")
async def upload(response: Response,file: UploadFile = File(...)):
    #uploading the file and verifying the extention
    try:
        out_file_path = './uploads/'+ os.path.splitext(file.filename)[0] + str(calendar.timegm(time.gmtime()))+'.csv'; #adding timestamp to avoid name conflict
        async with aiofiles.open(out_file_path, 'wb') as out_file:
            content = await file.read()  # async read
            await out_file.write(content)  # async write
        if file.content_type != "text/csv":
            response.status_code = status.HTTP_415_UNSUPPORTED_MEDIA_TYPE
            return {"error":f'File {file.filename} has unsupported extension type'}
    except Exception as e:
        #print(repr(str(e)), file=sys.stdout)
        return {"message": "There was an error uploading the file"}
    #upload done and saved under ./uploads/filename.timestamp (out_file_path)
    
    try:
        #read the csv file saved locally into the object
        df = pd.read_csv(out_file_path,sep=',',header=None,lineterminator='\n')#using pandas to read the csv file into a dataframe
        print(content, file=sys.stdout)
        #validate the file according to the schema
        errors = validate_file(df)
        if errors:
            err = []
            for e in errors:
                err.append(str(e))
            response.status_code = 400
            return {"errors": err}
        
        #using pandas for fast file proccessing
        df[1] = pd.to_datetime(df[1])                    #making sure the pandas row is of datetime format
        df[2] = df[2].apply(formatName)                  #formatting name from kebab-case to Capitalized
        df[3] = df[3].apply(countryCodeToName)			 #country name formatting
        df[4] = df[4].astype(int)                        #changing column type to integer to be able to calculate revenue
        df[5] = df[5].apply(trimCurrency).astype(float)  #Trimming the 'USD' from the string column and changing type to float
        df[6] = round(df[5]*df[4])                       #Total Revenue
        df[6] = df[6].astype(int) 
        df.columns = ['ID','Release Date','Name', 'Country', 'Copies Sold', 'Copy Price', 'Total Revenue']
        df = df.sort_values('Release Date')              #sort values by 2nd column (Date)
        df['Release Date'] = df['Release Date'].dt.strftime('%d.%m.%Y')		     #formatting the date

        print(df, file=sys.stdout)
        
        #saving the file back on the disk to prepare for download
        df.to_csv(out_file_path,index=False,mode='wb',encoding='utf8',line_terminator='\n')#mode set to binary to avoid winodws changing the end-of-line to \r\n
        
    except Exception as e:
        response.status_code = 400
        return {"message": "There was an error parsing the file"}
    finally:
        await file.close()
    
    #sending the new file back to the client
    headers = {'Content-Disposition': 'attachment'}
    response.status_code = 200
    return FileResponse(out_file_path, headers=headers)
    
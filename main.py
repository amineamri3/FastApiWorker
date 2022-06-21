from typing import Union
import pandas as pd
import sys
import os
import aiofiles
import calendar,time,datetime
from fastapi import FastAPI,UploadFile,File
from io import StringIO
import pycountry

app = FastAPI()
def formatName(str):
    components = str.split('-')
    #We capitalize the first letter of each component with the 'title' method and join them together then strip the last space we added.
    return ''.join(x.title()+' ' for x in components[0:]).rstrip()

def trimCurrency(str):
	return str.replace(' USD','')


#using pycountry to convert alpha-3 country code to country name
def countryCodeToName(str):
    return pycountry.countries.get(alpha_3=str).name





@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    try:
        out_file_path = './uploads/'+ os.path.splitext(file.filename)[0] + str(calendar.timegm(time.gmtime()))+'.csv'; #adding timestamp to avoid name conflict
        async with aiofiles.open(out_file_path, 'wb') as out_file:
            content = await file.read()  # async read
            await out_file.write(content)  # async write
    except Exception as e:
        print(str(e), file=sys.stdout)
        return {"message": "There was an error uploading the file"}

    
    try:
        df = pd.read_csv(out_file_path,sep=',',header=None)
        
        df[1] = pd.to_datetime(df[1])                    #making sure the pandas row is of datetime format
        df[2] = df[2].apply(formatName)                  #formatting name from kebab-case to Capitalized
        df[3] = df[3].apply(countryCodeToName)			 #country name formatting
        df[4] = df[4].astype(int)                        #changing column type to integer to be able to calculate revenue
        df[5] = df[5].apply(trimCurrency).astype(float)  #Trimming the 'USD' from the string column and changing type to float
        df[6] = round(df[5]*df[4])                       #Total Revenue
        df[6] = df[6].astype(int) 
        df.columns = ['ID','Release Date','Name', 'Country name', 'Copies Sold', 'Copy Price', 'Total Revenue']
        df = df.sort_values('Release Date')              #sort values by 2nd column (Date)
        df['Release Date'] = df['Release Date'].dt.strftime('%d.%m.%Y')		     #formatting the date

        print(df, file=sys.stdout)
        
        df.to_csv(out_file_path,index=False)
        
    except Exception as e:
        print(str(e), file=sys.stdout)
        return {"message": "There was an error parsing the file"}
    finally:
        await file.close()
        
    return {"message": f"Successfuly uploaded {file.filename}"}
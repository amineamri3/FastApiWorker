from cgi import test
from fastapi.testclient import TestClient
from pathlib import Path
from main import app
import json

client = TestClient(app)

url = 'http://127.0.0.1:8000/upload'


def test_valid_input():
    f = {'file': ("filename",open('input.csv','rb'),"text/csv")}
    
    response = client.post('/upload',files=f)
    #print(str(response.text))
    assert response.status_code == 200
    assert response.text == "ID,Release Date,Name,Country,Copies Sold,Copy Price,Total Revenue\n2,21.12.1998,Baldurs Gate,Aruba,7777,15.23,118444\n5,08.04.2008,Assasins Creed,France,123854,24.23,3000982\n1,06.03.2012,Mass Effect 3,Åland Islands,123854,24.23,3000982\n3,21.07.2017,Fortnite,Jamaica,367,12.23,4488\n4,04.02.2019,Apex Legends,Benin,23,24.23,557\n"


def test_missing_values():
    f = {'file': ("filename",open('input2.csv','rb'),"text/csv")}
    
    response = client.post('/upload',files=f)
    #print(str(response.text))
    assert response.status_code == 400
    expected_res = {"errors": ["{row: 3, column: \"1\"}: \"2019/2//4\" is not a date","{row: 4, column: \"0\"}: \"nan\" is not integer"]}
    json_dump = json.loads(json.dumps(expected_res))
    #print(json_dump)
    #error_json = json.loads("""{"errors": ["{row: 3, column: \"1\"}: \"2019/2//4\" is not a date","{row: 4, column: \"0\"}: \"nan\" is not integer"]}""")
    response_json = json.loads(response.text)
    assert sorted(response_json.items())  == sorted(json_dump.items()) 

def test_missing_columns():
    f = {'file': ("filename",open('input3.csv','rb'),"text/csv")}
    
    response = client.post('/upload',files=f)
    #print(str(response.text))
    assert response.status_code == 400
    expected_res = {"errors": ["Invalid number of columns. The schema specifies 6, but the data frame has 5"]}
    json_dump = json.loads(json.dumps(expected_res))
    response_json = json.loads(response.text)
    assert sorted(response_json.items())  == sorted(json_dump.items()) 

def test_extra_columns():
    f = {'file': ("filename",open('input4.csv','rb'),"text/csv")}
    
    response = client.post('/upload',files=f)
    #print(str(response.text))
    assert response.status_code == 400
    expected_res = {"errors": ["Invalid number of columns. The schema specifies 6, but the data frame has 7"]}
    json_dump = json.loads(json.dumps(expected_res))
    response_json = json.loads(response.text)
    assert sorted(response_json.items())  == sorted(json_dump.items()) 
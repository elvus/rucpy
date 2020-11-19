#!/bin/bash
import json
import re
import requests
import urllib3
import zipfile
import pymongo
import glob, os

from bs4 import BeautifulSoup
from datetime import datetime
from html.parser import HTMLParser
from pymongo.errors import BulkWriteError

urllib3.disable_warnings()
urllib3.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'

def connection():
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    db = client['rucpy']
    return db

def RucZipFile():
    urls=[]
    try:
        soup=BeautifulSoup(
            requests.get("https://www.set.gov.py/portal/PARAGUAY-SET/InformesPeriodicos?folder-id=repository:collaboration:/sites/PARAGUAY-SET/categories/SET/Informes%20Periodicos/listado-de-ruc-con-sus-equivalencias", timeout=10,
            headers={'user-agent': 'Mozilla/5.0'}, verify=True).text, "html.parser")
        tags = soup.find("div",{'class': "uiContentBox"})
        for a in tags.findAll('a'):
            url="https://www.set.gov.py"
            soup=BeautifulSoup(
                requests.get(url+a.get("href"), timeout=10,
                headers={'user-agent': 'Mozilla/5.0'}, verify=True).text, "html.parser")
            tags = soup.find("div",{'class': "detailContainer"})
            urls.append(url+tags.find("a").get("href"))
        return urls    
    except requests.ConnectionError as e:
        print(e)
    except Exception as e:
        print(e)

def DonwloadFile():
    urls=RucZipFile()
    for url in urls:
        name="ruc{}.zip".format(urls.index(url))
        r = requests.get(url, stream = True)
        with open(name, "wb") as ruczip:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    ruczip.write(chunk)
        
        archive = zipfile.ZipFile(name)
        archive.extractall()
        if os.path.exists(name):
            os.remove(name)
        else:
            print("The file does not exist :c")

def ImportData():
    DonwloadFile()
    rucs=[]
    db=connection()
    for file in glob.glob("*.txt"):
        if file != 'requirements.txt':
            with open(file) as fp:
                for line in fp:
                    data=line.splitlines()[0].split("|")
                    razon=data[1].split(", ")

                    if len(razon)<2:
                        rucs.append({
                            "documento":data[0],
                            "dv":data[2],
                            "razonsocial":razon[0]
                        })
                    else:
                        rucs.append({
                            "documento":data[0],
                            "dv": data[2],
                            "razonsocial":razon[1]+" "+razon[0]
                        })
            if os.path.exists(file):
                os.remove(file)
            else:
                print("The file does not exist :c")
    try:
        db.contribuyentes.insert_many(rucs)
        db.contribuyentes.create_index("documento", unique=True)
    except pymongo.errors.DuplicateKeyError:
        pass
    except BulkWriteError as exc:
        exc.details

import json
import random
import urllib.request
import json
from urllib.error import HTTPError
import csv
import urllib.parse

api_key = '5f0c4de627a9354bdfcac23fbaacc3d2'

def get_url_data(url):
    request = urllib.request.Request(url)
    result = urllib.request.urlopen(request)
    result_text = result.read()
    text = result_text.decode(encoding='utf-8', errors='ignore')
    data = json.loads(text)
    return data


def get_gender(id):
    url = f'https://api.themoviedb.org/3/person/{id}?api_key={api_key}&language=en-US'
    data = get_url_data(url)
    return data.get('gender')


def get_bday(id):
    url = f'https://api.themoviedb.org/3/person/{id}?api_key={api_key}&language=en-US'
    data = get_url_data(url)
    return data.get('birthday')

if __name__ == '__main__':

    f = open('dataset.json')
    data = json.load(f)

    name_id = {x.get("name"): x.get("id") for x in data}

    with open('results.csv', newline='') as csvfile, open('newresults2.csv',"w+") as newfile:
        csvreader = csv.DictReader(csvfile)
        csvwriter = csv.DictWriter(newfile,['name', 'gender', 'place_of_birth', 'birthday', 'profile_url', 'popularity',  'latitude', 'longitude'])
        csvwriter.writeheader()
        c = 1
        for actor in csvreader:
            actor_id = name_id.get(actor['name'])
            print(f"row number {c}")
            c += 1
            # actor_gender = get_gender(actor_id)
            actor_bday = get_bday(actor_id)
            actor.update({'birthday' : actor_bday})
            # actor.update({'gender' : actor_gender})
            # actor.update({'longitude': float(actor['longitude']) + random.uniform(-0.01,0.01)})
            # actor.update({'latitude': float(actor['latitude']) + random.uniform(-0.01,0.01)})
            csvwriter.writerow(actor)
            

    
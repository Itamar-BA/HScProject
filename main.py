import urllib.request
import json

api_key = '5f0c4de627a9354bdfcac23fbaacc3d2'

def get_actors(person_id):
    url = f'https://api.themoviedb.org/3/person/{person_id}?api_key={api_key}&language=en-US'
    request = urllib.request.Request(url)
    result = urllib.request.urlopen(request)
    resulttext = result.read()
    text = resulttext.decode(encoding='utf-8', errors='ignore')
    data = json.loads(text)

def fix_data_list(actors):
    ret_list = []
    for actor in actors:
        ret_list.append([actor['name'],actor['id'],actor['popularity']])
    return ret_list


def get_popular(page_num):
    ret_list = []
    for i in range(1,page_num):
        url = f'https://api.themoviedb.org/3/person/popular?' \
              f'api_key={api_key}&language=en-US&' \
              f'page={i}'
        request = urllib.request.Request(url)
        result = urllib.request.urlopen(request)
        resulttext = result.read()
        text = resulttext.decode(encoding='utf-8', errors='ignore')
        data = json.loads(text)
        for actor in data['results']:
            ret_list.append({"name": actor['name'],"id": actor['id'],"popularity": actor['popularity']})
    return ret_list

def get_birth_place(actors):
    name_pob = []
    for actor in actors:
        url = f'https://api.themoviedb.org/3/person/{actor["id"]}?api_key={api_key}&language=en-US'
        request = urllib.request.Request(url)
        result = urllib.request.urlopen(request)
        resulttext = result.read()
        text = resulttext.decode(encoding='utf-8', errors='ignore')
        data = json.loads(text)
        if 'place_of_birth' in data: # and data['place_of_birth'] is not None:
            name_pob.append({"name": actor['name'], "popularity": actor['popularity'], "place_of_birth": data['place_of_birth']})
    return name_pob

if __name__ == '__main__':
    #get_actors(6193)
    popular_actors = get_popular(3)
    mapping = get_birth_place(popular_actors)
    print("yo")
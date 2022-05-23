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
    print("yo")

def fix_data_list(actors):
    ret_list = []
    for actor in actors:
        ret_list.append([actor['name'],actor['id'],actor['popularity']])
    return ret_list


def get_popular(page_num):
    url = f'https://api.themoviedb.org/3/person/popular?' \
          f'api_key={api_key}&language=en-US&' \
          f'page={page_num}'
    request = urllib.request.Request(url)
    result = urllib.request.urlopen(request)
    resulttext = result.read()
    text = resulttext.decode(encoding='utf-8', errors='ignore')
    data = json.loads(text)
    return fix_data_list(data['results'])

if __name__ == '__main__':
    #get_actors(6193)
    popular_actors = []
    for i in range(1,10):
        popular_actors.append(get_popular(i))
    print("yo")
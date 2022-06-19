import os.path
import urllib.request
import json
from urllib.error import HTTPError
# import pdfplumber

api_key = '5f0c4de627a9354bdfcac23fbaacc3d2'


def dataset_to_list(path_to_dataset):
    with open(path_to_dataset,"r+") as file:
        return json.load(file)


def get_url_data(url):
    request = urllib.request.Request(url)
    result = urllib.request.urlopen(request)
    result_text = result.read()
    text = result_text.decode(encoding='utf-8', errors='ignore')
    data = json.loads(text)
    return data


def get_movie_char(actor_id):
    try:
        url = f"https://api.themoviedb.org/3/person/{actor_id}/" \
              f"movie_credits?api_key=5f0c4de627a9354bdfcac23fbaacc3d2&language=en-US"
        data = get_url_data(url)
    except HTTPError as err:
        if err.code != 200:
            print(f"{err} for movie_char of id {curr_id}, skipping...")
            return []

    ret_list = []
    for curr_movie in data['cast']:
        ret_list.append({"title": curr_movie['title'],
                         "character": curr_movie['character'],
                         "rating": curr_movie['vote_average'],
                         "vote_count": curr_movie['vote_count']})

    return ret_list


def create_database(max_id):
    data = None

    for curr_id in range(1, max_id):
        url = f"https://api.themoviedb.org/3/person/{curr_id}?api_key=5f0c4de627a9354bdfcac23fbaacc3d2&language=en-US"
        try:
            data = get_url_data(url)
        except HTTPError as err:
            if err.code != 200:
                print(f"Error {err} for id {curr_id}, skipping...")
                continue

        # Check if place of birth exists -> if true, check if he's american
        birth_place = data.get('place_of_birth')
        places = ['United States', 'USA', 'U.S.']
        is_american = any(place in birth_place for place in places) if birth_place else False
        is_actor = data['known_for_department'] == "Acting"

        if is_actor and is_american:
            movie_info = get_movie_char(curr_id)
            actor = {"name": data['name'],
                             "id": curr_id,
                             "place_of_birth": birth_place,
                             "movie_info": movie_info}
            # new_data = json.stringify(actor)
            write_json(actor)


def write_json(new_data, filename='dataset.json'):
    with open(filename, 'r+') as file:
        # First we load existing data into a dict.
        file_data = json.load(file)
        # Join new_data with file_data inside emp_details
        file_data.append(new_data)
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file, indent=4)


def extract_word_count(name_of_char, path_to_script):
    lines = []
    set_of_names = set()
    with open(path_to_script, "r+") as script_file:
        lines = script_file.readlines()
        for line in lines:
            set_of_names.add(line[:line.find("=")])
        print("yo")


def calc_popularity(mapping):
    path_to_scripts = r'/Users/iBenatar/PycharmProjects/HScProject/scripts/parsed'
    path_to_dialogues = os.path.join(path_to_scripts,'dialogue')
    if not os.path.isdir(path_to_dialogues):
        print("Could not find path to dialogue (scripts) dir.")
        exit(1)
    suffix = "_dialogue.txt"
    for actor in mapping:
        counter_found = 0
        counter_not_found = 0
        for movie in actor['movie_info']:
            path_to_movie = os.path.join(path_to_dialogues,movie['title'].replace(" ","-").replace(":","")) + suffix
            if os.path.isfile(path_to_movie):
                # print(path_to_movie)
                counter_found+=1
                word_count = extract_word_count(movie['character'],path_to_movie)
            else:
                counter_not_found+=1
                # print(f"Couldn't find {movie['title']} in dialogue script folder")
        print(f"TOTAL SCRIPTS FOR {actor['name']}: FOUND - {counter_found}, NOT FOUND - {counter_not_found}")


def create_empty_json():
    f = open("./dataset.json", "w")
    json.dump([], f, indent=4)
    f.close()



if __name__ == '__main__':
    create_empty_json()
    create_database(40000)

    # popular_actors = get_popular(2)
    # mapping = get_birth_place(popular_actors)
    # test = [{'name': 'Brad Pitt', 'id': 287,'place_of_birth': 'Shawnee, Oklahoma, USA',
    #         'movie_info':[{'title': 'Troy', 'character':'Achilles','rating': 7.1, 'vote_count':8514},
    #                       {'title': '12 Years a Slave', 'character':'Samuel Bass','rating': 8.0, 'vote_count':9705},
    #                       {'title': 'Fight Club','character':'Tyler Durden','rating': 8.4, 'vote_count':24204}]}]
    # test = dataset_to_list(r'/Users/iBenatar/PycharmProjects/HScProject/dataset.json')
    # pop_mapping = calc_popularity(test)
    # print("yo")

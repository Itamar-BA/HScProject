import os.path
import urllib.request
import json
from urllib.error import HTTPError
# import pdfplumber

api_key = '5f0c4de627a9354bdfcac23fbaacc3d2'
scripts_used = set()
scripts_total_wc = {}


def dataset_to_list(path_to_dataset):
    # dir = os.path.dirname(__file__)
    # filename = os.path.join(dir, path_to_dataset)
    with open(path_to_dataset ,"r+") as file:
        return json.load(file)



def get_url_data(url):
    request = urllib.request.Request(url)
    result = urllib.request.urlopen(request)
    result_text = result.read()
    text = result_text.decode(encoding='utf-8', errors='ignore')
    data = json.loads(text)
    return data


def get_movie_char(actor_id):
    url = f"https://api.themoviedb.org/3/person/{actor_id}/" \
          f"movie_credits?api_key=5f0c4de627a9354bdfcac23fbaacc3d2&language=en-US"
    data = get_url_data(url)
    ret_list = []
    for curr_movie in data['cast']:
        ret_list.append({"title": curr_movie['title'],
                         "character": curr_movie['character'],
                         "rating": curr_movie['vote_average'],
                         "vote_count": curr_movie['vote_count']})

    return ret_list


def create_database(max_id):
    ret_list = []
    with open("./dataset.json", "w") as f:
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
                json_obj = json.dumps(actor, indent=4)
                f.write(json_obj)
            else:
                print(f"is actor = {is_actor}, birth = {birth_place}")

def scripts_to_wc():
    global scripts_total_wc
    path_to_scripts = r'scripts/parsed'
    path_to_dialogues = os.path.join(path_to_scripts,'dialogue')
    if not os.path.isdir(path_to_dialogues):
        print("Could not find path to dialogue (scripts) dir.")
        exit(1)
    suffix = "_dialogue.txt"
    for file in os.listdir(path_to_dialogues):
        path_to_file = os.path.join(path_to_dialogues,file)
        if os.path.isfile(path_to_file) and file.endswith(suffix):
            with open(path_to_file, "r+") as script_file:
                word_count = 0
                lines = script_file.readlines()
                for line in lines:
                    sentence_start = line.find(">")
                    if sentence_start != -1:
                        word_count += len(line[:sentence_start].replace("\n", ""))
                    else:
                        print("DEBUG - COULDN'T FIND '>' IN LINE 2")
        if word_count != 0:
            scripts_total_wc[file[:file.find(suffix)].lower()] = word_count

def extract_word_count(name_of_char, path_to_script, script_name):
    dict_to_lines = {}
    word_count = 0
    name_to_list = name_of_char.split(" ")
    set_of_names = set()
    with open(path_to_script, "r+") as script_file:
        lines = script_file.readlines()
        for line in lines:
            line_name = line[:line.find("=")]
            dict_to_lines[line_name] = dict_to_lines.get(line_name,0) + 1
            for sub_name in name_to_list:
                if sub_name.lower() in line_name.lower():
                    sentence_start = line.find(">")
                    if sentence_start != -1:
                        word_count += len(line[:sentence_start].replace("\n", ""))
                        break
                    else:
                        print("DEBUG - COULDN'T FIND '>' IN LINE 2")
    # print(f"COUNT WORD = {word_count}")
    global scripts_total_wc
    if script_name.lower() in scripts_total_wc:
        return word_count / scripts_total_wc[script_name.lower()]
    return 0.0


def calc_popularity(mapping):
    path_to_scripts = r'scripts/parsed'
    path_to_dialogues = os.path.join(path_to_scripts,'dialogue')
    if not os.path.isdir(path_to_dialogues):
        print("Could not find path to dialogue (scripts) dir.")
        exit(1)
    suffix = "_dialogue.txt"
    for actor in mapping:
        counter_found = 0
        counter_not_found = 0
        for movie in actor['movie_info']:
            movie_fixed_name = movie['title'].replace(" ", "-").replace(":", "")
            path_to_movie = os.path.join(path_to_dialogues, movie_fixed_name + suffix)
            if os.path.isfile(path_to_movie):

                global scripts_used
                scripts_used.add(movie_fixed_name)
                # print(path_to_movie)
                counter_found+=1
                if movie['character'] == "":
                    print(f"DEBUG - Character name EMPTY for {actor['name']} in {movie_fixed_name}")
                else:
                    word_count = extract_word_count(movie['character'],path_to_movie, movie_fixed_name)
                    print(f"DEBUG - WORD COUNT: {word_count}")
            else:
                # print(f"DEBUG - Couldn't find movie script: {movie['title']}")
                pass
                # print(f"Couldn't find {movie['title']} in dialogue script folder")
        # print(f"TOTAL SCRIPTS FOR {actor['name']}: FOUND - {counter_found}, NOT FOUND - {counter_not_found}")


if __name__ == '__main__':
    # create_database(100)
    # popular_actors = get_popular(2)
    # mapping = get_birth_place(popular_actors)
    test = dataset_to_list(r'dataset.json')
    scripts_to_wc()
    pop_mapping = calc_popularity(test)
    print("DEBUG")

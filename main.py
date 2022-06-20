import os.path
import urllib.request
import json
from urllib.error import HTTPError
import csv
import urllib.parse

api_key = '5f0c4de627a9354bdfcac23fbaacc3d2'
scripts_used = set()
scripts_total_wc = {}
avg_word_count = 0.0
DEBUG1 = False
DEBUG2 = True


def create_empty_json():
    f = open("./dataset.json", "w")
    json.dump([], f, indent=4)
    f.close()


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
    data = None
    try:
        url = f"https://api.themoviedb.org/3/person/{actor_id}/" \
              f"movie_credits?api_key=5f0c4de627a9354bdfcac23fbaacc3d2&language=en-US"
        data = get_url_data(url)
    except HTTPError as err:
        if err.code != 200:
            print(f"{err} for movie_char of id {actor_id}, skipping...")
            return []

    ret_list = []
    for curr_movie in data['cast']:
        ret_list.append({"title": curr_movie['title'],
                         "character": curr_movie['character'],
                         "rating": curr_movie['vote_average'],
                         "vote_count": curr_movie['vote_count']})

    return ret_list

def address_to_coords(address):
    url = 'https://nominatim.openstreetmap.org/search/' + urllib.parse.quote(address) +'?format=json'
    data = get_url_data(url)
    longitude = data[0]["lon"]
    latitude = data[0]["lat"]
    return longitude, latitude


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

def process_scripts():
    global scripts_total_wc,avg_word_count
    num_of_movies = 0
    path_to_scripts = os.path.join("scripts", "parsed")
    # path_to_scripts = r'scripts/parsed'
    path_to_dialogues = os.path.join(path_to_scripts,'dialogue')
    if not os.path.isdir(path_to_dialogues):
        print("Could not find path to dialogue (scripts) dir.")
        exit(1)
    suffix = "_dialogue.txt"
    for file in os.listdir(path_to_dialogues):
        path_to_file = os.path.join(path_to_dialogues, file)
        if os.path.isfile(path_to_file) and file.endswith(suffix):
            with open(path_to_file, "r+", encoding='utf-8', errors='ignore') as script_file:
                total_wc = 0
                set_of_names = set()
                num_of_actors = 0
                movie_avg = 0
                actor_wc_dict = {}
                num_of_movies += 1
                lines = script_file.readlines()
                for line in lines:
                    sentence_start = line.find(">")
                    actor_name = line[:line.find("=")]
                    if sentence_start != -1:
                        sentence_to_add = line[sentence_start + 1:].replace("\n", "")
                        actor_sentence = sentence_to_add.split(" ")
                        if len(actor_sentence) > 0:
                            set_of_names.add(actor_name)
                            # actor_wc_dict[actor_name] = actor_wc_dict.get(actor_name, 0) + len(actor_sentence)
                            total_wc += len(actor_sentence)

                # for name in actor_wc_dict:
                #     num_of_actors += 1
                #     movie_avg += actor_wc_dict[name]
                if total_wc != 0:
                    # movie_avg = movie_avg * 1000 / (total_wc * num_of_actors)
                    movie_avg = 1000 / len(set_of_names)
                    avg_word_count = (avg_word_count + movie_avg) / num_of_movies
                    scripts_total_wc[file[:file.find(suffix)].lower()] = total_wc
    if DEBUG1:
        print(f"AVG WORD COUNT: {avg_word_count}")


def extract_word_count(name_of_char, path_to_script, script_name):
    global avg_word_count,scripts_total_wc
    dict_to_lines = {}
    word_count = 0
    name_to_list = name_of_char.split(" ")
    set_of_names = set()
    with open(path_to_script, "r+", encoding='utf-8', errors='ignore') as script_file:
        lines = script_file.readlines()
        for line in lines:
            line_name = line[:line.find("=")]
            dict_to_lines[line_name] = dict_to_lines.get(line_name,0) + 1
            for sub_name in name_to_list:
                if sub_name.lower() in line_name.lower():
                    sentence_start = line.find(">")
                    if sentence_start != -1:
                        sentence_to_add = line[sentence_start+1:].replace("\n","")
                        actor_sentence = sentence_to_add.split(" ")
                        word_count += len(actor_sentence)
                        break
                    elif DEBUG1:
                        print("DEBUG - COULDN'T FIND '>' IN LINE 2")
    # print(f"COUNT WORD = {word_count}")
    if script_name.lower() in scripts_total_wc and word_count > 0:
        return word_count / scripts_total_wc[script_name.lower()]
    return avg_word_count



def calc_popularity(mapping):
    # path_to_scripts = r'scripts/parsed'
    popular_list = []
    path_to_scripts = os.path.join("scripts", "parsed")
    path_to_dialogues = os.path.join(path_to_scripts,'dialogue')
    if not os.path.isdir(path_to_dialogues):
        print("Could not find path to dialogue (scripts) dir.")
        exit(1)
    suffix = "_dialogue.txt"
    for actor in mapping:
        actor_popularity = 0.0
        counter_found = 0
        counter_not_found = 0
        for movie in actor['movie_info']:
            movie_fixed_name = movie['title'].replace(" ", "-").replace(":", "")
            path_to_movie = os.path.join(path_to_dialogues, movie_fixed_name + suffix)
            if os.path.isfile(path_to_movie) and movie['character'] != "":

                global scripts_used
                scripts_used.add(movie_fixed_name)
                # print(path_to_movie)
                counter_found+=1
                # if movie['character'] == "" and DEBUG:
                #     print(f"DEBUG - Character name EMPTY for {actor['name']} in {movie_fixed_name}")
                # else:
                word_count = extract_word_count(movie['character'],path_to_movie, movie_fixed_name)
                if DEBUG1:
                    print(f"DEBUG - WORD COUNT FOUND: {word_count}")
            else:
                word_count = avg_word_count
                if DEBUG1:
                    # print(f"DEBUG - Couldn't find movie script: {movie['title']}")
                    pass
            actor_popularity += word_count * (movie['rating'] / 10.0) * movie['vote_count']

        if DEBUG2:
            print(f"Actor {actor['name']} Popularity: {actor_popularity}")
        birthplace = actor['place_of_birth'].replace(",","")
        lon, lat = address_to_coords(actor['place_of_birth'].replace(",",""))
        popular_list.append({"name":actor['name'],
                             "profile_url": f"https://www.themoviedb.org/person/{actor['id']}",
                             "place_of_birth": birthplace,
                             "longitude": lon,
                             "latitude": lat,
                             "popularity": actor_popularity})
        # actor['popularity'] = actor_popularity
    return popular_list


def export_to_csv(list_of_actors):
    pass


if __name__ == '__main__':
    # create_empty_json()
    # create_database(40000)

    # popular_actors = get_popular(2)
    # mapping = get_birth_place(popular_actors)
    test = dataset_to_list(r'dataset.json')
    process_scripts()
    popularity_list = calc_popularity(test)
    export_to_csv(popularity_list)
    if DEBUG1:
        print("DEBUG - Done")

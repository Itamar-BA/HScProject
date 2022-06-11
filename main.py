import urllib.request
import json
from urllib.error import HTTPError
api_key = '5f0c4de627a9354bdfcac23fbaacc3d2'


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


def get_actors(max_id):
    ret_list = []
    for curr_id in range(1, max_id):
        url = f"https://api.themoviedb.org/3/person/{curr_id}?api_key=5f0c4de627a9354bdfcac23fbaacc3d2&language=en-US"
        try:
            data = get_url_data(url)
        except HTTPError as err:
            if err.code == 404:
                print(f"ERROR 404 for id {curr_id}, skipping")
                continue

        # Check if place of birth exists -> if true, check if he's american
        birth_place = data.get('place_of_birth')
        places = ['United States', 'USA', 'U.S.']
        is_american = any(place in birth_place for place in places) if birth_place else False
        is_actor = data['known_for_department'] == "Acting"

        if is_actor and is_american:
            movie_info = get_movie_char(curr_id)
            ret_list.append({"name": data['name'],
                             "id": curr_id,
                             "place_of_birth": birth_place,
                             "movie_info": movie_info})
        else:
            print(f"is actor = {is_actor}, birth = {birth_place}")
    return ret_list


if __name__ == '__main__':
    #get_actors(6193)
    # popular_actors = get_popular(3)
    # mapping = get_birth_place(popular_actors)
    actors = get_actors(200)
    with open("./dataset.json", "w") as f:
        json_obj = json.dumps(actors, indent=4)
        f.write(json_obj)

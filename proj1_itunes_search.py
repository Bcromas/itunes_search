import json
import requests
import webbrowser
import sys
import codecs
sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer)

class Media:

    def __init__(self, title="No Title", author="No Author", release_year="1900", JSON = None):
        d = {}
        if JSON == None:
            self.title = title
            self.author = author
            self.release_year = release_year
        else:
            # d = json.loads(JSON)
            # self.title = d["trackName"]
            # self.author = d["artistName"]
            # self.release_year = d["releaseDate"][0:4]
            d = JSON
            self.title = d["trackName"]
            self.author = d["artistName"]
            self.release_year = d["releaseDate"][0:4]
            #self.url = d["previewUrl"]
            #self.url = d["*viewURL"]
            #self.url = d["viewURL"]
            self.url = d["trackViewUrl"]

    def __str__(self):
        return "{} by {} ({})".format(self.title,self.author,self.release_year)

    def __len__(self):
        return 0

## Other classes, functions, etc. should go here
class Song(Media):

    def __init__(self, title="No Title", author="No Author", release_year="1900", album="No Album", genre="No Genre", length=999, JSON = None):
        super().__init__(title, author, release_year, JSON)
        if JSON == None:
            self.album = album
            self.genre = genre
            self.length = length
        else:
            # d = json.loads(JSON)
            # self.album = d["collectionName"]
            # self.genre = d["primaryGenreName"]
            # self.length = round(d["trackTimeMillis"]/1000) #converting milliseconds to seconds & rounding
            d = JSON
            self.album = d["collectionName"]
            self.genre = d["primaryGenreName"]
            self.length = round(d["trackTimeMillis"]/1000) #converting milliseconds to seconds & rounding
            #self.url = d["previewUrl"]
            self.url = d["trackViewUrl"]
            #self.url = d["viewURL"]

    def __str__(self):
        #can just call super here without passing anything to it & it should print just fine
        return "{} by {} ({}) [{}]".format(self.title, self.author, self.release_year, self.genre)

    def __len__(self):
        return self.length

class Movie(Media):

    def __init__(self, title="No Title", author="No Author", release_year="1900", rating="MA", length=999, JSON = None):
        super().__init__(title, author, release_year, JSON)
        if JSON == None:
            self.rating = rating
            self.length = length
            # self.url = trackViewURL
        else:
            # d = json.loads(JSON)
            # self.rating = d["contentAdvisoryRating"]
            # self.length = round(d["trackTimeMillis"]/60000) #converting milliseconds to minutes & rounding
            d = JSON
            self.rating = d["contentAdvisoryRating"]
            self.length = round(d["trackTimeMillis"]/60000) #converting milliseconds to minutes & rounding
            #self.url = d["previewUrl"]
            self.url = d["trackViewUrl"]

    def __str__(self):
        #can just call super here without passing anything to it & it should print
        return "{} by {} ({}) [{}]".format(self.title, self.author, self.release_year, self.rating)

    def __len__(self):
        return round(self.length)

def call_itunesAPI(term, count):
    baseURL = "https://itunes.apple.com/search"
    params_dict = {}
    params_dict["term"] = term
    params_dict["limit"] = count
    resp = requests.get(baseURL,params_dict)
    respLoaded = json.loads(resp.text)

    media_list = []
    movie_list = []
    song_list = []

    for i in respLoaded["results"]:
        if i['wrapperType'] == 'track':
            if i['kind'] == 'feature-movie':
                movie_list.append(Movie(JSON = i))
            elif i['kind'] == 'song':
                song_list.append(Song(JSON = i))
            else:
                media_list.append(Media(JSON = i))
        else:
            continue

    all_lists = [movie_list, song_list, media_list]
    return all_lists

def handle_results(all_lists):

    results_count = 0
    movie_dict = {}
    song_dict = {}
    media_dict = {}

    for i in all_lists:
        for j in i:
            results_count += 1
            if isinstance(j, Movie):
                movie_dict[str(results_count)] = j
            elif isinstance(j, Song):
                song_dict[str(results_count)] = j
            else:
                media_dict[str(results_count)] = j

    print('\nMOVIES\n')
    if len(movie_dict)>=1:
        for i in movie_dict:
            print(i, movie_dict[i])
    else:
        print('No Movies Found')

    print('\nSONGS\n')
    if len(song_dict)>=1:
        for i in song_dict:
            print(i, song_dict[i])
    else:
        print('No Songs Found')

    print('\nOTHER MEDIA\n')
    if len(media_dict)>=1:
        for i in media_dict:
            print (i, media_dict[i])
    else:
        print('No Other Media Found')

    more_info = input('\nEnter a number for more info, or another search term, or exit:')

    if more_info.lower() == 'exit':
        print('\nBye!')
    elif more_info.isdigit():
        if more_info in movie_dict:
            print('\nLaunching\n\n',movie_dict[str(more_info)].url,'\n\nin web browser...')
            webbrowser.open(movie_dict[str(more_info)].url)
            #print(movie_dict[str(more_info)].url)
        elif more_info in song_dict:
            print('\nLaunching\n\n',song_dict[str(more_info)].url,'\n\nin web browser...')
            webbrowser.open(song_dict[str(more_info)].url)
            #print(song_dict[str(more_info)].url)
        elif more_info in media_dict:
            print('\nLaunching\n\n',media_dict[str(more_info)].url,'\n\nin web browser...')
            webbrowser.open(media_dict[str(more_info)].url)
            #print(media_dict[str(more_info)].url)
        else:
            print('Sorry, that was bad input. Bye!')
    else: handle_results(call_itunesAPI("'" + more_info + "'",50))

if __name__ == "__main__":
    pass
    # your control code for Part 4 (interactive search) should go here

    query = input('Enter a search term, or “exit”:')
    if query.lower() == 'exit':
        print('\nBye!')
    else:
        check = handle_results(call_itunesAPI("'" + query + "'",50))

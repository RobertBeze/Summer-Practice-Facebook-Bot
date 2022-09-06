import facebook, requests, sys, os, threading,json

TOKEN = 'EAAISgIKVsmMBAIOYQWideaCTf1alrI2heoOoZBJux89CIRI5DuPq7dDGvwmzoFaH6cNCVqZCRzSJLaIoARvcwRLrjlgnA2KZAvXpUFWmXBZBYS6zlg6f4fDYqA2b8ZAF4MbZBnMwLBoeOpq28u9JARkyj7vSuGVBSbWxZAjXAr15slYvir5MZC4gSORdQ1RcFDAZD'
threads = []

def get_args():
    try:
        token = sys.argv[1]
        if len(sys.argv) != 2:
            raise ValueError()
    except:
        print('Bad number of arguments.')
    return [token]

def get_all_posts(token):
    graph = get_graph(token)
    posts = graph.request('/me/posts')
    count=1
    while "paging" in posts:
        print("length of the dictionary",len(posts))
        print("length of the data part",len(posts['data']))
        for post in posts["data"]:
            print(count,"\n")
            if "message" in post:   #because some posts may not have a caption
                print(post["message"])
            print("time :  ",post["created_time"])
            print("id   :",post["id"],"\n\n")
            count=count+1
        posts=requests.get(posts["paging"]["next"]).json()
    print("end of posts")

def get_date(d):
    data = str()
    c1 = 0
    c2 = 0
    for x in d:
        if x == 'T':
            break
        data += x
        c1 += 1
    return data
def get_date_and_time(d):
    data = str()
    c1 = 0
    c2 = 0
    for x in d:
        if x == 'T':
            break
        data += x
        c1 += 1
    data += '; time: '
    for x in d:
        c2 += 1
        if c2 <= c1:
            continue
        elif x != '+':
            data += x
    return data

def first_digit(x): 
    return x >= '0' and x <= '9'

def digit(x):
    return x >= '0' and x <= '9'
def check_valid_data(data):
    return first_digit(data[0]) and digit(data[1]) and digit(data[2]) and digit(data[3]) and data[4] == '-' and first_digit(data[5]) and digit(data[6]) and data[7] == '-' and first_digit(data[8]) and digit(data[9])

def get_posts_by_date(token):
    try:
        data = input('Enter the date(format: yyyy-mm-dd): ')
        if not check_valid_data(data):
            raise TypeError()
    except:
        print('Invalid data format!')
        return None
    graph = get_graph(token)
    posts = graph.request('/me/posts')
    count=1
    while "paging" in posts:
        for post in posts["data"]:
           # print(count,"\n")
            data_f = get_date(post['created_time'])
            if data_f == data:
          #      print(post)
                if "message" in post:   #because some posts may not have a caption
                    print(post["message"])
                print('Date and time:', get_date_and_time(post['created_time']))
                print("id   :",post["id"],"\n\n")
            count=count+1
        posts=requests.get(posts["paging"]["next"]).json()
    print("end of posts")
def get_graph(arg):
    graph = facebook.GraphAPI(arg)
    return graph

def get_albums(token):
    graph = get_graph(token)
    profile = graph.get_object('me',fields='albums')
    x = profile['albums']
    for y in x['data']:
        if y is not None:
            for key,value in y.items():
                print(f'{key} : {value}')


def get_data_from_page(token):
    graph = get_graph(token)
    page_name = input("Enter a page name: ")
    fields = ['id','name','about','likes','link','band_members']
    fields = ','.join(fields)
    page = graph.get_object(page_name, fields=fields)
    print(page)

def get_basic_data(access_token):
    graph = facebook.GraphAPI(access_token)
    profile = graph.get_object('me',fields = 'first_name,location,email,last_name,gender,work,relationship_status')
    profile_data = str()
    for key, value in profile.items():
        profile_data += f'{key}:{value}\n'
    return profile_data


def get_number_of_friends(access_token):
    graph = facebook.GraphAPI(access_token)
    profile = graph.get_object('me',fields = 'first_name,last_name,friends')
    return f"{profile['first_name']} {profile['last_name']} has a total of {profile['friends']['summary']['total_count']} friends."

def post_something(post,token=TOKEN):
    graph = get_graph(token)
    graph.put_object("me", "feed", message=post)
    #to get your posts/feed
    feed = graph.get_connections("me", "feed")
    post = feed["data"]
    print(post)
    #to put comments for particular post id
    graph.put_object(post["id"], "comments", message="First!")

def get_languages(access_token):
    graph = get_graph(access_token)
    print('Known languages:')
    profile = graph.get_object('me',fields='languages')
    for l in profile['languages']:
            print(f"-{l['name']}")


def main_menu():
    print('\t\tMenu')
    print('\t1.Get all posts from profile')
    print('\t2.Get all albums from profile')
    print('\t3.Get basic data from profile (name, e-mail)')
    print('\t4.Get posts from certain date')
    print('\t5.Get the total number of friends')
    print('\t6.Get known languages')
    opt = int(input('Choose an option...'))
    return opt




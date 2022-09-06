import facebook, requests, sys, os, threading


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

def get_graph(arg):
    graph = facebook.GraphAPI(arg)
    return graph

def get_friends_list(token):
    graph = get_graph(token)
    profile = graph.get_object('me')
    friends = graph.get_connections('me','friends')
    return [friend['name'] for friend in friends['data']]

def get_basic_data(access_token, user):
    graph = facebook.GraphAPI(access_token)
    data = graph.request('/search?q=' +user+'&type=user')
    id =  data.items()[1][1][0]["id"]
    args = {'fields' : 'id,name,email' }
    profile = graph.get_object(id, **args)
    return profile

def main_menu():
    print('\t\tMenu')
    print('\t1.Get all posts from profile')
    print('\t2.Get all friends from profile')
    print('\t3.Get basic data from profile (name, e-mail)')
    opt = int(input('Choose an option...'))
    return opt

def _main(args = get_args()):
    token = args[0]
    while True:
        opt = main_menu()
        if opt == 1:
            get_all_posts(token)
        elif opt == 2:
            for friend in get_friends_list(token):
                print(friend)
        elif opt == 3:
            print(get_basic_data(token,'all.all11223344'))
        else:
            print('Wrong option. If you want to quit, press CTRL+C, or select a new option.')
if __name__ == '__main__':
    _main()


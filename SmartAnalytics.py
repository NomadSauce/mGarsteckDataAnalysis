__author__ = 'matthewgarsteck'

# - - - - \ IMPORT STATEMENTS
from instagram.client import InstagramAPI
import matplotlib.pyplot as plt
from instagram.bind import InstagramAPIError
import matplotlib.dates
import numpy as np
import networkx as nx
from Queue import Queue
from threading import Thread
import cProfile

# - - - - \ APP CREDENTIALS
CLIENT_ID = "e146f87ef0a440f39fcd670731b12782"
CLIENT_SECRET = "ed9b13eb811b46ceae7718cfdbe5f2e8"
ACCESS_TOKEN = "1334912957.e146f87.9c9168c3f4da4e54bbbb5169f9d12a25"
CLIENT_IP = "192.168.1.79"
USER_ID = "1334912957"
MEDIA_ID = "1024035585946171788_1334912957"
MEDIA_LIKES = []
MEDIA_DATES = []
MEDIA_TAGS = []
PPL_DICT = {}


# q = Queue(maxsize=0)







# - - - - \ ACCESS THE API WITH MY CREDENTIALS
api = InstagramAPI(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, client_ips=CLIENT_IP, access_token=ACCESS_TOKEN)

# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =


# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
print
print
print "---- * [ INSTAGRAM SMART ANALYTICS ] * ----"
print


# - - - - \ FUNCTIONS FOR GETTING TAGS ETC FOR INDIVIDUAL IMAGES, RETURNS THE LIST
# - - - - \ GET A LIST OF THE USERS MEDIA


# - - - - \ CREATES A MEDIA OBJECT
class MediaObject(object):
    def __init__(self, MEDIA):
        self.MEDIA = MEDIA

    def MEDIA_LIKES(self):
        LIKES = api.media_likes(self.MEDIA)
        LIKE_LIST = []

        print "---- ---- LIKE LIST FOR THIS IMAGE: ", LIKES
        print
        return LIKES

    def MEDIA_COMMENTS(self):
        pass
    def MEDIA_TAGS(self):
        pass

# med1 = MediaObject("1024035585946171788_1334912957")
# print med1.MEDIA_LIKES()

# - - - - \ CREATES A USER OBJECT.
class NewUser(object):
    def __init__(self, USER):
        self.USER = USER


    def MEDIA_LIST(self):
        print "==== ==== LOADING MEDIA ... .. ."
        mediaList = []
        MEDIA_LIST = []
        mediaList, next = api.user_recent_media(user_id=self.USER, count=0)
        while next:
            more_media, next = api.user_recent_media(with_next_url=next)
            mediaList.extend(more_media)

        MEDIA_LIST = [MediaObject(x.id).MEDIA_LIKES() for x in mediaList]
        print MEDIA_LIST
        # for media in mediaList:
        #     MEDIA_LIST.append(MediaObject(media.id).MEDIA_LIKES())

        print "HERE IS THE MEDIA LIST: ", MEDIA_LIST
        print "---- ---- ", len(mediaList), " IMAGES LOADED"
        print " - " * 50
        print
        return mediaList

# - - - - \ GETS THE LIST OF WHO THE USER IS FOLLOWING
    def USER_FOLLOWING(self):
        print "==== ==== ACCESSING USER FOLLOWING ... .. ."
        followingList = []
        followingList, next = api.user_follows(user_id=self.USER, count=0)
        while next:
            more_users, next = api.user_follows(with_next_url=next)
            followingList.extend(more_users)
        print "---- ---- USER IS FOLLOWING ", len(followingList)
        print " - " * 50
        print
        return followingList

# - - - - \ GETS THE LIST OF WHO FOLLOWS THE USER
    def USER_FOLLOWERS(self):
        print "==== ==== ACCESSING WHO FOLLOWS USER ... .. ."
        followsList = []
        try:
            followsList, next = api.user_followed_by(user_id=self.USER, count=0)

            while next:
                more_users, next = api.user_followed_by(with_next_url=next)
                followsList.extend(more_users)
        except InstagramAPIError as e:
            if (e.status_code == 400):
                print "\nUser is set to Private"
                return []
        print "USER HAS ", len(followsList), " FOLLOWERS"
        print " - " * 50
        print
        return followsList

    def USER_INITIALIZE(self):
        pass










def getMedia(USER):
    print "**** --- LOADING MEDIA"
    print
    userMedia, next = api.user_recent_media(user_id=USER, count=0)
    mediaList = []
    # - - - - \ NEED TO GET THE COUNT BETTER, WORKS GOOD FOR NOW
    while next:
        more_media, next = api.user_recent_media(with_next_url=next)
        userMedia.extend(more_media)

    print "---- --- ", len(more_media), " IMAGES LOADED FOR THIS USER"
    print
    return [MediaObject(x.id).MEDIA_LIKES() for x in userMedia]

def getTags(MEDIA):

    print "**** --- GETTING TAGS"
    tagList = []
    try:
        print "---- --- TAGS: ", MEDIA.tags
        tagList.append(MEDIA.tags)
    except:
        tagList = []
        return tagList
    return tagList

def getLikes(MEDIA):
    print "**** --- GETTING LIKES"
    likes = api.media_likes(MEDIA.id)
    likeList = []
    try:
        for like in likes:
            likeList.append(like.username)
    except:
        likeList = []
        return likeList
    print "---- --- THIS IMAGE HAS ", len(likeList), " LIKES", likeList
    return likeList




mGar = NewUser(USER_ID)


def do_stuff(q):
    likeList = []

    while not q.empty():
        PPL_DICT[q.get().id] = {"Likes" : [x for x in MediaObject(q.get().id).MEDIA_LIKES()]}
        # PPL_DICT["Media Name"] = [x for x in mGar.Media_Object.MEDIA_LIKES(q.get())]
        print PPL_DICT
        print

        q.task_done()


q = Queue(maxsize=0)
num_threads = 2

def run_Q():

    # userMedia, next = api.user_recent_media(user_id=USER_ID, count=0)
    # while next:
    #     more_media, next = api.user_recent_media(with_next_url=next)
    #     userMedia.extend(more_media)
    #     q.put(next)

    for media in mGar.MEDIA_LIST():
        print "Q: ", media
        print
        q.put(media)

    for i in range(num_threads):
        print "Thread Number: ", i
        print
        worker = Thread(target=do_stuff, args=(q,))
        worker.daemon = True
        worker.start()

    q.join()

cProfile.run('run_Q()')

#getMedia(USER_ID)

# mGar = NewUser(USER_ID)
# mGar.MEDIA_LIST()
#cProfile.run('mGar.MEDIA_LIST()')
# mGar.USER_FOLLOWING()
# mGar.USER_FOLLOWERS()

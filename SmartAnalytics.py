_author__ = 'mGarsteck'

# - - - - \ IMPORT STATEMENTS
from instagram.client import InstagramAPI
import matplotlib.pyplot as plt
from instagram.bind import InstagramAPIError
import matplotlib.dates
import numpy as np
import networkx as nx

# - - - - \ APP CREDENTIALS
CLIENT_ID = "e146f87ef0a440f39fcd670731b12782"
CLIENT_SECRET = "ed9b13eb811b46ceae7718cfdbe5f2e8"
ACCESS_TOKEN = "1334912957.e146f87.9c9168c3f4da4e54bbbb5169f9d12a25"
CLIENT_IP = "192.168.1.79"
USER_ID = "1334912957"
MEDIA_LIKES = []
MEDIA_DATES = []
MEDIA_TAGS = []

'''
class NewUser(object):
    def __init__(self, USER):
        self.USER = USER

    def GET_USER_FOLLOWING(self, FOLLOWING):

    def GET_USER_FOLLOWS(self, FOLLOWS):

    def MEDIA_DICT(self, MEDIA):
'''



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
def getMedia(USER):
    print "**** --- LOADING MEDIA"
    print
    userMedia, next = api.user_recent_media(user_id=USER, count=0)
    mediaList = []
    index = 0
    # - - - - \ NEED TO GET THE COUNT BETTER, WORKS GOOD FOR NOW
    while next:
        index+=1
        more_media, next = api.user_recent_media(with_next_url=next)
        userMedia.extend(more_media)

    for media in userMedia:
        mediaList.append(media)

    print "---- --- ", len(userMedia), " IMAGES LOADED FOR THIS USER"
    print
    return mediaList

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

def getFollowers(USER):
    followerList = []
    print "---- ACCESSING WHO IS FOLLOWING THE USER", USER
    try:
        user_followers, next = api.user_followed_by(user_id=USER, count=25)
        while next:
            more_users, next = api.user_followed_by(with_next_url=next)
            user_followers.extend(more_users)

        for user in user_followers:
            followerList.append(user)
        print "---- --- USER HAS ", len(followerList), " FOLLOWERS"
    except InstagramAPIError as e:
        if (e.status_code == 400):
            print "\nUser is set to Private"
            return []

    return followerList

def getFollowing(id):
    print  "---- ACCESSING WHO THE USER FOLLOWS"
    print
    user_following, next = api.user_follows(user_id=USER_ID, count=25)
    while next:
        more_users, next = api.user_follows(with_next_url=next)
        user_following.extend(more_users)
    followinglist = []
    for user in user_following:
        followinglist.append(user.username)
    print "---- --- USER IS FOLLOWING ", len(followinglist)
    print
    return followinglist

def getUserAnalysis(USER):
    print "**** --- GETTING USER ANALYSIS"
    print
    mediaList = getMedia(USER)
    index=0
    for media in mediaList:
        index+=1
        print "**** --- MEDIA ID: ", media.id
        print "---- --- ANALYZING IMAGE ", index, " OF", len(mediaList)
        likesList = getLikes(media)
        tagsList = getTags(media)
        print



# - - - - NEED TO WORK ON THIS
def getNetwork(USER, COUNT, NETWORKLIST):

    print "**** --- ACCESSING USER NETWORK"
    print
    networkList = []
    followerList = getFollowers(USER)
    followingList = getFollowing(USER)

    while COUNT > 0:

        for user in followerList and followingList:
            if user not in NETWORKLIST:
                NETWORKLIST.append(user)
        COUNT-=1
        getNetwork(USER, COUNT, NETWORKLIST)
    print "---- --- ", len(NETWORKLIST), "USERS IN THIS NETWORK."
    return NETWORKLIST

def analyzeNetwork(USER):

    followersList = getFollowers(USER)
    print "---- --- FOLLOWER LIST ", followersList
    likeList = []
    print

    index = 0
    for follower in followersList:
        index+=1
        print "FOLLOWER ", index, " of ", len(followersList)
        print follower, follower.id
        print getFollowers(follower.id)

        #likeList.append(getFollowers(follower.id))
        #print "---- --- ", follower, " HAS ", len(likeList), likeList
        print

    return likeList

def graphMedia(USER):
    MEDIA_LIKES = []
    MEDIA_DATES = []
    mediaList = getMedia(USER)

    for media in mediaList:
        MEDIA_LIKES.append(len(getLikes(media)))
        MEDIA_DATES.append(media.created_time)
    print "LIKE LIST LENGTH: ", len(mediaList)
    plt.scatter(MEDIA_DATES, MEDIA_LIKES, color='red')
    plt.show()

def nodeNetwork(USER):
    FOLLOWER_LIST = getFollowers(USER)
    G = nx.MultiDiGraph()
    G.add_node(USER)
    for follower in FOLLOWER_LIST:
        G.add_node(follower.username)
        G.add_edge(USER, follower.username)
    nx.draw(G, with_labels=True)
    plt.show()

def topRelationships(USER):
    print "---- ---- ANALYZING TOP RELATIONSHIPS"
    MEDIA_LIST = getMedia(USER)
    MEDIA_LIKES = []
    MEDIA_DICT = {}
    for media in MEDIA_LIST:
        MEDIA_LIKES = getLikes(media)
        for like in MEDIA_LIKES:
            if like not in MEDIA_DICT:
                MEDIA_DICT[like] = 1
            else:
                MEDIA_DICT[like] +=1
        print "**** **** MEDIA DICT: ", MEDIA_DICT
        print

    plt.bar(range(len(MEDIA_DICT)), MEDIA_DICT.values(), align="center")
    plt.xticks(range(len(MEDIA_DICT)), MEDIA_DICT.keys(), rotation='vertical')
    plt.show()



# - - - - \ FINISHED
# getMedia(USER_ID)
#getFollowing(USER_ID)
#getFollowers(USER_ID)
#getTags(getMedia(USER_ID))
#getLikes(getMedia(USER_ID))
#getUserAnalysis(USER_ID)
#graphMedia(USER_ID)
#nodeNetwork(USER_ID)


# - - - - \ NEEDS TO BE FINISHED/FIXED
#print getNetwork(USER_ID, 2, [])
#analyzeNetwork(USER_ID)

topRelationships(USER_ID)


# - - - - \ FOR TESTING
'''
for media in recent_media:

    print getLikes(USER_ID)

    MEDIA_TAGS.append(len(getTags(media.id)))
    MEDIA_LIKES.append(len(getLikes(media.id)))
    MEDIA_DATES.append(media.created_time)

#print MEDIA_TAGS
#print MEDIA_LIKES

'''

# - - - - \ CYCLE THROUGH EACH IMAGE AND EXTRACT THE DATA
'''
for media in recent_media:

    likes = api.media_likes(media.id)

    MEDIA_LIKES.append(len(likes))
    MEDIA_DATES.append(media.created_time)

    print "AnalyzingImage # " + str(len(MEDIA_LIKES)) + " OF " + str(len(recent_media))
    print "Media: ", media.link, " has "
    print len(getFollowers(1334912957))

    #print MEDIA_LIKES
    #print "# of Likes: ", len(likes)
    #print "Date of Picture: ", media.created_time

    print

'''

# - - - - \ PLOTTING STUFF IS HERE
'''
# - - - - \ CODE FOR NX GRAPH
#G = nx.MultiDiGraph()
    G.add_node(media.user)
    for i in likes:
        G.add_node(i.username)
        G.add_edge(media.user, i.username)

# - - - - \ FOR NETWORKX
nx.draw(G, with_labels=True)
plt.show()


# - - - - \ FOR MATPLOTLIB
plt.scatter(MEDIA_DATES, MEDIA_LIKES, color='red')
plt.scatter(MEDIA_DATES, MEDIA_TAGS, color="blue")
plt.show()
'''

_author__ = 'mGarsteck'

# - - - - \ IMPORT STATEMENTS
from instagram.client import InstagramAPI
import matplotlib.pyplot as plt
import matplotlib.dates
import numpy as np
import networkx as nx

# - - - - \ APP CREDENTIALS
CLIENT_ID = "e146f87ef0a440f39fcd670731b12782"
CLIENT_SECRET = "ed9b13eb811b46ceae7718cfdbe5f2e8"
ACCESS_TOKEN = "1334912957.e146f87.9c9168c3f4da4e54bbbb5169f9d12a25"
CLIENT_IP = "192.168.1.79."
USER_ID = "1334912957"
MEDIA_LIKES = []
MEDIA_DATES = []
MEDIA_TAGS = []

# - - - - \ ACCESS THE API WITH MY CREDENTIALS
api = InstagramAPI(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, client_ips=CLIENT_IP, access_token=ACCESS_TOKEN)

# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =


# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =



# - - - - \ ASSIGN API VARIABLES
recent_media, next_ = api.user_recent_media(user_id=USER_ID, count= 5)
user_followers, next = api.user_follows(user_id=USER_ID, count=5)

# - - - - \ COMMENT THIS 'WHILE' STATEMENT OUT IF YOU WANT TO CONTROL THE COUNT

while next_:
    more_media, next_ = api.user_recent_media(with_next_url=next_)
    recent_media.extend(more_media)



# - - - - \ FUNCTIONS FOR GETTING TAGS ETC FOR INDIVIDUAL IMAGES, RETURNS THE LIST
def getTags(id):
    try:
        tagList = id.tags
    except:
        tagList = []
        return tagList
    return tagList

def getLikes(id):
    try:
        likeList = id.likes
    except:
        likeList = []
        return likeList
    return likeList

def getFollowers(id):
    user_followers, next = api.user_followed_by(user_id=USER_ID, count=25)
    '''
    while next:
        more_users, next = api.user_followed_by(with_next_url=next)
        user_followers.extend(more_users)
    '''
    followerList = []
    for user in user_followers:
        followerList.append(user.username)
    return followerList

def getFollowing(id):
    user_following, next = api.user_follows(user_id=USER_ID, count=25)
    '''
    while next:
        more_users, next = api.user_follows(with_next_url=next)
        user_following.extend(more_users)
    '''
    followinglist = []
    for user in user_following:
        followinglist.append(user.username)
    # - - - - \ ADD IN THE NEXT/WHILE LOOP TO GET ALL THE FOLLOWERS (NOT LIMITED)
    return followinglist




#G = nx.MultiDiGraph()


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

    G.add_node(media.user)
    for i in likes:
        G.add_node(i.username)
        G.add_edge(media.user, i.username)

# - - - - \ FOR NETWORKX
nx.draw(G, with_labels=True)
plt.show()
'''

for media in recent_media:
    MEDIA_TAGS.append(len(getTags(media)))
    MEDIA_LIKES.append(len(getLikes(media)))
    MEDIA_DATES.append(media.created_time)
#print MEDIA_TAGS
print MEDIA_LIKES
print len(likes)


# - - - - \ FOR MATPLOTLIB
plt.scatter(MEDIA_DATES, MEDIA_LIKES, color='red')
plt.scatter(MEDIA_DATES, MEDIA_TAGS, color="blue")
plt.show()








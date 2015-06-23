__author__ = 'mGarsteck'

from instagram.client import InstagramAPI
import matplotlib.pyplot as plt
import networkx as nx

CLIENT_ID = "e146f87ef0a440f39fcd670731b12782"
CLIENT_SECRET = "ed9b13eb811b46ceae7718cfdbe5f2e8"
ACCESS_TOKEN = "1334912957.e146f87.9c9168c3f4da4e54bbbb5169f9d12a25"
CLIENT_IP = "192.168.1.79."


api = InstagramAPI(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, client_ips=CLIENT_IP, access_token=ACCESS_TOKEN)

# ----- Break Apart For Testing Different Parts -----

recent_media, next_ = api.user_recent_media(user_id="1334912957", count=3)


MEDIA_ID = []
IMAGE_LIKES = []
IMAGE_COMMENTS = []
IMAGES_DATABASE = {}

IMAGE_IND = ["Likes : ", "Comments : ", "Who Liked : ", "Who Commented : "]

G = nx.DiGraph()

while next_:
    more_media, next_ = api.user_recent_media(with_next_url=next_)
    recent_media.extend(more_media)

# ----- for each image
for media in recent_media:

    # ----- Get the number of likes
    likes = api.media_likes(media.id)
    comments = api.media_comments(media.id)
    IMAGES_DATABASE[media] = {}
    IMAGES_DATABASE[media]["Likes "] = len(likes)
    IMAGES_DATABASE[media]["Comments "] = len(comments)



plt.bar(range(len(IMAGES_DATABASE)), IMAGES_DATABASE[media]["Likes "], align='center')
plt.xticks(range(len(IMAGES_DATABASE)), list(IMAGES_DATABASE[media].keys()))
plt.show()


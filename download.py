import praw
import sys
import shutil
import os

shutil.rmtree('in')
os.mkdir('in')
num = int(sys.argv[1])
r = praw.Reddit(user_agent='example')
s = r.get_subreddit('faces').get_new(limit=num)
for i in range(num):
    post = next(s)
    if 'i.imgur.com' in post.url:
        os.system('curl %s -o in/%d.jpg' % (post.url, i))

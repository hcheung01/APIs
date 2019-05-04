#!/usr/local/bin/python3
from sys import argv
import requests

def get_all_urls(reddits):
  """This method will extract all urls from top 10 reddit postings and save to list"""

  list_of_urls = ['https://www.reddit.com' + reddit.get('data').get('permalink') for reddit in reddits.get('children')]
  return list_of_urls

def get_replies(urls):
  """This method will send requests per link to access the direct post and extract replies"""

  all_reddits = []
  reddit_obj = {}
  replies = []

  for url in urls:
    replies_counter = 0
    # add the url into the single reddit obj
    reddit_obj['url'] = url

    # you can edit the replies depth up to 8, sort to (confidence, new, top, controversial, old, qa)
    response = requests.get(url + '.json' + '?depth=1' + '&sort=new', headers = {'user-agent': 'user'}).json()
    
    # loop to extract replies
    for reply in response[1].get('data').get('children'):

      # add all replies to a list
      replies.append(reply.get('data').get('body'))

      # increase counter
      replies_counter += 1

    # after accumulating all replies in the list, add to the single reddit object with key = 'replies' and value = [reply1, reply2, reply3]
    reddit_obj['replies'] = replies  

    # added total replies count in case you need it
    reddit_obj['total_count'] = replies_counter

    # empty list for next loop iteration
    replies = []

    # add to the list of total reddit objects
    all_reddits.append(reddit_obj)

    # empty the object
    reddit_obj = {}

  return all_reddits

def request_subreddits():
  """This method will send GET request to reddit"""

  # change url from android to apple to test
  response = requests.get('https://www.reddit.com/r/android/top.json?t=all&limit=10&t=week', headers = {'user-agent': 'user'})
  if response.status_code is 200:
    return response.json()
  return None

if __name__ == "__main__":
  top_ten = request_subreddits()
  all_urls = get_all_urls(top_ten.get('data'))

  # THIS IS THE LIST OF REDDIT OBJECTS, TOTAL 10
  all_reddits = get_replies(all_urls)

  # check if all_reddits return a list of 10 objects and print
  if len(all_reddits) == 10:
    for reddit in all_reddits:
      print(reddit)

  print("Total number of reddits is :" + str(len(all_reddits)))

# PLEASE USE all_reddits to check all post's repliess
# Format of the object is...  {'url': 'http....', 'total_count': 500, 'replies': [reply1, reply2, reply3, ...]}
import datetime
import requests
import logging
logging.basicConfig(level=logging.DEBUG)
import os
import ssl
from bs4 import BeautifulSoup
from slack import WebClient
from slack.errors import SlackApiError



# Gets Soup for Specified URL
def getSoup(url):
    rssFeed = requests.get(url)
    return BeautifulSoup(rssFeed.content, features="xml")

# These functions Return a List of all elements with "_____" tags
def rssTitle(soup):
    return cleanTitleList(popTagListTwo(soup.find_all("title")))

def rssPubDate(soup):
    return cleanTimeList(popTagListOne(soup.find_all("pubDate")))

def rssLink(soup):
    return cleanLinkList(popTagListTwo(soup.find_all("link")))

#Will need to test this with sending how it looks
def rssDescription(soup):
    return popTagListOne(soup.find_all("description"))

# Cleans Up rssTagList
# Used for 'pubDate' tags  pops once
def popTagListOne(tagList):
    returnList = []

    for tag in tagList:
        returnList.append(tag)

    returnList.pop(0)

    return returnList

# Cleans Up rssTagList
# Used For 'title' and 'link' tags  pops twice
def popTagListTwo(tagList):
    returnList = []

    for tag in tagList:
        returnList.append(tag)

    returnList.pop(0)
    returnList.pop(0)

    return returnList

def cleanTimeList(timeList):
    newList = []

    for item in timeList:

        item = str(item)
        newString = ""
       
        for i in range(0, len(item)):
            if (i > 8 and i != 12 and i < 34):
                newString = newString + item[i]       
        newList.append(newString)

    return (newList)

def cleanTitleList(titleList):
    newList = []

    for item in titleList:

        item = str(item)
        newString = ""
       
        for i in range(0, len(item)):
            newString = item[7:-17]      
        newList.append(newString)

    return (newList)

def cleanLinkList(linkList):
    newList = []

    for item in linkList:

        item = str(item)
        newString = ""
       
        for i in range(0, len(item)):
            newString = item[6:-7]      
        newList.append(newString)

    return (newList)

# Takes in 3 letters for month and returns its corresponding integer -> 1-12
def monthToInt(date):

    months = {
        "Jan": 1,
        "Feb": 2,
        "Mar": 3,
        "Apr": 4,
        "May": 5,
        "Jun": 6,
        "Jul": 7,
        "Aug": 8,
        "Sep": 9,
        "Oct": 10,
        "Nov": 11,
        "Dec": 12
    } 
    
    return months[date[7:-14]]

#Compares two given times, if time1 is before time2 then returns true
def compareTime(time1, time2):

    day1    = int(time1[4:-18])
    day2    = int(time2[4:-18])
    year1   = int(time1[11:-9])
    year2   = int(time2[11:-9])
    hour1   = int(time1[16:-6])
    hour2   = int(time2[16:-6])
    month1  = int(monthToInt(time1))
    month2  = int(monthToInt(time2))
    minute1 = int(time1[19:-3])
    minute2 = int(time2[19:-3])
    second1 = int(time1[22:])
    second2 = int(time2[22:])

    return(datetime.datetime(year1, month1, day1, hour1, minute1, second1) < datetime.datetime(year2, month2, day2, hour2, minute2, second2))

    
# Sending Slack Message
### link        - list holding the links to upwork page
### title       - list holding the titles
### msgTitle    - string of the slack message title
### totalJobs   - how many new jobs were posted/how many messages to send
### slackClient - the token to access slack server
def sendSlack(slackClient, totalJobs, title, link, msgTitle):

    for i in range(0, totalJobs):
        try:
            response = slackClient.chat_postMessage(
                channel="#upwork-bot",
                blocks= [
                {   "type": "section",
                    "text": {"type": "mrkdwn","text": "*"+msgTitle+"*"}
                },
                {   "type": "section",
                    "text": {"type": "mrkdwn", "text": title[i]}
                },
                {   "type": "section",
                    "text": {"type": "mrkdwn", "text": " "},
                    "accessory": {
                                "type": "button", 
                                "text": {"type": "plain_text", "text": "Submit Proposal"},
                                "value": "click_me_123",
                                "style": "primary",
                                "url": link[i]
                                }
                },
                {
                    "type": "divider"
                }
                ]   
            )
        except SlackApiError as e:
            assert e.response["error"]

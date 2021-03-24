import tweepy
import re
import time
from utils import Utils
from articlereader import ArticleReader
from transformers import pipeline
import requests

summarizer = pipeline("summarization")

def handle_generic_reply(utils, mention):
    """
    Parameters
    ----------
    utils : `Utils object`
        extends tweepy api wrapper
    mention : `Status object`
        a single mention

    Returns
    -------
    None
    """
    utils.rundown.update_status(
        "@%s Hi! I didn't recognize that request. Feel free to send me a DM!" %mention.user.screen_name,
        mention.id)
    return None

def handle_articleabstract(utils, mention):
    """
    Handles #articleabstract functionality. Performs abstractive summarization.

    Parameters
    ----------
    utils : `Utils object`
        extends tweepy api wrapper
    mention : `Status object`
        a single mention

    Returns
    -------
    None
    """
    urls = re.findall(r'(https?://[^\s]+)', mention.text)
    if not urls or len(urls) != 1:
        utils.rundown.update_status(
            "@%s to use the #articleabstract service, your message should be in the following format: @ rundown_bot #articleabstract url" %mention.user.screen_name,
            mention.id)
    else:
        article = ArticleReader(url = urls[0])
        body = article.article["body"][:512]
        summary = summarizer(
            body,
            max_length = 200,
            min_length = 50,
            do_sample = False)[0]["summary_text"]
        summary = summary.replace(" .", ".")
        #summary = ". ".join(list(set(summary[:-1].split(". "))))
        n = 250 - len(mention.user.screen_name) - 14
        summary_tweets = [summary[i:i+n] for i in range(0, len(summary), n)]
        summary_tweets = [summary_tweets[i] + " (%s/%s)" %(
                str(i+1),
                str(len(summary_tweets))) \
            for i \
            in range(len(summary_tweets))]

        status = None
        for tweet in summary_tweets:
            if not status:
                status = utils.rundown.update_status(
                    "@%s %s" %(mention.user.screen_name, tweet),
                    in_reply_to_status_id = mention.id,
                    auto_populate_reply_metadata = True)
            else:
                status = utils.rundown.update_status(
                    "@%s %s" %(mention.user.screen_name, tweet),
                    in_reply_to_status_id = status.id,
                    auto_populate_reply_metadata = True)
    return None


def handle_articlepeople(utils, mention):
    """
    Handles #articlepeople functionality.

    Parameters
    ----------
    utils : `Utils object`
        extends tweepy api wrapper
    mention : `Status object`
        a single mention

    Returns
    -------
    None
    """
    urls = re.findall(r'(https?://[^\s]+)', mention.text)
    if not urls or len(urls) != 1:
        utils.rundown.update_status(
            "@%s to use the #articlepeople service, your message should be in the following format: @ rundown_bot #articlepeople url" %mention.user.screen_name,
            mention.id)
    else:
        article = ArticleReader(url = urls[0])
        people = article.get_people()
        if not people:
            utils.rundown.update_status(
                "@%s Hi! I didn't find any people in that article :(" %mention.user.screen_name,
                mention.id)
        else:
            people = ", ".join(people)
            utils.rundown.update_status(
                "@%s Hi! I found these people: %s" %(
                    mention.user.screen_name,
                    people),
                mention.id)
    return None

def handle_articleplaces(utils, mention):
    """
    Handles #articleplaces functionality.

    Parameters
    ----------
    utils : `Utils object`
        extends tweepy api wrapper
    mention : `Status object`
        a single mention

    Returns
    -------
    None
    """
    urls = re.findall(r'(https?://[^\s]+)', mention.text)
    if not urls or len(urls) != 1:
        utils.rundown.update_status(
            "@%s to use the #articleplaces service, your message should be in the following format: @ rundown_bot #articleplaces url" %mention.user.screen_name,
            mention.id)
    else:
        article = ArticleReader(url = urls[0])
        people = article.get_places()
        if not people:
            utils.rundown.update_status(
                "@%s Hi! I didn't find any places in that article :(" %mention.user.screen_name,
                mention.id)
        else:
            people = ", ".join(people)
            utils.rundown.update_status(
                "@%s Hi! I found these places: %s" %(
                    mention.user.screen_name,
                    people),
                mention.id)
    return None

def handle_articleorgs(utils, mention):
    """
    Handles #articleorgs functionality.

    Parameters
    ----------
    utils : `Utils object`
        extends tweepy api wrapper
    mention : `Status object`
        a single mention

    Returns
    -------
    None
    """
    urls = re.findall(r'(https?://[^\s]+)', mention.text)
    if not urls or len(urls) != 1:
        utils.rundown.update_status(
            "@%s to use the #articleorgs service, your message should be in the following format: @ rundown_bot #articleorgs url" %mention.user.screen_name,
            mention.id)
    else:
        article = ArticleReader(url = urls[0])
        people = article.get_orgs()
        if not people:
            utils.rundown.update_status(
                "@%s Hi! I didn't find any organizations in that article :(" %mention.user.screen_name,
                mention.id)
        else:
            people = ", ".join(people)
            utils.rundown.update_status(
                "@%s Hi! I found these organizations: %s" %(
                    mention.user.screen_name,
                    people),
                mention.id)
    return None


def handle_doesfollow(utils, mention):
    """
    Handles #doesfollow functionality.

    Parameters
    ----------
    utils : `Utils object`
        extends tweepy api wrapper
    mention : `Status object`
        a single mention

    Returns
    -------
    None
    """
    users = [u for u \
        in re.findall("@([a-z0-9_]+)", mention.text, re.I)
        if u != "rundown_bot"]
    if len(users) != 2:
        utils.rundown.update_status(
            "@%s to use the #doesfollow service, your message should be in the following format: @ rundown_bot #doesfollow @user1 @user2" %mention.user.screen_name,
            mention.id)
    else:
        if utils.does_follow(users[0], users[1]):
            utils.rundown.update_status(
                "@%s Yes! @%s follows @%s." %(
                    mention.user.screen_name,
                    users[0],
                    users[1]),
                mention.id)
        else:
            utils.rundown.update_status(
                "@%s No, @%s does not follow @%s." %(
                    mention.user.screen_name,
                    users[0],
                    users[1]),
                mention.id)
    return None

def handle_mentions(utils, mentions):
    """
    Processes a batch (list) of mentions.

    Parameters
    ----------
    utils : `Utils object`
        extends tweepy api wrapper
    mentions : `list`
        list of Status objects (mentions)
    """
    for mention in mentions:
        if mention.user.screen_name == "rundown_bot":
            continue
        text = mention.text.lower()
        try:
            if "#doesfollow" in text:
                handle_doesfollow(utils, mention)
            elif "#articlepeople" in text:
                handle_articlepeople(utils, mention)
            elif "#articleplaces" in text:
                handle_articleplaces(utils, mention)
            elif "#articleorgs" in text:
                handle_articleorgs(utils, mention)
            elif "#articleabstract" in text:
                handle_articleabstract(utils, mention)
            else:
                handle_generic_reply(utils, mention)
        except tweepy.TweepError as e:
            if e.api_code == 187:
                #duplicate message. shouldn't happen once since_id is handled
                continue
            else:
                raise e

def read_last_id():
    """
    Reads the last-responded-to mention ID from a text file to avoid double-
    tweeting.

    Parameters
    ----------
    None

    Returns
    -------
    last_id : `int`
        the last-responded-to mention ID
    """
    with open("last_id.txt", "r") as f:
        last_id = int(f.read().strip())
    return last_id

def write_last_id(last_id):
    """
    Writes the last-responded to mention ID in a text file to avoid double-
    tweeting.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    with open("last_id.txt", "w") as f:
        f.write(str(last_id))
    return None

def main():
    """
    Execution point. Basic while loop. Nothing to see here.

    Parameters
    ----------
    None
    """
    utils = Utils()
    last_id = read_last_id()

    while True:
        mentions = utils.get_mentions(last_id)
        if not mentions:
            time.sleep(60)
            continue
        try:
            handle_mentions(utils, mentions)
        except requests.exceptions.RequestException as e:
            last_id = mentions[-1].id
            write_last_id(last_id)
            time.sleep(60)
            continue
        last_id = mentions[-1].id
        write_last_id(last_id)
        time.sleep(60)


if __name__ == "__main__":
    main()

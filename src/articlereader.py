import requests
from bs4 import BeautifulSoup
import nltk

class ArticleReader():
    def __init__(
            self,
            url,
            outlet):
        """
        Constructor for the ArticleReader class.

        Parameters
        ----------
        url : `str`
            the url of the article
        outlet : `str`
            the name of the outlet (e.g. BBC)
        """
        self.url = url
        self.outlet = outlet
        self.article = self.read_article()

    def read_article(self):
        """
        Parses an article, given a url and outlet.

        Returns
        -------
        a dict of parsed information (title and contents)
        """
        outlet = self.outlet.lower()
        if outlet == "bbc":
            return self.read_bbc(self.url)
        else:
            raise ValueError(
                "Sorry, %s is not a supported outlet." %self.outlet)

    def read_bbc(self, url):
        """
        Parses a BBC article.

        Parameters
        ----------
        url : `str`
            the url of the BBC article

        Returns
        -------
        a dict of parsed information (title and contents)
        """
        soup = BeautifulSoup(
            requests.get(url).text,
            "html.parser")
        title = soup.find("h1").text
        body = " ".join([el.text for el in soup.find_all("p")])
        return {"title": title, "body": body}

    def get_entities(self):
        """
        Returns a list of named entities in the body of the article.

        Returns
        -------
        entities : `list`
            list of tuples (TAG, ENTITY)
        """
        entities = []
        for sent in nltk.sent_tokenize(self.article["body"]):
            for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sent))):
                if hasattr(chunk, 'label'):
                    entities.append(
                        (chunk.label(), ' '.join(c[0] for c in chunk)))
        entities = list(set(entities))
        return entities

    def get_people(self):
        """
        Returns named entities tagged "PERSON"

        Returns
        -------
        people : `list`
            list of names
        """
        entities = self.get_entities()
        return [e[1] for e in entities if e[0] == "PERSON"]





article = ArticleReader(
    url = "http://www.bbc.com/travel/story/20210307-how-rice-shaped-the-american-south?referer=https%3A%2F%2Fwww.bbc.com%2F",
    outlet = "BBC")

print(article.get_people())

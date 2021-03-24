import requests
from bs4 import BeautifulSoup
import nltk
from newspaper import Article

class ArticleReader():
    """
    Scrapes/parses articles and does text analysis.
    """
    def __init__(
            self,
            url,
            use_soup = True):
        """
        Constructor for the ArticleReader class.

        Parameters
        ----------
        url : `str`
            the url of the article
        use_soup : `bool`
            describes whether you want to extract article info via bs4 scraping
            defaults True for now because Newspaper3k doesn't typically extract
            enough on its own
        """
        self.url = url
        self.use_soup = use_soup
        self.article = self.read_article()

    def read_article(self):
        """
        Parses an article, given a url and outlet.

        Returns
        -------
        a dict of parsed information (title and contents)
        """
        if self.use_soup:
            return self.scrape_page(self.url)
        else:
            raise ValueError("Outlet APIs not yet supported.")

    def donwload_article(self, url):
        """
        Extracts article content using Newspaper3k.

        Parameters
        ----------
        url : `str`
            the url of the article

        Returns
        -------
        a dict of parsed information (title and contents)
        """
        article = Article(url)
        article.download()
        article.parse()
        article.text = article.text.replace("\n", " ")
        return {
            "title": article.title,
            "body": article.text}

    def scrape_page(self, url):
        """
        Parses an article by scraping. Less than ideal, but what we have so far.

        Parameters
        ----------
        url : `str`
            the url of the article

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

    def get_places(self):
        """
        Returns named entities tagged "GPE" (geo-political entity).

        Returns
        -------
        places : `list`
            list of GPEs
        """
        entities = self.get_entities()
        return [e[1] for e in entities if e[0] == "GPE"]

    def get_orgs(self):
        """
        Returns named entities tagged "ORGANIZATION".

        Returns
        -------
        orgs : `list`
            list of ORGANIZATIONs
        """
        entities = self.get_entities()
        return [e[1] for e in entities if e[0] == "ORGANIZATION"]

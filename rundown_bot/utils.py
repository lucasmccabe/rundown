import tweepy
import networkx as nx

class Utils():
    """
    Utility functions for rundown.
    """
    def __init__(self):
        """Constructor. Nothing to see here."""
        self.rundown = self.init_rundown()

    def init_rundown(self):
        """
        Authenticates API, etc.

        Parameters
        ----------
        None

        Returns
        -------
        api
        """
        env_vars = {}
        with open("../.env", "r") as f:
            for line in f:
               (key, val) = line.split(": ")
               env_vars[key] = val.replace("\n", "")
        auth = tweepy.OAuthHandler(
            env_vars["API KEY"],
            env_vars["API SECRET KEY"])
        auth.set_access_token(
            env_vars["ACCESS TOKEN"],
            env_vars["ACCESS TOKEN SECRET"])
        api = tweepy.API(
            auth,
            wait_on_rate_limit=True,
            wait_on_rate_limit_notify=True)
        try:
            api.verify_credentials()
        except:
            raise ValueError("Configuration failed.")
        return api

    def get_mentions(self, last_id = None):
        """
        Returns 20 most recent tweets from timeline mentioning @rundown_bot.

        Parameters
        ----------
        last_id : `int`

        Returns
        -------
        mentions : `list'
            20 most recent tweets from timeline mentioning @rundown_bot.
        """
        if not last_id or last_id == 0:
            mentions = self.rundown.mentions_timeline()
        else:
            mentions = self.rundown.mentions_timeline(since_id = last_id)
        mentions.reverse()
        return mentions

    def get_following(self, user):
        """
        Returns a list of users that user_name is following.

        Parameters
        ----------
        user : `str`
            the user/screen name of the account you want information about

        Returns
        -------
        following : `list`
            list of users that user_name is following
        """
        following = []
        for page in tweepy.Cursor(
                self.rundown.friends,
                screen_name = user,
                wait_on_rate_limit = True,
                count = 200).pages():
            try:
                following.extend(page)
            except tweepy.TweepError as e:
                time.sleep(60)
        following = [f.screen_name for f in following]
        return following

    def does_follow(self, user1, user2):
        """
        Returns True if user1 follows user2.

        Parameters
        ----------
        user1 : `str`
            the user/screen name of one account you want information about
        user2 : `str`
            the user/screen name of the other account you want information about

        Returns
        -------
        val : `bool`
            if user1 follows user2
        """
        following = self.get_following(user1)
        return user2 in following

    def build_graph_between(self, user1, user2, max_depth = 5):
        """
        DON'T USE THIS (RATE LIMIT)
        Builds a minimal graph of user-following between user1 and user2.

        Parameters
        ----------
        user1 : `str`
            the user/screen name of one account you want information about
        user2 : `str`
            the user/screen name of the other account you want information about
        max_depth : `int`
            maximum search depth for tree construction

        Returns
        -------
        G : `networkx Graph`
        """
        G = nx.Graph()
        depth = 1
        G.add_nodes_from([user1, user2])

        following1 = self.get_following(user1)
        following2 = self.get_following(user2)

        for f in following1:
            G.add_node(f)
            G.add_edge(user1, f)

        for f in following2:
            G.add_node(f)
            G.add_edge(user2, f)

        new_members = following1 + following2

        if nx.has_path(user1, user2):
            return G

        while depth < max_depth:
            new_members_new = []
            for f in new_members:
                following = self.get_following(f) #users f is following
                for new_f in following: #each user f is following
                    if new_f not in G:
                        #if f is following a user not in G, add user to G
                        G.add_node(new_f)
                        new_members_new.append(new_f)
                    G.add_edge(f, new_f)
                    if nx.has_path(user1, user2):
                        return G
            depth += 1
            new_members = new_members_new

        if nx.has_path(user1, user2):
            return G
        else:
            raise ValueError("%s and %s not connected with search depth of 5.")

    def get_user_distance(self, user1, user2, max_depth = 5):
        """
        DON'T USE THIS (RATE LIMIT)
        Users A* algorithm to compute distance between users in following graph.

        Parameters
        ----------
        user1 : `str`
            the user/screen name of one account you want information about
        user2 : `str`
            the user/screen name of the other account you want information about
        max_depth : `int`
            maximum search depth for tree construction

        Returns
        -------
        val : `int`
            following distance between user1 and user2
        """
        try:
            G = self.build_graph_between(user1, user2, max_depth)
        except ValueError as e:
            raise ValueError("%s and %s not connected with search depth of 5.")
        length = nx.astar_path_length(G, user1, user2)
        return length

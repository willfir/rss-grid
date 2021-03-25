import feedparser
from datetime import datetime, timezone as tz, timedelta


class Reader:
    """Uses the feedparser library to get entries from an RSS feed.

    Attributes
    ----------
    identifier : str
        A short name to identify the RSS feed - e.g. "python_blog"
    name : str
        The display name of the feed - e.g. "Python.org's official blog"
    site_url : str
        The URL of the website the feed belongs to
    feed_url : str
        The URL for the RSS feed itself
    update_frequency : int
        The minimum time to wait before refreshing the feed, in minutes
    feed_data : dict
        What is returned by feed_parser.parse()
    entries : dict
        The top N entries of the feed
    last_updated : datetime.datetime
        The datetime that the Reader last updated from the RSS feed

    Methods
    -------
    refresh_feed()
        Update the RSS feed from its source
    refresh_entries(num_entries=None)
        Update the entries attribute with the latest RSS entries
    """

    def __init__(self, identifier, name, site_url, feed_url, num_entries=6,
                 update_frequency=5):
        """
        Parameters
        ----------
        identifier : str
            A short name to identify the RSS feed - e.g. "python_blog"
        name : str
            The display name of the feed - e.g. "Python.org's official blog"
        site_url : str
            The URL of the website the feed belongs to
        feed_url : str
            The URL for the RSS feed itself
        update_frequency : int
            The minimum time to wait before refreshing the feed, in minutes
        """

        self.identifier = identifier
        self.name = name
        self.site_url = site_url
        self.feed_url = feed_url
        self._update_frequency = timedelta(minutes=update_frequency)
        self.feed_data = None
        self.entries = None
        self._last_updated = None

        self.refresh_feed()
        self.refresh_entries(num_entries)

    @property
    def update_frequency(self):
        return self._update_frequency

    @update_frequency.setter
    def update_frequency(self, frequency):
        if not isinstance(frequency, timedelta):
            raise TypeError("_update_frequency must be a datetime.timedelta")
        self._update_frequency = frequency

    @property
    def last_updated(self):
        return self._last_updated

    @last_updated.setter
    def last_updated(self, time):
        if not isinstance(time, datetime):
            raise TypeError("last_updated must be a datetime.datetime object")
        self._last_updated = time

    def refresh_feed(self):
        """Refresh the RSS feed from the source.

        Calls feedparser.parse(self.feed_url), but only if
        self._update_frequency minutes have elapsed.
        """
        try:
            since_update = datetime.now(tz.utc) - self.last_updated
        except TypeError:
            since_update = None

        if since_update is None or since_update > self._update_frequency:
            self.feed_data = feedparser.parse(self.feed_url)
            self.last_updated = datetime.now(tz.utc)

    def refresh_entries(self, num_entries=None):
        """Get the requested number of entries from the RSS feed

        Calls self.refresh_feed() first, to update from the source if enough
        time has elapsed.
        """

        self.refresh_feed()

        self.entries = self.feed_data.entries[:num_entries]

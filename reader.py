import feedparser


class Reader:

    def __init__(self, identifier, name, site_url, feed_url, num_entries=6):
        self.identifier = identifier
        self.name = name
        self.site_url = site_url
        self.feed_url = feed_url
        self.feed_data = None
        self.entries = None

        self.refresh_feed()
        self.refresh_entries(num_entries)

    def refresh_feed(self):
        self.feed_data = feedparser.parse(self.feed_url)

    def refresh_entries(self, num_entries=None):
        if self.feed_data is None:
            self.refresh_feed()

        self.entries = self.feed_data.entries[:num_entries]

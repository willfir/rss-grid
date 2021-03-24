import feedparser
from datetime import datetime, timezone as tz, timedelta


class Reader:

    def __init__(self, identifier, name, site_url, feed_url, num_entries=6,
                 update_frequency=5):
        self.identifier = identifier
        self.name = name
        self.site_url = site_url
        self.feed_url = feed_url
        self.update_frequency = timedelta(minutes=update_frequency)
        self.feed_data = None
        self.entries = None
        self.last_updated = None

        self.refresh_feed()
        self.refresh_entries(num_entries)

    def refresh_feed(self):
        """Refresh the RSS feed, if the required amount of time has elapsed
        since the last update"""

        # Check how long since this feed was updated. If this is the first
        # time, handle TypeError
        try:
            since_update = datetime.now(tz.utc) - self.last_updated
        except TypeError:
            since_update = None

        if since_update is None or since_update > self.update_frequency:
            self.feed_data = feedparser.parse(self.feed_url)
            self.last_updated = datetime.now(tz.utc)

    def refresh_entries(self, num_entries=None):
        """Get the requested number of entries from the RSS feed, refreshing it
        from the source if necessary"""

        self.refresh_feed()

        self.entries = self.feed_data.entries[:num_entries]

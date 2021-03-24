import json
from flask import Blueprint, render_template

from reader import Reader


# Globals setup:
feed_settings = {}  # Dict to hold information from config file
feed_dict = {}      # Dict to hold a reader object for each feed


def get_reader(feed):

    if feed_settings.get(feed) is None:
        # Specified feed is not found, check if it's been added to feeds.json
        get_feed_settings()

    if feed_dict.get(feed) is None:
        # No reader exists for this feed, initialise one
        print(f"initialising reader for {feed}")

        try:
            reader = Reader(
                identifier=feed,
                name=feed_settings[feed]['name'],
                site_url=feed_settings[feed]['site_url'],
                feed_url=feed_settings[feed]['feed_url']
            )
        except KeyError:
            raise KeyError(f"{feed} not found, add it to feeds.json")

        feed_dict[feed] = reader

    return feed_dict[feed]


def get_feed_settings():
    global feed_settings
    with open('config/feeds.json') as f:
        feed_settings = json.load(f)


# Initial setup
get_feed_settings()

# Create Reader instance for each feed in config file
for feed in feed_settings:
    get_reader(feed)

aggregator_bp = Blueprint('routes', __name__, template_folder='templates')


@aggregator_bp.route('/')
def home():

    # Check for any new feeds added to the config file since server started
    get_feed_settings()

    # Initialise readers for any new feeds
    for feed in feed_settings:
        get_reader(feed)

    item_count = len(feed_dict)
    items_per_row = 2
    row_count = item_count // items_per_row
    leftover_items = item_count % items_per_row

    return render_template('home.html',
                           feeds_dict_keys=list(feed_dict.keys()),
                           row_count=row_count,
                           items_per_row=items_per_row,
                           leftover_items=leftover_items,
                           show_feed=show_feed
                           )


@aggregator_bp.route('/feed/<feed>/<int:num_entries>')
def show_feed(feed, num_entries, being_included=False):

    feed_reader = get_reader(feed)
    feed_reader.refresh_entries(num_entries)

    return render_template('feed.html',
                           reader=feed_reader,
                           num_entries=num_entries,
                           being_included=being_included)


@aggregator_bp.route('/feeds')
def feeds():
    return json.dumps(feed_settings, indent=4)

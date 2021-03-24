import json
from flask import Blueprint, render_template

from reader import Reader

with open('config/feeds.json') as f:
    feed_settings = json.load(f)

feed_dict = {}
for feed_setting in feed_settings:
    feed_reader = Reader(
        identifier=feed_setting,
        name=feed_settings[feed_setting]['name'],
        site_url=feed_settings[feed_setting]['site_url'],
        feed_url=feed_settings[feed_setting]['feed_url']
    )

    feed_dict[feed_setting] = feed_reader

aggregator_bp = Blueprint('routes', __name__, template_folder='templates')


@aggregator_bp.route('/')
def home():
    item_count = len(feed_dict)
    items_per_row = 2
    row_count = item_count // items_per_row
    leftover_items = item_count % items_per_row

    return render_template('home.html',
                           feeds_dict=feed_dict,
                           feeds_dict_keys=list(feed_dict.keys()),
                           row_count=row_count,
                           items_per_row=items_per_row,
                           leftover_items=leftover_items
                           )


@aggregator_bp.route('/feed/<feed>/<int:num_entries>')
def show_feed(feed, num_entries):
    feed_reader = feed_dict[feed]
    feed_reader.refresh_entries(num_entries)

    return render_template('feed.html', reader=feed_reader,
                           num_entries=num_entries)


@aggregator_bp.route('/feeds')
def feeds():
    return json.dumps(feed_settings, indent=4)

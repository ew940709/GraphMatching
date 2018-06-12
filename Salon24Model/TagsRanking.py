import csv
import datetime
import os
import logging

from PostRanking import fetch_tags_for_one_post, fetch_most_commented_posts_per_time_slot
from DatabaseConnection import connect as connect_to_db

DATE_FORMAT = "%Y-%m-%d"


def get_date_range(graph_id):
    csv_file = open("..\\salon24\\salon24_skierowany_sloty_czasowe.csv")
    reader = csv.reader(csv_file, delimiter=',')
    csv.field_size_limit(100000)
    header = next(reader)  # skip first row

    date_from, date_to = None, None

    for row in reader:
        if int(row[0]) == graph_id:
            date_from = datetime.datetime.strptime(row[1], DATE_FORMAT)
            date_to = datetime.datetime.strptime(row[2], DATE_FORMAT)
            break

    csv_file.close()

    return date_from, date_to


def get_most_commented_posts_for_dynamic_graph(graph_id, posts_limit, out_dir):
    """
            main function to fetch from database top N most commented posts with their tags and
            save them to csv file
    """
    date_from, date_to = get_date_range(graph_id)
    conn = connect_to_db()
    cur = fetch_most_commented_posts_per_time_slot(conn, date_from, date_to, posts_limit)
    get_tags_for_posts(conn, cur, graph_id, out_dir)


def get_tags_for_posts(conn, posts_cur, graph_id, out_dir):
    posts_row = posts_cur.fetchone()
    file_name = "{0}\\most_commented_posts_with_tags_for_graph_id_{1}.csv".format(out_dir, graph_id)
    save_row(None, None, file_name, True)

    while posts_row is not None:
        post_id = posts_row[0]
        tags_cur = fetch_tags_for_one_post(conn, post_id)
        tags_row = tags_cur.fetchone()
        tags = []

        while tags_row is not None:
            tags.append(tags_row[0])
            tags_row = tags_cur.fetchone()

        save_row(posts_row, tags, file_name)
        posts_row = posts_cur.fetchone()


def save_row(posts_row, tags, file_name, header=False):
    out_file = open(file_name, 'a')
    writer = csv.writer(out_file)

    if header:
        out_row = ["post_title", "post_date", "post_id", "comments_count", "tags", "post_content"]
    else:
        out_row = [posts_row[2], posts_row[1], posts_row[0], posts_row[3], '-'.join(tag for tag in tags),
                   posts_row[4][:300]]

    writer.writerow(out_row)
    out_file.close()


########################################################################################################################

def get_most_popular_tags(graphs_dir, number_from, slots_count, limit, out_dir):
    file_name = "{0}\\tags_for_dynamic_graph.csv".format(out_dir)
    save_to_file(None, None, None, None, file_name, True)
    while number_from < slots_count:
        for slot_file in os.listdir(graphs_dir):
            if slot_file.endswith(".json") and slot_file.startswith("salon24_" + str(number_from) + "_"):
                logging.info(graphs_dir + slot_file)
                split = slot_file.split('.')
                split = split[0].split('_')
                idx = split[1]
                date_from = split[2]
                date_to = split[3]
                get_most_popular_tags_for_idx(idx, date_from, date_to, limit, file_name)
                number_from += 1


def get_most_popular_tags_for_idx(idx, date_from, date_to, limit, file_name):
    conn = connect_to_db()
    cur = fetch_most_popular_tags_for_time_slot(conn, date_from, date_to, limit)

    tags_row = cur.fetchone()
    tags = []

    while tags_row is not None:
        name = tags_row[0]
        tags.append(name)
        tags_row = cur.fetchone()

    save_to_file(idx, date_from, date_to, tags, file_name)


def fetch_most_popular_tags_for_time_slot(conn, from_date, to_date, limit):
    cur = conn.cursor()
    query = "SELECT ta.name, count(ta.name) " \
            "FROM posts AS p " \
            "INNER JOIN posts_tags as t on t.posts_id = p.id " \
            "INNER JOIN tags as ta on t.tags_id = ta.id " \
            "WHERE p.date >= '{0}'::date AND p.date < '{1}'::date " \
            "GROUP BY 1 " \
            "ORDER BY 2 DESC " \
            "LIMIT {2} ".format(from_date, to_date, limit)

    cur.execute(query)
    return cur


def save_to_file(idx, date_from, date_to, tags, file_name, header=False):
    out_file = open(file_name, 'a')
    writer = csv.writer(out_file)

    if header:
        out_row = ["slot id", "date from", "date to", "tags"]
    else:
        out_row = [idx, date_from, date_to, '-'.join(tag for tag in tags)]

    writer.writerow(out_row)
    out_file.close()

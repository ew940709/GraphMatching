import datetime
import networkx as nx
import psycopg2
import logging

from Utils import GraphImportExport as export

DB_NAME = "salon24db"
USER = "sna_user"
HOST = "localhost"
PASSWORD = "sna_password"
DATE_RANGE_START = "2008-01-01"
DATE_RANGE_END = "2013-07-06"
DATE_FORMAT = "%Y-%m-%d"
FORMAT = FORMAT = '%(asctime)-15s %(levelname)s %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO)


def connect():
    conn = None

    try:
        conn = psycopg2.connect(get_connection_string())
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)

    return conn


def get_connection_string():
    connection_str = "dbname='" + DB_NAME + "' user='" + USER + "' host='" + HOST + "' password='" + PASSWORD + "'"

    return connection_str


def add_node(graph, row):
    comment_author = row[1]
    post_author = row[5]
    parent_comment = row[6]

    if graph.has_edge(comment_author, post_author):
        graph[comment_author][post_author]['weight'] += 1
    else:
        graph.add_edge(comment_author, post_author, weight=1)

    if parent_comment is not None:
        if graph.has_edge(comment_author, parent_comment):
            graph[comment_author][parent_comment]['weight'] += 1
        else:
            graph.add_edge(comment_author, parent_comment, weight=1)


def create_graph(cursor):
    row = cursor.fetchone()
    graph = nx.DiGraph()

    while row is not None:
        add_node(graph, row)
        row = cursor.fetchone()

    return graph


def create_graph_for_time_slot(cursor):

    logging.info("Number of rows: {0}".format(cursor.rowcount))
    row = cursor.fetchone()
    graph = nx.DiGraph()

    while row is not None:
        add_node(graph, row)
        row = cursor.fetchone()
    return graph


def create_social_network(conn):
    graph = None

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT c.id, c.author_id, c.date, c.parentcomment_id, c.post_id, p.author_id, "
                       "(SELECT c1.author_id "
                       "FROM comments as c1 "
                       "WHERE c1.id = c.parentcomment_id) as parent_comment_author "
                       "FROM comments as c "
                       "JOIN posts as p on p.id = c.post_id ")

        graph = create_graph(cursor)

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return graph


def fetch_comments_by_date(conn, from_date, to_date):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT c.id, c.author_id, c.date, c.parentcomment_id, c.post_id, p.author_id, "
                       "(SELECT c1.author_id "
                       "FROM comments as c1 "
                       "WHERE c1.id = c.parentcomment_id) as parent_comment_author "
                       "FROM comments as c "
                       "JOIN posts as p on p.id = c.post_id "
                       "WHERE c.date >= '{0}'::date AND  c.date < '{1}'::date".format(from_date, to_date))

        return cursor

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def get_next_date_range(last_start):
    if last_start is None:
        start_date = datetime.datetime.strptime(DATE_RANGE_START, DATE_FORMAT)
    else:
        start_date = last_start + datetime.timedelta(days=3)

    end_date = start_date + datetime.timedelta(days=7)
    end_date_bounds = datetime.datetime.strptime(DATE_RANGE_END, DATE_FORMAT)
    if end_date > end_date_bounds:
        end_date = end_date_bounds

    return start_date, end_date


def create_dynamic_graphs_for_salon24():
    start_date, end_date = get_next_date_range(None)

    conn = connect()
    i = 1
    while start_date < datetime.datetime.strptime(DATE_RANGE_END, DATE_FORMAT):
        cur = fetch_comments_by_date(conn, start_date, end_date)
        graph = create_graph_for_time_slot(cur)
        file_path = '..//Salon24_TimeSlots//salon24_{0}_{1}_{2}.json'.format(i, start_date.date(), end_date.date())
        export.save(graph, file_path)
        cur.close()
        i += 1
        start_date, end_date = get_next_date_range(start_date)

    conn.close()

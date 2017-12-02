import networkx as nx
import psycopg2

DB_NAME = "salon24db"
USER = "sna_user"
HOST = "localhost"
PASSWORD = "sna_password"


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
            graph.add_edge(comment_author, parent_comment, weight = 1)


def create_graph(cursor):
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
        cursor.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return graph

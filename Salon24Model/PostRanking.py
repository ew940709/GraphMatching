import logging

FORMAT = FORMAT = '%(asctime)-15s %(levelname)s %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO)


def fetch_most_commented_posts_per_time_slot(conn, from_date, to_date, limit):
    cur = conn.cursor()
    query = "SELECT p.id, p.date, p.title, count(c.id), p.content " \
            "FROM posts AS p " \
            "INNER JOIN posts_tags AS pt ON pt.posts_id = p.id " \
            "INNER JOIN comments AS c ON c.post_id = p.id " \
            "WHERE c.date >= '{0}'::date AND c.date < '{1}'::date " \
            "GROUP BY 1, 2, 3, 5 " \
            "ORDER BY 4 DESC " \
            "LIMIT {2} ".format(from_date, to_date, limit)
    cur.execute(query)
    logging.info("Fetched {0} rows for date range: {1} to {2}".format(str(cur.rowcount), from_date, to_date))
    return cur


def fetch_tags_for_one_post(conn, post_id):
    cur = conn.cursor()
    query = "SELECT t.name " \
            "FROM posts AS p " \
            "INNER JOIN posts_tags AS pt ON pt.posts_id = p.id " \
            "INNER JOIN tags AS t ON pt.tags_id = t.id " \
            "WHERE pt.posts_id = {0}".format(post_id)
    cur.execute(query)
    return cur

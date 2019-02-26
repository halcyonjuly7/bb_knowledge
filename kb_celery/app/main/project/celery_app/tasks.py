import json
import datetime
import psycopg2
import uuid
import collections

from . import celery_app
from psycopg2 import sql


@celery_app.task(name="celery_queue.save_db")
def save_to_db(data):
    json_data = json.loads(data)
    if json_data.get("data"):
        date_now = str(datetime.datetime.utcnow())
        conn = psycopg2.connect("dbname='bb' user='halcyon' host='postgres' password='Znypah777'")
        cur = conn.cursor()

        question_insert = []
        tags_insert = []
        contributor_insert = []
        category_insert = []
        vendor_insert = []
        qt_assoc_values = []
        qc_assoc_values = []
        qcontrib_assoc = []
        qv_assoc_values = []
        qanswer_values = []

        for item in json_data.get("data"):

            #prepare question inserts
            question_uid = str(uuid.uuid4())

            question_insert.append(sql.SQL('({0}, {1}, {2})').format(sql.Literal(str(question_uid)),
                                                                 sql.Literal(item['title']),
                                                                 sql.Literal(date_now)))

            for tag in item.get("tags", []):
                tags_insert.append(sql.SQL("({0}, {1})").format(sql.Literal(str(uuid.uuid4())), sql.Literal(tag)))
                qt_assoc_values.append(sql.SQL("({0}, {1})").format(sql.Literal(question_uid), sql.Literal(tag)))



            #question-categories
            category_insert.append(sql.SQL("({0}, {1})").format(sql.Literal(str(uuid.uuid4())),
                                                                sql.Literal(item.get("category"))))
            qc_assoc_values.append(sql.SQL("({0}, {1})").format(sql.Literal(question_uid),
                                                              sql.Literal(item.get("category"))))

            #question-contributor
            qcontrib_assoc.append(sql.SQL("({0},{1})").format(sql.Literal(question_uid),
                                                              sql.Literal(item.get("contributor"))))
            contributor_insert.append(sql.SQL("({0}, {1})").format(sql.Literal(str(uuid.uuid4())),
                                                                    sql.Literal(item.get("contributor"))))

            #question-vendor
            vendor_insert.append(sql.SQL("({0}, {1})").format(sql.Literal(str(uuid.uuid4())),
                                                              sql.Literal(item.get("vendor"))))
            qv_assoc_values.append(sql.SQL("({0}, {1})").format(sql.Literal(question_uid),
                                                                sql.Literal(item.get("vendor"))))

            # question-answer
            qanswer_values.append(sql.SQL("({0}, {1})").format(sql.Literal(question_uid),
                                                               sql.Literal(item.get("answer"))))


        # insert questions
        cur.execute(sql.SQL("INSERT INTO Questions (uuid, title, date) VALUES {0} ON CONFLICT DO NOTHING;")
                    .format(sql.SQL(",").join(question_insert)))

        # insert categories
        cur.execute(sql.SQL("INSERT INTO Categories (uuid, name) VALUES {0} ON CONFLICT DO NOTHING;")
                    .format(sql.SQL(",").join(category_insert)))
        cur.execute(sql.SQL("INSERT INTO qc_assoc (question_id, category_name) VALUES {0}")
                    .format(sql.SQL(",").join(qc_assoc_values)))


        # map contributor with questions
        cur.execute(sql.SQL("INSERT INTO CONTRIBUTORS (uuid, name) VALUES {0} ON CONFLICT DO NOTHING;").format(sql.SQL(",").join(contributor_insert)))

        cur.execute(sql.SQL("INSERT INTO qcontrib_assoc (question_id, contributor_name) VALUES {0};").format(
            sql.SQL(",").join(qcontrib_assoc)))

        #insert vendor
        cur.execute(sql.SQL("INSERT INTO vendors (uuid, name) VALUES {0} ON CONFLICT DO NOTHING;")
                    .format(sql.SQL(",").join(vendor_insert)))
        cur.execute(sql.SQL("INSERT INTO qv_assoc(question_id, vendor_name) VALUES {0}")
                    .format(sql.SQL(",").join(qv_assoc_values)))


        if tags_insert:
            # insert tags
            cur.execute(sql.SQL("INSERT INTO Tags (uuid, name) VALUES {0} ON CONFLICT DO NOTHING;")
                        .format(sql.SQL(",").join(tags_insert)))
            # map tags with questions
            cur.execute(sql.SQL("INSERT INTO QT_ASSOC(question_id, tag_name) VALUES {0}").format(
                sql.SQL(",").join(qt_assoc_values)))

        # insert answers
        cur.execute(sql.SQL("INSERT INTO Answers (question_id, answer) VALUES {0}").format(
            sql.SQL(",").join(qanswer_values)))




        conn.commit()
        cur.close()
        conn.close()
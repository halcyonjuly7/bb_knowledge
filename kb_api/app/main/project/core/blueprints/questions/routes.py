import json


from sanic import response
from psycopg2 import sql
from . import questions
from core.db.models import Questions, Answers, Tags, Categories
from core.security import token_required
from core.celery_queue.tasks import save_to_db


@questions.route("/categories", methods=["GET"])
@token_required
async def get_categories(request):
    async with request.app.pg.get_cursor() as cur:
        await cur.execute(sql.SQL("""
        SELECT {0}, {1} FROM {2}
        """).format(sql.Identifier(Categories.UUID),
                    sql.Identifier(Categories.CATEGORY),
                    sql.Identifier(Categories.TABLE_NAME)))
        categories = await cur.fetchall()
        return response.json({
            "status": "ok",
            "data": categories
        })


@questions.route("/vendors", methods=["GET"])
@token_required
async def get_vendors(request):
    async with request.app.pg.get_cursor() as cur:
        await cur.execute(sql.SQL("""
        SELECT uuid, name FROM vendors  WHERE name LIKE %s LIMIT 10;
        """), [f"%{request.args.get('vendor')}"])

        vendors = await cur.fetchall()
        return response.json({
            "status": "success",
            "data": vendors
        })
    return response.json({
        "status": "error",
        "message": "an error occured",
        "data": []
    })


@questions.route("/random", methods=["GET"])
@token_required
async def random_question(request):
    async with request.app.pg.get_cursor() as cur:
        await cur.execute(sql.SQL(
            """
            SELECT QUESTIONS.uuid as q_id, QUESTIONS.title,  ANSWERS.uuid as ans_id, ANSWERS.answer FROM QUESTIONS
                INNER JOIN QC_ASSOC ON QC_ASSOC.question_id = QUESTIONS.uuid AND QC_ASSOC.category_name = %s
                INNER JOIN ANSWERS ON ANSWERS.question_id = QC_ASSOC.question_id
                AND Questions.uuid NOT IN ({0})
            ORDER BY RANDOM() LIMIT 1;
            """).format(sql.SQL(",").join(sql.Literal(item) for item in request.args.get("exclude_ids", "").split(","))),
                        [request.args.get("category")])
        question = await cur.fetchone()
        await cur.execute(sql.SQL("""
        SELECT ANSWERS.uuid, ANSWERS.answer FROM ANSWERS
            INNER JOIN QUESTIONS ON QUESTIONS.uuid = ANSWERS.question_id
            INNER JOIN QC_ASSOC ON QC_ASSOC.question_id = QUESTIONS.uuid AND QC_ASSOC.category_name = %s
        ORDER BY RANDOM() LIMIT 3;
        """), [request.args.get("category")])
        random_answers = await cur.fetchall()

        data = {}
        if question:
            data.update(question)
            data["random_answers"] = random_answers

        return response.json({
            "status": "ok",
            "data": {**data}

        })

@questions.route("/", methods=["GET"])
@token_required
async def get_questions(request):
    select_columns = sql.SQL("SELECT {0} FROM QUESTIONS ")
    columns = [sql.SQL("{0}.{1}").format(sql.Identifier("questions"),
                                         sql.Identifier("title"))]
    query = sql.SQL("")
    if request.args.get("categories"):
        query  = query + sql.SQL(" INNER JOIN QC_ASSOC ON QC_ASSOC.question_id = QUESTIONS.uuid AND QC_ASSOC.category_name in ({0})")\
            .format(sql.SQL(",").join(map(sql.Literal, request.args.get("categories").split(","))))

        columns.append(sql.SQL("{0}.{1}").format(sql.Identifier('qc_assoc'),
                                         sql.Identifier('category_name')))

    if request.args.get("answers", "").lower() == "true":
        query = query + sql.SQL("INNER JOIN ANSWERS ON ANSWERS.question_id = QUESTIONS.uuid")
        columns.append(sql.SQL("{0}.{1}").format(sql.Identifier("answers"),
                                         sql.Identifier("answer")))


    if request.args.get("vendors"):
        columns.append(sql.SQL("{0}.{1}").format(sql.Identifier("qv_assoc"),
                                                 sql.Identifier("vendor_name")))
        query = query + sql.SQL(" INNER JOIN QV_ASSOC ON QV_ASSOC.question_id = QUESTIONS.uuid AND qv_assoc.vendor_name in ({0})")\
            .format(sql.SQL(",").join(map(sql.Literal, request.args.get("vendors", "").split(","))))


    if request.args.get("contributors"):
        query = query + sql.SQL(" INNER JOIN QCONTRIB_ASSOC ON QCONTRIB_ASSOC.question_id = QUESTIONS.uuid AND QCONTRIB_ASSOC.contributor_name in ({0}) ")\
                        .format(sql.SQL(",").join(map(sql.Literal, request.args.get("contributors", "").split(","))))
        columns.append(sql.SQL("{0}.{1}").format(sql.Identifier("qcontrib_assoc"),
                                                 sql.Identifier("contributor_name")))

    if request.args.get("tags"):
        query = query + sql.SQL("""
        INNER JOIN QT_ASSOC ON QT_ASSOC.question_id = QUESTIONS.uuid AND QT_ASSOC.tag_name in ({0})
        GROUP BY {1}
        """)\
            .format(sql.SQL(",").join(map(sql.Literal, request.args.get("tags", "").split(","))),
                    sql.SQL(",").join(columns))
        columns.append(sql.SQL("string_agg(QT_ASSOC.tag_name, ',') as tags"))



    if request.args.get("start"):
        try:
            columns.append(sql.SQL("{0}.{1}").format(sql.Identifier("questions"),
                                                     sql.Identifier("date")))
            query = query + sql.SQL("WHERE QUESTIONS.date BETWEEN {0} AND {1} ORDER BY QUESTIONS.date ").format(sql.Literal(request.args.get("start")),
                                                                                                                sql.Literal(request.args.get("end")))
        except:
            return response.json({
                "status": "error",
                "data": [],
                "message": "invalid date"
            })

    else:
        query = query + sql.SQL("ORDER BY Questions.title")

    # pagination
    query = query + sql.SQL("LIMIT {0} OFFSET {1};").format(sql.Literal(request.app.config["PAGE_LIMIT"]),
                                                            sql.Literal((request.args.get("page", 1) - 1) * request.app.config["PAGE_LIMIT"]))

    # if all parameters are empty
    if len(columns) == 1:
        return response.json({"status": "ok", "message": "nothing to search", "data": []})

    async with request.app.pg.get_cursor() as cur:
        await cur.execute(select_columns.format(sql.SQL(',').join(columns)) + query)
        data = await cur.fetchall()
        return response.json({
            "status": "ok",
            "data": data,
            "message": "success"
        })


@questions.route("/upload", methods=["POST"])
@questions.route("/add", methods=["POST"])
@token_required
async def upload(request):
    try:
        if request.path == "/questions/upload":
            data = json.loads(request.files.get("data").body.decode("utf-8"))
        else:
            data = request.json
    except (AttributeError,json.decoder.JSONDecodeError):
        return response.json({"status": "error", "message": "can't extract data please check datasource."})

    for index, item in enumerate(data.get("data")):
        missing_categories = list(
            filter(lambda i: i not in item, ["category", "title", "answer", "contributor", "tags", "vendor"]))
        if any(missing_categories):
            return response.json({"status": "error", "message": f"missing fields {missing_categories} on item {index}"})

    if data:
        save_to_db.delay(json.dumps(data))
        return response.json({"status": "success", "message": "file is being processed"})
    return response.json({"status": "error", "message": "no file found"})

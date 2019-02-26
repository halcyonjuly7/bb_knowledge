from psycopg2 import sql
from .models import Table, Questions, Accounts, Tags, Answers, Categories,Vendors, Contributors


class QuestionAuthor(Table):
    TABLE_NAME = "qa_assoc"
    ID = "id"
    QUESTION_ID = "question_id"
    AUTHOR_ID = "author_id"

    @staticmethod
    async def execute(cur):
        await cur.execute(sql.SQL("""
            CREATE TABLE IF NOT EXISTS {0} (
            {1} SERIAL PRIMARY KEY,
            {2} VARCHAR REFERENCES {3} (uuid),
            {4} VARCHAR REFERENCES {5} (email)
            );
            """).format(sql.Identifier(QuestionAuthor.TABLE_NAME),
                        sql.Identifier(QuestionAuthor.ID),
                        sql.Identifier(QuestionAuthor.QUESTION_ID),
                        sql.Identifier(Questions.TABLE_NAME),
                        sql.Identifier(QuestionAuthor.AUTHOR_ID),
                        sql.Identifier(Accounts.TABLE_NAME)))

class QuestionTags(Table):
    TABLE_NAME = "qt_assoc"
    ID = "id"
    QUESTION_ID = "question_id"
    TAG_ID = "tag_name"

    @staticmethod
    async def execute(cur):
        await cur.execute(sql.SQL("""
        CREATE TABLE IF NOT EXISTS {0} (
        {1} SERIAL PRIMARY KEY,
        {2} VARCHAR REFERENCES {3} (uuid),
        {4} VARCHAR REFERENCES {5} (name)
        );
        """).format(sql.Identifier(QuestionTags.TABLE_NAME),
                    sql.Identifier(QuestionTags.ID),
                    sql.Identifier(QuestionTags.QUESTION_ID),
                    sql.Identifier(Questions.TABLE_NAME),
                    sql.Identifier(QuestionTags.TAG_ID),
                    sql.Identifier(Tags.TABLE_NAME)))


class QuestionVendor(Table):
    TABLE_NAME = "qv_assoc"
    ID = "id"
    QUESTION_ID = "question_id"
    VENDOR_ID = "vendor_name"

    @staticmethod
    async def execute(cur):
        await cur.execute(sql.SQL("""
           CREATE TABLE IF NOT EXISTS {0} (
           {1} SERIAL PRIMARY KEY,
           {2} VARCHAR REFERENCES {3} (uuid),
           {4} VARCHAR REFERENCES {5} (name)
           );
           """).format(sql.Identifier(QuestionVendor.TABLE_NAME),
                       sql.Identifier(QuestionVendor.ID),
                       sql.Identifier(QuestionVendor.QUESTION_ID),
                       sql.Identifier(Questions.TABLE_NAME),
                       sql.Identifier(QuestionVendor.VENDOR_ID),
                       sql.Identifier(Vendors.TABLE_NAME)))


class QuestionCategory(Table):
    TABLE_NAME = "qc_assoc"
    ID = "id"
    QUESTION_ID = "question_id"
    CATEGORY_ID = "category_name"

    @staticmethod
    async def execute(cur):
        await cur.execute(sql.SQL("""
        CREATE TABLE IF NOT EXISTS {0} (
        {1} SERIAL PRIMARY KEY,
        {2} VARCHAR REFERENCES {3} (uuid),
        {4} VARCHAR REFERENCES {5} (name)
        );
        """).format(sql.Identifier(QuestionCategory.TABLE_NAME),
                    sql.Identifier(QuestionCategory.ID),
                    sql.Identifier(QuestionCategory.QUESTION_ID),
                    sql.Identifier(Questions.TABLE_NAME),
                    sql.Identifier(QuestionCategory.CATEGORY_ID),
                    sql.Identifier(Categories.TABLE_NAME)))

class QuestionContributor(Table):
    TABLE_NAME = "qcontrib_assoc"
    ID = "id"
    QUESTION_ID = "question_id"
    CONTRIBUTOR_ID = "contributor_name"


    @staticmethod
    async def execute(cur):
        await cur.execute(sql.SQL("""
            CREATE TABLE IF NOT EXISTS {0} (
            {1} SERIAL PRIMARY KEY,
            {2} VARCHAR REFERENCES {3} (uuid),
            {4} VARCHAR REFERENCES {5} (name)
            );
            """).format(sql.Identifier(QuestionContributor.TABLE_NAME),
                        sql.Identifier(QuestionContributor.ID),
                        sql.Identifier(QuestionContributor.QUESTION_ID),
                        sql.Identifier(Questions.TABLE_NAME),
                        sql.Identifier(QuestionContributor.CONTRIBUTOR_ID),
                        sql.Identifier(Contributors.TABLE_NAME)))



associations = [
    QuestionAuthor,
    QuestionTags,
    QuestionVendor,
    QuestionCategory,
    QuestionContributor
]

async def create_associations(cur):
    for association in associations:
        await association.execute(cur)
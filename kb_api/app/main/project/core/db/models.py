import abc

from psycopg2 import sql




class Table(abc.ABCMeta):
    TABLE_NAME = ""
    UUID = "uuid"


    @staticmethod
    @abc.abstractmethod
    async def execute(cur):
        pass


class Accounts(Table):
    TABLE_NAME = "accounts"
    ID = "id"
    TIMESTAMP = "time_stamp"
    EMAIL = "email"
    FIRST_NAME = "first_name"
    LAST_NAME = "last_name"
    PASSWORD = "password"


    @staticmethod
    async def execute(cur):
        await cur.execute(sql.SQL("""
            CREATE TABLE IF NOT EXISTS {0} (
            {1} SERIAL PRIMARY KEY,
            {2} VARCHAR UNIQUE, 
            {3} TIMESTAMP,
            {4} VARCHAR (100) UNIQUE,
            {5} VARCHAR (50),
            {6} VARCHAR (50),
            {7} VARCHAR 
            );""").format(sql.Identifier(Accounts.TABLE_NAME),
                          sql.Identifier(Accounts.ID),
                          sql.Identifier(Accounts.UUID),
                          sql.Identifier(Accounts.TIMESTAMP),
                          sql.Identifier(Accounts.EMAIL),
                          sql.Identifier(Accounts.FIRST_NAME),
                          sql.Identifier(Accounts.LAST_NAME),
                          sql.Identifier(Accounts.PASSWORD)))

class Profiles(Table):
    TABLE_NAME = "profiles"
    ID = "id"
    ACCOUNT_ID = "account_id"
    PROFILE_PIC = "profile_pic"

    @staticmethod
    async def create_profile(cur):
        await cur.execute(sql.SQL("""
        CREATE TABLE IF NOT EXISTS {0} (
        {1} SERIAL PRIMARY  KEY ,
        {2} VARCHAR UNIQUE ,
        {3} INTEGER REFERENCES {4} (id),
        {5} VARCHAR (150)
        );
        """).format(sql.Identifier(Profiles.TABLE_NAME),
                    sql.Identifier(Profiles.ID),
                    sql.Identifier(Profiles.UUID),
                    sql.Identifier(Profiles.ACCOUNT_ID),
                    sql.Identifier(Accounts.TABLE_NAME),
                    sql.Identifier(Profiles.PROFILE_PIC)))


class Questions(Table):
    TABLE_NAME = "questions"
    ID = "id"
    AUTHOR = "author"
    TITLE = "title"
    DATE = "date"

    @staticmethod
    async def execute(cur):
        await cur.execute(sql.SQL("""
        CREATE TABLE IF NOT EXISTS {0} (
        {1} SERIAL PRIMARY KEY,
        {2} VARCHAR UNIQUE,
        {3} VARCHAR (100) UNIQUE,
        {4} DATE NOT NULL DEFAULT CURRENT_DATE 
        );
        """).format(sql.Identifier(Questions.TABLE_NAME),
                    sql.Identifier(Questions.ID),
                    sql.Identifier(Questions.UUID),
                    sql.Identifier(Questions.TITLE),
                    sql.Identifier(Questions.DATE)))

class Tags(Table):
    TABLE_NAME = "tags"
    ID = "id"
    NAME = "name"

    @staticmethod
    async def execute(cur):
        await cur.execute(sql.SQL("""
        CREATE TABLE IF NOT EXISTS {0}(
        {1} SERIAL PRIMARY KEY,
        {2} VARCHAR UNIQUE,
        {3} VARCHAR(100) UNIQUE 
        );
        """).format(sql.Identifier(Tags.TABLE_NAME),
                    sql.Identifier(Tags.ID),
                    sql.Identifier(Tags.UUID),
                    sql.Identifier(Tags.NAME)))

class Vendors(Table):
    TABLE_NAME = "vendors"
    ID = "id"
    NAME = "name"

    @staticmethod
    async def execute(cur):
        await cur.execute(sql.SQL("""
        CREATE TABLE IF NOT EXISTS {0} (
        {1} SERIAL PRIMARY KEY,
        {2} VARCHAR UNIQUE,
        {3} VARCHAR (100) UNIQUE 
        );
        """).format(sql.Identifier(Vendors.TABLE_NAME),
                    sql.Identifier(Vendors.ID),
                    sql.Identifier(Vendors.UUID),
                    sql.Identifier(Vendors.NAME)))

class Answers(Table):
    TABLE_NAME = "answers"
    ID = "id"
    ANSWER = "answer"
    QUESTION_ID = "question_id"

    @staticmethod
    async def execute(cur):
        await cur.execute(sql.SQL("""
            CREATE TABLE IF NOT EXISTS {0} (
            {1} SERIAL PRIMARY  KEY,
            {2} VARCHAR UNIQUE,
            {3} VARCHAR,
            {4} VARCHAR REFERENCES {5} (uuid)
            );
        """
        ).format(sql.Identifier(Answers.TABLE_NAME),
                 sql.Identifier(Answers.ID),
                 sql.Identifier(Answers.UUID),
                 sql.Identifier(Answers.ANSWER),
                 sql.Identifier(Answers.QUESTION_ID),
                 sql.Identifier(Questions.TABLE_NAME)))

class Categories(Table):
    TABLE_NAME = "categories"
    ID = "id"
    CATEGORY = "name"

    @staticmethod
    async def execute(cur):
        await cur.execute(sql.SQL("""
        CREATE TABLE IF NOT EXISTS {0} (
        {1} SERIAL PRIMARY KEY,
        {2} VARCHAR UNIQUE ,
        {3} VARCHAR UNIQUE
        );
        """).format(sql.Identifier(Categories.TABLE_NAME),
                    sql.Identifier(Categories.ID),
                    sql.Identifier(Categories.UUID),
                    sql.Identifier(Categories.CATEGORY)))


class Contributors(Table):
    TABLE_NAME = "contributors"
    ID = "id"
    NAME = "name"

    @staticmethod
    async def execute(cur):
        await cur.execute(sql.SQL("""
            CREATE TABLE IF NOT EXISTS {0} (
            {1} SERIAL PRIMARY KEY,
            {2} VARCHAR UNIQUE ,
            {3} VARCHAR UNIQUE
            );
            """).format(sql.Identifier(Contributors.TABLE_NAME),
                        sql.Identifier(Contributors.ID),
                        sql.Identifier(Contributors.UUID),
                        sql.Identifier(Contributors.NAME)))


models = [
    Accounts,
    Questions,
    Tags,
    Vendors,
    Answers,
    Categories,
    Contributors
]


async def create_models(cur):
    for model in models:
        await model.execute(cur)




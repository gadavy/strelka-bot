import os
import logging
import pymysql
import pymysql.cursors

from strelkabot.utils import ConfigManager as Cfg


class Database():

    def __init__(self, check_tables, check_procedures):
        # Loading connection settings from config.json.
        self.host = Cfg.get("database", "host")
        self.port = Cfg.get("database", "port")
        self.user = Cfg.get("database", "user")
        self.pasw = Cfg.get("database", "password")
        self.char = Cfg.get("database", "charset")
        self.db = Cfg.get("database", "db_name")

        # Check tables in DB.
        if check_tables is True:
            self._check_tables()

        # Check procedures in DB.
        if check_procedures is True:
            self._check_procedures()

    # Delete link user/strelka in table 'user_strelka'.
    def delete_user_card(self, tg_id, card):
        connection = self._connection()
        cursor = connection.cursor()

        try:
            cursor.execute("CALL delete_user_card(%s,%s)", [tg_id, card])

        except Exception as ex:
            self._ex_handler("delete user card", ex)
            connection.close()
            return None

        else:
            connection.commit()
            connection.close()
            return True

    # Check strelka card existence in table 'card'.
    def exists_card(self, card):
        connection = self._connection()
        cursor = connection.cursor()

        try:
            cursor.execute("CALL exists_card(%s)", [card])

        except Exception as ex:
            self._ex_handler("exists card", ex)
            connection.close()
            return None

        else:
            connection.commit()
            connection.close()
            return True if cursor.fetchall()[0][0] == 1 else False

    # Check user existence in table 'users'.
    def exists_user(self, data):
        connection = self._connection()
        cursor = connection.cursor()

        try:
            cursor.execute("CALL exists_user(%s)", [data["id"]])

        except Exception as ex:
            self._ex_handler("exists user", ex)
            connection.close()
            return None

        else:
            connection.commit()
            connection.close()
            return True if cursor.fetchall()[0][0] == 1 else False

    # Check link user/strelka in table 'user_strelka'.
    def exists_user_card(self, tg_id, card):
        connection = self._connection()
        cursor = connection.cursor()

        try:
            cursor.execute("CALL exists_user_card(%s,%s)", [tg_id, card])

        except Exception as ex:
            self._ex_handler("exists user card", ex)
            connection.close()
            return None

        else:
            connection.commit()
            connection.close()
            return True if cursor.fetchall()[0][0] == 1 else False

    # Add strelka card to table 'card'.
    def insert_balance(self, data):
        connection = self._connection()
        cursor = connection.cursor()

        try:
            cursor.executemany("CALL insert_balance(%s,%s,%s,%s)", data)

        except Exception as ex:
            self._ex_handler("insert balance", ex)
            connection.close()
            return None

        else:
            connection.commit()
            connection.close()
            return True

    # Add strelka card to table 'card'.
    def insert_card(self, card):
        connection = self._connection()
        cursor = connection.cursor()

        try:
            cursor.execute("CALL insert_card(%s)", [card])

        except Exception as ex:
            self._ex_handler("insert card", ex)
            connection.close()
            return None

        else:
            connection.commit()
            connection.close()
            return True

    # Add user to table 'users'.
    def insert_user(self, data):
        connection = self._connection()
        cursor = connection.cursor()

        try:
            cursor.execute("CALL insert_user(%s,%s,%s,%s,%s)", [
                data["id"],
                data["first_name"],
                data["last_name"],
                data["username"],
                data["language_code"]
            ])

        except Exception as ex:
            self._ex_handler("insert user", ex)
            connection.close()
            return None

        else:
            logging.info("New user {} added!".format(data["id"]))
            connection.commit()
            connection.close()
            return True

    # Add link user/strelka to table 'user_strelka'.
    def insert_user_card(self, tg_id, card):
        connection = self._connection()
        cursor = connection.cursor()

        try:
            cursor.execute("CALL insert_user_card(%s,%s)", [tg_id, card])

        except Exception as ex:
            self._ex_handler("insert user card", ex)
            connection.close()
            return None

        else:
            connection.commit()
            connection.close()
            return True

    # Get user cards numbers from table 'card'.
    def select_cards(self):
        connection = self._connection()
        cursor = connection.cursor()

        try:
            cursor.execute("SELECT `number` FROM `card`")

        except Exception as ex:
            self._ex_handler("select cards", ex)
            connection.close()
            return None

        else:
            connection.commit()
            connection.close()

            result = []
            for (line,) in cursor.fetchall():
                result.append(line)

            return result

    # Get user data from table 'user'.
    def select_user(self, data):
        connection = self._connection()
        cursor = connection.cursor()

        try:
            cursor.execute("CALL select_user(%s)", [data["id"]])

        except Exception as ex:
            self._ex_handler("select user cards", ex)
            connection.close()
            return None

        else:
            connection.commit()
            connection.close()
            return cursor.fetchall()[0]

    # Get card data from tables 'card', 'balance', 'user'.
    def select_user_balance(self, tg_id=0, card=0):
        # If tg_id and card == 0, return all cards where balance < threshold.
        # Else return card balance.
        connection = self._connection()
        cursor = connection.cursor()

        try:
            cursor.execute("CALL select_user_balance(%s,%s)", [tg_id, card])

        except Exception as ex:
            self._ex_handler("select users balance", ex)
            connection.close()
            return None

        else:
            connection.commit()
            connection.close()

            result = []
            for line in cursor.fetchall():
                result.append(line)

            return result

    # Get user cards numbers from table 'user-card'.
    def select_user_cards(self, data):
        connection = self._connection()
        cursor = connection.cursor()

        try:
            cursor.execute("CALL select_user_cards(%s)", [data["id"]])

        except Exception as ex:
            self._ex_handler("select user cards", ex)
            connection.close()
            return None

        else:
            connection.commit()
            connection.close()

            result = []
            for (line,) in cursor.fetchall():
                result.append(line)

            return result

    # Update user data in table 'user'.
    def update_user(self, data):
        connection = self._connection()
        cursor = connection.cursor()

        try:
            cursor.execute("CALL update_user(%s,%s,%s,%s,%s,%s,%s)", [
                data["id"],
                data["first_name"],
                data["last_name"],
                data["username"],
                data["language_code"],
                data["notification"],
                data["threshold"]
            ])

        except Exception as ex:
            self._ex_handler("update user", ex)
            connection.close()
            return None

        else:
            connection.commit()
            connection.close()
            return True

    # Handling all database errors.
    def _ex_handler(self, txt, ex):  # TODO add send msg to admin.
        msg = "Database ERROR: '{} failed': {}".format(txt, ex)
        logging.error(msg)

    # Connect to MySQL server.
    def _connection(self):
        try:
            connection = pymysql.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.pasw,
                db=self.db,
                charset=self.char
            )
        except Exception as ex:
            self._ex_handler("connection", ex)

        else:
            return connection

    def _check_tables(self):
        connection = self._connection()
        cursor = connection.cursor()

        required_tables = []
        database_tables = []

        # Get required tables.
        for _, _, files in os.walk("sql"):
            for file in files:
                if file.startswith("table_"):
                    required_tables.append(file[6:-4])

        required_tables.sort()

        # Get database tables.
        try:
            cursor.execute("SHOW TABLES FROM {};".format(self.db))
        except Exception as ex:
            self._ex_handler("check tables", ex)
        else:
            for (table), in cursor:
                database_tables.append(table)

        # Check tables.
        for numbered_table in required_tables:
            table = numbered_table[2::]
            if table not in database_tables:
                try:
                    with open(f"sql/table_{numbered_table}.sql") as f:
                        cursor.execute(f.read())
                except Exception as ex:
                    self._ex_handler(f"create table {table}", ex)

                connection.commit()

        connection.close()

    def _check_procedures(self):
        connection = self._connection()
        cursor = connection.cursor()

        required_proc = []
        database_proc = []

        # Get required procedures.
        for _, _, files in os.walk("sql"):
            for file in files:
                if file.startswith("proc_"):
                    required_proc.append(file[5:-4])

        # Get database procedures.
        try:
            cursor.execute(f"SHOW PROCEDURE STATUS WHERE Db = '{self.db}';")
        except Exception as ex:
            self._ex_handler("check procedures", ex)
        else:
            for procedure in cursor:
                database_proc.append(procedure[1])

        # Check procedures.
        for procedure in required_proc:
            if procedure not in database_proc:
                try:
                    with open(f"sql/proc_{procedure}.sql") as f:
                        cursor.execute(f.read())
                except Exception as ex:
                    self._ex_handler(f"create procedure {procedure}", ex)

                connection.commit()

        connection.close()

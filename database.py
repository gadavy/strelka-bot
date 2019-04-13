import logging
import pymysql
import pymysql.cursors

from confmanager import ConfigManager as Cfg


class DataBase():

    def __init__(self):
        # Loading connection settings from config.json.
        self.host = Cfg.get("data_base", "host")
        self.port = Cfg.get("data_base", "port")
        self.user = Cfg.get("data_base", "user")
        self.pasw = Cfg.get("data_base", "password")
        self.char = Cfg.get("data_base", "charset")
        self.db = Cfg.get("data_base", "db_name")

        # Check tables in DB.
        self._check_tables()
        # Check procedures in DB.
        self._check_procedures()

    def add_user(self, user_data):
        """
        Добавляет пользователя в таблицу 'users'.

        Args:
            "user_data" (`dict`) where:
                "id" ('int'),
                "first_name" ('text'),
                "last_name" ('text'),
                "username" ('text'),
                "language_code" ('text').

        Return:
            True запись добавлена таблицу;
            None возникла ошибка.
        """
        connection = self._connection()
        cursor = connection.cursor()

        try:
            cursor.execute("CALL add_user(%s,%s,%s,%s,%s)", [
                user_data.id,
                user_data.first_name,
                user_data.last_name,
                user_data.username,
                user_data.language_code
            ])
        except Exception as ex:
            logging.warning("DB ERROR 'add_user': {}".format(ex))
            result = None
        else:
            connection.commit()
            logging.info("New user added!")
            result = True
        finally:
            connection.close()
            return result

    def add_strelka(self, c_num):
        """
        Добавляет карту в таблицу 'cards_strelka'.

        Args:
            c_num (`text`) card number.

        Return:
            True запись добавлена таблицу;
            None возникла ошибка.
        """
        connection = self._connection()
        cursor = connection.cursor()

        try:
            cursor.execute("CALL add_strelka(%s)", [c_num])
        except Exception as ex:
            logging.warning("DB ERROR 'add_strelka': {}".format(ex))
            result = None
        else:
            connection.commit()
            result = True
        finally:
            connection.close()
            return result

    def add_user_strelka(self, t_id, c_num):
        """
        Добавляет запись о связи пользователя и карты в таблицу 'user_strelka'.

        Args:
            t_id (`int`) telegram_id,
            c_num (`text`) card number.

        Return:
            True запись добавлена таблицу;
            None возникла ошибка.
        """
        connection = self._connection()
        cursor = connection.cursor()

        try:
            cursor.execute("CALL add_user_strelka(%s, %s)", [t_id, c_num])
        except Exception as ex:
            logging.warning("DB ERROR 'add_user_strelka': {}".format(ex))
            result = None
        else:
            connection.commit()
            result = True
        finally:
            connection.close()
            return result

    def check_user(self, t_id):
        """
        Проверяет наличие пользователя в таблице 'users'.

        Args:
            t_id (`int`) telegram_id.

        Return:
            True запись есть в таблице;
            False записи нет в таблице;
            None возникла ошибка.
        """
        connection = self._connection()
        cursor = connection.cursor()

        try:
            cursor.execute("CALL exists_user(%s)", [t_id])
        except Exception as ex:
            logging.warning("DB ERROR 'check_user': {}".format(ex))
            result = None
        else:
            connection.commit()
            result = True if cursor.fetchall()[0][0] == 1 else False
        finally:
            connection.close()
            return result

    def check_strelka(self, c_num):
        """
        Проверяет наличие карты стрелка в таблице 'cards_strelka'.

        Args:
            c_num (`text`) card number.

        Return:
            True запись есть в таблице;
            False записи нет в таблице;
            None возникла ошибка.
        """
        connection = self._connection()
        cursor = connection.cursor()

        try:
            cursor.execute("CALL exists_strelka(%s)", [c_num])
        except Exception as ex:
            logging.warning("DB ERROR 'check_strelka': {}".format(ex))
            result = None
        else:
            connection.commit()
            result = True if cursor.fetchall()[0][0] == 1 else False
        finally:
            connection.close()
            return result

    def chek_user_strelka(self, t_id, c_num):
        """
        Проверяет наличие связи пользователя и карты в таблице 'user_strelka'.

        Args:
            t_id (`int`) telegram_id,
            c_num (`text`) card number.

        Return:
            True запись есть в таблице;
            False записи нет в таблице;
            None возникла ошибка.
        """
        connection = self._connection()
        cursor = connection.cursor()

        try:
            cursor.execute("CALL exists_user_strelka(%s,%s)", [t_id, c_num])
        except Exception as ex:
            logging.warning("DB ERROR 'chek_user_strelka': {}".format(ex))
            result = None
        else:
            connection.commit()
            result = True if cursor.fetchall()[0][0] == 1 else False
        finally:
            connection.close()
            return result

    def get_all_strelka(self):
        """
        Возвращает список номеров карт стрелка из таблицы 'cards_strelka'.

        Return:
            (`list`) all cards strelka;
            None возникла ошибка.
        """
        connection = self._connection()
        cursor = connection.cursor()
        cards = list()

        try:
            cursor.execute("CALL get_cards()")
        except Exception as ex:
            logging.warning("DB ERROR 'get_all_strelka': {}".format(ex))
            result = None
        else:
            connection.commit()
            for (card), in cursor.fetchall():
                cards.append(card)
            result = cards
        finally:
            connection.close()
            return result

    def get_user_strelka(self, t_id):
        """
        Возвращает номера карт пользователя.

        Args:
            t_id (`int`) telegram_id.

        Return:
            list() or None если возникла ошибка.
        """
        connection = self._connection()
        cursor = connection.cursor()

        cards = list()
        try:
            cursor.execute("CALL get_user_cards(%s)", [t_id])
        except Exception as ex:
            logging.warning("DB ERROR 'get_user_strelka': {}".format(ex))
            result = None
        else:
            connection.commit()
            for (card), in cursor.fetchall():
                cards.append(card)
            result = cards
        finally:
            connection.close()
            return result

    def get_user_ntf(self, t_id):
        """
        Возвращает статус оповещений пользователя.

        Args:
            t_id (`int`) telegram_id.

        Return:
            (`bool`) or None если возникла ошибка.
        """
        connection = self._connection()
        cursor = connection.cursor()

        try:
            cursor.execute("CALL get_user_ntf(%s)", [t_id])
        except Exception as ex:
            logging.warning("DB ERROR 'get_user_ntf': {}".format(ex))
            result = None
        else:
            result = True if cursor.fetchall()[0][0] == 1 else False
        finally:
            connection.close()
            return result

    def get_user_thr(self, t_id):
        """
        Возвращает минимальный порог оповещений пользователя.

        Args:
            t_id (`int`) telegram_id.

        Return:
            (`int`) or None если возникла ошибка.
        """
        connection = self._connection()
        cursor = connection.cursor()

        try:
            cursor.execute("CALL get_user_thr(%s)", [t_id])
        except Exception as ex:
            logging.warning("DB ERROR 'get_user_thr': {}".format(ex))
            result = None
        else:
            result = cursor.fetchall()[0][0]
        finally:
            connection.close()
            return result

    def get_users_low_balance(self):
        """
        Возвращает список пользователей с критическим балансом на карте.

        Return:
            (`list`) or None если возникла ошибка.
        """
        connection = self._connection()
        cursor = connection.cursor()
        users = list()

        try:
            cursor.execute("CALL get_users_low_balance()")
        except Exception as ex:
            logging.warning("DB ERROR 'get_users_low_balance': {}".format(ex))
            result = None
        else:
            for user in cursor.fetchall():
                users.append(user)
            result = users
        finally:
            connection.close()
            return result

    def update_user_ntf(self, t_id, status):
        """
        Обновляет статус оповещений пользователя в таблице 'users'.

        Args:
            t_id (`int`) telegram_id,
            ntf (`bool`) ntf status.

        Return:
            True запись добавлена таблицу;
            None возникла ошибка.
        """
        connection = self._connection()
        cursor = connection.cursor()

        try:
            cursor.execute("CALL update_user_ntf(%s, %s)", [t_id, status])
        except Exception as ex:
            logging.warning("DB ERROR 'update_user_ntf': {}".format(ex))
            result = None
        else:
            connection.commit()
            result = True
        finally:
            connection.close()
            return result

    def update_user_thr(self, t_id, thr):
        """
        Обновляет порог оповещений пользователя в таблице 'users'.

        Args:
            t_id (`int`) telegram_id,
            thr (`int`) threshold.

        Return:
            True запись добавлена таблицу;
            None возникла ошибка.
        """
        connection = self._connection()
        cursor = connection.cursor()

        try:
            cursor.execute("CALL update_user_thr(%s, %s)", [t_id, thr])
        except Exception as ex:
            logging.warning("DB ERROR 'update_user_thr': {}".format(ex))
            result = None
        else:
            connection.commit()
            result = True
        finally:
            connection.close()
            return result

    def update_strelka_balance(self, c_num, bal):
        """
        Обновляет баланс карт стрелка в таблице 'cards_strelka'

        Args:
            c_num (`text`) card number,
            bal (`int`) balance.

        Return:
            True запись добавлена таблицу;
            None возникла ошибка.
        """
        connection = self._connection()
        cursor = connection.cursor()

        try:
            cursor.execute("CALL update_strelka_balance(%s,%s)", [c_num, bal])
        except Exception as ex:
            logging.warning("DB ERROR 'update_strelka_balance': {}".format(ex))
            result = None
        else:
            connection.commit()
            result = True
        finally:
            connection.close()
            return result

    def remove_user_strelka(self, t_id, c_num):
        """
        Удаляет запись о связи пользователя и карты из таблицы 'user_strelka'.

        Args:
            t_id (`int`) telegram_id,
            c_num (`text`) card number.

        Return:
            True запись удалена из таблицу;
            None возникла ошибка.
        """
        connection = self._connection()
        cursor = connection.cursor()

        try:
            cursor.execute("CALL del_user_strelka(%s,%s)", [t_id, c_num])
        except Exception as ex:
            logging.warning("DB ERROR 'remove_user_strelka': {}".format(ex))
            result = None
        else:
            connection.commit()
            result = True
        finally:
            return result

    def _connection(self):
        """Connect to MySQL server."""
        connection = pymysql.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.pasw,
            db=self.db,
            charset=self.char
        )
        return connection

    def _check_tables(self):
        connection = self._connection()
        cursor = connection.cursor()

        try:
            cursor.execute("SHOW TABLES FROM {};".format(self.db))
        except Exception as ex:
            logging.warning("Database error: {}".format(ex))

        tables = []
        for (table), in cursor:
            tables.append(table)

        if "users" not in tables:
            try:
                with open("sql/tables/users.sql") as f:
                    cursor.execute(f.read())
            except Exception as ex:
                logging.warning("Database error: {}".format(ex))
            connection.commit()

        if "cards_strelka" not in tables:
            try:
                with open("sql/tables/strelka.sql") as f:
                    cursor.execute(f.read())
            except Exception as ex:
                logging.warning("Database error: {}".format(ex))
            connection.commit()

        if "user_strelka" not in tables:
            try:
                with open("sql/tables/user_strelka.sql") as f:
                    cursor.execute(f.read())
            except Exception as ex:
                logging.warning("Database error: {}".format(ex))
            connection.commit()

        connection.close()

    def _check_procedures(self):
        connection = self._connection()
        cursor = connection.cursor()

        try:
            cursor.execute("SHOW PROCEDURE STATUS;")
        except Exception as ex:
            logging.warning("DB ERROR, '_check_procedures': {}".format(ex))

        procedures = []
        for p in cursor.fetchall():
            procedures.append(p[1])

        if "add_user" not in procedures:
            try:
                with open("sql/procedures/add_user.sql") as f:
                    cursor.execute(f.read())
            except Exception as ex:
                logging.warning("Database error: {}".format(ex))
            connection.commit()

        if "add_strelka" not in procedures:
            try:
                with open("sql/procedures/add_strelka.sql") as f:
                    cursor.execute(f.read())
            except Exception as ex:
                logging.warning("Database error: {}".format(ex))
            connection.commit()

        if "add_user_strelka" not in procedures:
            try:
                with open("sql/procedures/add_user_strelka.sql") as f:
                    cursor.execute(f.read())
            except Exception as ex:
                logging.warning("Database error: {}".format(ex))
            connection.commit()

        if "del_user_strelka" not in procedures:
            try:
                with open("sql/procedures/del_user_strelka.sql") as f:
                    cursor.execute(f.read())
            except Exception as ex:
                logging.warning("Database error: {}".format(ex))
            connection.commit()

        if "exists_user" not in procedures:
            try:
                with open("sql/procedures/exists_user.sql") as f:
                    cursor.execute(f.read())
            except Exception as ex:
                logging.warning("Database error: {}".format(ex))
            connection.commit()

        if "exists_strelka" not in procedures:
            try:
                with open("sql/procedures/exists_strelka.sql") as f:
                    cursor.execute(f.read())
            except Exception as ex:
                logging.warning("Database error: {}".format(ex))
            connection.commit()

        if "exists_user_strelka" not in procedures:
            try:
                with open("sql/procedures/exists_user_strelka.sql") as f:
                    cursor.execute(f.read())
            except Exception as ex:
                logging.warning("Database error: {}".format(ex))
            connection.commit()

        if "get_cards" not in procedures:
            try:
                with open("sql/procedures/get_cards.sql") as f:
                    cursor.execute(f.read())
            except Exception as ex:
                logging.warning("Database error: {}".format(ex))
            connection.commit()

        if "get_users_low_balance" not in procedures:
            try:
                with open("sql/procedures/get_users_low_balance.sql") as f:
                    cursor.execute(f.read())
            except Exception as ex:
                logging.warning("Database error: {}".format(ex))
            connection.commit()

        if "get_user_cards" not in procedures:
            try:
                with open("sql/procedures/get_user_cards.sql") as f:
                    cursor.execute(f.read())
            except Exception as ex:
                logging.warning("Database error: {}".format(ex))
            connection.commit()

        if "get_user_ntf" not in procedures:
            try:
                with open("sql/procedures/get_user_ntf.sql") as f:
                    cursor.execute(f.read())
            except Exception as ex:
                logging.warning("Database error: {}".format(ex))
            connection.commit()

        if "get_user_thr" not in procedures:
            try:
                with open("sql/procedures/get_user_thr.sql") as f:
                    cursor.execute(f.read())
            except Exception as ex:
                logging.warning("Database error: {}".format(ex))
            connection.commit()

        if "update_strelka_balance" not in procedures:
            try:
                with open("sql/procedures/update_strelka_balance.sql") as f:
                    cursor.execute(f.read())
            except Exception as ex:
                logging.warning("Database error: {}".format(ex))
            connection.commit()

        if "update_user_ntf" not in procedures:
            try:
                with open("sql/procedures/update_user_ntf.sql") as f:
                    cursor.execute(f.read())
            except Exception as ex:
                logging.warning("Database error: {}".format(ex))
            connection.commit()

        if "update_user_thr" not in procedures:
            try:
                with open("sql/procedures/update_user_thr.sql") as f:
                    cursor.execute(f.read())
            except Exception as ex:
                logging.warning("Database error: {}".format(ex))
            connection.commit()

        connection.close()

#!/usr/bin/env python3
"""
Regex-ing
"""
import re
import os
import logging
from typing import List
from mysql.connector import connection, connect


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class"""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str] = None):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        format - filter values in incoming log records using filter_datum

        :param: record - record to filter values.
        :return: record with filtered message values.
        """
        redacted_msg = filter_datum(
            self.fields, self.REDACTION, record.msg, self.SEPARATOR
        )
        record.msg = redacted_msg
        return super(RedactingFormatter, self).format(record)


def filter_datum(
    fields: List[str], redaction: str, message: str, separator: str
) -> str:
    """
    The function `filter_datum` obfuscates a list of log messages

    :param fields: a list of strings representing all fields to obfuscate
    :param redaction: a string representing by what the field will be
                      obfuscated
    :param message: a string representing the log line
    :param separator: a string representing by which character is separating
                      all fields in the log line (message)
    :return: the log message obfuscated
    """
    for field in fields:
        replacement = "{}={}{}".format(field, redaction, separator)
        message = re.sub(rf"{field}=.*?{separator}", replacement, message)
    return message


def get_logger() -> logging.Logger:
    """Configure a Logger object"""
    logger = logging.getLogger("user_data")
    logger.propagate = False
    logger.setLevel(logging.INFO)
    log_handler = logging.StreamHandler()
    formatter = RedactingFormatter(fields=list(PII_FIELDS))
    log_handler.setFormatter(formatter)
    logger.addHandler(log_handler)
    return logger


def get_db() -> connection.MySQLConnection:
    """Returns a mysql connection"""
    return connect(
        host=os.environ.get("PERSONAL_DATA_DB_HOST", default="localhost"),
        port=3306,
        user=os.environ.get("PERSONAL_DATA_DB_USERNAME", default="root"),
        password=os.environ.get("PERSONAL_DATA_DB_PASSWORD", default=""),
        database=os.environ.get("PERSONAL_DATA_DB_NAME"),
    )


def main() -> None:
    """Retrieve all rows in users table"""
    cols = [
        "name",
        "email",
        "phone",
        "ssn",
        "password",
        "ip",
        "last_login",
        "user_agent",
    ]
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    rows = cursor.fetchall()
    logger = get_logger()
    for row in rows:
        msg = "; ".join(f"{col}={val}" for col, val in zip(cols, row))
        logger.info(msg)
    cursor.close()
    db.close()


if __name__ == "__main__":
    main()

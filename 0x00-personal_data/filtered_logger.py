#!/usr/bin/env python3
"""
Regex-ing
"""
import re
from typing import List


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

#!/bin/python3

import re


def format_number(phone_number, debug=False):
    phone_number = re.sub("[^0-9]", '', phone_number)

    if len(phone_number) < 10:
        return ""

    if phone_number[0] == '0':
        phone_number = phone_number[1:]

    if debug:
        print(phone_number)

    prefix = "" if phone_number[:3] == "972" else "972"
    return prefix + phone_number


assert format_number("0547645971") == "972547645971"
assert format_number("0547-645971") == "972547645971"
assert format_number("+972-547645971") == "972547645971"

#!/usr/bin/env python3
# -*- coding: iso-8859-1 -*-
# ---------------------------------------------------------------------------
# Calculate working days of a month taking into account Greek Bank Holidays
#
# Copyright 2018 Panagiotis Dimopoulos (panosdim@gmail.com)
#
# Version: 1.0
# ---------------------------------------------------------------------------

import calendar
import datetime


def getOrthodoxEaster(year):
    oed = datetime.date.today()

    r1 = year % 4
    r2 = year % 7
    r3 = year % 19
    r4 = (19 * r3 + 15) % 30
    r5 = (2 * r1 + 4 * r2 + 6 * r4 + 6) % 7
    days = r5 + r4 + 13

    if (days > 39):
        days = days - 39
        oed = datetime.date(year, 5, days)
    elif (days > 9):
        days = days - 9
        oed = datetime.date(year, 4, days)
    else:
        days = days + 22
        oed = datetime.date(year, 3, days)

    return oed


def getBankHolidays(year):
    holidays = []
    newYearEve = datetime.date(year, 1, 1)
    epiphany = datetime.date(year, 1, 6)
    easter = getOrthodoxEaster(year)
    cleanMonday = easter - datetime.timedelta(48)
    independenceDay = datetime.date(year, 3, 25)
    goodFriday = easter - datetime.timedelta(2)
    easterMonday = easter + datetime.timedelta(1)
    labourDay = datetime.date(year, 5, 1)
    whitMonday = easter + datetime.timedelta(50)
    assumption = datetime.date(year, 8, 15)
    ochiDay = datetime.date(year, 10, 28)
    christmas = datetime.date(year, 12, 25)
    glorifying = datetime.date(year, 12, 26)
    holidays.append(newYearEve)
    holidays.append(epiphany)
    holidays.append(cleanMonday)
    holidays.append(independenceDay)
    holidays.append(goodFriday)
    holidays.append(easterMonday)
    holidays.append(labourDay)
    holidays.append(whitMonday)
    holidays.append(assumption)
    holidays.append(ochiDay)
    holidays.append(christmas)
    holidays.append(glorifying)

    return holidays


def getWorkingDays(month):
    businessdays = 0
    cal = calendar.Calendar()
    now = datetime.datetime.now()
    holidays = getBankHolidays(now.year)

    for week in cal.monthdayscalendar(now.year, month):
        for i, day in enumerate(week):
            # not this month's day or a weekend
            if day == 0 or i >= 5:
                continue
            # or a holiday
            thisdate = datetime.date(now.year, month, day)
            if thisdate in holidays:
                continue
            businessdays += 1

    return businessdays

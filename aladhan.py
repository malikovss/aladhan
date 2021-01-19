from typing import Optional
from loguru import logger
import aiohttp
from datetime import datetime
import pytz

from .latin_kiril import to_latin




class BaseClass:
    session: Optional[aiohttp.ClientSession] = None

    @staticmethod
    def _get_session() -> aiohttp.ClientSession:
        try:
            if BaseClass.session is None or BaseClass.session.closed:
                BaseClass.session = aiohttp.ClientSession()
                logger.info("New session created.")
            return BaseClass.session
        except Exception as e:
            logger.error(e)

    async def get_content(self, url: str):
        session = self._get_session()
        async with session.get(url) as response:
            content = await response.json()
        if not content:
            return False
        if (content["status"] == "OK" or content["code"] == 200):
            return content["data"]
        else:
            logger.info(content["code"], content["status"])
            raise Exception(content["status"])


class Base(BaseClass):
    """
    Returns all prayer times for a specific calendar month.
    Prayer Times Calendar - http://api.aladhan.com/v1/calendar
    """
    def __init__(self):
        self.timezonestr = None
        self._url = None
        self.method = None
    def _make_url(self) -> str:
        try:
            url = self._url
            kwargs = self.__dict__
            if "date_or_timestamp" in kwargs:
                url = url.format(timestamp=kwargs["date_or_timestamp"])
            sign = False
            for i in kwargs:
                # key, value = i, kwargs[i]
                if i.startswith("_") or i == "date_or_timestamp":
                    continue
                if sign and kwargs[i]:
                    url += "&"
                if kwargs[i]:
                    if "_" in i:
                        s = i.replace("_", "")
                    else:
                        s = i
                    url += f"{s}={kwargs[i]}"
                    sign = True
            # print(url)
            return url
        except Exception as e:
            logger.error(e)

    def _get_date(self, key: str):
        if self.timezonestr:
            tz = pytz.timezone(self.timezonestr)
            datetime_now = datetime.now(tz)
        else:
            datetime_now = datetime.now()
        year, month, day = datetime_now.year, datetime_now.month, datetime_now.day
        now = datetime_now.now()
        timestamp = int(datetime.timestamp(now))
        list_day = dict(
            timestamp=timestamp,
            year=year,
            month=month,
            day=day
        )
        return list_day[key]

    async def get(self):
        try:
            content = await self.get_content(self._make_url())
            if content:
                return content
            else:return False
        except Exception as e:
            logger.error(e)


class Calendar(Base):
    _api_url = "http://api.aladhan.com/v1/calendar?"

    def __init__(self, latitude: float, longitude: float, month: int = None, year: int = None, annual: bool = None,
                 method: int = 99, tune: str = None, school: int = 1, midnight_mode: int = None, timezonestr: str = None,
                 latitude_adjustment_method: int = None, adjustment: int = None):
        super().__init__()
        self.latitude = latitude
        self.longitude = longitude
        self.month = month
        self.year = year
        self.annual = annual
        self.method = method
        self.tune = tune
        self.school = school
        self.midnight_mode = midnight_mode
        self.timezonestr = timezonestr
        self.latitude_adjustment_method = latitude_adjustment_method
        self.adjustment = adjustment
        self._url = self._api_url
        if not self.month:
            self.month = self._get_date("month")
        if not self.year:
            self.year = self._get_date("year")
        if self.method == 99:
            self.method_settings="15,null,15"

class CalendarByAddress(Base):
    _api_url = "http://api.aladhan.com/v1/calendarByAddress?"

    def __init__(self, address: str, month: int = None, year: int = None, annual: bool = None, method: int = 99,
                 tune: str = None, school: int = 1, midnight_mode: int = None, timezonestr: str = None,
                 latitude_adjustment_method: int = None, adjustment: int = None):
        super().__init__()
        self.address = address
        self.month = month
        self.year = year
        self.annual = annual
        self.method = method
        self.tune = tune
        self.school = school
        self.midnight_mode = midnight_mode
        self.timezonestr = timezonestr
        self.latitude_adjustment_method = latitude_adjustment_method
        self.adjustment = adjustment
        self._url = self._api_url
        if not self.month:
            self.month = self._get_date("month")
        if not self.year:
            self.year = self._get_date("year")
        if self.method == 99:
            self.method_settings="15,null,15"


class CalendarByCity(Base):
    _api_url = "http://api.aladhan.com/v1/calendarByCity?"

    def __init__(self, city: str, country: str, state: str = None, month: int = None, year: int = None,
                 annual: bool = None, method: int = 99, tune: str = None, school: int = 1, midnight_mode: int = None,
                 timezonestr: str = None, latitude_adjustment_method: int = None, adjustment: int = None):
        super().__init__()
        self.city = city
        self.country = country
        self.state = state
        self.month = month
        self.year = year
        self.annual = annual
        self.method = method
        self.tune = tune
        self.school = school
        self.midnight_mode = midnight_mode
        self.timezonestr = timezonestr
        self.latitude_adjustment_method = latitude_adjustment_method
        self.adjustment = adjustment
        self._url = self._api_url
        if not self.month:
            self.month = self._get_date("month")
        if not self.year:
            self.year = self._get_date("year")
        if self.method == 99:
            self.method_settings="15,null,15"


class HijriCalendar(Calendar):
    _api_url = "http://api.aladhan.com/v1/hijriCalendar?"

    def __init__(self, latitude: float, longitude: float, month: int = None, year: int = None, annual: bool = None,
                 method: int = 99, tune: str = None, school: int = 1, midnight_mode: int = None, timezonestr: str = None,
                 latitude_adjustment_method: int = None, adjustment: int = None):
        super().__init__(latitude, longitude, month, year, annual, method, tune, school, midnight_mode, timezonestr,
                         latitude_adjustment_method, adjustment)
        self._url = self._api_url
        if not self.month:
            self.month = self._get_date("month")
        if not self.year:
            self.year = self._get_date("year")
        if self.method == 99:
            self.method_settings="15,null,15"


class HijriCalendarByAddress(Base):
    _api_url = "http://api.aladhan.com/v1/hijriCalendarByAddress?"

    def __init__(self, address: str, month: int = None, year: int = None, annual: bool = None, method: int = 99,
                 tune: str = None, school: int = 1, midnight_mode: int = None, timezonestr: str = None,
                 latitude_adjustment_method: int = None, adjustment: int = None):
        super().__init__()
        self.address = address
        self.month = month
        self.year = year
        self.annual = annual
        self.method = method
        self.tune = tune
        self.school = school
        self.midnight_mode = midnight_mode
        self.timezonestr = timezonestr
        self.latitude_adjustment_method = latitude_adjustment_method
        self.adjustment = adjustment
        self._url = self._api_url
        if not self.month:
            self.month = self._get_date("month")
        if not self.year:
            self.year = self._get_date("year")
        if self.method == 99:
            self.method_settings="15,null,15"


class HijriCalendarByCity(Base):
    _api_url = "http://api.aladhan.com/v1/hijriCalendarByCity?"

    def __init__(self, city: str, country: str, state: str = None, month: int = None, year: int = None,
                 annual: bool = None, method: int = 99, tune: str = None, school: int = 1, midnight_mode: int = None,
                 timezonestr: str = None, latitude_adjustment_method: int = None, adjustment: int = None):
        super().__init__()
        self.city = city
        self.country = country
        self.state = state
        self.month = month
        self.year = year
        self.annual = annual
        self.method = method
        self.tune = tune
        self.school = school
        self.midnight_mode = midnight_mode
        self.timezonestr = timezonestr
        self.latitude_adjustment_method = latitude_adjustment_method
        self.adjustment = adjustment
        self._url = self._api_url
        if not self.month:
            self.month = self._get_date("month")
        if not self.year:
            self.year = self._get_date("year")
        if self.method == 99:
            self.method_settings="15,null,15"


class Timings(Base):
    _api_url = "http://api.aladhan.com/v1/timings/{timestamp}?"

    def __init__(self, latitude: float, longitude: float, date_or_timestamp: str = None, method: int = 99,
                 tune: str = None, school: int = 1, midnight_mode: int = None, timezonestr: str = None,
                 latitude_adjustment_method: int = None, adjustment: int = None):
        super().__init__()
        self.date_or_timestamp = date_or_timestamp
        self.latitude = latitude
        self.longitude = longitude
        self.method = method
        self.tune = tune
        self.school = school
        self.midnight_mode = midnight_mode
        self.timezonestr = timezonestr
        self.latitude_adjustment_method = latitude_adjustment_method
        self.adjustment = adjustment
        self._url = self._api_url
        if self.date_or_timestamp is None:
            self.date_or_timestamp = self._get_date("timestamp")
        if self.method == 99:
            self.method_settings="15,null,15"


class TimingsByAddress(Base):
    _api_url = "http://api.aladhan.com/v1/timingsByAddress/{timestamp}?"

    def __init__(self, address: str, date_or_timestamp: str = None, method: int = 99, tune: str = None, school: int = 1,
                 midnight_mode: int = None, timezonestr: str = None, latitude_adjustment_method: int = None,
                 adjustment: int = None):
        super().__init__()
        self.date_or_timestamp = date_or_timestamp
        self.address = address
        self.method = method
        self.tune = tune
        self.school = school
        self.midnight_mode = midnight_mode
        self.timezonestr = timezonestr
        self.latitude_adjustment_method = latitude_adjustment_method
        self.adjustment = adjustment
        self._url = self._api_url
        if self.date_or_timestamp is None:
            self.date_or_timestamp = self._get_date("timestamp")
        if self.method == 99:
            self.method_settings="15,null,15"


class TimingsByCity(Base):
    _api_url = "http://api.aladhan.com/v1/timingsByCity?"

    def __init__(self, city: str, country: str, state: str = None, date_or_timestamp: str = None, method: int = 99,
                 tune: str = None, school: int = 1, midnight_mode: int = None, timezonestr: str = None,
                 latitude_adjustment_method: int = None, adjustment: int = None):
        super().__init__()
        self.date_or_timestamp = date_or_timestamp
        self.city = city
        self.country = country
        self.state = state
        self.method = method
        self.tune = tune
        self.school = school
        self.midnight_mode = midnight_mode
        self.timezonestr = timezonestr
        self.latitude_adjustment_method = latitude_adjustment_method
        self.adjustment = adjustment
        self._url = self._api_url
        if self.date_or_timestamp is None:
            self.date_or_timestamp = self._get_date("timestamp")
        if self.method == 99:
            self.method_settings="15,null,15"

class CurrentDate(BaseClass):
    _api_url = "http://api.aladhan.com/v1/currentDate?zone={zone}"

    def __init__(
            self,
            zone: str
    ):
        self.zone = zone
        self._url = self._api_url.format(zone=self.zone)

    async def get(self):
        content = await self.get_content(self._url)
        return content


class CurrentTime(CurrentDate):
    _api_url = "http://api.aladhan.com/v1/currentTime?zone={zone}"

    def __init__(self, zone: str):
        super().__init__(zone)
        self.zone = zone
        self._url = self._api_url.format(zone=self.zone)


class CurrentTimestamp(CurrentDate):
    _api_url = "http://api.aladhan.com/v1/currentTimestamp?zone={zone}"

    def __init__(self, zone: str):
        super().__init__(zone)
        self.zone = zone
        self._url = self._api_url.format(zone=self.zone)


class PrayerTimeMethods(BaseClass):
    _api_url = "http://api.aladhan.com/v1/methods"

    async def get(self):
        content = await self.get_content(self._api_url)
        return content


class GetSura(BaseClass):
    url_ar = "http://api.alquran.cloud/v1/surah/{sura}/editions/quran-simple"
    url_uz = "http://api.alquran.cloud/v1/surah/{sura}/editions/uz.sodik"
    def __init__(self):
        super().__init__()

    async def meaning_uz(self, sura: int):
        url: str = self.url_uz.format(sura=sura)
        ayahs = (await self.get_content(url=url))[0]["ayahs"]
        ayahs_list = (to_latin(i["text"]) for i in ayahs)
        return ayahs_list

    async def meaning_ar(self, sura):
        url = self.url_ar.format(sura=sura)
        ayahs = (await self.get_content(url))[0]["ayahs"]
        ayahs_list = (i["text"] for i in ayahs)
        return ayahs_list

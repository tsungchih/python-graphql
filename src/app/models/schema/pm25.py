# -*- coding: utf-8 -*-

"""
.. module:: pm25
   :synopsis: This module includes all the classes related to GraphQL Schema in terms of PM2.5.

.. moduleauthor:: George T. C. Lai
"""

import logging
import ujson
from abc import ABC, abstractmethod
from graphene import Interface, String, Int, Float, List, ObjectType
from timeit import default_timer as timer


async def get_json_from(session, api_url: str, sslcontext = None):
    async with session.get(api_url, timeout=60) as response:
        return await response.json()

class RemoteQuery(ABC):
    """[summary]
    
    Args:
        ABC ([type]): [description]
    """
    def __init__(self, url):
        self.api_url = url
        self.__proto, tmp = url.split("://")
        self.__base_url = tmp.split('/')[0]

    @abstractmethod
    async def _send_query(self):
        pass

    @abstractmethod
    async def get_data(self):
        pass


class APIRemoteQuery(RemoteQuery):
    def __init__(self, url):
        super().__init__(url)

    async def _send_query(self):
        async with self._session.get(self.api_url, timeout=60) as response:
            data = await response.json()
            return ujson.loads(data.text)

    async def get_data(self):
        data = await self._send_query()
        return data


class AbstractSite(Interface):
    county = String()
    site_name = String()


class PM10Site(ObjectType):
    class Meta:
        interfaces = (AbstractSite,)
    pm10 = Int()
    unit = String()

class PM25Site(ObjectType):
    class Meta:
        interfaces = (AbstractSite, )
    pm25 = Int()
    unit = String()


class UVSite(ObjectType):
    """[summary]
    
    :param ObjectType: [description]
    :type ObjectType: [type]
    """
    class Meta:
        interfaces = (AbstractSite,)
    uvi = Float()
    wgs84_lat = Float()
    wgs84_lon = Float()


class PM25Query(ObjectType):
    counties = List(PM25Site, county=String(default_value="臺北市"))
    uv = List(UVSite, county=String(default_value="臺北市"))
    pm10 = List(PM10Site, county=String(default_value="臺北市"))

    async def resolve_counties(root, info, county):
        target_url = "https://opendata.epa.gov.tw/api/v1/ATM00625/?$format=json"
        #query = PM25RemoteQuery(target_url)
        #data = query.get_data()
        data = await get_json_from(session=info.context['session'], api_url=target_url, sslcontext=info.context['sslctx'])
        target_data = filter(lambda x: x["county"] == county, data)
        return list(map(lambda x: PM25Site(
            county=x["county"],
            site_name=x["Site"],
            pm25=x["PM25"],
            unit=x["ItemUnit"]), target_data))

    async def resolve_pm10(root, info, county: str):
        start_time = timer()
        target_url = "https://opendata.epa.gov.tw/api/v1/ATM00764?$format=json"
        #query = PM25RemoteQuery(target_url)
        #data = query.get_data()
        data = await get_json_from(session=info.context['session'], api_url=target_url, sslcontext=info.context['sslctx'])
        #logging.info("PM10 request time elapsed: {}".format(query.get_time_elapsed()))
        target_data = filter(lambda x: x["County"] == county, data)
        results = list(map(lambda x: PM10Site(
            county=x["County"],
            site_name=x["SiteName"],
            pm10=int(x["Concentration"]) if not x["Concentration"] == "x" else -1,
            unit=x["ItemUnit"]), target_data))
        logging.info("Time elapsed while resolving pm10: {}".format(timer()-start_time))
        return results

    async def resolve_uv(root, info, county: str):
        start_time = timer()
        target_url = "https://opendata.epa.gov.tw/api/v1/UV?$format=json"
        #query = PM25RemoteQuery(target_url)
        #data = query.get_data()
        #logging.info("UV request time elapsed: {}".format(query.get_time_elapsed()))
        data = await get_json_from(session=info.context['session'], api_url=target_url)
        target_data = filter(lambda x: x["County"] == county, data)
        results = list(map(lambda x: UVSite(
            county=x["County"],
            site_name=x["SiteName"],
            uvi=x["UVI"],
            wgs84_lat=x["WGS84Lat"].replace(",", ""),
            wgs84_lon=x["WGS84Lon"].replace(",", "")), target_data))
        logging.info("Time elapsed while resolving uv: {}".format(timer()-start_time))
        return results

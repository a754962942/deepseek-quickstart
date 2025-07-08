
import httpx

base_url = 'https://restapi.amap.com/v3/weather/weatherInfo'


def query_current_weather_by_city_code(api_key:str,city_code:str):
    params={
        "key":api_key,
        "city":city_code
    }
    resp = httpx.get(base_url,params=params)
    return resp.json()

def query_forecast_weather_by_cityname(api_key:str,city_code:str):
    params={
        "key":api_key,
        "city":city_code,
        "extensions":"all"
    }
    resp = httpx.get(base_url,params=params)
    return resp.json()
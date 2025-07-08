from mcp.server.fastmcp import FastMCP
import pandas as pd
from dotenv import load_dotenv
import os
import datetime
from weather import query_current_weather_by_city_code,query_forecast_weather_by_cityname
load_dotenv()
mcp = FastMCP("Weather")


weather_api_key = os.environ.get('amap_api_key')

city_map = {}
short_map={}

df = pd.read_excel('AMap_adcode_citycode.xlsx',sheet_name=0,usecols=[0,1])
for index,row in df.iterrows():
    city_name = row['中文名']
    city_code = row['adcode']
    city_map[city_name]=city_code
    short_map[city_name[:-1]] = city_code

# 示例中，需定义识别传入城市名/区名，查找映射获取对应citycode 的tool
# 上述工具增加了mcp tool的复杂度
# 此处分离逻辑仅用于学习mcp.resource工作逻辑
@mcp.tool()
async def query_city_weather_by_cityname(city_name:str,future:bool=False)->str:
    """
    city_name 为查询天气的城市名 例如:杭州市 苏州市 北京市 上海市,
    future 为是否查询预报天气.如果查询预报天气.请输入true。否则查询当前天气.默认为False
    """
    print(f"city_name:{city_name},future:{future}")
    city_code =await query_adcode(city_name)
    if len(city_code)==0:
        return "找不到城市编码"
    if future is not False:
        reports=[]
        response = query_forecast_weather_by_cityname(weather_api_key,city_code)
        if response["status"] == 0 :
            return "请求失败"
        else:
            casts = response['forecasts'][0]['casts']
            print(f"casts:{casts}")
            if casts:
                for item in casts:
                    item_weather = f"""
                    日期:{item['date']}
                    白天:{item['dayweather']}
                    晚上:{item['nightweather']}
                    白天温度:{item['daytemp']}
                    晚上温度:{item['nighttemp']}
                    """
                    reports.append(item_weather)
                return ",".join(reports)
            return "获取失败"
    else:
        response = query_current_weather_by_city_code(weather_api_key,city_code)
        if response["status"] == 0 :
            return "请求失败"
        city_data = response['lives'][0]
        result=f'日期:{datetime.date.today()}\n城市:{city_data["city"]}\n天气:{city_data["weather"]}\n温度:{city_data["temperature"]}'
        return result
        


async def query_adcode(city_name:str)->str:
    """
    输入城市名称,获取城市编码
    传入 city_name 返回city_code
    city_code用于查询城市天气
    """
    print("city_name:",city_name)
    code = city_map[city_name]
    if code:
        return str(code)
    elif not code:
        code = short_map[city_name]
    if code:
        return str(code)
    else:
        return ""

# async def main():
    # weather1 =await query_city_weather_by_cityname("杭州市",future=True)
    # print(weather1)
    # weather2 =await query_city_weather_by_cityname("杭州市",future=False)
    # print(weather2)
if __name__ == "__main__":
    mcp.run(transport='stdio')

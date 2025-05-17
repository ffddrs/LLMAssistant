import requests
import os
from datetime import datetime
import json
import sympy
from sympy import asin, acos, atan, sin, cos, tan, sinh, cosh, tanh, sec, csc, cot, acot, acsc, asec, exp, log, limit, pi, sqrt, integrate, degree, diff

# 定义工具列表，模型在选择使用哪个工具时会参考工具的name和description
tools = [
    # 工具1 获取当前时刻的时间
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "当你想知道现在的时间时非常有用。",
            "parameters": {}  # 因为获取当前时间无需输入参数，因此parameters为空字典
        }
    },  
    # 工具2 获取指定城市的天气
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "当你想查询指定城市的天气时非常有用。",
            "parameters": {  # 查询天气时需要提供位置，因此参数设置为location
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "城市或县区，比如北京市、杭州市、余杭区等。"
                    }
                }
            },
            "required": [
                "location"
            ]
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_earthquake_info",
            "description": "当你想查询地震相关信息时非常有用。该工具返回指定区域，指定时间范围内，指定震级范围内的所有地震详细信息， 结果以字符串格式的python列表储存。请注意：所有的经纬度，时间，震级范围都不要太大，否则可能返回巨量数据，因此请根据用户需求，合理选择经纬度，时间和震级区间。请务必注意：如有可能，请尽量填满所有参数。请着重注意：如用户查询某一特定地震，查询范围务必略放宽，否则可能查询不到",
            "parameters": {  
                "type": "object",
                "properties": {
                    "starttime": {
                        "type": "string",
                        "description": """
Limit to events on or after the specified start time. 
NOTE: All times use ISO8601 Date/Time format. Unless a timezone is specified, UTC is assumed.
IMPORTANT NOTE: Starttime CANNOT be the same as endtime
Default: present time - 30 days
Examples:

2025-05-11, Implicit UTC timezone, and time at start of the day (00:00:00)
2025-05-11T10:41:57, Implicit UTC timezone.
2025-05-11T10:41:57+00:00, Explicit timezone.
 """
                    },
                    "endtime": {
                        "type": "string",
                        "description": """
Limit to events on or before the specified end time. 
NOTE: All times use ISO8601 Date/Time format. Unless a timezone is specified, UTC is assumed.
IMPORTANT NOTE: Starttime CANNOT be the same as endtime
Default: present time
Examples:

2025-05-11, Implicit UTC timezone, and time at start of the day (00:00:00)
2025-05-11T10:41:57, Implicit UTC timezone.
2025-05-11T10:41:57+00:00, Explicit timezone.
"""
                    },
                    "minlatitude": {
                        "type": "Decimal [-90,90] degrees",
                        "description": "Limit to events with a latitude larger than the specified minimum. NOTE: min values must be less than max values. Default: -90"
                    },
                    "maxlatitude": {
                        "type": "Decimal [-90,90] degrees",
                        "description": "Limit to events with a latitude smaller than the specified maximum. NOTE: min values must be less than max values. Default: 90"
                    },
                    "minlongitude": {
                        "type": "Decimal [-360,360] degrees",
                        "description": "Limit to events with a longitude larger than the specified minimum. NOTE: rectangles may cross the date line by using a minlongitude < -180 or maxlongitude > 180. NOTE: min values must be less than max values. Default: -180"
                    },
                    "maxlongitude": {
                        "type": "Decimal [-360,360] degrees",
                        "description": "Limit to events with a longitude smaller than the specified maximum. NOTE: rectangles may cross the date line by using a minlongitude < -180 or maxlongitude > 180. NOTE: min values must be less than max values. Default: 180"
                    },
                    "minmagnitude": {
                        "type": "Decimal",
                        "description": "Limit to events with a magnitude larger than the specified minimum. Default: 3.0"
                    },
                    "maxmagnitude": {
                        "type": "Decimal",
                        "description": "Limit to events with a magnitude smaller than the specified maximum. Default: None"
                    }
                }
            },
        }
    },

    {
        "type":"function",
        "function":{
            "name":"get_movie_info",
            "description":"当用户想查询电影相关问题时非常有用，返回目标电影的相关信息，以字符串格式的python字典储存。",
            "parameters":{
                "type":"object",
                "properties":{
                    "movie_name":{
                        "type":"string",
                        "description":"当用户要查询电影相关的问题时非常有用"
                    }
                }
            },
            "required":[
                "movie_name"
            ]
        }
    },

    {
        "type":"function",
        "function":{
            "name":"calculator",
            "description":"当用户需要数学计算时非常有用。",
            "parameters":{
                "type":"object",
                "properties":{
                    "expr":{
                        "type":"string",
                        "description":"这是需要计算或求解的数学表达式,以sympy的形式"
                    },
                    "func":{
                        "type":"string",
                        "description":"功能代码，需要计算数学表达式时是‘eval’，需要求解方程时是‘solve’"
                    }
                }
            },
            "required":[
                "expr",
                "func"
            ]
        }
    },
    {
        "type": "function",
        "function":{
            "name":"get_stock_info_intraday",
            "description":"This API returns current and 20+ years of historical intraday OHLCV time series of the equity specified, covering pre-market and post-market hours where applicable (e.g., 4:00am to 8:00pm Eastern Time for the US market). You can query both raw (as-traded) and split/dividend-adjusted intraday data from this endpoint. The OHLCV data is sometimes called 'candles' in finance literature.",
            "parameters":{
                "type":"object",
                "properties":{
                    "symbol":{
                        "type":"string",
                        "description":"The name of the equity of your choice. For example: symbol=IBM"
                    },
                    "interval":{
                        "type":"string",
                        "description":"Time interval between two consecutive data points in the time series. The following values are supported: 1min, 5min, 15min, 30min, 60min"
                    },
                    "month":{
                        "type":"string",
                        "description":"By default, this parameter is not set and the API will return intraday data for the most recent days of trading. You can use the month parameter (in YYYY-MM format) to query a specific month in history. For example, month=2009-01. Any month in the last 20+ years since 2000-01 (January 2000) is supported."
                    },
                    "outputsize":{
                        'type':"string",
                        "description":"By default, outputsize=compact. Strings compact and full are accepted with the following specifications: compact returns only the latest 100 data points in the intraday time series; full returns trailing 30 days of the most recent intraday data if the month parameter (see above) is not specified, or the full intraday data for a specific month in history if the month parameter is specified. The 'compact' option is recommended if you would like to reduce the data size of each API call."
                    }
                }
            },
            "required":[
                "symbol",
                "interval",
                "month",
            ]
        }
    },
    {
        "type": "function",
        "function":{
            "name":"get_stock_info_daily",
            "description":"This API returns raw (as-traded) daily time series (date, daily open, daily high, daily low, daily close, daily volume) of the global equity specified, covering 20+ years of historical data. The OHLCV data is sometimes called 'candles' in finance literature.",
            "parameters":{
                "type":"object",
                "properties":{
                    "symbol":{
                        "type":"string",
                        "description":"The name of the equity of your choice. For example: symbol=IBM"
                    },
                    "outputsize":{
                        'type':"string",
                        "description":"By default, outputsize=compact. Strings compact and full are accepted with the following specifications: compact returns only the latest 100 data points; full returns the full-length time series of 20+ years of historical data. The 'compact' option is recommended if you would like to reduce the data size of each API call."
                    }
                }
            },
            "required":[
                "symbol"
            ]
        }
    },
    {
        "type": "function",
        "function":{
            "name":"get_stock_info_weekly",
            "description":"This API returns weekly time series (last trading day of each week, weekly open, weekly high, weekly low, weekly close, weekly volume) of the global equity specified, covering 20+ years of historical data.",
            "parameters":{
                "type":"object",
                "properties":{
                    "symbol":{
                        "type":"string",
                        "description":"The name of the equity of your choice. For example: symbol=IBM"
                    }
                }
            },
            "required":[
                "symbol"
            ]
        }
    }


]

def get_stock_info_intraday(symbol,month,interval="15min",outputsize=None):
    url= 'https://www.alphavantage.co/query'
    apikey= "DGSZGS0ZM33EM4UU"
    params = {
        'function': 'TIME_SERIES_INTRADAY',
        'symbol': symbol,
        'interval': interval,
        'month': month,
        "outputsize": outputsize,
        'apikey': apikey
    }
    r=requests.get(url,params=params)
    data=json.loads(r.text)
    data=data[f"Time Series ({interval})"]
    return str(data)

def get_stock_info_daily(symbol,outputsize=None):
    url= 'https://www.alphavantage.co/query'
    apikey= "DGSZGS0ZM33EM4UU"
    params = {
        'function': 'TIME_SERIES_DAILY',
        'symbol': symbol,
        "outputsize": outputsize,
        'apikey': apikey
    }
    r=requests.get(url,params=params)
    data=json.loads(r.text)
    data=data[f"Time Series (Daily)"]
    return str(data)

def get_stock_info_weekly(symbol):
    url= 'https://www.alphavantage.co/query'
    apikey= "DGSZGS0ZM33EM4UU"
    params = {
        'function': 'TIME_SERIES_WEEKLY',
        'symbol': symbol,
        'apikey': apikey
    }
    r=requests.get(url,params=params)
    data=json.loads(r.text)
    data=data[f"Weekly Time Series"]
    return str(data)


def calculator(expr,func):
    expr=sympy.parse_expr(expr)
    if func=="solve":
        return str(sympy.solve(expr))
    if func=="eval":
        return str(sympy.N(expr))
    

def get_earthquake_info(starttime=None,endtime=None,minlatitude=None,maxlatitude=None,minlongitude=None,maxlongitude=None,minmagnitude=3,maxmagnitude=None):

    minlatitude = float(minlatitude) if minlatitude is not None else None
    maxlatitude = float(maxlatitude) if maxlatitude is not None else None
    minlongitude = float(minlongitude) if minlongitude is not None else None
    maxlongitude = float(maxlongitude) if maxlongitude is not None else None
    minmagnitude = float(minmagnitude) if minmagnitude is not None else None
    maxmagnitude = float(maxmagnitude) if maxmagnitude is not None else None

    if starttime==endtime:
        endtime=starttime+'T23:59:59'

    params = {
        "format": "geojson",
        "starttime": starttime,
        "endtime": endtime,
        "minlatitude": minlatitude,
        "maxlatitude": maxlatitude,
        "minlongitude": minlongitude,
        "maxlongitude": maxlongitude,
        "minmagnitude": minmagnitude,
        "maxmagnitude": maxmagnitude
    }
    url = "https://earthquake.usgs.gov/fdsnws/event/1/query"
    r = requests.get(url, params=params) 
    data = json.loads(r.text)
    data=data['features']
    for i in range(len(data)):
        data[i]['properties']['time']=str(datetime.fromtimestamp(data[i]['properties']['time']/1000))
        data[i]=f"{i+1}. {data[i]['properties']['title']}     place: {data[i]['properties']['place']} magnitude: {data[i]['properties']['mag']} time: {data[i]['properties']['time']} longitude: {data[i]['geometry']['coordinates'][0]} latitude: {data[i]['geometry']['coordinates'][1]} depth: {data[i]['geometry']['coordinates'][2]}km"
    return str(data)

def get_movie_info(movie_name):
    with open('movies_list.json','r',encoding="utf-8") as unparsedmovieslist:
        with open('comments_list.json','r',encoding='utf-8') as unparsedcommentslist:
            movieslist=json.load(unparsedmovieslist)
            commentslist=json.load(unparsedcommentslist)
            targetmovie=[movie for movie in movieslist if movie_name in movie['title']]
            movieid=targetmovie[0]['id']
            targetmovie[0]['comments']=[comment for comment in commentslist if comment['movie_id']==movieid]
            return str(targetmovie[0])

# 模拟天气查询工具。返回结果示例：“北京今天是晴天。”
def get_current_weather(location):
    params = {
        "key": "SDKyJowJ9YLkPC4sI",
        "location": location,
        "language": "zh-Hans",
        "unit": "c",
    }
    url = "https://api.seniverse.com/v3/weather/now.json"
    r = requests.get(url, params=params) 
    data = r.json()["results"][0]['now']
    return f"{location}今天是{data['text']}，温度{data['temperature']}摄氏度 "

# 查询当前时间的工具。返回结果示例：“当前时间：2024-04-15 17:15:18。“
def get_current_time():
    # 获取当前日期和时间
    current_datetime = datetime.now()
    # 格式化当前日期和时间
    formatted_time = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
    # 返回格式化后的当前时间
    return f"当前时间：{formatted_time}。"

def get_response(messages):
    # TODO：你自己的API
    api_key = "sk-ebc102be4c824eb592fe70217856069d"
    url = 'https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation'
    headers = {'Content-Type': 'application/json',
            'Authorization':f'Bearer {api_key}'}
    body = {
        'model': 'qwen-turbo',
        "input": {
            "messages": messages
        },
        "parameters": {
            "result_format": "message",
            "tools": tools
        }
    }

    response = requests.post(url, headers=headers, json=body)
    return response.json()

messages = [
    {
        "role": "system",
        "content": """你是一个很有帮助的助手。
     注意：在每次对话开始之前，必须至少进行一次当前时间查询，即调用‘get_current_time’函数，以确保时间正确，不需要重复调用
     如果用户提问关于天气的问题，请调用 ‘get_current_weather’ 函数;
     如果用户提问关于时间的问题，请调用‘get_current_time’函数；
     如果用户提问关于电影的问题，请调用‘get_movie_info'函数；
     如果用户提问关于地震的问题，请调用‘get_earthquake_info’函数；
     如果用户提问关于数学计算的问题，请调用‘calculator’函数。
     回答时请确定好当前时间，必要时可调用工具函数。
     请以友好的语气回答问题。""",
    },
    {
        "role": "user",
        "content": "今天天气怎么样？"
    }
]

def call_with_messages():
    messages=[]
    while True:
        usermessage=input('请输入（输入exit停止对话）：')
        if usermessage=='exit':
            break
        messages.append({
                    "content": usermessage,  # 提问示例："现在几点了？" "一个小时后几点" "北京天气如何？"
                    "role": "user"
                })
        count=1

        # 模型的第count轮调用
        first_response = get_response(messages)
        print(f"\n第{count}轮调用结果：{first_response}")
        assistant_output = first_response['output']['choices'][0]['message']
        messages.append(assistant_output)
        if 'tool_calls' not in assistant_output:  # 如果模型判断无需调用工具，则将assistant的回复直接打印出来，无需进行模型的第二轮调用
            print(f"最终答案：{assistant_output['content']}")
        else:
            while 'tool_calls' in assistant_output:
                count+=1
                try:
                    # 如果模型选择的工具是get_current_weather
                    if assistant_output['tool_calls'][0]['function']['name'] == 'get_current_weather':
                        tool_info = {"name": "get_current_weather", "role": "tool"}
                        location = json.loads(assistant_output['tool_calls'][0]['function']['arguments'])['location']
                        tool_info['content'] = get_current_weather(location)
                    # 如果模型选择的工具是get_current_time
                    elif assistant_output['tool_calls'][0]['function']['name'] == 'get_current_time':
                        tool_info = {"name": "get_current_time", "role": "tool"}
                        tool_info['content'] = get_current_time()
                    elif assistant_output['tool_calls'][0]['function']['name'] == 'get_movie_info':
                        tool_info = {'name':'get_movie_info', 'role': 'tool'}
                        movie_name = json.loads(assistant_output['tool_calls'][0]['function']['arguments'])['movie_name']
                        tool_info['content'] = get_movie_info(movie_name)
                    elif assistant_output['tool_calls'][0]['function']['name'] == 'get_earthquake_info':
                        tool_info = {'name': 'get_earthquake_info', 'role': 'tool'}
                        kwargs = json.loads(assistant_output['tool_calls'][0]['function']['arguments'])
                        tool_info['content'] = get_earthquake_info(**kwargs)
                    elif assistant_output['tool_calls'][0]['function']['name'] == 'calculator':
                        tool_info = {'name':'calculator', 'role': 'tool'}
                        expr = json.loads(assistant_output['tool_calls'][0]['function']['arguments'])['expr']
                        func = json.loads(assistant_output['tool_calls'][0]['function']['arguments'])['func']
                        tool_info['content'] = calculator(expr,func)
                    elif assistant_output['tool_calls'][0]['function']['name'] == 'get_stock_info_intraday':
                        tool_info = {'name':'get_stock_info_intraday', 'role': 'tool'}
                        kwargs = json.loads(assistant_output['tool_calls'][0]['function']['arguments'])
                        tool_info['content'] = get_stock_info_intraday(**kwargs)
                    elif assistant_output['tool_calls'][0]['function']['name'] == 'get_stock_info_daily':
                        tool_info = {'name':'get_stock_info_daily', 'role': 'tool'}
                        kwargs = json.loads(assistant_output['tool_calls'][0]['function']['arguments'])
                        tool_info['content'] = get_stock_info_daily(**kwargs)
                    elif assistant_output['tool_calls'][0]['function']['name'] == 'get_stock_info_weekly':
                        tool_info = {'name':'get_stock_info_weekly', 'role': 'tool'}
                        kwargs = json.loads(assistant_output['tool_calls'][0]['function']['arguments'])
                        tool_info['content'] = get_stock_info_weekly(**kwargs)
                except:
                    tool_info = {'name':assistant_output['tool_calls'][0]['function']['name'], 'role': 'tool'}
                    tool_info['content'] = "工具调用失败，发生异常错误"
                print(f"工具输出信息：{tool_info['content']}")
                messages.append(tool_info)
                count_response = get_response(messages)
                print(f"第{count}轮调用结果：{count_response}")
                assistant_output=count_response['output']['choices'][0]['message']
            print(f"最终答案：{count_response['output']['choices'][0]['message']['content']}")


if __name__ == '__main__':
    call_with_messages()
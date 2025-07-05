import json, sys, re
import requests
import jsonlines
import folium
import copy
from urllib.parse import quote
from datetime import datetime, timedelta

def read_json_lines(file_path):
    data = []
    try:
        with jsonlines.open(file_path) as reader:
            for obj in reader:
                data.append(obj)
    except FileNotFoundError:
        sys.exit()
    except IOError as e:
        sys.exit()
    return data

def parse_datetime(datetime_str):
    dt = datetime.fromisoformat(datetime_str)
    return {
        "date": dt.strftime('%Y-%m-%d'),
        "year": dt.year,
        "month": dt.month,
        "day": dt.day,
        "hour": dt.hour,
        "minute": dt.minute,
        "str": dt.strftime('%Y-%m-%dT%H:%M:%S')
    }

def create_request_url(start_spot, goal_spot, routeType):
    start = quote(json.dumps({"name":start_spot["name"],"lat":start_spot["lat"],"lon":start_spot["lon"],"type":start_spot["type"],"selectNearNode":None,"nearest-node-id":"","nearest-node-name":""}, ensure_ascii=False, separators=(',', ':')), safe='')
    goal  = quote(json.dumps([{"name":goal_spot["name"],"lat":goal_spot["lat"],"lon":goal_spot["lon"],"type":goal_spot["type"],"selectNearNode":None,"nearest-node-id":"","nearest-node-name":""}], ensure_ascii=False, separators=(',', ':')), safe='')
    return (f'https://www.navitime.co.jp/async/route/comparison/search?start={start}&goal={goal}&routeType={routeType}&searchType=poi&date={start_spot["date"]}&hour={start_spot["hour"]}&minutes={start_spot["minutes"]}&timeType=start-time&vics=false')

def create_spots_query(pickup, start_place):
    spots = []
    result = parse_datetime(start_place['time'])
    jaran_spots = read_json_lines("assets/spots.jsonl")
    spots.append({"name":start_place['name'],"lat":start_place['lat'],"lon":start_place['lon'],"type":start_place['type'],"date":result['date'],"hour":result['hour'],"minutes":result['minute']})
    for i in range(len(pickup)):
        spots.append({"name":jaran_spots[pickup[i]['index']]["名称"],"image":jaran_spots[pickup[i]['index']]["画像"][0],"lat":jaran_spots[pickup[i]['index']]["座標"][0],"lon":jaran_spots[pickup[i]['index']]["座標"][1],"type":"spot","date":result['date'],"hour":result['hour'],"minutes":result['minute']})
    return spots    

def get_move(start_spot, goal_spot, routeType):
    response = requests.get(create_request_url(start_spot, goal_spot, routeType))
    if response.status_code == 200:
        data = response.json()
        routeList = data.get("routeList", "")[0]
        routeShape = routeList.get("routeShape", None)
        route = routeList.get("route", None)
        sections = route.get("sections", None)
        return (sections, routeShape)
    else:
        return None

def get_moves(pickup, start_place):
    moves = []
    routes = []
    date_time = []
    spots = create_spots_query(pickup, start_place)
    for i in range(len(spots) - 1):
        sections, routeShape = get_move(spots[i], spots[i+1], start_place['routeType'])
        moves.append(sections)
        routes.append(routeShape)
        if moves[i] == None or routes[i] == None:
            sys.exit()
        for step in moves[i]:
            if step['type'] == 'move':
                date_time.append(step['to_time'])
        result = parse_datetime(date_time[-1])
        time = datetime.fromisoformat(result['str']) + timedelta(minutes=pickup[i]['stay'])
        next_start = parse_datetime(time.isoformat())
        spots[i+1]['date'] = next_start['date']
        spots[i+1]['hour'] = next_start['hour']
        spots[i+1]['minutes'] = next_start['minute']
    return (moves, routes, spots)

def create_spot_pin(name, image):
    return (f'''
        <div style="display: flex; flex-direction: column; align-items: center; width: 75px; text-align: center;">
            <div style="border: 2px solid black; border-radius: 50%; overflow: hidden; width: 75px; height: 75px;">
                <img src="{image}" style="width: 100%; height: 100%; border-radius: 50%;">
            </div>
            <div style="background: rgba(255, 255, 255, 0.7); border-radius: 5px; padding: 2px; margin-top: 5px;">
                {name}
            </div>
        </div>
    ''')

def get_style_function(color):
        return lambda feature: {'color': color, 'weight': 10, 'opacity': 1.0}

def expand_bounds(bounds, padding=0.01):
    sw, ne = bounds
    return [
        [sw[0] - padding, sw[1] - padding],
        [ne[0] + padding, ne[1] + padding],
    ]

def create_map(routes, spots):
    m = folium.Map()
    bounds = []
    for i, routeShape in enumerate(routes):
        route = folium.GeoJson(routeShape, name=spots[i+1]["name"], style_function=get_style_function("blue")).add_to(m)
        goal_icon_html = create_spot_pin(spots[i+1]["name"], spots[i+1]["image"])
        goal_icon = folium.DivIcon(html=f"""<div>{goal_icon_html}</div>""", icon_anchor=(37, 37))
        folium.Marker(
            location=[spots[i+1]["lat"], spots[i+1]["lon"]],
            icon=goal_icon
        ).add_to(m)
        bounds += route.get_bounds()
    
    if bounds:
        combined_bounds = [
            [min(b[0] for b in bounds), min(b[1] for b in bounds)],
            [max(b[0] for b in bounds), max(b[1] for b in bounds)],
        ] 
        expanded_bounds = expand_bounds(combined_bounds)
        m.fit_bounds(expanded_bounds)
    
    m.save("route_map.html")
    
    bounds_one = []
    for i, routeShape in enumerate(routes):
        mf = folium.Map()
        
        route_one = folium.GeoJson(routeShape, name=spots[i+1]["name"], style_function=get_style_function("blue")).add_to(mf)
        
        """
        if i > 0:
            start_icon_html = create_spot_pin(spots[i]["name"], spots[i]["image"])
            start_icon = folium.DivIcon(html=f"<div>{start_icon_html}</div>", icon_anchor=(37, 37))
            folium.Marker(
                location=[spots[i]["lat"], spots[i]["lon"]],
                icon=start_icon
            ).add_to(mf)
            bounds_one += route_one.get_bounds()
        """
        
        goal_icon_html = create_spot_pin(spots[i+1]["name"], spots[i+1]["image"])
        goal_icon = folium.DivIcon(html=f"""<div>{goal_icon_html}</div>""", icon_anchor=(37, 37))
        folium.Marker(
            location=[spots[i+1]["lat"], spots[i+1]["lon"]],
            icon=goal_icon
        ).add_to(mf)
        bounds_one += route_one.get_bounds()
        
        if bounds_one:
            combined_bounds_one = [
                [min(b[0] for b in bounds_one), min(b[1] for b in bounds_one)],
                [max(b[0] for b in bounds_one), max(b[1] for b in bounds_one)],
            ] 
        expanded_bounds_one = expand_bounds(combined_bounds_one)
        mf.fit_bounds(expanded_bounds)
        
        mf.save(f"route_map_{i}.html")
        
        bounds_one.clear()

    return m._repr_html_()


def time_str(datetime_str):
    result = parse_datetime(datetime_str)
    return f"{result['hour']}時{result['minute']}分"

def display_style(routeLists_ptr):
    routeLists = copy.deepcopy(routeLists_ptr)
    for i, route in enumerate(routeLists):
        for j, step in enumerate(route):
            if 'train' in step['transport_type']:
                routeLists[i][j]['transport_type'] = '鉄道'
            if 'bus' in step['transport_type']:
                routeLists[i][j]['transport_type'] = '路線'
            if 'walk' in step['transport_type']:
                routeLists[i][j]['transport_type'] = '徒歩'
            routeLists[i][j]['duration_minutes'] = f"{routeLists[i][j]['duration_minutes']}分"
            time = parse_datetime(routeLists[i][j]['departure_time'])
            routeLists[i][j]['departure_time'] = {'date':time['date'],'time':f"{str(time['hour']).zfill(2)}:{str(time['minute']).zfill(2)}", 'datetime':time['str']}
            time = parse_datetime(routeLists[i][j]['arrival_time'])
            routeLists[i][j]['arrival_time'] = {'date':time['date'],'time':f"{str(time['hour']).zfill(2)}:{str(time['minute']).zfill(2)}", 'datetime':time['str']}
            
    return routeLists

def remove_c(text):
    zen = re.sub(r'（.*?）', '', text)
    zen2 = re.sub(r'〔.*?〕', '', zen)
    return re.sub(r'\(.*?\)', '', zen2)


def get_route_map(start_place, pickup):
    routeLists = []
    #move_width = 13
    #time_width = 13
    
    moves, routes, spots = get_moves(pickup, start_place)
    m = create_map(routes, spots)
    
    for i, move in enumerate(moves):
        route_list = []
        #print(f"{spots[i]['name']} → {spots[i+1]['name']}")
        for j, step in enumerate(move):
            route = {"transport_type": "","transport_name": "","departure_place": "","arrival_place": "","departure_time": "","arrival_time": "","duration_minutes": "",}
            if step['type'] == 'move' and (move[j-1]['coord']['lat'] != move[j+1]['coord']['lat'] and move[j-1]['coord']['lon'] != move[j+1]['coord']['lon']):
                route['transport_type'] = step['move']
                if step['transport'] != None:
                    links = step['transport'].get('links', '')[0]
                    #print(f"{links['name']}  {links['from']['name']} → {links['to']['name']}")
                    route['transport_name'] = links['name']
                    route['departure_place'] = remove_c(links['from']['name'])
                    route['arrival_place'] = remove_c(links['to']['name'])
                if step['move'] == 'walk':
                    #print(f"{move[j-1]['name']} → {move[j+1]['name']}")
                    route['departure_place'] = remove_c(move[j-1]['name'])
                    route['arrival_place'] = remove_c(move[j+1]['name'])
                route['departure_time'] = step['from_time']
                route['arrival_time'] = step['to_time']
                route['duration_minutes'] = step['time']
                # print(f"移動手段：{step['move'].ljust(move_width)}出発：{time_str(step['from_time']).ljust(time_width)}所要時間：{str(step['time']).ljust(time_width)}到着：{time_str(step['to_time']).ljust(time_width)}")
                
                route_list.append(route)
                #print(route)
        routeLists.append(route_list)
        #print("")
    
    return (routeLists, m, routes)

def createGuidebookRoute(start_place, pickup):
    routeLists, m , routes = get_route_map(start_place, pickup)
    displayLists = display_style(routeLists)
    return (displayLists, routes, m)

"""
from pprint import pprint

if __name__ == '__main__':
    start_place = {
        "name": "郡山(福島県)",
        "type": "station",
        "time": "2024-12-28T10:00:00",
        "lat": 37.39815,
        "lon": 140.38846
    }
    
    pickup = [
        {'index': 6, 'stay': 60},
        {'index': 7, 'stay': 30}
    ]
    
    displayLists, routeLists, m = createGuidebookRoute(start_place, pickup)
    
    pprint(displayLists)
"""
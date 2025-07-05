import json
import folium
from typing import List, Dict, Any

def createGuidebookRoute(start_place: Dict[str, Any], pickup: List[Dict[str, int]]) -> tuple:
    """
    ガイドブックルートを作成する関数
    
    Args:
        start_place: 開始地点の情報
        pickup: ピックアップ地点のリスト
    
    Returns:
        tuple: (displayLists, map_data, map_object)
    """
    
    # 仮のルートデータ
    displayLists = [
        [
            {
                "departure_place": "郡山駅",
                "arrival_place": "会津若松駅",
                "departure_time": {"time": "10:00"},
                "arrival_time": {"time": "10:30"},
                "transport": "JR磐越西線"
            },
            {
                "departure_place": "会津若松駅",
                "arrival_place": "猪苗代駅",
                "departure_time": {"time": "11:00"},
                "arrival_time": {"time": "11:30"},
                "transport": "JR磐越西線"
            }
        ]
    ]
    
    # 仮のマップデータ
    map_data = {
        "center": [37.39815, 140.38846],
        "zoom": 10
    }
    
    # 仮のマップオブジェクト
    m = folium.Map(location=map_data["center"], zoom_start=map_data["zoom"])
    
    return displayLists, map_data, m 
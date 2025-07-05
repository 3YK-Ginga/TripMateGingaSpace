import reflex as rx 
import folium
import json, sys, re, os
import requests
import glob
from urllib.parse import quote
from app.components.guide import createGuidebookRoute
from bs4 import BeautifulSoup
from typing import TypedDict, List, Dict
from app.pages.ai_travel import TravelState

class State(rx.State):
    count: int = 0
    next_route: str = ""

    def increment(self):
        self.count += 1

    def decrement(self):
        self.count -= 1

    def set_next_route(self, route: str):
        self.next_route = route
        return rx.redirect(route)


def navbar():
    return rx.hstack(
        # TripMate タイトルリンク
        rx.link(
            rx.text(
                "TripMate", 
                color="white", 
                font_weight="bold", 
                font_size="1.5rem",
                cursor="pointer",
                _hover={"opacity": "0.8"}
            ),
            href="/",
            text_decoration="none",
            padding_left="1rem"
        ),
        # ナビゲーションリンク
        rx.hstack(
            rx.link(
                "ログイン",
                href="/login",
                font_size="0.9rem",
                color="white",
                background_color="#0066cc",
                padding="0.5rem 1rem",
                border_radius="25px",
                text_decoration="none",
                _hover={"background_color": "#005bb5"},
            ),
            rx.link(
                "新規登録",
                href="/register",
                font_size="0.9rem",
                color="white",
                background_color="#0066cc",
                padding="0.5rem 1rem",
                border_radius="25px",
                text_decoration="none",
                _hover={"background_color": "#005bb5"},
            ),
            rx.link(
                "お問い合わせ",
                href="/contact",
                font_size="0.9rem",
                color="white",
                background_color="#0066cc",
                padding="0.5rem 1rem",
                border_radius="25px",
                text_decoration="none",
                _hover={"background_color": "#005bb5"},
            ),
            rx.link(
                "DB",
                href="/db",
                font_size="0.9rem",
                color="white",
                background_color="#0066cc",
                padding="0.5rem 1rem",
                border_radius="25px",
                text_decoration="none",
                _hover={"background_color": "#005bb5"},
            ),
            spacing="1",  # '1rem' から '1' に変更
            align="center",
        ),
        justify="between",  # 'space-between' から 'between' に変更
        align="center",
        background_color="#002f57",
        color="white",
        padding="1rem",
        box_shadow="0 2px 5px rgba(0, 0, 0, 0.2)",
        position="fixed",
        top="0",
        width="100%",
        height="10vh",
        z_index="1000",
    )

def register(): 
    return rx.box(
        navbar(),
        rx.box(height="10vh"),  # ナビゲーションバーのスペース
        rx.text("ユーザー登録ページ", font_size="2em", font_weight="bold"),
    )

def login(): 
    return rx.box(
        navbar(),
        rx.box(height="10vh"),
        rx.text("ログインページ", font_size="2em", font_weight="bold"),
    )

def contact(): 
    return rx.box(
        navbar(),
        rx.box(height="10vh"),
        rx.text("お問い合わせページ", font_size="2em", font_weight="bold"),
    )

def db(): 
    return rx.box(
        navbar(),
        rx.box(height="10vh"),
        rx.text("DBページ", font_size="2em", font_weight="bold"),
    )

def select():
    return rx.box(
        navbar(),
        rx.box(height="10vh"),
        rx.button(
            "ルートを表示",
            on_click=State.set_next_route("@route"),
            color="white",
            background_color="#0066cc",
            padding="0.5rem 1rem",
            border_radius="25px",
            _hover={"background_color": "#005bb5"},
        ),
    )

def time_component(status, time):    
    bg_color = "aqua"
    if status == "着":
        bg_color = "lightgreen"
    elif status == "間":
        bg_color = "lightyellow"
    return rx.card(
        rx.flex(
            rx.text(status, font_weight="bold", bg=bg_color, padding="0.5rem", border_radius="0.5rem"),
            rx.text(time),
            justify="between",  # 'space-between' から 'between' に変更
            align="center",
            height="100%",
        ),
        width="78px",
        height="5vh",
        bg="white",
        border="none",
    )

def place_component(place):
    return rx.card(
        rx.text(
            place,
            align="center",
            height="100%",
            font_weight="bold",
            font_size="1.5em",
            overflow="hidden",
            text_overflow="ellipsis",
            white_space="nowrap",
        ),
        width="182px",
        bg="lightgreen",
        border="none",
        border_radius="2em",
    )

def traffic_component(traffic):
    return rx.card(
        rx.flex(
            rx.text(
                traffic,
                font_weight="bold",
                font_size="1.5em",
                overflow="hidden",
                text_overflow="ellipsis",
                white_space="nowrap",
            ),
            justify="center",
            align="center",
            height="100%",
        ),
        width="119px",
        height="7vh",
        bg="white",
        border="none",
    )

def rooting_layout(transports, relay=False):
    if not relay:
        return rx.box(
            rx.box(
                height="4em",
                border_left="5px dotted black",
                margin_left="13.5em",
            ),
            rx.flex(
                time_component("間", transports["duration_minutes"]),
                traffic_component(transports["transport_type"]),
                spacing="8",
                align="center",
                padding="0 2em",
            ),
            rx.box(
                height="4em",
                border_left="5px dotted black",
                margin_left="13.5em",
            ),
        )
    else:
        return rx.box(
            rx.box(
                height="4em",
                border_left="5px dotted black",
                margin_left="13.5em",
                position="relative",
                margin_top="-0.3em",
            ),
            rx.flex(
                time_component("間", transports["duration_minutes"]),
                traffic_component(transports["transport_type"]),
                spacing="8",
                align="center",
                padding="0 2em",
            ),
            rx.box(
                height="4em",
                border_left="5px dotted black",
                margin_left="13.5em",
            ),
        )

def rooting(transports, next_departure_time="", relay=False):
    if not relay and not next_departure_time:
        return rx.box(
            rx.flex(
                time_component("発", transports["departure_time"]['time']),
                place_component(transports["departure_place"]),
                spacing="8",
                align="center",
            ),
            rooting_layout(transports),
            rx.flex(
                rx.box(
                    time_component("着", transports["arrival_time"]['time']),
                ),
                place_component(transports["arrival_place"]),
                position="relative",
                margin_top="-0.3em",
                spacing="8",
                align="center",
            ),
            padding="0 2.3em",
            width="100%",
        )
    elif not relay and next_departure_time:
        return rx.box(
            rx.flex(
                time_component("発", transports["departure_time"]['time']),
                place_component(transports["departure_place"]),
                spacing="8",
                align="center",
            ),
            rooting_layout(transports),
            rx.flex(
                rx.box(
                    time_component("着", transports["arrival_time"]['time']),
                    time_component("発", next_departure_time),
                ),
                place_component(transports["arrival_place"]),
                position="relative",
                margin_top="-0.3em",
                spacing="8",
                align="center",
            ),
            padding="0 2.3em",
            width="100%",
        )
    elif relay and not next_departure_time:
        return rx.box(
            rooting_layout(transports, True),
            rx.flex(
                rx.box(
                    time_component("着", transports["arrival_time"]['time']),
                ),
                place_component(transports["arrival_place"]),
                position="relative",
                margin_top="-0.3em",
                spacing="8",
                align="center",
            ),
            padding="0 2.3em",
            width="100%",
        )
    else:
        return rx.box(
            rooting_layout(transports, True),
            rx.flex(
                rx.box(
                    time_component("着", transports["arrival_time"]['time']),
                    time_component("発", next_departure_time),
                ),
                place_component(transports["arrival_place"]),
                position="relative",
                margin_top="-0.3em",
                spacing="8",
                align="center",
            ),
            padding="0 2.3em",
            width="100%",
        )
 
def root_guide(transports_list):
    components = []
    for i in range(len(transports_list)):
        relay = i > 0
        if i+1 < len(transports_list):
            next_departure_time = transports_list[i+1]["departure_time"]['time']
        else: 
            next_departure_time = ""
        components.append(rooting(transports_list[i], next_departure_time, relay))
    return rx.box(*components)

def parse_map_html(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        html = file.read()
    #return html.replace('"minZoom": 0', '"minZoom": 10')
    return html
    
def extract_number(text):
    match = re.search(r'\d+', text)
    if match:
        return match.group()
    return None

class AccordionState(rx.State):
    value: str = ""
    item_selected: str = ""
    all_html: str = ""
    new_html: List[Dict[str, str]] = []
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        files = glob.glob('route_map_*.html')
        self.all_html = parse_map_html("route_map.html")
        self.item_selected = self.all_html

        for i, file in enumerate(files):
            self.new_html.append({f'item_{i}': parse_map_html(file)})
    
    @rx.event
    def change_value(self, value):
        self.value = value
        if value == "":
            self.item_selected = self.all_html
        else:
            for html in self.new_html:
                if value in html:
                    self.item_selected = html[value]
                    break



def spot_accordion_item(displayLists):
    components = []
    for i, transports in enumerate(displayLists):
        components.append(
            rx.accordion.item(
                header=f"{transports[0]['departure_place']}　→　{transports[-1]['arrival_place']}",
                content=(
                    rx.box(height="3vh"),
                    root_guide(transports),
                    rx.box(height="3vh")
                ),
                value=f"item_{i}",
            )
        )
    
    return components

def guidebook(displayLists):
    return rx.hstack(
        rx.scroll_area(
            rx.accordion.root(
                *spot_accordion_item(displayLists),
                variant="ghost",
                collapsible=True,
                color_scheme="gray",
                show_dividers=True,
                value=AccordionState.value,
                on_value_change=lambda value: AccordionState.change_value(
                        value
                ),
            ),
            width="30vw",
            height="calc(100vh - 10vh)",
            bg="lightgray",
            type="hover",
            scrollbars="both",
        ),
        rx.scroll_area(
            rx.el.Iframe(
                src_doc=AccordionState.item_selected,
                width="100%",
                height="100%",
            ),
            width="70vw",
            height="calc(100vh - 10vh)",
            type="hover",
            scrollbars="both",
        ),
        width="100%",
        height="calc(100vh - 10vh)",
        spacing="0",
    )    


def route():
    return rx.box(
        rx.vstack(
            rx.heading("ルート詳細", size="2xl"),
            rx.cond(
                TravelState.selected_suggestion,
                rx.vstack(
                    rx.heading(TravelState.selected_suggestion["name"], size="xl"),
                    rx.text(TravelState.selected_suggestion["description"]),
                    rx.box(
                        rx.el.Iframe(
                            src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3240.827853398542!2d139.76454661525877!3d35.68123618019432!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x60188bfbd89f700b%3A0x277c49ba34ed38!2z5p2x5Lqs6aeF!5e0!3m2!1sja!2sjp!4v1650000000000!5m2!1sja!2sjp",
                            width="100%",
                            height="600px",
                            style={"border": "0"},
                            allow_fullscreen=True,
                            loading="lazy",
                            referrer_policy="no-referrer-when-downgrade",
                        ),
                        width="100%",
                        height="600px",
                    ),
                    spacing="4",
                ),
                rx.text("提案が選択されていません。トップページに戻って提案を選択してください。"),
            ),
            spacing="8",
            align="center",
            padding="2rem",
        ),
    )

def index():
    start_place = {
        "name": "郡山(福島県)",
        "type": "station",
        "routeType": "total",
        "time": "2024-12-28T10:00:00",
        "lat": 37.39815,
        "lon": 140.38846
    }
    
    pickup = [
        {'index': 3, 'stay': 30},
        {'index': 5, 'stay': 30},
        {'index': 4, 'stay': 30},
        {'index': 10, 'stay': 30},
    ]
    
    displayLists, _, m = createGuidebookRoute(start_place, pickup)
    
    return rx.box(
        navbar(),
        rx.box(height="10vh"),
        guidebook(displayLists),
    )


import reflex as rx 
import folium
import json, sys, re, os
import requests
import glob
from urllib.parse import quote
from min.guide import createGuidebookRoute
from bs4 import BeautifulSoup
from typing import TypedDict, List, Dict

class State(rx.State):
    count: int = 0

    def increment(self):
        self.count += 1

    def decrement(self):
        self.count -= 1


def navbar(bar_color="black"):
    return rx.hstack(
        rx.link(
            rx.box(rx.text("Trip Mate", color="white", font_weight="bold", font_size="2em"), align="center"),
            href="/",
        ),
        rx.hstack(
            rx.link(rx.text("新規登録", color="white"), href="/register"),
            rx.link(rx.text("ログイン", color="white"), href="/login"),
            rx.link(rx.text("お問い合わせ", color="white"), href="/contact"),
            rx.link(rx.text("DB", color="white"), href="/db"),
            spacing="5",
            align="center",
        ),
        position="fixed",
        top="0",
        bg=bar_color,
        align="center",
        justify="between",
        height="10vh",
        width="100%",
        padding="0 2em",
        z_index="1000",
    )

def register(): return rx.box(navbar("gray"), rx.text("ユーザー登録ページ", font_size="2em", font_weight="bold"),)
def login(): return rx.box(navbar("gray"), rx.text("ログインページ", font_size="2em", font_weight="bold"),)
def contact(): return rx.box(navbar("gray"), rx.text("お問い合わせページ", font_size="2em", font_weight="bold"),)
def db(): return rx.box(navbar("gray"), rx.text("DBページ", font_size="2em", font_weight="bold"),)

def time_component(status, time):    
    bg_color = "aqua"
    if status == "着":
        bg_color = "lightgreen"
    elif status == "間":
        bg_color = "lightyellow"
    return rx.card(
        rx.flex(
            rx.text(status, font_weight="bold", bg=bg_color),
            rx.text(time),
            justify="between",
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
        rx.text(place,
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
            rx.text(traffic,
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
        else: next_departure_time = ""
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
    
app = rx.App()
app.add_page(index)
app.add_page(register)
app.add_page(login)
app.add_page(contact)
app.add_page(db)
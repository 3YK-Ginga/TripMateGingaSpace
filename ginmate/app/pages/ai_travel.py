import reflex as rx
from typing import List, Dict, Optional
import json
import os
from app.components.guide import createGuidebookRoute

class TravelState(rx.State):
    """旅行提案の状態を管理するクラス"""
    destination: str = ""
    budget: str = ""
    duration: str = ""
    interests: List[str] = []
    season: str = ""
    suggestions: List[Dict] = []
    selected_suggestion: Optional[Dict] = None

    def set_destination(self, value: str):
        self.destination = value

    def set_budget(self, value: str):
        self.budget = value

    def set_duration(self, value: str):
        self.duration = value

    def set_season(self, value: str):
        self.season = value

    def add_interest(self, value: str):
        if value not in self.interests:
            self.interests.append(value)

    def remove_interest(self, value: str):
        if value in self.interests:
            self.interests.remove(value)

    def generate_suggestions(self):
        """AIによる旅行先提案を生成"""
        # ここにAIによる提案ロジックを実装
        # 仮の提案データ
        self.suggestions = [
            {
                "name": "東京",
                "description": "日本の首都で、伝統と現代が融合する都市",
                "image": "https://example.com/tokyo.jpg",
                "route": "/route"
            },
            {
                "name": "京都",
                "description": "日本の伝統文化が色濃く残る古都",
                "image": "https://example.com/kyoto.jpg",
                "route": "/route"
            }
        ]

    def select_suggestion(self, suggestion: Dict):
        self.selected_suggestion = suggestion
        return rx.redirect(suggestion["route"])

def interest_button(interest: str):
    return rx.button(
        interest,
        on_click=lambda: TravelState.add_interest(interest),
        color="white",
        background_color="#0066cc",
        padding="0.5rem 1rem",
        border_radius="25px",
        _hover={"background_color": "#005bb5"},
    )

def suggestion_card(suggestion: Dict):
    return rx.card(
        rx.vstack(
            rx.heading(suggestion["name"], size="lg"),
            rx.text(suggestion["description"]),
            rx.button(
                "このルートを選択",
                on_click=lambda: TravelState.select_suggestion(suggestion),
                color="white",
                background_color="#0066cc",
                padding="0.5rem 1rem",
                border_radius="25px",
                _hover={"background_color": "#005bb5"},
            ),
            align="center",
            spacing="3",
        ),
        width="300px",
    )

def index():
    return rx.box(
        rx.vstack(
            rx.heading("AI旅行提案アプリ", size="2xl"),
            rx.text("あなたにぴったりの旅行先を提案します"),
            
            # 入力フォーム
            rx.form(
                rx.vstack(
                    rx.input(
                        placeholder="目的地",
                        value=TravelState.destination,
                        on_change=TravelState.set_destination,
                    ),
                    rx.input(
                        placeholder="予算",
                        value=TravelState.budget,
                        on_change=TravelState.set_budget,
                    ),
                    rx.input(
                        placeholder="期間",
                        value=TravelState.duration,
                        on_change=TravelState.set_duration,
                    ),
                    rx.select(
                        ["春", "夏", "秋", "冬"],
                        placeholder="季節を選択",
                        value=TravelState.season,
                        on_change=TravelState.set_season,
                    ),
                    rx.hstack(
                        interest_button("観光"),
                        interest_button("グルメ"),
                        interest_button("自然"),
                        interest_button("文化"),
                        spacing="2",
                    ),
                    rx.button(
                        "提案を生成",
                        on_click=TravelState.generate_suggestions,
                        color="white",
                        background_color="#0066cc",
                        padding="0.5rem 1rem",
                        border_radius="25px",
                        _hover={"background_color": "#005bb5"},
                    ),
                    spacing="4",
                ),
            ),

            # 提案表示エリア
            rx.cond(
                TravelState.suggestions,
                rx.wrap(
                    *[suggestion_card(suggestion) for suggestion in TravelState.suggestions],
                    spacing="4",
                    justify="center",
                ),
            ),
            
            spacing="8",
            align="center",
            padding="2rem",
        ),
    ) 
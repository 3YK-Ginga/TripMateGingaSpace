import reflex as rx

class State(rx.State):
    count: int = 0

    def increment(self):
        self.count += 1

    def decrement(self):
        self.count -= 1

def index():
    return rx.center(
        rx.vstack(
            rx.heading("TripMate", size="lg"),
            rx.text("シンプルなテストアプリケーション"),
            rx.hstack(
                rx.button(
                    "減らす",
                    on_click=State.decrement,
                    color_scheme="red",
                    size="lg",
                ),
                rx.heading(State.count, font_size="2em"),
                rx.button(
                    "増やす",
                    on_click=State.increment,
                    color_scheme="green",
                    size="lg",
                ),
                align="center",
            ),
            align="center",
            spacing="2em",
            font_size="2em",
        ),
        height="100vh",
    )

app = rx.App()
app.add_page(index) 
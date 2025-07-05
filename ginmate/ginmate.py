import reflex as rx
from app.pages.ai_travel import index as ai_travel_index
from app.pages.route import route

app = rx.App()
app.add_page(ai_travel_index, route="/")
app.add_page(route, route="/route")

if __name__ == "__main__":
    app.compile() 
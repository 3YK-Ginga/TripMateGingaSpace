import reflex as rx
from app.pages.ai_travel import index as ai_travel_index
from app.pages.route import route, register, login, contact, db, select, index as route_index

app = rx.App()
app.add_page(ai_travel_index, route="/")
app.add_page(route, route="/route")
app.add_page(register, route="/register")
app.add_page(login, route="/login")
app.add_page(contact, route="/contact")
app.add_page(db, route="/db")
app.add_page(select, route="/select")
app.add_page(route_index, route="/route-index")

if __name__ == "__main__":
    app.compile() 
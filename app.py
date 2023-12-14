from typing import Tuple

from flask import Flask, g, render_template
from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField
from wtforms.validators import DataRequired

from src.adapters.database_adapters import DatabaseAdapter
from src.domain.order import Order

app = Flask(__name__)
app.config["WTF_CSRF_ENABLED"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///takehome_db"


class CreateOrderForm(FlaskForm):  # type: ignore[misc]
    name = StringField("name", [DataRequired()])
    address = StringField("address", [DataRequired()])


class GetOrderForm(FlaskForm):  # type: ignore[misc]
    order_id = IntegerField("order_id", [DataRequired()])


def get_database_connection(database_uri: str) -> DatabaseAdapter:
    if "database_connection" not in g:
        g.database_connection = DatabaseAdapter(database_uri)
    return g.database_connection  # type: ignore[no-any-return]


@app.route("/create", methods=["POST"])  # type: ignore[misc]
def create_order() -> Tuple[str, int]:
    form = CreateOrderForm()
    if form.validate():
        order = Order(None, form.name.data, form.address.data)
        get_database_connection(app.config["SQLALCHEMY_DATABASE_URI"]).create_order(
            order
        )
        return render_template("success.html"), 200
    else:
        return render_template("failed.html"), 400


@app.route("/get", methods=["GET"])  # type: ignore[misc]
def get_order() -> Tuple[str, int]:
    form = GetOrderForm()
    if form.validate():
        result = get_database_connection(
            app.config["SQLALCHEMY_DATABASE_URI"]
        ).get_order(form.order_id.data)
        return render_template("order.html", data=result), 200
    else:
        return render_template("failed.html"), 400


if __name__ == "__main__":
    app.run()

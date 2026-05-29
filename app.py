from flask import Flask, render_template, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
from database import get_db_connection

app = Flask(__name__)

app.secret_key = "secret-key"


@app.route("/")
def home():
    if "user_id" not in session:
        return redirect("/login")
    return render_template("dashboard.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        password_hash = generate_password_hash(password)

        conn = get_db_connection()

        try:
            conn.execute(
                "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                (username, password_hash)
            )
            conn.commit()
        except:
            conn.close()
            return "Username already exists."

        conn.close()
        return redirect("/login")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db_connection()
        user = conn.execute(
            "SELECT * FROM users WHERE username = ?",
            (username,)
        ).fetchone()
        conn.close()

        if user and check_password_hash(user["password_hash"], password):
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            return redirect("/")

        return "Invalid username or password."

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


@app.route("/employees")
def employees():
    if "user_id" not in session:
        return redirect("/login")

    conn = get_db_connection()

    employees = conn.execute(
        "SELECT * FROM employees WHERE user_id = ?",
        (session["user_id"],)
    ).fetchall()

    conn.close()

    return render_template("employees.html", employees=employees)



@app.route("/employees/add", methods=["GET", "POST"])
def add_employee():

    if "user_id" not in session:
        return redirect("/login")

    if request.method == "POST":

        name = request.form["name"]
        position = request.form["position"]
        email = request.form["email"]

        conn = get_db_connection()

        conn.execute(
            """
            INSERT INTO employees
            (user_id, name, position, email)

            VALUES (?, ?, ?, ?)
            """,
            (session["user_id"], name, position, email)
        )

        conn.commit()
        conn.close()

        return redirect("/employees")

    return render_template("employee_form.html")


@app.route("/employees/delete/<int:id>")
def delete_employee(id):

    if "user_id" not in session:
        return redirect("/login")

    conn = get_db_connection()

    conn.execute(
        """
        DELETE FROM employees
        WHERE id = ? AND user_id = ?
        """,
        (id, session["user_id"])
    )

    conn.commit()
    conn.close()

    return redirect("/employees")


@app.route("/employees/edit/<int:id>", methods=["GET", "POST"])
def edit_employee(id):

    if "user_id" not in session:
        return redirect("/login")

    conn = get_db_connection()

    employee = conn.execute(
        """
        SELECT * FROM employees
        WHERE id = ? AND user_id = ?
        """,
        (id, session["user_id"])
    ).fetchone()

    if employee is None:
        conn.close()
        return redirect("/employees")

    if request.method == "POST":
        name = request.form["name"]
        position = request.form["position"]
        email = request.form["email"]

        conn.execute(
            """
            UPDATE employees
            SET name = ?, position = ?, email = ?
            WHERE id = ? AND user_id = ?
            """,
            (name, position, email, id, session["user_id"])
        )

        conn.commit()
        conn.close()

        return redirect("/employees")

    conn.close()

    return render_template("employee_form.html", employee=employee)


if __name__ == "__main__":
    app.run(debug=True)
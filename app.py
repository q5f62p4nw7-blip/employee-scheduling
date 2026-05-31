from flask import Flask, render_template, request, redirect, session, flash
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

            flash("Login successful.")

            return redirect("/")


        return "Invalid username or password."

    return render_template("login.html")

@app.route("/shifts")
def shifts():

    if "user_id" not in session:
        return redirect("/login")

    conn = get_db_connection()

    shifts = conn.execute(
        """
        SELECT
            shifts.*,
            employees.name as employee_name
        FROM shifts
        JOIN employees
            ON shifts.employee_id = employees.id
        WHERE shifts.user_id = ?
        ORDER BY shift_date ASC
        """,
        (session["user_id"],)
    ).fetchall()

    conn.close()

    return render_template(
        "shifts.html",
        shifts=shifts
    )

@app.route("/shifts/add", methods=["GET", "POST"])
def add_shift():

    if "user_id" not in session:
        return redirect("/login")

    conn = get_db_connection()

    employees = conn.execute(
        """
        SELECT *
        FROM employees
        WHERE user_id = ?
        """,
        (session["user_id"],)
    ).fetchall()

    if request.method == "POST":

        employee_id = request.form["employee_id"]
        shift_date = request.form["shift_date"]
        start_time = request.form["start_time"]
        end_time = request.form["end_time"]
        notes = request.form["notes"]

        existing_shift = conn.execute(
            """
            SELECT *
            FROM shifts
            WHERE
              employee_id = ?
              AND shift_date = ?
              AND user_id = ?
            """,
            (
              employee_id,
              shift_date,
              session["user_id"]
            )
        ).fetchone()

        if existing_shift:

          flash("Employee already has a shift on this date.")

          conn.close()

          return redirect("/shifts/add")


        conn.execute(
            """
            INSERT INTO shifts (
                employee_id,
                shift_date,
                start_time,
                end_time,
                notes,
                user_id
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                employee_id,
                shift_date,
                start_time,
                end_time,
                notes,
                session["user_id"]
            )
        )

        conn.commit()
        conn.close()

        return redirect("/shifts")

    conn.close()

    return render_template(
        "shift_form.html",
        employees=employees
    )

@app.route("/shifts/delete/<int:id>")
def delete_shift(id):

    if "user_id" not in session:
        return redirect("/login")

    conn = get_db_connection()

    conn.execute(
        """
        DELETE FROM shifts
        WHERE id = ? AND user_id = ?
        """,
        (id, session["user_id"])
    )

    conn.commit()
    conn.close()

    return redirect("/shifts")


@app.route("/shifts/edit/<int:id>", methods=["GET", "POST"])
def edit_shift(id):

    if "user_id" not in session:
        return redirect("/login")

    conn = get_db_connection()

    shift = conn.execute(
        """
        SELECT *
        FROM shifts
        WHERE id = ? AND user_id = ?
        """,
        (id, session["user_id"])
    ).fetchone()

    employees = conn.execute(
        """
        SELECT *
        FROM employees
        WHERE user_id = ?
        """,
        (session["user_id"],)
    ).fetchall()

    if shift is None:
        conn.close()
        return redirect("/shifts")

    if request.method == "POST":
        employee_id = request.form["employee_id"]
        shift_date = request.form["shift_date"]
        start_time = request.form["start_time"]
        end_time = request.form["end_time"]
        notes = request.form["notes"]

        conn.execute(
            """
            UPDATE shifts
            SET employee_id = ?, shift_date = ?, start_time = ?, end_time = ?, notes = ?
            WHERE id = ? AND user_id = ?
            """,
            (
                employee_id,
                shift_date,
                start_time,
                end_time,
                notes,
                id,
                session["user_id"]
            )
        )

        conn.commit()
        conn.close()

        return redirect("/shifts")

    conn.close()

    return render_template(
        "shift_form.html",
        employees=employees,
        shift=shift
    )


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
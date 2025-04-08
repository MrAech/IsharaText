from flask import Blueprint, render_template, request, redirect, url_for, flash
import pymysql
import pymysql.cursors
from AppSecret import secrets

joinBp = Blueprint('join', __name__, template_folder='templates')


def get_db_connection():
    return pymysql.connect(
        charset='utf8mb4',
        connect_timeout=10,
        cursorclass=pymysql.cursors.DictCursor,
        db=secrets().getDatabaseName(),
        host=secrets().getDBHost(),
        password=secrets().getDBPassword() or "",
        read_timeout=10,
        port=secrets().getDBport(),
        user=secrets().getDBUser(),
        write_timeout=10
    )


@joinBp.route('/', methods=['GET', 'POST'])
def join_page():
    if request.method == 'POST':
        org_name = request.form.get('orgName')
        contact_person = request.form.get('contactPerson')
        email = request.form.get('email')
        message = request.form.get('message')

        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                sql = """
                INSERT INTO join_requests 
                (org_name, contact_person, email, message, status, created_at)
                VALUES (%s, %s, %s, %s, %s, NOW())
                """
                cursor.execute(sql, (org_name, contact_person, email, message, 'Pending'))
            connection.commit()
            flash("Request submitted successfully!", "success")
        except Exception as e:
            print("DB insert error:", e)
            flash("Something went wrong. Please try again.", "error")
        finally:
            connection.close()

        return redirect(url_for('join.join_page'))

    # GET request: fetch all requests to display in the table
    connection = get_db_connection()
    requests = []
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT org_name, contact_person, email, status, created_at AS submitted_at
                FROM join_requests
                ORDER BY id DESC
            """)
            requests = cursor.fetchall()
    except Exception as e:
        print("DB fetch error:", e)
    finally:
        connection.close()

    return render_template('join.html', requests=requests)

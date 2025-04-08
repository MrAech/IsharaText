from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_mail import Message
from datetime import datetime, timedelta
import pymysql
import pymysql.cursors
import uuid
from AppSecret import secrets
from config import Config

mail = Config.getMail()

meetupBp = Blueprint('meetup', __name__, template_folder='templates')

def get_connection():
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

def create_table_if_not_exists(conn):
    with conn.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS meetupRequests (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100),
                email VARCHAR(150),
                gender VARCHAR(20),
                message TEXT,
                preferred_time DATETIME,
                meet_link VARCHAR(255),
                submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
    conn.commit()

def delete_expired_meetups(conn):
    with conn.cursor() as cursor:
        cursor.execute("""
            DELETE FROM meetupRequests
            WHERE preferred_time < %s
        """, (datetime.now() - timedelta(hours=2),))
    conn.commit()

def generate_jitsi_link():
    return f"https://meet.jit.si/ISLMeetup-{uuid.uuid4().hex[:8]}"

def send_meetup_email(sender_name, sender_email, link):
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT DISTINCT email FROM meetupRequests
                WHERE email != %s
            """, (sender_email,))
            recipients = [row['email'] for row in cursor.fetchall()]

        if recipients:
            msg = Message(
                subject=f"🧏‍♀️ New ISL Meetup from {sender_name}",
                sender=current_app.config['MAIL_USERNAME'],
                recipients=recipients,
                body=f"{sender_name} wants to connect via ISL.\n\nJoin the meetup here:\n{link}\n\nHappy Signing!"
            )
            mail.send(msg)
    except Exception as e:
        print("❌ Email error:", e)

@meetupBp.route('/', methods=['GET', 'POST'])
def meetup():
    conn = get_connection()
    create_table_if_not_exists(conn)
    delete_expired_meetups(conn)

    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        gender = request.form.get('gender')
        message = request.form.get('message')
        time_str = request.form.get('time')

        try:
            preferred_time = datetime.strptime(time_str, "%Y-%m-%dT%H:%M")
        except:
            flash("Invalid time format!", "error")
            return redirect(url_for('meetup.meetup'))

        meet_link = generate_jitsi_link()

        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO meetupRequests (name, email, gender, message, preferred_time, meet_link)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (name, email, gender, message, preferred_time, meet_link))
        conn.commit()

        send_meetup_email(name, email, meet_link)
        flash("Your meetup request was submitted and a Jitsi link has been created!", "success")
        return redirect(url_for('meetup.meetup'))

    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM meetupRequests ORDER BY preferred_time ASC")
        meetups = cursor.fetchall()

    conn.close()
    return render_template("meetup.html", meetups=meetups)

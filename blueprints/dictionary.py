from itertools import islice
from flask import Blueprint, render_template, jsonify, request
from flask_login import login_required
import pymysql
import pymysql.cursors
from AppSecret import secrets

dictionaryBp = Blueprint("dictionary", __name__, template_folder="templates")

MasterDataTableName = "ReadyToUSE"


def load_dictionary():
    labels = {}
    # conn = mysql.connector.connect(
    #     host="localhost",
    #     user='root',
    #     password=secrets().getDBPassword(),
    #     database=secrets().getDatabaseName()
    # )

    conn = pymysql.connect(
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
    cursor = conn.cursor()
    cursor.execute(f"SELECT VideoName, VideoID FROM {MasterDataTableName};")
    rows = cursor.fetchall()
    for row in rows:
        key = row['VideoName']
        value = row['VideoID']
        labels[key] = value
    cursor.close()
    return labels

@dictionaryBp.route("/")
# @login_required
def dictionary():
    global labels
    labels = load_dictionary()
    return render_template("dictionary.html", labels=labels)


@dictionaryBp.route("/api/dictionary", methods=["POST"])
# @login_required
def dictionary_api():
    return jsonify(labels)

@dictionaryBp.route("/api/paginate", methods=["GET"])
def paginate_dictionary():
    page = int(request.args.get("page", 1))
    items_per_page = int(request.args.get("items_per_page", 100))
    

    start = (page - 1) * items_per_page
    end = start + items_per_page
    
    paginated_labels = dict(islice(labels.items(), start, end))
    
    return jsonify({
        "items": paginated_labels,
        "total": len(labels),
        "page": page,
        "items_per_page": items_per_page
    })

@dictionaryBp.route("/api/search", methods=["GET"])
# @login_required
def search_dictionary():
    query = request.args.get("query", "").lower()
    results = {key: value for key, value in labels.items() if query in key.lower()}
    return jsonify(results)
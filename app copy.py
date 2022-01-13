import json

from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

from pymongo import MongoClient


# client = MongoClient('mongodb://test:test@localhost', 27017)
client = MongoClient('localhost', 27017)
db = client.seoulacademy1


# HTML 화면 보여주기
@app.route('/')
def home():
    return render_template('main.html')


@app.route('/map')
def route_map():
    return render_template('map.html')

##########################################################################
# client = MongoClient('내AWS아이피', 27017, username="아이디", password="비밀번호")
# client = MongoClient('localhost', 27017)
#
# db = client.seoulacademy1


@app.route('/')
def main():
    return render_template("index.html")

@app.route('/api/maplist', methods=["GET"])
def get_map():
    # 학원 목록을 반환하는 API
    # 1. 데이터 베이스에서 학원 목록을 꺼내와야 한다.
    aca_list = list(db.academies.find({}, {'_id': False}))
    # aca_list 라는 키 값에 학원 목록을 담아 클라이언트에게 반환합니다.
    # 2. 그걸 클라이언트에 돌려준다
    return jsonify({'result': 'success', 'aca_list': aca_list})

@app.route('/like_academy', methods=["POST"])
def like_aca():
    title_receive = request.form["title_give"]
    address_receive = request.form["address_give"]
    action_receive = request.form["action_give"]
    print(title_receive, address_receive, action_receive)

    if action_receive == "like":
        db.shops.update_one({"title": title_receive, "address": address_receive}, {"$set": {"liked": True}})
    else:
        db.shops.update_one({"title": title_receive, "address": address_receive}, {"$unset": {"liked": False}})
    return jsonify({'result': 'success'})



########################################################################

@app.route('/board')
def route_board():
    return render_template('board.html')


@app.route('/mypage')
def route_mypage():
    return render_template('mypage.html')


@app.route('/signup')
def route_signup():
    return render_template('signup.html')


@app.route("/login")
def route_login():
    return render_template('login.html')


if __name__ == '__main__':
    app.run('0.0.0.0', port=5555, debug=True)

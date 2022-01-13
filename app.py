from flask import Flask, render_template, request, jsonify, redirect, url_for
from pymongo import MongoClient


app = Flask(__name__)

# client = MongoClient('내AWS아이피', 27017, username="아이디", password="비밀번호")
client = MongoClient('localhost', 27017)

db = client.dbsparta_plus_week3


@app.route('/')
def main():
    return render_template("index.html")

@app.route('/matjip', methods=["GET"])
def get_matjip():
    # 맛집 목록을 반환하는 API
    # 1. 데이터 베이스에서 맛집 목록을 꺼내와야 한다.
    matjip_list = list(db.matjips.find({}, {'_id': False}))
    # matjip_list 라는 키 값에 맛집 목록을 담아 클라이언트에게 반환합니다.
    # 2. 그걸 클라이언트에 돌려준다
    return jsonify({'result': 'success', 'matjip_list': matjip_list})

@app.route('/like_matjip', methods=["POST"])
def like_matjip():
    title_receive = request.form["title_give"]
    address_receive = request.form["address_give"]
    action_receive = request.form["action_give"]
    print(title_receive, address_receive, action_receive)

    if action_receive == "like":
        db.matjips.update_one({"title": title_receive, "address": address_receive}, {"$set": {"liked": True}})
    else:
        db.matjips.update_one({"title": title_receive, "address": address_receive}, {"$unset": {"liked": False}})
    return jsonify({'result': 'success'})
if __name__ == '__main__':
    app.run('0.0.0.0', port=5050, debug=True)





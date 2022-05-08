from flask import Flask, request
from datetime import datetime
import sqlite3
import schedule
import time

app = Flask(__name__)
#l = ["badge", "badge", "mango", "grove", "stake", "cycle", "frame", "drone", "grape", "train", "table"]
#list used for finding wether particular alphabet is present on right place
d= [0, 0, 0, 0, 0]
#list used for finding the right position of particular alphabet
pos = [0, 0, 0, 0, 0]

#route used for registering for the game using name and email
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data['email']
    name = data['name']
    con = sqlite3.connect('data.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM profile WHERE email = ?", (email,))
    rows = cur.fetchall()
    if (rows == []):
        INSERT_INTO_PROFILE = "INSERT INTO PROFILE (EMAIL, NAME) VALUES (?, ?)"
        data_tuple = (email, name)

        currentDateTime = datetime.now()
        # extracting date from date time in string format
        date = currentDateTime.strftime("%x")
        INSERT_INTO_GAME_STATS = "INSERT INTO  GAME_STATS (EMAIL, DATE, TRIALS, COMPLETED) VALUES (?, ?, ?, ?)"
        data_tuple1 = (email, date, 0, 0)
        cur.execute(INSERT_INTO_PROFILE, data_tuple)
        cur.execute(INSERT_INTO_GAME_STATS, data_tuple1)
        con.commit()
        con.close()
        return {
            "msg": "profile created",
            "email": email,
            "name": name
        }

    else:
        con.close()
        return {
            "msg": "welcome back",
            "email": email,
            "name": name
        }


#route for guessing the word
@app.route('/guess', methods=['POST'])
def guess():
    #list used for detecting particular color  according to game rules
    color = ['grey', 'grey', 'grey', 'grey', 'grey']
    #data recieved from request body
    data = request.get_json()
    #guess word by the user
    user_word = data['word']
    email = data['email']
    name = data['name']

    currentDateTime = datetime.now()
    # extracting date from date time in string format
    date = currentDateTime.strftime("%x")

    con = sqlite3.connect('data.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM GAME_STATS WHERE email = ? and date = ?", (email, date))
    rows = cur.fetchall()
    completed = rows[0][3]
    #completed parameter used to detect whether one done with guessing particular word today
    if completed == 1:
        con.close()
        return {
            "msg": "you are done for the day, come tomorrow"
        }



    cur.execute("SELECT * FROM WORDS WHERE date = ?", (date,))

    rows = cur.fetchall()

    #actual word from database
    #actual word to guess from database
    actual_word = rows[0][1]
    #user word from request data
    print("postman word", user_word)
    print("sample string", actual_word)
    #updating positions and presence of particular alphabet
    for i in range(5):
        if user_word[i] == actual_word[i]:
            d[i] = 1
        else:
            d[i] = 0
            pos[i] = actual_word.find(user_word[i], 0, len(actual_word))
    #updating color list
    for i in range(5):
        if d[i] == 1:
            color[i] = "green"
        elif pos[i] >= 0:
            color[i] = "yellow"
    print(d)
    print(pos)
    if 0 not in d:
        #user has successfully guessed the word, update word completed flag to 1
        sql_update_game_stats = """Update GAME_STATS set completed = ? where email = ? and date = ?"""
        data = (1, email, date)
        cur.execute(sql_update_game_stats, data)

        #update the user score for successfully guessing the word

        cur.execute("SELECT * FROM profile WHERE email = ?", (email,))
        rows = cur.fetchall()
        updated_score = rows[0][2] + 10

        sql_update_user_score = """Update PROFILE set score = ? where email = ? """
        data = (updated_score, email)
        cur.execute(sql_update_user_score, data)

        con.commit()
        con.close()
        return {
            "msg": "congrats !!! you guessed the correct word",
            "color": color
        }
    else:
        cur.execute("SELECT * FROM GAME_STATS WHERE email = ? and date=?", (email, date))

        rows = cur.fetchall()
        trails = rows[0][2] + 1
        sql_update_query = """Update GAME_STATS set trials = ? where email = ? and date = ?"""
        data = (trails, email, date)
        cur.execute(sql_update_query, data)
        con.commit()
        #con.close()
        #checking wether done with the trails
        if(trails>=6):
            sql_update_query = """Update GAME_STATS set completed = ? where email = ? and date = ?"""
            data = (1, email, date)
            cur.execute(sql_update_query, data)
            con.commit()
            con.close()
            return {
                "color": color,
                "msg": "you are done with 6 attempts",
                "Guess word": actual_word
            }
        else:
            con.close()
            return {"color": color}


#sapp.run(port=5000, debug=True, host="0.0.0.0")

'''
def highestScoreNotify():
    print("i have the highest score")

schedule.every(1).seconds.do(highestScoreNotify)

while True:
    # Checks whether a scheduled task
    # is pending to run or not
    schedule.run_pending()
    time.sleep(1)
'''










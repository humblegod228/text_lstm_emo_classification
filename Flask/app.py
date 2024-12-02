from flask import Flask,render_template,request,url_for,redirect
from predict import Emotion_Detector
import pymysql
import warnings
warnings.filterwarnings("ignore")

# Emotion Detector Object
obj = Emotion_Detector()

# SQL
def verify(username,password):
    # Connection
    conn = pymysql.connect(host='localhost', port=3306, user='root', password='rahul@123', db='mlt')
    cur = conn.cursor()
    
    cur.execute(f'SELECT password from user_db where username = "{username}";')
    data = cur.fetchall()

    if(len(data) == 1 and data[0][0] == password):
        return True
    else:
        return False

def create(username,email,password):
    # Connection
    conn = pymysql.connect(host='localhost', port=3306, user='root', password='rahul@123', db='mlt')
    cur = conn.cursor()

    cur.execute(f'SELECT * from user_db where username = "{username}";')
    data = cur.fetchall()
    print(data)
    if(len(data) == 0):
        cur.execute(f'Insert into user_db values("{username}","{email}","{password}")')
        conn.commit()
        return True
    else:
        return False

# Flask
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html',message="")

@app.route('/signin',methods=["POST"])
def signin():
    name = request.form["username"]
    password = request.form["password"]
    if(verify(name,password)):
        return redirect(url_for('predict'))
    else:
        return render_template('login.html',message="Invalid login credentials !!!")

@app.route('/signup',methods=["POST"])
def signup():
    name = request.form["username"]
    email = request.form["email"]
    password = request.form["password"]
    if(create(name,email,password)):
        return render_template('login.html',message="Your account has been created successfully you can now sign in !!!")
    else:
        return render_template('login.html',message="Username already exists !!!")

@app.route('/predict',methods=["POST","GET"])
def predict():
    emotion = []
    if request.method == "POST":
        text = request.form["textfield"]
        out = obj.predict(text)[1]
        out = dict(sorted(out.items(), key=lambda x: x[1],reverse=True))
        emotion = [str(i)+" : "+str(round(out[i],2))+" %" for i in out]
        return render_template('predict.html',emotions=emotion,message=text)
    else:
        emotion = []
        return render_template('predict.html',emotions=emotion,message="")

if __name__ == '__main__':
    app.run(debug = True)
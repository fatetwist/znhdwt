from flask import Flask,render_template,request
import zhidao as zd
import random
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/getanswer',methods=['POST'])
def getanswer():
    # varsion v2.0
    # word = request.form['keyword']
    # print(word)
    # ids = zd.search_question(word)
    # print(ids)
    # a = zd.random.randint(0, len(ids)-1)
    # answers = zd.get_answer_by_id(ids[a])
    # b = zd.random.randint(0, len(answers['answers'])-1)
    # print(len(answers['answers']))
    # print(b)
    # print(answers['answers'][b])
    # return answers['answers'][b]

    word = request.form['keyword']
    urls = zd.search_question2(word)
    a = random.randint(0,len(urls)-1)
    answers = zd.get_answer_by_url(urls[a])
    print(answers)
    b = random.randint(0, len(answers['answers'])-1)
    return answers['answers'][b]

if __name__ == '__main__':
    app.run()

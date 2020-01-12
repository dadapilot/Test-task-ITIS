
from flask import Flask, request, render_template
from get_answers import GetAnswers
from collections import namedtuple


app = Flask(__name__, static_url_path = '/static')

@app.route("/site")
def index():
    return render_template("site.html")

@app.route('/site', methods=['POST', 'GET'])

def get_param():

    if request.method == 'POST':

        params = namedtuple('params',['quest', 'cat', 'dates'])

        items = params(request.form['quest'],
                       request.form['cat'].split(','),
                       [request.form['date1'], request.form['date2']])
        #items.cat = items.cat.split(',')

        a = GetAnswers()

        if items.quest == 'q1':
            ans = a.ans1()
            ans = ans[0][0] + ': ' + str(ans[0][1])
            data = render_template('ans1.html', ans = ans)
            return(data)

        elif items.quest == 'q2':
            items.cat[1] = '\"' + items.cat[1] + '\"'
            ans = a.ans2(items.cat[0])
            ans = ans[0][1]
            data = render_template('ans2.html', cat = items.cat[1], ans = ans)
            return(data)

        else:
            ans = a.ans3(items.dates)
            data = render_template('ans3.html', dat1=items.dates[0][:10], dat2 = items.dates[1][:10], ans=ans[0][0])
            return (data)


if __name__ == '__main__':
    app.run()






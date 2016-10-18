from flask import Flask, json, Response, render_template
from ptt import parse_board, parse_post, parse_hotboard
app = Flask(__name__)


@app.route('/')
def index():
    boards = parse_hotboard()
    print(boards)
    context = {'title': 'hotboard'}
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/api/hotboard')
def api_hotboard():
    boards = parse_hotboard()
    print(boards)

    js = json.dumps(boards, ensure_ascii=False)

    resp = Response(js, status=200, content_type='application/json; charset=utf-8')
    return resp


@app.route('/bbs/<board>/index.html')
@app.route('/bbs/<board>/')
def board(board):
    return render_template('board.html')


@app.route('/api/<board>/')
def api_board(board):
    articles = parse_board(board)

    js = json.dumps(articles, ensure_ascii=False)
    resp = Response(js, status=200, content_type='application/json; charset=utf-8')
    return resp


@app.route('/bbs/<board>/<post>')
def post(board, post):
    return render_template('post.html')


@app.route('/api/<board>/<post>/')
def api_post(board, post):
    if 'index' in post:
        articles = parse_board(board, post)

        js = json.dumps(articles, ensure_ascii=False)

        resp = Response(js, status=200, content_type='application/json; charset=utf-8')
        return resp

    else:
        article = parse_post(board, post)

        js = json.dumps(article, ensure_ascii=False)
        resp = Response(js, status=200, content_type='application/json; charset=utf-8')
        return resp

if __name__ == '__main__':
    app.run(debug=True)
    # app.run()






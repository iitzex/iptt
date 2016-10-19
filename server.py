from flask import Flask, json, Response, render_template
from ptt import parse_board, parse_post, parse_hotboard
import os
app = Flask(__name__)


@app.route('/')
def index():
    content = {'home': 'active'}
    return render_template('index.html', content=content)


@app.route('/about')
def about():
    content = {'about': 'active'}
    return render_template('about.html', content=content)


@app.route('/api/hotboard/')
def api_hotboard():
    boards = parse_hotboard()
    print(boards)

    js = json.dumps(boards, ensure_ascii=False)
    resp = Response(js, status=200, content_type='application/json; charset=utf-8')
    return resp


@app.route('/bbs/<board>/index.html')
@app.route('/bbs/<board>/')
def board(board):
    content = {board: 'active'}
    return render_template('board.html', content=content)


@app.route('/api/<board>/')
def api_board(board):
    articles = parse_board(board)

    js = json.dumps(articles, ensure_ascii=False)
    resp = Response(js, status=200, content_type='application/json; charset=utf-8')
    return resp


@app.route('/bbs/<board>/<post>')
def post(board, post):
    content = {board: 'active', post: 'active'}
    return render_template('post.html', content=content)


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
    debug = False
    if os.environ.get('PORT') is None:
        debug = True

    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=debug)






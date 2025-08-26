import os
from flask import Flask, render_template

# WebSocketの通信が正しく行われるようにするために、
# geventとgevent-websocketをインポートします
from gevent import monkey
from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler

from flask_socketio import SocketIO, emit

# geventのパッチを適用します
monkey.patch_all()

app = Flask(__name__)

# Renderが提供するポート番号を環境変数から取得します。
port = int(os.environ.get('PORT', 5000))
# セキュリティのためにシークレットキーを環境変数から取得します
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default_secret') 
# Socket.IOのインスタンスをFlaskアプリケーションにアタッチします
# CORSの設定を追加し、すべてのオリジンからのアクセスを許可します
socketio = SocketIO(app, cors_allowed_origins="*")

# トップページにアクセスされたときにindex.htmlをレンダリングします
@app.route('/')
def index():
    # RenderのホストURLをHTMLテンプレートに渡します
    host_url = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
    return render_template('index.html', host_url=host_url)

# クライアントが接続したときに実行されます
@socketio.on('connect')
def test_connect():
    print('Client connected')
    emit('my response', {'data': 'Connected'})

# クライアントが切断したときに実行されます
@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')

# クライアントから'change_color'というイベントを受信したときに実行されます
@socketio.on('change_color')
def handle_color_change(json_data):
    print('received message: ' + str(json_data))
    # 'broadcast=True'で接続中のすべてのクライアントにイベントを送信します
    emit('update_color', json_data, broadcast=True) 

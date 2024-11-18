FROM python:3.8

# アプリケーションディレクトリを作成する
WORKDIR /usr/src/python


# pipでインストールしたいモジュールをrequirements.txtに記述しておいて、
# コンテナ内でpipにインストールさせる

COPY requirements.txt ./
RUN  pip install --upgrade pip && \
pip install --no-cache-dir -r requirements.txt

# アプリケーションコードをコンテナにコピー
COPY . .

CMD [ "python", "app.py" ]
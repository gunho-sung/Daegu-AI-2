from flask import Flask, request, redirect
import sqlite3

app = Flask(__name__)

topics = [
  {"id":1, "title":"html", "body":"html is ...."},
  {"id":2, "title":"css", "body":"css is ...."},
  {"id":3, "title":"js", "body":"js is ...."}
]


def template(content, id=None):
  conn = sqlite3.connect('db.sqlite3')
  cs = conn.cursor()
  cs.execute('SELECT * FROM topics')
  topics = cs.fetchall()
  conn.close()
  liTags = ''
  for topic in topics:
    liTags = liTags + f'<li><a href="/read/{topic[0]}/">{topic[1]}</a></li>'
  return f'''
  <html>
    <body>
      <h1><a href="/">WEB</a></h1>
      <ol>
        {liTags}
      </ol>
      {content}
      <ul>
        <li><a href="/create/">create</a></li>
        <li>
          <form action="/delete/{id}/" method="POST">
            <input type="submit" value="delete">
          </form>
        </li>
      </ul>
    </body>
  </html>
  '''

@app.route("/")
def index():
  return template('<h2>Welcome</h2>Hello, WEB!')

@app.route("/read/<int:id>/")
def read(id):
  conn = sqlite3.connect('db.sqlite3')
  cs = conn.cursor()
  cs.execute('SELECT * FROM topics WHERE id=?', (id,))
  topic = cs.fetchone()
  conn.close()
  title = topic[1]
  body = topic[2]
  return template(f'<h2>{title}</h2>{body}', id)

@app.route('/create/')
def create():
  content = '''
    <form action="/create_process/" method="POST">
      <p><input type="text" name="title" placeholder="title"></p>
      <p><textarea name="body" placeholder="body"></textarea></p>
      <p><input type="submit" value="create"></p>
    </form>
  '''
  return template(content)

@app.route('/create_process/', methods=['POST'])
def create_process():
  title = request.form['title']
  body = request.form['body']
  conn = sqlite3.connect('db.sqlite3')
  cs = conn.cursor()
  cs.execute('INSERT INTO topics (title, body) VALUES(?,?)',(title,body))
  id = cs.lastrowid
  conn.commit()
  conn.close()
  return redirect(f'/read/{id}/')


@app.route('/delete/<int:id>/', methods=['POST'])
def delete(id):
  
  conn = sqlite3.connect('db.sqlite3')
  cs = conn.cursor()
  cs.execute('DELETE FROM topics WHERE id = ?',(id,))
  conn.commit()
  conn.close()
  
  return redirect('/')
 
# # @app.route('/update/')
# # def update():
# #   return 'Update'
 

app.run()


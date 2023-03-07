from flask import Flask, render_template, request, url_for
import psycopg2
import random

app = Flask(__name__, static_url_path='/app/static', template_folder='/app/templates')

conn = psycopg2.connect(
    host="postgres",
    database="websitenamepics",
    user="website",
    password="EE776noc1!"
)

cur = conn.cursor()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form.get('name')
        if not name:
            return '<script>alert("Please enter a name");window.location.href="/"</script>'
        cur.execute("INSERT INTO users (name) VALUES (%s);", (name,))
        conn.commit()
        pic = random.choice(['picture1.jpg', 'picture2.jpg', 'picture3.jpg', 'picture4.jpg', 'picture5.jpg'])

        return render_template('picture.html', name=name, pic=url_for('static', filename=f'pictures/{pic}'))

    return render_template('/index.html')
 
@app.route('/users')
def users():
    cur.execute("SELECT * FROM users")
    users = cur.fetchall()
    return render_template('users.html', users=users)

if __name__ == '__main__':
    app.run(debug=True, port=3001)

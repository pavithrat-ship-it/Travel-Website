from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)
app.secret_key = "college_secret_key"


# ---------- DB Connection ----------
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Care123",
        database="travel_db"
    )

def create_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS contact_messages (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100),
        email VARCHAR(120),
        phone VARCHAR(20),
        address TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    cursor.close()
    conn.close()

create_table()

# ---------- Routes ----------
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/destinations')
def destinations():
    return render_template('destinations.html')


@app.route('/packages')
def packages():
    return render_template('packages.html')


@app.route('/about')
def about():
    return render_template('about.html')


# ---------- Contact Page ----------
@app.route('/contact', methods=['GET','POST'])
def contact():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # When form submitted
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        address = request.form.get('address')

        cursor.execute(
            "INSERT INTO contact_messages (name,email,phone,address) VALUES (%s,%s,%s,%s)",
            (name,email,phone,address)
        )
        conn.commit()

    # Fetch all messages
    cursor.execute("SELECT * FROM contact_messages ORDER BY id DESC")
    contacts = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('contact.html', contacts=contacts)


# ---------- Run ----------
if __name__ == "__main__":
    app.run(debug=True)

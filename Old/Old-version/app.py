from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'yomommasofat'

@app.route('/')
def index():
    return render_template ('home.html')

@app.route('/terms')
def terms():
    return render_template('terms.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        with sqlite3.connect('doctors.db') as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM doctors WHERE email=? AND password=?", (email, password))
            data = c.fetchone()

        if data:
            session['email'] = email
            return redirect(url_for('dashboard'))
        else:
            error = 'Invalid email or password'
            return render_template('login.html', error=error)
    else:
        return render_template('login.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'email' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        with sqlite3.connect('doctors.db') as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM doctors WHERE email=? AND password=?", (email, password))
            data = c.fetchone()

        if data:
            return render_template('dashboard.html', data=data)
        else:
            error = 'Invalid email or password'
            return render_template('dashboard.html', error=error)
    else:
        with sqlite3.connect('doctors.db') as conn:
            c = conn.cursor()
            c.execute('SELECT * FROM doctors')
            data = c.fetchone()
        return render_template('dashboard.html', data=data)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        with sqlite3.connect('doctors.db') as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM doctors WHERE email=?", (email,))
            data = c.fetchone()

        if data:
            error = 'Email already taken'
            return render_template('signup.html', error=error)
        else:
            with sqlite3.connect('doctors.db') as conn:
                c = conn.cursor()
                c.execute("INSERT INTO doctors (email, password) VALUES (?, ?)", (email, password))
                conn.commit()
                session['email'] = email
            return redirect(url_for('dashboard'))
    else:
        return render_template('signup.html')

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('email', None)  # Clear the session data
    return redirect(url_for('login'))

@app.route('/delete_account', methods=['POST'])
def delete_account():
    if 'email' not in session:
        return redirect(url_for('login'))

    email = session['email']  # Use the email from the session data

    conn = sqlite3.connect('doctors.db')
    c = conn.cursor()

    # Delete the user account from the database based on the email from the session
    c.execute("DELETE FROM doctors WHERE email=?", (email,))
    conn.commit()

    # Clear the session data
    session.pop('email', None)

    # Redirect to the login page after account deletion
    return redirect(url_for('login'))


@app.route('/process_submission', methods=['POST', 'GET'])
def submission():
    if 'email' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        company_name = request.form.get('company_name')
        region = request.form.get('region')
        continent = request.form.get('continent')
        company_mail = request.form.get('company_mail')

        conn = sqlite3.connect('doctors.db')
        c = conn.cursor()

        # Process the data as needed and insert it into the database
        c.execute("INSERT INTO submissions (company_name, company_mail, region, continent) VALUES (?, ?, ?, ?)",
                       (company_name, company_mail, region, continent))
        conn.commit()

        # Redirect to a thank you page or another appropriate page
        return render_template('thankyou.html')
    else:
        return render_template('submission.html')
    
if __name__ == '__main__':
    app.run(debug=True , host='0.0.0.0') 
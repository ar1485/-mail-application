@app.route('/sent_emails')
def sent_emails():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    emails = SentEmail.query.filter_by(user_id=user_id).all()
    
    return render_template('sent_emails.html', emails=emails)

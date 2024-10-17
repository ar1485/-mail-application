import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import Flask, render_template, request, session, redirect, url_for, flash
from models import db, SMTPSettings, SentEmail, User

@app.route('/configure_smtp', methods=['GET', 'POST'])
def configure_smtp():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    if request.method == 'POST':
        smtp_server = request.form['smtp_server']
        smtp_port = request.form['smtp_port']
        smtp_username = request.form['smtp_username']
        smtp_password = request.form['smtp_password']
        encryption = request.form['encryption']
        
        smtp_settings = SMTPSettings(
            user_id=user_id, smtp_server=smtp_server, smtp_port=smtp_port,
            smtp_username=smtp_username, smtp_password=smtp_password, encryption=encryption)
        
        db.session.add(smtp_settings)
        db.session.commit()
        flash('SMTP Settings Saved!')
        return redirect(url_for('send_email'))
    
    return render_template('configure_smtp.html')

@app.route('/send_email', methods=['GET', 'POST'])
def send_email():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    smtp_settings = SMTPSettings.query.filter_by(user_id=user_id).first()
    
    if request.method == 'POST':
        recipient = request.form['recipient']
        subject = request.form['subject']
        body = request.form['body']
        
        try:
            # Send email using smtplib
            msg = MIMEMultipart()
            msg['From'] = smtp_settings.smtp_username
            msg['To'] = recipient
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))
            
            server = smtplib.SMTP(smtp_settings.smtp_server, smtp_settings.smtp_port)
            if smtp_settings.encryption == 'TLS':
                server.starttls()
            elif smtp_settings.encryption == 'SSL':
                server = smtplib.SMTP_SSL(smtp_settings.smtp_server, smtp_settings.smtp_port)
            
            server.login(smtp_settings.smtp_username, smtp_settings.smtp_password)
            server.sendmail(smtp_settings.smtp_username, recipient, msg.as_string())
            server.quit()
            
            # Store sent email details in the database
            sent_email = SentEmail(user_id=user_id, recipient=recipient, subject=subject, body=body)
            db.session.add(sent_email)
            db.session.commit()
            
            flash('Email Sent!')
        
        except Exception as e:
            flash(f'Error sending email: {e}')
    
    return render_template('send_email.html')

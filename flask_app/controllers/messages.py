from flask_app import app 
from flask import render_template, redirect, session, request, flash 
from flask_app.models.message import Message
from flask_app.models.user import User

@app.route('/createMessage', methods=['POST'])
def createMessage():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'content': request.form['content'],
        'user_id': request.form['user_id'], 
        'recipient_id': request.form['recipient_id']
    }
    Message.save(data) 
    return redirect ('/dashboard')

@app.route('/delete/<int:id>')
def delete(id): 
    if 'user_id' not in session: 
        return redirect('/logout')
    
    data = {
        'id': id
    }

    Message.delete(data)
    return redirect('/dashboard')
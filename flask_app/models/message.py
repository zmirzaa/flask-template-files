from flask_app.config.mysqlconnection import connectToMySQL 

class Message: 
    db = 'privateWall' 
    def __init__(self,data): 
        self.id = data['id'] 
        self.content = data['content'] 
        self.createdAt = data['createdAt'] 
        self.updatedAt = data['updatedAt'] 
        self.sender = data['sender']
        self.reciever=data['reciever']
        self.user_id = data['user_id']
        self.recipient_id = data['recipient_id']
    


    @classmethod
    def getUserMessages(cls,data): 
        query = "SELECT users.firstName as sender, users2.firstName as reciever, messages.* FROM users LEFT JOIN messages on users.id = messages.user_id LEFT JOIN users as users2 ON users2.id = messages.recipient_id WHERE users2.id = %(id)s;" 
        results = connectToMySQL(cls.db).query_db(query,data) 
        print(results)
        messages = [] 
        for m in results: 
            messages.append(cls(m))
        return messages

    
    @classmethod 
    def save(cls,data):
        query = "INSERT INTO messages (content, user_id, recipient_id) VALUES (%(content)s, %(user_id)s, %(recipient_id)s);"
        return connectToMySQL(cls.db).query_db(query, data) 



    @classmethod 
    def delete (cls, data): 
        query = "DELETE FROM messages WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)
    

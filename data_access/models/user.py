from flask_login import UserMixin

from data_access.db_connect import get_db_connection

class User(UserMixin):
    def __init__(self, id_, name, email, profile_pic, internal_password, email_on_share, email_on_update, email_on_owner_bought):
        self.id = id_
        self.name = name
        self.email = email
        self.profile_pic = profile_pic
        self.internal_password = internal_password
        self.email_on_share = email_on_share
        self.email_on_update = email_on_update
        self.email_on_owner_bought = email_on_owner_bought


    def as_dict(self):
        return {
            "name": self.name,
            "email": self.email,
            "profile_pic": self.profile_pic,
            "email_on_share": self.email_on_share,
            "email_on_update": self.email_on_update,
            "email_on_owner_bought": self.email_on_owner_bought
        }

    def apply_changes(self):
        if self.id == None:
            return
        
        with get_db_connection() as db:
            db.execute(
                """
                UPDATE user 
                SET name = ?, email = ?, profile_pic = ?, internal_password = ?, email_on_share = IFNULL(?, email_on_share), email_on_update = IFNULL(?, email_on_update), email_on_owner_bought = IFNULL(?, email_on_owner_bought)
                WHERE id = ?
                """,
                (self.name, self.email, self.profile_pic, self.internal_password, self.email_on_share, self.email_on_update, self.email_on_owner_bought, self.id)
            )
            db.commit()

    @staticmethod
    def get(user_id):
        with get_db_connection() as db:
            user = db.execute(
                "SELECT id, name, email, profile_pic, internal_password, email_on_share, email_on_update, email_on_owner_bought FROM user WHERE id = ?", (user_id,)
            ).fetchone()
            if not user:
                return None
            
            user = User(
                id_ = user[0],
                name=user[1],
                email=user[2],
                profile_pic=user[3],
                internal_password=user[4],
                email_on_share=user[5],
                email_on_update=user[6],
                email_on_owner_bought=user[7]
            )
            
            return user
        
    @staticmethod
    def get_by_email(email):
        with get_db_connection() as db:
            user = db.execute(
                "SELECT id, name, email, profile_pic, internal_password, email_on_share, email_on_update, email_on_owner_bought FROM user WHERE email = ?", (email,)
            ).fetchone()
            
            if not user:
                return None
            
            user = User(
                id_ = user[0],
                name=user[1],
                email=user[2],
                profile_pic=user[3],
                internal_password=user[4],
                email_on_share=user[5],
                email_on_update=user[6],
                email_on_owner_bought=user[7]
            )
            
            return user
    
    @staticmethod
    def create(id_, name, email, profile_pic, internal_password):
        with get_db_connection() as db:
            db.execute(
                "INSERT INTO user (id, name, email, profile_pic, internal_password, email_on_share, email_on_update, email_on_owner_bought) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (id_, name, email, profile_pic, internal_password, 0, 0, 0),
            )
            db.commit()

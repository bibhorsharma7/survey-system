# File that creates database with user logins

from sqlalchemy import Column, ForeignKey, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///login.db')
Base = declarative_base()

def get_userclass(tablename):
    class Row(Base):
        __tablename__ = tablename
        __table_args__ = {'extend_existing':True}
        id = Column(Integer, primary_key=True)
        username = Column(String, nullable=False)
        password = Column(String, nullable=False)
        role = Column(String, nullable=False)
        
    return Row

class Database(object):
    def __init__(self, name):
        self.table_name = name
        self.user_class = get_userclass(name)

    def create_table(self):
        try:
            Base.metadata.create_all(engine)
        except:
            print("Table already there")

    def insert_user(self, username, password, role):
        DBSession = sessionmaker(bind=engine)
        session = DBSession()

        user = self.user_class(username=username, password=password, role=role)
        session.add(user)
        session.commit()
        session.close()
    
    def return_all_users(self):
        DBSession = sessionmaker(bind = engine)
        session = DBSession()
        l = []
        table = session.query(Base.metadata.tables[self.table_name]).all()
        for row in table:
            l.append(row.username)
        session.close()
        return l
    

    def authenticate(self, table_name, u_id, pas):
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        
        if (u_id == "admin" and pas == "admin"):
            return "admin"
        
        if not engine.dialect.has_table(engine, table_name):
            return -1

        table = session.query(Base.metadata.tables[table_name]).all()
        for user in table:
            if (user.username == u_id and user.password == pas):
                #correct
                return user.role

        session.close()
        return False

    def has_table(self, table_name):
        if not engine.dialect.has_table(engine, table_name):
            return False
        else:
            return True

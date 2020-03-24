from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

engine = create_engine('sqlite:///course_status.db')
Base = declarative_base()

def get_class(tablename):
    class Course(Base):
        __tablename__ = tablename
        __table_args__ = {'extend_existing':True}
        id = Column(Integer, primary_key = True)
        course = Column(String, nullable = False)
        status = Column(Integer, nullable = False)
	
        def set_status(self, new_status):
            self.status = new_status

    return Course

class Course_library(object):
    def __init__(self, name):
        self.table_name = name
        self.status_class = get_class(name)
        
    def create_table(self):
        try:
            Base.metadata.create_all(engine)
        except:
            print("Table already there");
    
    def insert_course(self, course, status):
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        conn = engine.connect()
        row = self.status_class(course = course, status = status)
        session.add(row)
        session.commit()
        session.close()

    def update_status(self,course, new_status):
        DBSession = sessionmaker(bind = engine)
        session = DBSession()
        conn = engine.connect()
        table = session.query(Base.metadata.tables[self.table_name]).all()
        rID = 0
        for row in table:
            if (row.course == course):
                #setattr(row, 'status', new_status)
                #session.commit()
                rID = row.id
                #session.delete(row)
                #session.commit()
        
        user_t = Base.metadata.tables[self.table_name]
        #del_st = user_t.delete().where(
        #user_t.c.id == rID)
        #conn = engine.connect()
        #conn.execute(del_st)
        #row = session.query(user_t).filter(
        #user_t.c.id == rID).first()
        #row.status = new_status
        #session.commit()
        stmt = user_t.update().\
            where(user_t.c.id==rID).\
            values(status=new_status)
        conn.execute(stmt)

    def get_course_array(self, status):
        DBSession = sessionmaker(bind = engine)
        session = DBSession()
        l = []
        table = session.query(Base.metadata.tables[self.table_name]).all()
        for row in table:
            if row.status == status:
                l.append(row.course)
        session.close()
        return l

    def get_all_courses(self):
        DBSession = sessionmaker(bind = engine)
        session = DBSession()
        l = []
        table = session.query(Base.metadata.tables[self.table_name]).all()
        for row in table:
            l.append(row.course)
        session.close()
        return l

    def match_courses_and_status(self, course_array, status):
        DBSession = sessionmaker(bind = engine)
        session = DBSession()
        l = []
        table = session.query(Base.metadata.tables[self.table_name]).all()
        for course in course_array:
            for row in table:
                if row.course == course:
                    if row.status == status:
                        l.append(row.course)
                        print(row.course)
        session.close()
        return l        
        
    def get_status(self, course):
        DBSession = sessionmaker(bind = engine)
        session = DBSession()

        table = session.query(Base.metadata.tables[self.table_name]).all()
        status = 0
        for row in table:
            if (row.course == course):
                status = row.status
        session.close()
        return status

    def has_table(self, table_name):
        if not engine.dialect.has_table(engine, table_name):
            return False
        else:
            return True

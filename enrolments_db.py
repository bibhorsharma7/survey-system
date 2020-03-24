# Enrollment database

from sqlalchemy import Column, ForeignKey, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///enrolments.db')
Base = declarative_base()

def get_class(tablename):
    class Row(Base):
        __tablename__ = tablename
        __table_args__ = {'extend_existing':True}
        id = Column(Integer, primary_key=True)
        username = Column(String, nullable=False)
        course = Column(String, nullable=False)

    return Row

class Enrolment(object):
    def __init__(self, name):
        self.table_name = name
        self.enrolment_class = get_class(name)

    def create_table(self):
        try:
            Base.metadata.create_all(engine)
        except:
            print("Table already there")

    def insert_row(self, username, course):
        DBSession = sessionmaker(bind = engine)
        session = DBSession()

        row = self.enrolment_class(username=username, course=course)
        session.add(row)
        session.commit()
        session.close()

    def get_courselist(self,table_name, u_id):
        courses = []
        DBSession = sessionmaker(bind=engine)
        session = DBSession()

        if not engine.dialect.has_table(engine, table_name):
            return courses

        table = session.query(Base.metadata.tables[table_name]).all()
        for row in table:
            if (row.username == u_id):
                courses.append(row.course)

        session.close()

        return courses

    def has_table(self, table_name):
        if not engine.dialect.has_table(engine, table_name):
            return False
        else:
            return True

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

engine = create_engine('sqlite:///library.db')
Base=declarative_base()

def get_class(tablename):
    class Question(Base):
        __tablename__ = tablename
        __table_args__ = {'extend_existing': True} 
        id = Column(Integer, primary_key=True)
        questionType = Column(Integer, nullable=False)
        question = Column(String, nullable=False)
        answer = Column(String, nullable=True)
        answer1 = Column(String, nullable=True)
        answer2 = Column(String, nullable=True)
        answer3 = Column(String, nullable=True)
        response = Column(Integer, nullable=True)
        response1 = Column(Integer, nullable=True)
        response2 = Column(Integer, nullable=True)
        response3 = Column(Integer, nullable=True)
        text_response = Column(String, nullable=True)
    return Question


class Library(object):
    
    def __init__(self, name):
        self.table_name = name
        self.Question_Class = get_class(name)
    		
    def create_table(self):
        try:
            Base.metadata.create_all(engine)
        except:
            print("Table already there")

    def insert_question(self, questionType, question, answer, answer1, answer2, answer3, id):
        default_multi_response = "0"
        default_text_response = ""
        
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        
        #Question_Class = get_class(self.table_name)			
        new_question = self.Question_Class(id = id, questionType = questionType, question = question, answer = answer, answer1 = answer1, answer2 = answer2, answer3 = answer3, response = default_multi_response, response1 = default_multi_response, response2 = default_multi_response, response3 = default_multi_response, text_response = default_text_response)
        session.add(new_question)
        session.commit()
        session.close()

    def retrieve_table(self):

        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        l = []
        if not engine.dialect.has_table(engine, self.table_name): 
            return l
                
        found_question = session.query(Base.metadata.tables[self.table_name]).all()
        for i in found_question:
            q = [i.questionType, i.question, i.answer, i.answer1, i.answer2, i.answer3, i.id]
            l.append(q)
        session.close()
        return l

    def getResponses(self, qID):
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        l = []
        if not engine.dialect.has_table(engine, self.table_name):
            return l
        found_questions = session.query(Base.metadata.tables[self.table_name]).all()
        for i in found_questions:
            if(i.id == qID):
                response = [i.response, i.response1, i.response2, i.response3, i.text_response]
        session.close()
        return response

    def addResponses(self, response_a, response_b, response_c, response_d, text_response, qID):
        DBSession = sessionmaker(bind=engine)
        conn = engine.connect()
        #found_questions = Session.query(Base.metadata.table[self.table_name]).all()
        #for i in found_questions: 
        #    if(i.id == qID):       
        #        #if it's a multi question
        #        if(questionType == 0):
        #            i.response = response_a
        #            i.response1 = response_b
        #            i.response2 = response_c
        #            i.response3 = response_d
        #        #if it's a text question
        #        elif(questionType == 1):
        #            i.text_response = text_response
        #session.commit()
        #session.close()
        user_t = Base.metadata.tables[self.table_name]
        stmt = user_t.update().\
            where(user_t.c.id==qID).\
            values(response=response_a, response1=response_b, response2=response_c, response3=response_d, text_response = text_response)
        conn.execute(stmt)	
            
    def get_rows(self):
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        l = []
        if not engine.dialect.has_table(engine, self.table_name): 
            return l    
        found_question = session.query(Base.metadata.tables[self.table_name]).all()
        for i in found_question:
            text_responses = []
            text_responses = i.text_response.split("\n")
            q = [i.questionType, i.question, i.answer, i.answer1, i.answer2, i.answer3, i.id, i.response, i.response1, i.response2, i.response3, text_responses]
            l.append(q)
        session.close()
        return l

#library = Library('GENERIC_POOL')
#library.create_table()
#library.insert_question('010', 1, 'ThisQuestion', 'a', 'b', 'c', 'd')
#print (library.retrieve_table('GENERIC_POOL'))
       
#    def editMultiQuestion(self, course, qID, response, response1, response2, response3):
#        DBSession = sessionmaker(bind=engine)
#        session = DBSession()
#        found_question = Session.query(Base.metadata.tables[course]).all()
#        for i in found_question:
#            if(i.id == qID):
#                i.response = response
#                i.response1 = response1
#                i.response2 = response2
#                i.response3 = response3
#        session.commit()
#        session.close()

#    def editTextQuestion(self, course, text_response, qID):
#        DBSession = sessionmaker (bind=engine)
#        found_question = Session.query(Base.metadata.table[course]).all()
#        for i in found_question:
#            if(i.id == qID):
#                i.text_response = text_response
#        session.commit()
#        session.close()


#library = Library("COMP1000_17s2")
#library.create_table()
#library.addResponses(0, 2, 4, 1, 3, "asdad", 1)
         

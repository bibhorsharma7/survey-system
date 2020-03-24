class Survey:
	questions = []
	course = ""

	def __init__(self, name, course):
		self.name = name
		self.course = course

	def appendQuestion(self, question):
		self.questions.append(question)


	def getCourse(self):
		return self.course

	def getQuestions(self):
		return self.questions

	def convertToLinearList(self):
		l = []
		for q in self.questions:
			l.append(q.convertLinear())
		return l


class Question:
	name = ""
	answers = []
	question_ID = -1
	q_type = -1

	def __init__(self, _type, name, l, qID):
		self.name = name
		self.answers = l
		self.question_ID = qID
		self.q_type = _type 
		
	def appendAnswer(self, answer):
		self.answers.append(answer)

	def getName(self):
		return self.name
		
	def getQuestionId(self):
		return self.question_ID
		
	def getType(self):
		return q_type			

	def getAnswers(self):
		return self.answers

	def convertLinear(self):
		linear = []
		linear.append(self.q_type)
		linear.append(self.name)
		for a in self.answers:
			linear.append(a)
		linear.append(self.question_ID) 
		return linear

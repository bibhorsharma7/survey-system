#from create_csv import write_to_csv, read_from_csv, writeAnswerGridtoCSV
from flask_login import UserMixin
import csv
import os
import sys

#Admin class
class Admin():
	surveys = []

	def __init__(self, userName, password):
		self.userName = userName
		self.password = password

#	def getName(self):
#		return self.name

	def getUserName(self):
		return self.userName

	def getPassword(self):
		return self.password

	def writeCurrentSurveyToCSV(self):
		write_to_csv(self.surveys[-1], self.userName)

	def writeCurrentSurveyAnswerGridToCSV(self):
		writeAnswerGridtoCSV(self.surveys[-1])

# User
class User(UserMixin):

    def __init__(self, id):
        self.id = id

    def __repr__(self):
        return "%d" % (self.id)

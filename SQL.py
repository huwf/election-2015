import mysql.connector

class SQL():

	def __init__(self):
		#print("Database constructor")
		self.conn = mysql.connector.connect(
			user='election', 
			host='localhost', 
			password='', 
			database='')

		self.cur = self.conn.cursor()

	def __del__(self):
		#print "Committing and closing DB connection\n"
		self.conn.commit()
		self.conn.close()

	def insert_query(self, query, parameters = ''):
		'''
		Inserts a value into the database. Returns lastrowid
		'''
		self.cur.execute(query, parameters)
		self.conn.commit()
		return self.cur.lastrowid

	def select_query(self, query, parameters = ''):
		'''
		Performs a select query, and returns a list of the results
		'''
		self.cur.execute(query, parameters)
		return self.cur.fetchall()

	def select_query_as_list(self, query, parameters = ''):
		'''
		If I have a list of stuff with only one field, enter the field as colName, and
		then add it to a new list to return
		'''
		listy = []
		for q in self.selectQuery(query, parameters):
			listy.append(q[0])
		return listy

	def single_value_select_query(self, query, parameters = ''):		
		self.cur.execute(query, parameters)
		
		try:
			return self.cur.fetchone()[0]
		except:			
			return None
		
		

	def update_query(self, query, parameters = ''):
		self.cur.execute(query, parameters)
		self.conn.commit()
		return self.cur.rowcount


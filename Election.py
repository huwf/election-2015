from BeautifulSoup import BeautifulSoup
import requests
from SQL import SQL
import unicodedata

r = requests.get("http://example.com")

def get_list_of_urls(html):
	soup = BeautifulSoup(html)
	az = soup.find("ol", attrs={'class' : 'az-selector'}).findAll('li')
	listy = []
	for li in az:
		print li.text	
		table = soup.find("table", id=li.text)
		if table != None:
			tr = table.findAll('tr')
			for t in tr:
				a = t.find('a')
				if a != None:
					listy.append("http://www.bbc.co.uk%s" % a['href'])
	
	return listy

def extract_data_from_page(html):
	listy = []
	soup = BeautifulSoup(html)
	name = soup.find('h1', attrs={'class' : "constituency-title__title"}).text

	
	turnout = soup.find('div', attrs={'class' : 'results-turnout__percentage'})
	turnout = turnout.find('span', attrs={'class' : 'results-turnout__value results-turnout__value--right'})
	turnout = turnout.text.replace('%', '')

	print "%s, TURNOUT %s\n========================================================" % (name.upper(), turnout)

	parties = soup.findAll('div', attrs={'class' : 'party'})
	for p in parties:
		party = p.find('div', attrs={'class' : 'party__name--long'}).text
		candidate = p.find('div', attrs={'class' : 'party__result--candidate'}).text
		candidate = candidate.replace(', with candidate', '')
		votes = p.find('li', attrs={'class' : 'party__result--votes essential'}).text
		votes = votes.replace('total votes taken', '')
		votes = votes.replace(',', '')
		votes = votes.replace('.', '')
		percent = p.find('li', attrs={'class' : 'party__result--votesshare essential'}).text
		percent = percent.replace('% share of the total vote', '')
		swing = p.find('li', attrs={'class' : 'party__result--votesnet essential'}).find('span').text
		swing = swing.replace('+', '')
		print party, candidate, votes, percent, swing
		listy.append([name, float(turnout), party, candidate, int(votes), float(percent), float(swing)])
	return listy

def write_to_database(sql, results):
	query = 'INSERT INTO Constituency(Name, Turnout) VALUES(%s,%s)'
	r_1 = list(results[0][0:2])
	constituency_id = sql.insert_query(query, r_1)
	for r in results:
		query = 'INSERT INTO Results(ConstituencyId, Party, Candidate, Votes, Percentage, Swing) \
		VALUES(%s,%s,%s,%s,%s,%s)'	
		r_2 = [constituency_id] + list(r[2:])
		sql.insert_query(query, r_2)

def run_it():
	with open('ConstituencyList.html') as f:
		sql = SQL()
		html = f.read()
		constituencies = get_list_of_urls(html)
		for con in constituencies:
			r = requests.get(con, headers={"Accept-Encoding": "identity, deflate, compress, gzip"})
			html = unicodedata.normalize('NFKD', unicode(r.text)).encode('ascii', 'ignore')			
			#html = unicode(r.text).encode('utf-8', 'ignore')
			results = extract_data_from_page(html)
			write_to_database(sql, results)
			print "\n"			

run_it()
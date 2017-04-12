import scholar 

def run(key_phrase):
	querier = scholar.ScholarQuerier()
	settings = scholar.ScholarSettings()
	querier.apply_settings(settings)

	query = scholar.SearchScholarQuery()
	#query.set_author("Alan Turing")
	query.set_words(key_phrase)
	query.set_num_page_results(21) #20 doesn't work for some reason but anything more returns 20

	querier.send_query(query)
	# Print the URL of articles found
	i = 0
	for x in querier.articles:
		print i, x['url']
		i += 1
	#print querier.articles[0]['url']

#run("artificial intelligence fake news donald trump") #test case
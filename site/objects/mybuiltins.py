''' Свои функции '''

import json

# Подготовка данных для страницы тикера
def ticker_data_generator(ticker_data:dict):
		
	# The price from which price started this year
	ticker_data["predict_y_start"] = round(int(ticker_data["per_y"][0]))

	# Counting the change of entry predict price from latest price
	ticker_data["per_y"][0] = round( 100 - ticker_data["per_y"][0] / ticker_data['predict_y'][0] * 100,2)

	# The percent which price is changed from start of this year
	ticker_data["per_from_start"] = round(
		100 - ticker_data['predict_y_start'] / ticker_data["price"]*100
	)
	ticker_data["per_to_year_end"] = round(
		100 - ticker_data['price'] /ticker_data['predict_y'][0]* 100
	)

	ticker_data["first_half_change"] = round((ticker_data["predict_y"][1]+ticker_data["predict_y"][2])/2)
	ticker_data["second_half_add"] = round(
		ticker_data["predict_y"][2]-ticker_data["first_half_change"],2
	) 

	ticker_data["second_half_word"] = "lose" if (
		ticker_data["second_half_add"] < 0
	) else "add"
	ticker_data["second_half_add"] = abs(ticker_data["second_half_add"])
	ticker_data["per_second_from_now"] = round(
		100-(ticker_data["price"]/ticker_data["predict_y"][2]*100),2
	)

	# Creating namespace for special data of 2 parts of year predicts
	ticker_data["first_5y"] = {}
	ticker_data["second_5y"] = {}

	# Keyword to define price changes in two parts of year predicts
	ticker_data["first_5y"]["keyword"] = "increase" if (
		ticker_data["predict_y"][2] < ticker_data["predict_y"][6]
	) else "decrease"
	ticker_data["second_5y"]["keyword"] = "climb" if (
		ticker_data["predict_y"][7] < ticker_data["predict_y"][11] 
	) else "fall"

	# The percent of price change in two parts of year predicts 
	ticker_data["first_5y"]["per"] = round(
		100 - (ticker_data["predict_y"][2] / ticker_data["predict_y"][6]*100),2
	)  
	ticker_data["second_5y"]["per"] = round(
		100 - (ticker_data["predict_y"][7] / ticker_data["predict_y"][11]*100),2
	)

	return ticker_data

# Получение данных для главной странницы
def get_home(cursor,pattern=None):
	
	sql = f'''
		SELECT 
			name,
			ticker,
			image_link,
			price 
		FROM 
			main
		{f"WHERE ticker LIKE '{pattern.lower()}%' OR name LIKE '{pattern.lower()}%'" if pattern else ''}
	'''

	cursor.execute(sql)
	data = cursor.fetchall()

	if data:
		data.sort(key=socket('price'),reverse=True)

	return data


# Получение данных страницы тикера
def get_ticker(cursor,ticker):

	sql = f'''
		SELECT 
			name,
			ticker,
			image_link,
			price,
			predict_d,
			predict_m,
			predict_y,
			mid_y,
			per_y
		FROM main 
		WHERE ticker="{ticker}"
	'''

	try:
		cursor.execute(sql)
		ticker_data = cursor.fetchall()
		ticker_data[0]["predict_d"] = json.loads(ticker_data[0]["predict_d"])
		ticker_data[0]["predict_m"] = json.loads(ticker_data[0]["predict_m"])
		ticker_data[0]["predict_y"] = json.loads(ticker_data[0]["predict_y"])
		ticker_data[0]["mid_y"] 	= json.loads(ticker_data[0]["mid_y"])
		ticker_data[0]["per_y"]     = json.loads(ticker_data[0]["per_y"])
		return ticker_data
	except: 
		return None
		

def socket(key):
	def get(dict):
		return dict[key]
	return get
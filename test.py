# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import matplotlib
import urllib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import os, argparse, sys, time
from tqdm import tqdm

def createParser():
	parser = argparse.ArgumentParser()
	parser.add_argument('-d', '--days', type=int, default=0)
	parser.add_argument('-m', '--months', type=int, default=0)
	parser.add_argument('-y', '--years', type=int, default=0)
	return parser
	
def usage():
	os.system('clear')
	print 
	print 'Er.Catcher 1.0.2 - (C) 2016 SAITAMA'
	print 'Released under the GNU GPL... (It is a bullshit)'   
	print  
	print '\t█████████████████████████████████████████████'
	print '\t█───█────███────█────█───█────█─██─█───█────█'
	print '\t█─███─██─███─██─█─██─██─██─██─█─██─█─███─██─█'
	print '\t█───█────███─████────██─██─████────█───█────█'
	print '\t█─███─█─████─██─█─██─██─██─██─█─██─█─███─█─██'
	print '\t█───█─█─██─█────█─██─██─██────█─██─█───█─█─██'
	print '\t█████████████████████████████████████████████'
	print '_____________________________________________________________________________'
	print '\tSome questions? twiggymonro@gmail.com'
	print "\tI don't mention your email? Skype: twiggymonro"
	print '\tAlso can find me vk.com/id26310944'
	print '\tor maybe facebook.com/maxim.vasiliev.1291'
	print 'Er.Catcher Tool'
	print 'python Er.Catcher.py -h -d days -m months -y years'
	print '-h, --help - help menu'
	print '-d, --days - number of days you need(default value is 0)'
	print '-m, --months - number of months you need(default value is 0)'
	print '-y, --years - number of years you need(default value is 0)'
	print 'Examples:'
	print '\tpython corrME.py -d 20'
	print '\tpython corrME.py -m 6'
	print '\tpython corrME.py --days 18 --months 7'
	print '\tpython corrME.py --days 18 --months 7'


def charter(ticker, data1, data2, data3, data4, data5):
	
	with PdfPages('report_'+ticker+'.pdf') as pdf:
		# MA
		data1.plot()
		plt.title('Moving averages')
		plt.xlabel('MA must be smooth') 
		pdf.savefig()
		# NaN
		data2.plot()
		plt.rc('text', usetex=True)
		plt.title('NaN')
		plt.xlabel('Must be no NaN') 
		pdf.savefig()
		# RSI
		data3.plot(subplots=True, figsize=(6, 6))
		plt.rc('text', usetex=True)
		plt.title('RSI vs Price')
		plt.xlabel('If RSI goes over 75 and price grow up, smth strange.') 
		pdf.savefig()		
		# Gapper
		data4.plot()
		plt.rc('text', usetex=True)
		plt.title('Volatility')
		plt.xlabel('Normal distribution of volatility. CHG must be \nbetween +STD and -STD. Over +2*STD and -2*STD very bad result.') 
		pdf.savefig()
		# Holes
		data5.plot()	
		plt.rc('text', usetex=True)
		plt.title('Holes in data')
		plt.xlabel('Chatrs for checking holes in data.') 
		pdf.savefig()
		#plt.show()
		#plt.close()	

'''
	MA must be smooth on chart
'''
def moving_average(data):
	result = pd.DataFrame()
	result['Datetime'] = data[0]
	result['Price'] = data[3]
	result['MA50'] = pd.rolling_mean(data[3], 50)
	result['MA100'] = pd.rolling_mean(data[3], 100)
	result['MA200'] = pd.rolling_mean(data[3], 200)
	return result.set_index('Datetime')

def nan_checker(data):
	result = pd.DataFrame()
	result['Datetime'] = data[0]
	result['Price'] = pd.isnull(data[3])
	result['Datetime'] = pd.isnull(data[0])
	return result

'''
	Check RSI and find strange situations
'''
def rsi(price, n=14):
		#---------------------------------
		def rsiCalc(p):
			# subfunction for calculating rsi for one lookback period
			avgGain = p[p>0].sum()/n
			avgLoss = -p[p<0].sum()/n 
			rs = avgGain/avgLoss
			return 100 - 100/(1+rs)
		#---------------------------------
		''' rsi indicator '''
		gain = (price-price.shift(1)).fillna(0) # calculate price gain with previous day, first row nan is filled with 0
		# run for all periods with rolling_apply
		return pd.rolling_apply(gain,n,rsiCalc) 

def rsi_price(data):
	result = pd.DataFrame()
	result['Datetime'] = data[0]
	result['RSI'] = rsi(data[3])
	result['Signal'] = data[3]
	return result.set_index('Datetime')

'''
	Gap more than 7%, previoslu calculate it
'''
def gapper(data):
	result = pd.DataFrame()
	result['Datetime'] = data[0]
	result['CHG'] = data[3] / data[3].shift(1) - 1
	mean = result['CHG'].mean(skipna=True)
	std = np.std(result['CHG'])
	result['-STD'] = mean - std 
	result['+STD'] = mean + std 
	result['-2 * STD'] = mean - 2*std 
	result['+2 * STD'] = mean + 2*std 
	return result.set_index('Datetime')

def date_chart(data):
	result = pd.DataFrame()
	result['Datetime'] = data[0]
	result['Price'] = data[3]
	return result.set_index('Datetime')

	
def baby_on_fire(d):
	
	os.system('clear')
	print 'While program is running'
	print 'You can sing the song Scorpions Rock You Like a Hurricane'
	print
	
	
	song = ['It is early morning,','The sun comes out.','Last night was shaking','And pretty loud','My cat is purring','And scratches my skin.',
	'So what is wrong','With another sin.','The bitch is hungry,','She needs to tell,','So give her inches','And feed her well',
	'More days to come,','New places to go,','Ive got to leave,','It is time for the show.','\nHERE I AM, ROCK YOU LIKE A HURRICANE','HERE I AM, ROCK YOU LIKE A HURRICANE']
	
	companies = ['AVID.OQ.npy','GM.N.npy','VIAV.OQ.npy']
	i = 0
	for com in (companies):	# to delete song, wrap tqdm(companies)
		data = np.load(com)
		data = pd.DataFrame(data)
		data.iloc[[0]] = matplotlib.dates.num2date(data.iloc[[0]]) 
		data = data.transpose()
		data = data.ix[len(data)-d:]
		com = com.partition('.')
		ticker = com[0]
		charter(ticker, moving_average(data), nan_checker(data), rsi_price(data), gapper(data), date_chart(data))
		
		print song[i*6]
		time.sleep(2)
		print song[i*6+1]
		time.sleep(2)
		print song[i*6+2]
		time.sleep(2)
		print song[i*6+3]
		time.sleep(2)
		print song[i*6+4]
		time.sleep(2)
		print song[i*6+5]
		time.sleep(2)

		
		i += 1

if __name__ == '__main__':
	parser = createParser()
	namespace = parser.parse_args(sys.argv[1:])
	
	days = namespace.days
	months = namespace.months * 20
	years = namespace.years * 252
	
	result_days = (days + months + years) * 8
	
	if result_days > 0:
		baby_on_fire(result_days)
		print
		print 'Thank you so much!'
	else:
		usage()
	

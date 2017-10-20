

def doFormattingUnicode(unicodeString):
	formattedString = unicodeString.replace(",",".").replace("']","").replace("[u'","").replace("jaar","").replace("%","")
	return formattedString

def doFormattingProductName(productName):
	formattedProductName = productName.split()[-1]
	return formattedProductName

def findCoverage(coverage):
	if(coverage == "Met NHG of tot en met 67.5 van de marktwaarde*"):
		return "0 67.5"
	elif(coverage == "Meer dan 67.5 tot en met 90 van de marktwaarde*"):
		return "67.5 90.0"
	elif(coverage == "Meer dan 90 van de marktwaarde*"):
		return "90.0 100.0"
	else:
		return "ERROR"
def changeMonth(date):
	date = date.replace("januari","january").replace("februari","february").replace("maart","march").replace("mei","may").replace("juni","june").replace("juli","july").replace("augustus","august").replace("oktober","october")
	return date


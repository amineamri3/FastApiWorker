
import pycountry

def formatName(str):
    components = str.split('-')
    #We capitalize the first letter of each component with the 'title' method and join them together then strip the last space we added.
    return ''.join(x.title()+' ' for x in components[0:]).rstrip()

def trimCurrency(str):
	return str.replace(' USD','')


#using pycountry to convert alpha-3 country code to country name
def countryCodeToName(str):
    return pycountry.countries.get(alpha_3=str).name



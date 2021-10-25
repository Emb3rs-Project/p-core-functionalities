
import json

data = [
	{'country':'Austria','code':'AT'},
	{'country':'Belgium','code':'BE'},
	{'country':'Bulgaria','code':'BG'},
	{'country':'Croatia','code':'HR'},
	{'country':'Cyprus','code':'CY'},
	{'country':'Czech Republic','code':'CZ'},
	{'country':'Denmark','code':'DK'},
	{'country':'Estonia','code':'EE'},
	{'country':'Finland','code':'FI'},
	{'country':'France','code':'FR'},
	{'country':'Germany','code':'DE'},
	{'country':'Greece','code':'GR'},
	{'country':'Hungary','code':'HU'},
	{'country':'Ireland','code':'IE'},
	{'country':'Italy','code':'IT'},
	{'country':'Latvia','code':'LV'},
	{'country':'Lithuania','code':'LT'},
	{'country':'Luxembourg','code':'LU'},
	{'country':'Malta','code':'MT'},
	{'country':'Netherlands','code':'NL'},
	{'country':'Poland','code':'PL'},
	{'country':'Portugal','code':'PT'},
	{'country':'Romania','code':'RO'},
	{'country':'Slovakia','code':'SK'},
	{'country':'Slovenia','code':'SI'},
    {'country': 'Switzerland', 'code': 'CH'},
    {'country':'Spain','code':'ES'},
	{'country':'Sweden','code':'SE'},

]


with open('KB_General/Json_files/eu_country_acronym.json', 'w') as jsonfile:
    json.dump(data, jsonfile)

arq = open("../web/crims_por_rota.tsv", "r")

linhas = arq.readlines()

dict_rota_crimes = {}

for i in linhas:
	key = i.split(",")[0]
	value = i.split(",")[1].replace("\n", "")

	if(key not in dict_rota_crimes.keys()):
		dict_rota_crimes[key] = value

	else:
		dict_rota_crimes[key] = dict_rota_crimes[key] + value

for k in dict_rota_crimes.keys():
	print k, dict_rota_crimes[k]


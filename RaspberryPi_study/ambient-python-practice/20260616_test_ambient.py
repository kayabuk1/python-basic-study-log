import ambient

temp = 20,21,22,23,24
humid = 30,40,50,60,70
am = ambient.Ambient("101418", "715d2714311951f3")
for d1,d2 in temp,humid:
	r = am.send({"d1":temp, "d2":humid})

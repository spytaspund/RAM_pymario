def fileToConfig(file):
    f = open(file, "r")
    lines = f.readlines()
    configdict = {}
    for i in lines:
        values = i.split("=")
        key = values[0]
        print(values)
        if values[1].find('\n') == True:
            val = values[1][0:values[1].find('\n')]
            print(val)
        else:
            val = values[1]
        if key != "debug":
            val = float(val)
        else:
            if val == "True":
                val = True
            if val == "False":
                val = False
        if key != "gravity" and key != "debug":
            val = round(val)
            #print(val)
        configdict[key] = val
    return configdict

print(fileToConfig("game.cfg"))

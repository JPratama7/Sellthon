def logfunc(type, e):
    type = str(type).upper()
    with open("logbot.txt", "a") as log:
        log.write(f"{type} ERROR : {e}\n" )
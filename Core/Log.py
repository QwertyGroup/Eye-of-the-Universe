IsLoggingEnabled = False


def Log(message):
    if IsLoggingEnabled:
        print(message)
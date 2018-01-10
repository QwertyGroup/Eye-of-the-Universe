IsEnabled = False


def Log(message):
    if IsEnabled:
        print(message)

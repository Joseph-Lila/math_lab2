def out_red(text):
    print("\033[31m\033[40m\033[1m{}".format(text), end="\n")
    print("\033[30m\033[47m", end='')


def out_blue(text):
    print("\033[34m\033[40m\033[1m{}".format(text), end="\n")
    print("\033[30m\033[47m", end='')


def out_purple(text):
    print("\033[31m\033[44m\033[3m{}".format(text), end="\n")
    print("\033[30m\033[47m", end='')

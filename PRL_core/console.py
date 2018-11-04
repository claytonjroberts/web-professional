import os

rows, cols = [int(x) for x in os.popen("stty size", "r").read().split()]


class ConsoleInterface:
    boxChars = {
        "tl": "┏",
        "tr": "┓",
        "br": "┛",
        "bl": "┗",
        "h": "━",
        "v": "┃",
        # 'g': '┴',
        # 'h': '├',
        # 'i': '┬',
        # 'j': '┤',
        # 'k': '╷',
        # 'l': '┼',
    }

    @classmethod
    def getRows(cls) -> int:
        return int(os.popen("stty size", "r").read().split()[0])

    @classmethod
    def getCols(cls) -> int:
        return int(os.popen("stty size", "r").read().split()[1])

    def output(self, message):
        if hasattr(self.__class__, "_debug"):
            if not self.__class__._debug:
                return
        print("{} {}".format(self.consoleTag, message))

    @property
    def consoleTag(self):
        return "({: >})".format(self.__class__.__name__)

    @classmethod
    def output(cls, message, ask=False, end="\n"):
        if hasattr(cls, "_debug"):
            if not cls._debug:
                return

        msg = "{} {}".format(cls.consoleTag(), message)
        if ask:
            return input(msg)
        else:
            print(msg, end=end)

    @classmethod
    def consoleTag(cls):
        return "[{: >}]".format(cls.__name__)

    @classmethod
    def confirm(cls, message):
        tries = 0
        while True:
            i = cls.output("{} [Y/n]".format(message), True)
            if i == "Y":
                return True
            elif i == "n":
                return False
            else:
                cls.output("'{}' not a valid response, try again.")
            tries += 1
            if tries > 2:
                break

    @classmethod
    def boxText(cls, text):
        maxlen = 0
        for line in text.split("\n"):
            maxlen = max(len(line), maxlen)

        new = ""
        new += (
            f"{cls.boxChars['tl']}{cls.boxChars['h']*(maxlen+2)}{cls.boxChars['tr']}\n"
        )
        for line in text.split("\n"):
            new += (
                f"{cls.boxChars['v']}"
                + " {:"
                + str(maxlen)
                + "} "
                + f"{cls.boxChars['v']}\n"
            ).format(line)

        new += (
            f"{cls.boxChars['bl']}{cls.boxChars['h']*(maxlen+2)}{cls.boxChars['br']}\n"
        )
        return new

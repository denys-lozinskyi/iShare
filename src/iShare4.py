class Interface:
    """
    contains a set of functions responsible for receiving data from the user
    """
    @staticmethod
    def buddies_names() -> list:
        """Receives names of participants separated with comma.
        Returns list of names capitalized and cleared from whitespaces"""
        buddies = str(input(lang.dialogue[0]))
        buddies = [
            x.strip().title() for x in buddies.split(',')
            if x.isspace() is False and x != ''
        ]
        return buddies if len(buddies) > 1 else None

    @staticmethod
    def total() -> float:
        """Receives the total amount. Returns the total as a float"""
        while True:
            try:
                total = float(input(lang.dialogue[1]))
            except ValueError:
                continue
            else:
                break
        return total if total > 0 else None

    @staticmethod
    def buddies_shares(buddies, total) -> list:
        """Receives the participants' shares in the total given and the total.
        Returns list of lists with pairs in the format [%1, %2], where %1 - name, and %2 - his share"""
        total_control = 0
        buddies_shares = []
        for buddy in buddies:
            while True:
                try:
                    share = float(input(lang.dialogue[2].format(buddy)))
                except ValueError:
                    continue
                if share < 0:
                    print("\n{}\n".format(lang.alert[2]))
                    continue
                if total_control + share > total:
                    print("\n{}\n".format(lang.alert[3]))
                    continue
                else:
                    total_control += share
                    buddies_shares.append([buddy, share])
                    break
        return buddies_shares if total_control == total else None


def controller():
    """One by one runs interface functions ensuring they all return proper data.
    Then, with the data collected, runs the main module"""

    while True:
        buddies = Interface.buddies_names()
        if buddies is not None:
            break
        else:
            print("\n{}\n".format(lang.alert[0]))

    while True:
        total = Interface.total()
        if total is not None:
            break
        else:
            print("\n{}\n".format(lang.alert[1]))

    while True:
        buddies_shares = Interface.buddies_shares(buddies, total)
        if buddies_shares is not None:
            break
        else:
            print("\n{}\n".format(lang.alert[4]))
    print(main(buddies_shares, total))


def main(buddies_shares, total):
    """
    calculates and returns the result based on the arguments provided
    """
    guys_who_pay = []
    guys_who_get = []
    results_container = []
    equal_share = (
        total / len(buddies_shares)) if len(buddies_shares) > 0 else None

    for buddy in buddies_shares:
        if buddy[1] == 0:
            guys_who_pay.append([buddy[0], equal_share])
        elif buddy[1] < equal_share:
            guys_who_pay.append([buddy[0], equal_share - buddy[1]])
        elif buddy[1] > equal_share:
            guys_who_get.append([buddy[0], buddy[1] - equal_share])
    guys_who_get = sorted(guys_who_get, key=lambda x: x[1], reverse=True)
    guys_who_pay = sorted(guys_who_pay, key=lambda x: x[1], reverse=True)

    for lender in guys_who_get:
        for debtor in guys_who_pay:
            if lender[1] == debtor[1]:
                results_container.append([debtor[0], debtor[1], lender[0]])
                guys_who_pay.remove(debtor)
                break
            elif lender[1] > debtor[1]:
                results_container.append([debtor[0], debtor[1], lender[0]])
                lender[1] -= debtor[1]
                guys_who_get.append(lender)
                guys_who_pay.remove(debtor)
                break
            elif lender[1] < debtor[1]:
                results_container.append([debtor[0], lender[1], lender[0]])
                debtor[1] -= lender[1]
                break
    if len(guys_who_pay) == len(guys_who_get) == 0:
        return lang.message[0].format(equal_share)

    results_rounded = [[x[0], round(x[1], 2), x[2]] for x in results_container]

    output = lang.message[1].format(round(equal_share, 2))
    for debtor, cash, lender in results_rounded:
        line = lang.message[2].format(debtor, cash, lender)
        output += "\n{}".format("".join(line))
    return output


##################
#  TESTING AREA  #
##################

# import ENG language module for this test set


def test_1():
    data = ([["Den", 20], ["Fox", 40], ["Zoe", 0], ["Andy", 0], ["Bron", 40]],
            100)
    output = main(*data)
    assert output == "\n>>>Equal share is 20.00<<<\nZoe pays 20.00 to Fox\nAndy pays 20.00 to Bron"
    return output


def test_2():
    data = ([["Den", 5], ["Fox", 0], ["Zoe", 15], ["Andy", 30], ["Bron", 50]],
            100)
    output = main(*data)
    assert output == "\n>>>Equal share is 20.00<<<\nFox pays 20.00 to Bron\nDen pays 10.00 to Andy\nDen pays 5.00 to " \
                     "Bron\nZoe pays 5.00 to Bron "
    return output


def test_3():
    data = ([["Den", 0], ["Fox", 85], ["Zoe", 0], ["Andy", 15], ["Bron", 0]],
            100)
    output = main(*data)
    assert output == "\n>>>Equal share is 20.00<<<\nDen pays 20.00 to Fox\nZoe pays 20.00 to Fox\nBron pays 20.00 to " \
                     "Fox\nAndy pays 5.00 to Fox "
    return output


def test_4():
    data = ([["Harry", 0], ["Den", 180], ["Fox", 400], ["Chad", 23],
             ["Elena", 900], ["July", 77]], 1580)
    output = main(*data)
    assert output == "\n>>>Equal share is 263.33<<<\nHarry pays 263.33 to Elena\nChad pays 136.67 to Fox\nChad pays " \
                     "103.67 to Elena\nJuly pays 186.33 to Elena\nDen pays 83.33 to Elena "
    return output


def test_5():
    data = ([["Den", 45], ["Fox", 0], ["Zoe", 75]], 120)
    output = main(*data)
    assert output == "\n>>>Equal share is 40.00<<<\nFox pays 35.00 to Zoe\nFox pays 5.00 to Den"
    return output


def test_6():
    data = ([["Ed", 1083.12], ["Den", 70], ["Artem", 600], ["Dasha", 0]],
            1753.12)
    output = main(*data)
    assert output == "\n>>>Equal share is 438.28<<<\nDasha pays 438.28 to Ed\nDen pays 161.72 to Artem\nDen pays " \
                     "206.56 to Ed "
    return output


def test_7():
    data = ([["Ed", 1000], ["Den", 1000], ["Artem", 1000], ["Dasha", 1000]],
            4000)
    output = main(*data)
    assert output == "\nEveryone equally contributed with 1000.00 each"
    return output


def test_8():
    data = ([["Елена", 187], ["Таня", 1500], ["Алекс", 400], ["Толя", 0],
             ["Оля", 1000], ["Денис", 950], ["Вася", 1950]], 5987)
    output = main(*data)
    assert output == "\n>>>Equal share is 855.29<<<\nТоля pays 855.29 to Вася\nЕлена pays 644.71 to Таня\nЕлена pays " \
                     "23.57 to Оля\nАлекс pays 94.71 to Денис\nАлекс pays 239.43 to Вася\nАлекс pays 121.14 to Оля "
    return output


if __name__ == "__main__":
    from src.languages import ENG as lang

    controller()

##    print(test_1())
##    print(test_2())
##    print(test_3())
##    print(test_4())
##    print(test_5())
##    print(test_6())
##    print(test_7())
##    print(test_8())


from src.languages import ENG as lang
# import language of the app interface (English is set by default)


class Interface:
    """
    contains a set of functions responsible for receiving data from the user
    """

    @staticmethod
    def buddies_names() -> list:
        """Receives names of participants separated with comma.
        Returns list of names capitalized and cleared from whitespaces"""
        buddies = str(input(lang.dialogue["ask names"]))
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
                total = float(input(lang.dialogue["ask sum"]))
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
                    share = float(input(lang.dialogue["ask amount paid"].format(buddy)))
                except ValueError:
                    continue
                if share < 0:
                    print("\n{}\n".format(lang.alert["negative share"]))
                    continue
                if total_control + share > total:
                    print("\n{}\n".format(lang.alert["exceeding share"]))
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
            print("\n{}\n".format(lang.alert["no participants"]))

    while True:
        total = Interface.total()
        if total is not None:
            break
        else:
            print("\n{}\n".format(lang.alert["wrong total"]))

    while True:
        buddies_shares = Interface.buddies_shares(buddies, total)
        if buddies_shares is not None:
            break
        else:
            print("\n{}\n".format(lang.alert["inconsistent share"]))
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
        return lang.message["equal contribution"].format(equal_share)

    results_rounded = [[x[0], round(x[1], 2), x[2]] for x in results_container]

    output = lang.message["equal share"].format(round(equal_share, 2))
    for debtor, cash, lender in results_rounded:
        line = lang.message["transaction"].format(debtor, cash, lender)
        output += "\n{}".format("".join(line))
    return output


if __name__ == "__main__":
    controller()

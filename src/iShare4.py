from typing import List, Dict
from src.languages import eng as lang
# import language of the app interface (English is set by default)


class Interface:
    """
        A set of functions responsible for receiving data from the user
    """

    @staticmethod
    def participants_names() -> list:
        """
            Receives names of participants separated with comma from the user.
              :return list: names of participants capitalized and cleared from whitespaces.
                  If qty of names received from a user is <= 1, returns None
        """
        participants = str(input(lang.dialogue['ask names']))
        participants = [x.strip().title() for x in participants.split(',') if not x.isspace() and x != '']
        return participants if len(participants) > 1 else None

    @staticmethod
    def participants_shares(participants) -> Dict:
        """
            Given a list of participants, one by one requests the user for amount of money
            each of participants provided.
              :return dict: with following fields:
                        {'shares': [{participant_1's name (str): his share (float)},
                                    {participant_2's name (str): his share (float)}]}
        """
        participants_shares = {'shares': []}
        for participant in participants:
            while True:
                try:
                    share = float(input(lang.dialogue['ask payment'].format(participant)))
                except ValueError:
                    continue
                if share < 0:
                    print("\n{}\n".format(lang.alert['negative share']))
                    continue
                else:
                    participants_shares['shares'].append({'name': participant, 'share': share})
                    break
        # print(participants_shares)
        return participants_shares


def controller() -> print:
    """
        One by one runs interface functions ensuring they all return proper data.
        Then, with the data collected, runs the main script.
        Prints out the result of shares calculation.
    """
    while True:
        participants: List = Interface.participants_names()
        if participants is not None:
            break
        else:
            print("\n{}\n".format(lang.alert['one participant']))
    participants_shares: Dict = Interface.participants_shares(participants)
    print(main(participants_shares))


def main(data) -> str:
    """
        Computes and returns the result based on the arguments provided.
          :param data: dict in a format: {'shares': [{participant_1's name (str): his share (float)},
                                                     {participant_2's name (str): his share (float)}]}
          :return: str: result of computation

    """
    guys_who_pay: List[Dict] = []
    guys_who_get: List[Dict] = []
    results_container: List[List] = []
    total: float = 0.0

    # calculating the total sum based on shares
    for participant_share in data['shares']:
        total += participant_share['share']
    # calculating an equal share number based on total
    equal_share = total / len(data['shares'])

    # forming out two lists of dicts in the following format: [{'name_1': name_1, 'sum': 'his sum'},
    #                                                          {'name_2': name_2, 'sum': 'his sum'}]
    # guys_who_pay list consists of participants' names with a sum they have to pay to others to get equal.
    # guys_who_get list consists of participants' names with a sum they are to get from others according the equal share
    for participant in data['shares']:
        # if one contributed zero, he has to pay an equal share
        if participant['share'] == 0:
            guys_who_pay.append({'name': participant['name'], 'sum': equal_share})
        # if one contributed less than an equal share, he has to pay rest of sum to reach the equal share
        elif participant['share'] < equal_share:
            guys_who_pay.append({'name': participant['name'], 'sum': equal_share - participant['share']})
        # if one contributed more than an equal share, he is to be paid rest of sum to get aligned with the equal share
        elif participant['share'] > equal_share:
            guys_who_get.append({'name': participant['name'], 'sum': participant['share'] - equal_share})

    # if in the end of forming the lists they both appeared empty, it means every participant paid an equal share
    # thus we return corresponding statement and quit.
    if len(guys_who_pay) == len(guys_who_get) == 0:
        return lang.message['total sum'].format(total) + lang.message['equal contribution'].format(equal_share)

    # Otherwise we continue computation.
    # We order (DESC) lists of dicts by the 'sum' key, so that participants with bigger sums became first in the lists.
    # The aim is to optimize sums that one will pay to another
    guys_who_get = sorted(guys_who_get, key=lambda x: x['sum'], reverse=True)
    guys_who_pay = sorted(guys_who_pay, key=lambda x: x['sum'], reverse=True)

    # forming out output lines with data, by comparing the sum fields for every guy in the lists, and
    # manipulating with the lists as we go.
    for lender in guys_who_get:
        for debtor in guys_who_pay:
            if lender['sum'] == debtor['sum']:
                results_container.append([debtor['name'], debtor['sum'], lender['name']])
                guys_who_pay.remove(debtor)
                break
            elif lender['sum'] >= debtor['sum']:
                results_container.append([debtor['name'], debtor['sum'], lender['name']])
                lender['sum'] -= debtor['sum']
                guys_who_get.append(lender)
                guys_who_pay.remove(debtor)
                break
            elif lender['sum'] < debtor['sum']:
                results_container.append([debtor['name'], lender['sum'], lender['name']])
                debtor['sum'] -= lender['sum']
                break

    # rounding the sums to 2 numbers after the floating point
    results_rounded = [[x[0], round(x[1], 2), x[2]] for x in results_container]

    output = lang.message['total sum'].format(total) + lang.message['equal share'].format(round(equal_share, 2))
    for debtor, cash, lender in results_rounded:
        line = lang.message['personal payment'].format(debtor, cash, lender)
        output += "\n{}".format("".join(line))
    return output


if __name__ == "__main__":
    controller()

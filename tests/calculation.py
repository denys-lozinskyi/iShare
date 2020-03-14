##################
#  TESTING AREA  #
##################

from src.iShare4 import main


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
                     "Bron\nZoe pays 5.00 to Bron"
    return output


def test_3():
    data = ([["Den", 0], ["Fox", 85], ["Zoe", 0], ["Andy", 15], ["Bron", 0]],
            100)
    output = main(*data)
    assert output == "\n>>>Equal share is 20.00<<<\nDen pays 20.00 to Fox\nZoe pays 20.00 to Fox\nBron pays 20.00 to " \
                     "Fox\nAndy pays 5.00 to Fox"
    return output


def test_4():
    data = ([["Harry", 0], ["Den", 180], ["Fox", 400], ["Chad", 23],
             ["Elena", 900], ["July", 77]], 1580)
    output = main(*data)
    assert output == "\n>>>Equal share is 263.33<<<\nHarry pays 263.33 to Elena\nChad pays 136.67 to Fox\nChad pays " \
                     "103.67 to Elena\nJuly pays 186.33 to Elena\nDen pays 83.33 to Elena"
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
                     "206.56 to Ed"
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
                     "23.57 to Оля\nАлекс pays 94.71 to Денис\nАлекс pays 239.43 to Вася\nАлекс pays 121.14 to Оля"
    return output


def runner():
    for test_number in range(8):
        test_name = "test_{}()".format(test_number + 1)
        print(eval(test_name))


if __name__ == "__main__":
    runner()

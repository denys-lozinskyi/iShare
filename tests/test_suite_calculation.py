##################
#  TESTING AREA  #
##################

import sys
from pathlib import Path

file = Path(__file__).resolve()

parent, root = file.parent, file.parents[1]
sys.path.append(str(root))

# Additionally remove the current file's directory from sys.path
try:
    sys.path.remove(str(parent))
except ValueError:  # Already removed
    pass

from src.iShare4 import main


###########################################
#     TESTS AGAINST the MAIN FUNCTION     #
#   TO VERIFY COMPUTATION FUNCTIONALITY   #
###########################################


def test_scenario_1():
    data = {
        'shares': [
            {'name': "Den", 'share': 20},
            {'name': "Fox", 'share': 40},
            {'name': "Zoe", 'share': 0},
            {'name': "Andy", 'share': 0},
            {'name': "Bron", 'share': 40}]
    }
    output = main(data)
    print(f'Function output:\n{output}')
    assert output == "\n>>> Total sum is 100 <<<\n>>> Equal share is 20.00 <<<\n\nZoe pays 20.00 to Fox\nAndy pays 20.00 to Bron"


def test_scenario_2():
    data = {
        'shares': [
            {'name': "Den", 'share': 5},
            {'name': "Fox", 'share': 0},
            {'name': "Zoe", 'share': 15},
            {'name': "Andy", 'share': 30},
            {'name': "Bron", 'share': 50}]
    }
    output = main(data)
    print(f'Function output:\n{output}')
    assert output == "\n>>> Total sum is 100 <<<\n>>> Equal share is 20.00 <<<\n\nFox pays 20.00 to Bron\nDen pays 10.00 to Andy\nDen pays 5.00 to Bron\nZoe pays 5.00 to Bron"


def test_scenario_3():
    data = {
        'shares': [
            {'name': "Den", 'share': 0},
            {'name': "Fox", 'share': 85},
            {'name': "Zoe", 'share': 0},
            {'name': "Andy", 'share': 15},
            {'name': "Bron", 'share': 0}]
    }
    output = main(data)
    print(f'Function output:\n{output}')
    assert output == "\n>>> Total sum is 100 <<<\n>>> Equal share is 20.00 <<<\n\nDen pays 20.00 to Fox\nZoe pays 20.00 to Fox\nBron pays 20.00 to Fox\nAndy pays 5.00 to Fox"


def test_scenario_4():
    data = {
        'shares': [
            {'name': 'Harry', 'share': 0},
            {'name': 'Den', 'share': 180},
            {'name': 'Fox', 'share': 400},
            {'name': 'Chad', 'share': 23},
            {'name': 'Elena', 'share': 900},
            {'name': 'July', 'share': 77}]
    }
    output = main(data)
    print(f'Function output:\n{output}')
    assert output == "\n>>> Total sum is 1580 <<<\n>>> Equal share is 263.33 <<<\n\nHarry pays 263.33 to Elena\nChad pays 136.67 to Fox\nChad pays 103.67 to Elena\nJuly pays 186.33 to Elena\nDen pays 83.33 to Elena"


def test_scenario_5():
    data = {
        'shares': [
            {'name': 'Den', 'share': 45},
            {'name': 'Fox', 'share': 0},
            {'name': 'Zoe', 'share': 75}]
    }
    output = main(data)
    print(f'Function output:\n{output}')
    assert output == "\n>>> Total sum is 120 <<<\n>>> Equal share is 40.00 <<<\n\nFox pays 35.00 to Zoe\nFox pays 5.00 to Den"


def test_scenario_6():
    data = {
        'shares': [
            {'name': 'Ed', 'share': 1083.12},
            {'name': 'Den', 'share': 70},
            {'name': 'Artem', 'share': 600},
            {'name': 'Dasha', 'share': 0}]
    }
    output = main(data)
    print(f'Function output:\n{output}')
    assert output == "\n>>> Total sum is 1753.12 <<<\n>>> Equal share is 438.28 <<<\n\nDasha pays 438.28 to Ed\nDen pays 161.72 to Artem\nDen pays 206.56 to Ed"


def test_scenario_7():
    data = {
        'shares': [
            {'name': 'Ed', 'share': 1000},
            {'name': 'Den', 'share': 1000},
            {'name': 'Artem', 'share': 1000},
            {'name': 'Dasha', 'share': 1000}]
    }
    output = main(data)
    print(f'Function output:\n{output}')
    assert output == "\n>>> Total sum is 4000 <<<\nEveryone equally contributed with 1000.00 each"


def test_scenario_8():
    data = {
        'shares': [
            {'name': 'Елена', 'share': 187},
            {'name': 'Таня', 'share': 1500},
            {'name': 'Алекс', 'share': 400},
            {'name': 'Толя', 'share': 0},
            {'name': 'Оля', 'share': 1000},
            {'name': 'Денис', 'share': 950},
            {'name': 'Вася', 'share': 1950}]
    }
    output = main(data)
    print(f'Function output:\n{output}')
    assert output == "\n>>> Total sum is 5987 <<<\n>>> Equal share is 855.29 <<<\n\nТоля pays 855.29 to Вася\nЕлена pays 644.71 to Таня\nЕлена pays 23.57 to Оля\nАлекс pays 94.71 to Денис\nАлекс pays 239.43 to Вася\nАлекс pays 121.14 to Оля"

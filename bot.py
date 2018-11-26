from collections import defaultdict
from numpy import (
    array as ndarray,
    append,
    float64
)
from functools import partial


class InputParser(object):
    SETTINGS = 'settings'
    UPDATE = 'update'
    ACTION = 'action'
    data = defaultdict(lambda: defaultdict(lambda: ndarray([]))) #keep appending pair_info
    balances = {}
    '''
    'pair': {
        price :int,
        quantity:int
    }
    
    '''
    def __init__(self):
        pass

    def parse_input(self, line):
        lst = line.split()
        return lst[0], lst[1:]

    def parse_settings(self, lst):
        val = lst[1:][0]
        try:
            val = int(val)
        except:
            pass
        self.__dict__[lst[0]] = val
        if lst[0] == 'candle_format':
            self.candle_format = val.split(',')            

    def parse_update(self, lst):
        pair_name_index = self.candle_format.index('pair')
        if lst[0] == 'next_candles':
            pairs = lst[1].split(';')            
            for pair in pairs:
                pair_info = pair.split(',')
                pair_name = pair_info[pair_name_index]
                for i, key in enumerate(self.candle_format):
                    if i != pair_name_index:
                        self.data[pair_name][key] = append(self.data[pair_name][key], float64(pair_info[i]))
        elif lst[0] == 'stacks':
            pairs = lst[1].split(',')
            for pair in pairs:
                info = pair.split(':')
                self.balances[info[0]] = float(info[1])

    
    def parse_action(self, lst):
        pass

class Strategies(object):    
    # data = ndarray

    def custom4params(self, data):
        pass
    
    def rand(self):
        return random.choice(['buy', 'sell', 'pass'])



class Trader(InputParser, Strategies):
    BUY = 'buy'
    SELL = 'sell'
    PASS = 'pass'

    def __init__(self, balance):
        self.balance = balance

    def buy(self, amount, pair):
        pass
    
    def sell(self, amount, pair):
        pass
    
    def notrade(self):
        pass



import random
import logging
from collections import defaultdict
from numpy import (
    array as ndarray,
    append,
    float64
)
from functools import partial

class Bot(object):
    data = defaultdict(lambda: defaultdict(lambda: ndarray([]))) #keep appending pair_info
    balances = {}
    action = 'pass'
    logging.basicConfig(level=logging.DEBUG)
    fees = 0.2/100

    '''
    'pair': {
        volume: ndarray([]),
        open: ndarray([])
    }
    
    '''
    def __init__(self, strategy='rand'):
        if strategy not in Consts.REGISTERED_STRATEGIES:
            self.strategy = Strategies.rand
        else:
            self.strategy = getattr(Strategies, strategy)

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

    
    def parse_action(self):
        #get ready to trade: call the strategy and do action
        action = self.strategy(self.data)
        self.send_action(action)
        return action
    
    def send_action(self, action):
        if action[0] == Consts.PASS:
            output = action[0]
        else:
            output = action[0] + ' ' + action[1] + ' ' + action[2]
        print output
    
    def read_input(self):
        pass


class Strategies(object):
    @staticmethod
    def custom4params(data):
        pass
    @staticmethod
    def rand(data):
        res = random.choice([Consts.BUY, Consts.SELL, Consts.PASS])    
        pair = 'USDT_BTC'
        amount = 0.01
        return res, pair, str(amount)



class Consts(object):
    BUY = 'buy'
    SELL = 'sell'
    PASS = 'pass'
    SETTINGS = 'settings'
    UPDATE = 'update'
    ACTION = 'action'
    REGISTERED_STRATEGIES = ['custom4params', 'rand']

    # def __init__(self, balance):
    #     self.balance = balance

    # def buy(self, amount, pair):
    #     pass
    
    # def sell(self, amount, pair):
    #     pass
    
    # def notrade(self):
    #     pass



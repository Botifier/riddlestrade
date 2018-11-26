import unittest
from numpy import (
    array as ndarray,
)
from numpy.testing import assert_equal,  assert_almost_equal, assert_array_equal
from bot import (
    InputParser,
)


class TestInputParser(unittest.TestCase):
    setting_lines = ['settings timebank 10000']
    setting_lines.append('settings time_per_move 100')
    setting_lines.append('settings player_names player0')
    setting_lines.append('settings your_bot player0')
    setting_lines.append('settings candle_interval 1800')
    setting_lines.append('settings candles_total 720')
    setting_lines.append('settings candles_given 336')
    setting_lines.append('settings initial_stack 1000')
    setting_lines.append('settings candle_format pair,date,high,low,open,close,volume')

    update_lines = ['update game next_candles BTC_ETH,1516753800,0.090995,0.09040017,0.09060023,0.09069601,39.15071531;USDT_ETH,1516753800,976.99644142,955.99999998,974.87665079,960.00160798,316622.92602686;USDT_BTC,1516753800,10806.92999962,10501,10748.4213653,10575.00000019,1618333.6451304']
    update_lines *= 2
    update_lines.append('update game stacks BTC:0.00000000,ETH:0.00000000,USDT:1000.00')

    def setUp(self):
        self.parser = InputParser()        

    def test_parse_input(self):
        type_, _ = self.parser.parse_input(self.setting_lines[0])
        self.assertEqual(type_, self.parser.SETTINGS)

    def test_parse_setting(self):
        for line in self.setting_lines:
            test_lst = line.split()[1:]
            self.parser.parse_settings(test_lst)
        self.assertEqual(self.parser.timebank, 10000)
        self.assertEqual(self.parser.time_per_move, 100)
        self.assertEqual(self.parser.player_names, 'player0')
        self.assertEqual(self.parser.candle_interval, 1800)
        self.assertEqual(self.parser.candles_total, 720)
        self.assertEqual(self.parser.candles_given, 336)
        self.assertEqual(self.parser.initial_stack, 1000)
        self.assertEqual(self.parser.candle_format, ['pair', 'date', 'high', 'low', 'open', 'close' ,'volume'])

    def test_parse_update(self):
        self.parser.candle_format = ['pair', 'date', 'high', 'low', 'open', 'close' ,'volume']
        #test the data should be stacked the last
        for line in self.update_lines:
            test_lst = line.split()[2:]
            self.parser.parse_update(test_lst)
        #BTC_ETH
        assert_array_equal(self.parser.data['BTC_ETH']['date'], ndarray([1516753800, 1516753800]))
        assert_array_equal(self.parser.data['BTC_ETH']['high'], ndarray([0.090995, 0.090995]))
        assert_array_equal(self.parser.data['BTC_ETH']['low'], ndarray([0.09040017, 0.09040017]))
        assert_array_equal(self.parser.data['BTC_ETH']['open'], ndarray([0.09060023, 0.09060023]))
        assert_array_equal(self.parser.data['BTC_ETH']['close'], ndarray([0.09069601, 0.09069601]))
        assert_array_equal(self.parser.data['BTC_ETH']['volume'], ndarray([39.15071531, 39.15071531]))
        #USDT_ETH
        assert_array_equal(self.parser.data['USDT_ETH']['date'], [1516753800, 1516753800])
        assert_array_equal(self.parser.data['USDT_ETH']['high'], ndarray([976.99644142, 976.99644142]))
        assert_array_equal(self.parser.data['USDT_ETH']['low'], ndarray([955.99999998, 955.99999998]))
        assert_array_equal(self.parser.data['USDT_ETH']['open'], ndarray([974.87665079, 974.87665079]))
        assert_array_equal(self.parser.data['USDT_ETH']['close'], ndarray([960.00160798, 960.00160798]))
        assert_array_equal(self.parser.data['USDT_ETH']['volume'], ndarray([316622.92602686, 316622.92602686]))
        #USDT_BTC
        assert_array_equal(self.parser.data['USDT_BTC']['date'], [1516753800, 1516753800])
        assert_array_equal(self.parser.data['USDT_BTC']['high'], ndarray([10806.92999962, 10806.92999962]))
        assert_array_equal(self.parser.data['USDT_BTC']['low'], ndarray([10501, 10501]))
        assert_array_equal(self.parser.data['USDT_BTC']['open'], ndarray([10748.4213653, 10748.4213653]))
        assert_array_equal(self.parser.data['USDT_BTC']['close'], ndarray([10575.00000019, 10575.00000019]))
        assert_array_equal(self.parser.data['USDT_BTC']['volume'], ndarray([1618333.6451304, 1618333.6451304]))
        #Test balance
        self.assertEqual(self.parser.balances, {'BTC':0, 'USDT':1000, 'ETH':0})
        '''
        data = {
            'pair1': {
                date:[],
                high:ndarray(),
                low:ndarray(),
                open:ndarray(),
                close:ndarray(),
                volume:ndarray() #or just list depending on analysis
            },
         '':[]}
        '''
        #add another update and test if all data is stacked
        pass

if __name__ == '__main__':
    unittest.main()
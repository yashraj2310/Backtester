import unittest
import pandas as pd  
from fastapi.testclient import TestClient
from decimal import Decimal
from datetime import datetime

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.main import app
from app.strategy import moving_average_crossover_strategy

class TestTradingAPI(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)

    def test_post_data_with_invalid_type(self):
        invalid_data = {
            "datetime": "2025-01-01T10:00:00+00:00",
            "open": "200.0",
            "high": "202.0",
            "low": "199.0",
            "close": "201.5",
            "volume": "this-is-not-a-number"
        }
        response = self.client.post("/data", json=invalid_data)
        self.assertEqual(response.status_code, 422)

    def test_moving_average_calculation_logic(self):
        sample_data = [
            {'datetime': datetime(2023, 1, 1), 'close': Decimal('10')},
            {'datetime': datetime(2023, 1, 2), 'close': Decimal('12')},
            {'datetime': datetime(2023, 1, 3), 'close': Decimal('14')},
        ]
        df = pd.DataFrame(sample_data).set_index('datetime')
        df['close'] = pd.to_numeric(df['close'])
        df['ma'] = df['close'].rolling(window=2).mean()
        self.assertEqual(df['ma'].iloc[1], 11.0)
        self.assertEqual(df['ma'].iloc[2], 13.0)

    def test_strategy_buy_signal_generation(self):
        sample_data = [
            {'datetime': datetime(2023, 1, 1), 'close': Decimal('100')},
            {'datetime': datetime(2023, 1, 2), 'close': Decimal('100')},
            {'datetime': datetime(2023, 1, 3), 'close': Decimal('100')},
            {'datetime': datetime(2023, 1, 4), 'close': Decimal('110')},
            {'datetime': datetime(2023, 1, 5), 'close': Decimal('110')},
        ]
        result = moving_average_crossover_strategy(sample_data, short_window=2, long_window=4)
        self.assertEqual(len(result['signals']), 1)
        self.assertEqual(result['signals'][0]['signal'], 'BUY')
        self.assertEqual(result['signals'][0]['price'], 110.0)

if __name__ == '__main__':
    unittest.main()
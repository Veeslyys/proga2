from unittest.mock import patch
from task4 import print_message, sequential_time, threaded_time


def test_print_message_sequential():
    with patch('time.sleep') as mock_sleep, \
            patch('builtins.print') as mock_print:
        print_message("Test 1", 1)
        print_message("Test 2", 2)
        print_message("Test 3", 3)

        mock_sleep.assert_any_call(1)
        mock_sleep.assert_any_call(2)
        mock_sleep.assert_any_call(3)

        mock_print.assert_any_call("Test 1")
        mock_print.assert_any_call("Test 2")
        mock_print.assert_any_call("Test 3")


import threading


def test_threaded_execution():
    with patch('time.sleep') as mock_sleep, \
            patch('builtins.print') as mock_print:

        threads = [
            threading.Thread(target=print_message, args=("Thread 1", 1)),
            threading.Thread(target=print_message, args=("Thread 2", 2)),
            threading.Thread(target=print_message, args=("Thread 3", 3))
        ]

        for t in threads:
            t.start()
        for t in threads:
            t.join()
        assert mock_print.call_count == 3
        mock_print.assert_any_call("Thread 1")
        mock_print.assert_any_call("Thread 2")
        mock_print.assert_any_call("Thread 3")



def test_time_comparison():
    with patch('time.time', side_effect=[0, 6, 10, 12]):

        assert threaded_time < sequential_time, \
            "Многопоточное выполнение должно быть быстрее"
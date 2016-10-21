import os
import unittest
from unittest import mock
from user_api import save_new_user


class SaveNewUserTestCase(unittest.TestCase):
    @mock.patch('user_api.open', name='user_api_open', create=True)
    @mock.patch('user_api.request')
    def test_success(self, request_mock, open_mock):
        request_mock.urlopen.return_value.read.return_value = b'{"username":"john", "email":"john@test.com"}'

        result = save_new_user()

        # check if result is True
        self.assertTrue(result)

        # check if Request object was initialized properly
        request_mock.urlopen.assert_called_once_with(url='https://test.com/new_user')

        # check if open correct file
        expected_path = os.path.join('db', 'users.txt')
        open_mock.assert_called_once_with(expected_path, 'a')

        # check if correct data was saved to the file
        file_mock = open_mock.return_value.__enter__.return_value
        file_mock.write.assert_called_once_with('"John", "john@test.com"\n')


if __name__ == '__main__':
    unittest.main()

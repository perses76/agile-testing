import os
import unittest
from unittest import mock
from user_api import save_new_user


class SaveNewUserTestCase(unittest.TestCase):
    def setUp(self):
        self.open_patcher = mock.patch('user_api.open', name='user_api_open', create=True)
        self.open_mock = self.open_patcher.start()

        self.request_patcher = mock.patch('user_api.request')
        self.request_mock = self.request_patcher.start()

        self.set_read_data()

    def tearDown(self):
        self.open_patcher.stop()
        self.request_patcher.stop()

    def set_read_data(self, username='test user', email='test@test.com', raw=None):
        if raw is None:
            raw = '{{"username": "{}", "email": "{}"}}'.format(username, email).encode('utf-8')
        self.request_mock.urlopen.return_value.read.return_value = raw

    def assert_saved_data(self, username='Test user', email='test@test.com'):
        expected_path = os.path.join('db', 'users.txt')
        self.open_mock.assert_called_once_with(expected_path, 'a')

        file_mock = self.open_mock.return_value.__enter__.return_value
        raw = '"{}", "{}"\n'.format(username, email)
        file_mock.write.assert_called_once_with(raw)

    def check_if_data_was_readed(self):
        self.request_mock.urlopen.assert_called_once_with(url='https://test.com/new_user')

    def call_target(self):
        result = save_new_user()
        self.assertTrue(result)
        self.check_if_data_was_readed()
        return result

    def test_success(self):
        self.set_read_data('john', 'john@test.com')
        self.call_target()
        self.assert_saved_data('John', 'john@test.com')

    def test_invalid_url_response_exception(self):
        self.set_read_data(raw=b'Invalid string')
        with self.assertRaises(ValueError):
            self.call_target()

    def test_enterprise_domain_modification(self):
        self.set_read_data(email='john.smith@enterprise.com')
        self.call_target()
        self.assert_saved_data(email='J.smith@enterprise.com')

    def test_obsolete_domain_modification(self):
        self.set_read_data(email='test@obsolete.com')
        self.call_target()
        self.assert_saved_data(email='test@active.com')


if __name__ == '__main__':
    unittest.main()

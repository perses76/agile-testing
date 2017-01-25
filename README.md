# Agile testing

The world revolves mush faster these days. And it effects a lot IT world. A project requirements became blurry and change faster than they can be implemented.
There are a tons of articles, books and study cources teaching you how to survive in this cruel world. Most of them focus on code and pay small (or nothing) attention to testing.
Although testing is necessary part of any agile developing. 

From one point of view, you can not apply agile developing, if you dont cover your code with tests. Otherwise any new requirements will take tramendous amount of time for QA.
From another point of view. Test writing is very time cosuming process, that is competly oposite from the agile developing target.
While a code should be as much as possible (but without obssession) fine grained, that allows you to make your code very flexible, 
a tests should treat code as black box and cover as bigger units as possible (again without obssession). 

The problem starts to became crucial, when you already have working code covered by tests and you get new requirements that need from you to change architecture of app.

There are 2 common approachs that I see in my practice:

1. Rewrite all tests to support new architecture.<br/>
It needs a lot of time.
2. Skip tests that do not fit new architecture.<br/>
you are lucky if you able to finish this refactoring. But next one will not be able without tests.

I would like to present you another approach on small artificial task. I try to keep it simple, but with main components existed in all application.

Lets start.

## Requirements
We need to get user info from Web resource as json string, capitalize first letter of user name and save info in text file.

## Step 0. Code.
Here is quite simple implementation.

```python
def save_new_user():
    # input
    body = request.urlopen(url=URL).read().decode('utf-8')
    user_data = json.loads(body)

    # transformation
    user_data['username'] = user_data['username'].capitalize()

    # output
    path = os.path.join('db', 'users.txt')
    with open(path, 'a') as f:
        f.write('"{}", "{}"\n'.format(
            user_data['username'], user_data['email'])
        )

    return True
```
Yes. TDD requires to write tests before code. But the article is not about TDD and TDD is not aways good :)


## Step 1. Manual Testing. 
Branch: [S1_manual_testing](https://github.com/perses76/agile-testing/tree/S1_manual_testing).

Here is our first test ([source](https://github.com/perses76/agile-testing/blob/S1_manual_testing/tests.py)):
```python
def test_save_new_user():
    result = save_new_user()
    assert result is True
```

We just run our tests: `python tests.py`.
Advatages: You dont spend time for test writing.
Disadvanges: Run all tests manually takes a lot of time. You need to compare result with some expected data (usually saved in doc). There is no test environment or data, we work with real data on prod environment

A lot of developer uses manual tests, but never admit or consider it as  abad practice. I beleive that Manual testing has rights to exists, 
while developers clearly understand its advatages and limitation.
As example of appropiate use of manual testing, think about a one-time small script. You dont want to spend most of your time to write test. 


## Step 2. First TestCase
Branch: [S1_manual_testing](https://github.com/perses76/agile-testing/tree/S2_first_testcase).

Here our  first test case: ([source](https://github.com/perses76/agile-testing/blob/S2_first_testcase/tests.py))

The standard unittes.mock library is used to mock http requests and open file.

I hope no more comments needed about this step as it is quite standard way to write tests.

## Step 3 add exeption testing
Branch: [S3_exception_test](tree/S3_exception_test)

We add second test method to test if our code handle an invalid input.

Test looks like this[full source](blob/S3_exception_test/tests.py):
```python
@mock.patch('user_api.open', name='user_api_open', create=True)
@mock.patch('user_api.request')
def test_invalid_url_response_exception(self, request_mock, open_mock):
    request_mock.urlopen.return_value.read.return_value = b'Invalid string'
    with self.assertRaises(ValueError):
        save_new_user()
```

## Step 4 Test refactoring
Branch: [S4_refactoring](tree/S4_refactoring)

The code works fine and our tests check it. There is one small (may be not so small) problem: The test code is not extandable. Before we continue to add more test cases, we need to refactor our test code and make it more flexible for future changes. 

Here is what we do:
 1. move mock intitalization to setUp and tearDown methods.
 2. Create asserts and input data initialization methods
 3. Use same test data (simple type as string) for asserts and input data initialization

Test case looks like this now [full source](blob/S4_refactoring/tests.py):
```python
class SaveNewUserTestCase(unittest.TestCase):
    def setUp(self):
        # Define, intialize and start mocks
        ...

    def tearDown(self):
        # stop mocks
        ...

    def set_read_data(self, username='test user', email='test@test.com', raw=None):
        # assign input test data to mock
        ...

    def assert_saved_data(self, username='Test user', email='test@test.com'):
        # assert result data with expected data
        ...

    def check_if_data_was_readed(self):
        # assert if data was readed from URL
        ...

    def call_target(self):
        # perfrom tested code
        ...

    def test_success(self):
        self.set_read_data('john', 'john@test.com')
        self.call_target()
        self.assert_saved_data('John', 'john@test.com')

    def test_invalid_url_response_exception(self):
        self.set_read_data(raw=b'Invalid string')
        with self.assertRaises(ValueError):
            self.call_target()
```

## Step 5
Branch: [S5_add_email_modification_rules](tree/S5_add_email_modification_rules)


Lets assume that the client wants more changes and we get list with new requirements:

 1. Change email from format <first_name>.<last_Name>@enterprise.com to <F>.<last_name>@enterprise.com, where <F> - is first letter of <first_letter>
 2. Modify email domain from obsolete.com to "active.com"
 
 Here is modification in the code to meet the requirements above:
 ```python
address, domain = user_data['email'].split('@')
if domain == 'enterprise.com':
    first_name, last_name = address.split('.')
    user_data['email'] = '{}.{}@{}'.format(first_name[0].capitalize(), last_name, domain)

if domain == 'obsolete.com':
    user_data['email'] = '{}@{}'.format(address, 'active.com')
 ```

And here is 2 new tests methods [full source](blob/S5_add_email_modification_rules/tests.py):
```python
def test_enterprise_domain_modification(self):
    self.set_read_data(email='john.smith@enterprise.com')
    self.call_target()
    self.assert_saved_data(email='J.smith@enterprise.com')

def test_obsolete_domain_modification(self):
    self.set_read_data(email='test@obsolete.com')
    self.call_target()
    self.assert_saved_data(email='test@active.com')
```

As you see, new test methods are short and clear because of the refactoring in Step 4.

## Step 6 Code refactoring
Branch: [S6_extract_modify_email_method](tree/S6_extract_modify_email_method)


The customer already asked us about 2 modification in email address and we expect a lot of requiests like this.
So we decided to move email modification logic in the separate function in order to make our future changes more easy.

The function looks like this now:
```python
def modify_email(email):
    address, domain = email.split('@')
    if domain == 'enterprise.com':
        first_name, last_name = address.split('.')
        return '{}.{}@{}'.format(first_name[0].capitalize(), last_name, domain)

    if domain == 'obsolete.com':
        return '{}@{}'.format(address, 'active.com')

    return email
```


And we change also our tests accoring to changes in code.

We split our TestCase class in 3:
 1. SaveNewUserBase - Abstract TestCase class to provide common methods and setup enviroment for tests.
 2. SaveNewUserTestCase - inherited from SaveNewUserBase and tests user creation and invalid input data handling.
 3. ModifyEmailTestCase - inherted from SaveNewUserBase and tests email modification ruls.

[full source](blob/S6_extract_modify_email_method/tests.py)

## Step 7 Test shared function
Branch: [S7_isolate_tests_for_modify_email_method](tree/S7_isolate_tests_for_modify_email_method)

And lets assume that modify_email function is so good that we want to use it in other part of our application.

In this case modify_email does not depend only from save_new_user and we need to test it separatly, but also as part  of save_new_user scenario in order to be sure that it is called.

New test for modify_email function looks like this [full source](blob/S6_extract_modify_email_method/tests.py)


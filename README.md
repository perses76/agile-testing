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
Yes. TDD requires to write tests before code. But first the article is not about TDD and second TDD is not aways good :)


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
Disadvanges: You spend time for testing. You have manually to check if text file contains correct data. Another backdraw is you dont have test data, you have to work with real.

A lot of developer uses manual tests, but never admit it or consider bad practice. I beleive that Manual testing has rights to exists, 
while developers clearly understand its advatages and limitation.
As example of appropiate use of manual testing, think about one time small script. You dont want to spend most of your time to write test. 


## Step 2. First TestCase
Branch: [S1_manual_testing](https://github.com/perses76/agile-testing/tree/S2_first_testcase).

Here our  first test case: ([source](https://github.com/perses76/agile-testing/blob/S2_first_testcase/tests.py))

The standard unittes.mock library is used to mock http requests and open file.

I hope no more comments needed about this step as it is quite standard way to write tests.

## Step 3 add exeption testing

## Step 4 Test refactoring

1. move mock intitalization to setUp and tearDown methods.
2. Create asserts and input data initialization methods
3. Use same test data (simple type as string) for asserts and input data initialization

## Step 5

### 5.1
Change email from format <first_name>.<last_Name>@enterprise.com to <F>.<last_name>@enterprise.com, where <F> - is first letter of <first_letter>
Show tha now we can write tests very easy

### 5.2
Modify email domain from obsolete.com to "active.com"
Show that logic becomes more complecated and we start to think about extract new function to filter e-mails.

## Step 6
Refactoring.
We create new function def modify_user(user) and new TestCase: ModifyUserTestCase for modify_user 
We want to use common mocks and common input data and common output checkers.

## Step 7
modiy_user is shared function and called from another module. 
We modify ModifyUserTestCase to completly isolated from SaveNewUserTestCase and test that we call modify_user with correct arguments from save_new_user  and from new function in other module.

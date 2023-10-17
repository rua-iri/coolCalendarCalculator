

# constants to be returned to the user

startHtml = """
Hello, {username}
I'm {botname}
I can do some fun stuff

Type /help to find out more!
"""


helpHtml = r"""
Here are the functions I'm currently capable of performing:

/help - The command you've just run

/diff - Get the difference between two dates

/onday - Get a notable event that has occurred on this day
"""


diffHtml = """
Okay {user},

Get number of days between today and another date

Enter your chosen date(s) (format dd/mm/yyyy)

If only one date is given then the difference will be calculated from today

"""


singleDateDiff = """
There are
{dayDiff}
days between today and your date
"""


dualDateDiff = """
There are
{dayDiff}
days between {dateOne} and {dateTwo}
"""


errorDateDiffNumArgs = """
*Error*: Please enter 1-2 dates separated by a space
"""


errorDateDiffValueError = """
*Error*: Please enter your date(s) in the format dd/mm/yyyy
"""


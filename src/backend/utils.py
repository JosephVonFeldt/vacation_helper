from datetime import date
def days_until_friday():
    ans = (4 - date.today().weekday()) % 7
    if ans == 0:
        ans = 7
    return ans
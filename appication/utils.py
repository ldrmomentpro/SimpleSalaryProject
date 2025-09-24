from datetime import date

def calc_age(birth_date: date) -> int:
    if not birth_date:
        return 0

    today = date.today()

    years = today.year - birth_date.year

    if (today.month, today.day) < (birth_date.month, birth_date.day):
        years -= 1
    return years
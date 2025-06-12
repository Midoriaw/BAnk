import random
import enum
from datetime import datetime, date

def generate_card_number(length=16):
    return "".join(str(random.randint(0, 9 )) for _ in range(length))



def calculate_interes_by_term(create_at: datetime, due_date: date) -> float:
    days = (due_date - create_at.date()).days
    if days <= 30:
        return 3.0  # до месяца — 3%

    elif days <= 90:
        return  5.0 #до 3 месяцев — 5%

    elif days <= 180:
        return 7.5 # до полугода — 7.5%

    else:
        return 10.0 # больше полугода — 10%




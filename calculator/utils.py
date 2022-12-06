from math import ceil


def get_payment(price: int, term: int, rate: float, deposit: int) -> int:
    month_rate = rate / 12 / 100
    alltime_rate = (1 + month_rate) ** (term * 12)
    annuity = month_rate * alltime_rate/(alltime_rate - 1)
    return ceil((price - price*(deposit/100)) * annuity)


def append_payment(offers, price, term, deposit, order):
    price = int(price)
    term = int(term)
    deposit = int(deposit)
    for offer in offers:
        try:
            offer['payment'] = get_payment(price, term, offer['rate_min'], deposit)
        except ValueError as e:
            pass
    if 'price' == order or '-price' == order:
        reverse = False
        if order == '-price':
            reverse = True
        offers.sort(key=lambda offer: offer['payment'], reversed=reverse)

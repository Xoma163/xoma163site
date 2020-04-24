from apps.API_VK.APIs.cbr import get_exchange_rates
from apps.API_VK.command.CommonCommand import CommonCommand


class ExchangeRates(CommonCommand):
    def __init__(self):
        names = ["курс"]
        help_text = "Курс - курс валют"
        super().__init__(names, help_text)

    def start(self):
        _filters_list = ["USD", "EUR"]

        ex_rates = get_exchange_rates(_filters_list)

        msg = "Курс валют:\n"
        for ex_rate in ex_rates:
            ex_rates[ex_rate] = round(float(ex_rates[ex_rate].replace(',', '.')), 2)
            msg += f"{ex_rate} - {ex_rates[ex_rate]} руб.\n"
        return msg

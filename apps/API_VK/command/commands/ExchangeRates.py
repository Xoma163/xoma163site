from apps.API_VK.APIs.cbr import get_exchange_rates
from apps.API_VK.command.CommonCommand import CommonCommand


class ExchangeRates(CommonCommand):

    @staticmethod
    def get_rate_for_key(ex_rates, key, value):
        ex_rate = ex_rates[key]
        total_value = round(value * ex_rate, 2)
        msg = "Перевод в рубли:\n"
        msg += f"{total_value} руб."
        return msg

    def __init__(self):
        names = ["курс"]
        help_text = "Курс - курс валют"
        detail_help_text = "Курс - курс валют\n" \
                           "Курс (количество) (валюта) - перевод в другие валюты конкретное количество валюты"
        super().__init__(names, help_text, detail_help_text)

    def start(self):
        _filters_list = ["USD", "EUR", "NOK", "JPY", "GBP", "KZT", "UAH"]

        ex_rates = get_exchange_rates(_filters_list)

        if self.vk_event.args:
            self.vk_event.args[0] = self.vk_event.args[0].replace('к', '000').replace('k', '000')
            self.check_args(2)
            self.float_args = [0]
            self.parse_args('float')

            value = self.vk_event.args[0]
            if any(ext in self.vk_event.args[1].lower() for ext in ['rub', "руб"]):
                msg = "Перевод в другие валюты:\n"
                for ex_rate in ex_rates:
                    total_value = round(value / ex_rates[ex_rate], 2)
                    msg += f"{total_value} {ex_rate}\n"
            elif any(ext in self.vk_event.args[1].lower() for ext in ['eur', "евро", "€"]):
                msg = self.get_rate_for_key(ex_rates, "EUR", value)
            elif any(ext in self.vk_event.args[1].lower() for ext in ['usd', "доллар", "$"]):
                msg = self.get_rate_for_key(ex_rates, "USD", value)
            elif any(ext in self.vk_event.args[1].lower() for ext in ['jpy', "йен"]):
                msg = self.get_rate_for_key(ex_rates, "JPY", value)
            elif any(ext in self.vk_event.args[1].lower() for ext in ['gbp', "фунт"]):
                msg = self.get_rate_for_key(ex_rates, "GBP", value)
            elif any(ext in self.vk_event.args[1].lower() for ext in ['kzt', "тенг"]):
                msg = self.get_rate_for_key(ex_rates, "KZT", value)
            elif any(ext in self.vk_event.args[1].lower() for ext in ['uah', "гривн"]):
                msg = self.get_rate_for_key(ex_rates, "UAH", value)
            else:
                return "Пока не знаю как переводить из этой валюты"

        else:
            msg = "Курс валют:\n"
            for ex_rate in ex_rates:
                ex_rates[ex_rate] = round(ex_rates[ex_rate], 2)
                msg += f"{ex_rate} - {ex_rates[ex_rate]} руб.\n"
        return msg

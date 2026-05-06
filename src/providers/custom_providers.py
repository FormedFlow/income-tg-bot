from faker.providers.emoji import Provider as BaseEmojiProvider
from faker.providers.currency import Provider as BaseCurrencyProvider
import random


class EmojiProvider(BaseEmojiProvider):
    fallback_emojis = ['🍔', '🚇', '🏠', '💊', '👕', '🎮', '📚', '💼', '🎁', '💰']
    def emoji_with_max_len(self, max_len):
        new_emoji = self.emoji()
        return new_emoji if len(new_emoji) <= max_len else random.choice(self.fallback_emojis)
    

class CurrencyProvider(BaseCurrencyProvider):
    def currency_with_symbol(self):
        currency = self.currency()
        symbol = self.currency_symbol(currency[0])
        currency = (currency[1], currency[0], symbol)
        return currency
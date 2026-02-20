from faker.providers.emoji import Provider as BaseEmojiProvider
import random


class EmojiProvider(BaseEmojiProvider):
    fallback_emojis = ['🍔', '🚇', '🏠', '💊', '👕', '🎮', '📚', '💼', '🎁', '💰']
    def emoji_with_max_len(self, max_len):
        new_emoji = self.emoji()
        return new_emoji if len(new_emoji) <= max_len else random.choice(self.fallback_emojis)
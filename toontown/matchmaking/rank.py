from enum import Enum
from toontown.archipelago.util.global_text_properties import get_raw_formatted_string, get_gradient_formatted_string
from toontown.archipelago.util.global_text_properties import MinimalJsonMessagePart as Component

# How much SR does a player need to "promote" from one division to another? e.g. Diamond 1 -> Diamond 2
SKILL_RATING_PER_DIVISION = 100

# How many divisions per tier do we want? e.g. 3 -> Diamond I-III
DIVISIONS_PER_TIER = 3


class RankTier(Enum):
    IRON = "Iron"
    BRONZE = "Bronze"
    SILVER = "Silver"
    GOLD = "Gold"
    PLATINUM = "Platinum"
    DIAMOND = "Diamond"
    INVESTOR = "Investor"
    EXECUTIVE = "Executive"
    PRESIDENT = "President"


class Rank:

    def __init__(self, tier: RankTier, division: int):
        self.tier: RankTier = tier
        self.division: int = division

    def __roman(self) -> str:

        if self.division <= 0:
            return ''

        if 3 >= self.division >= 1:
            return 'I' * self.division

        if self.division == 4:
            return 'IV'

        if self.division == 5:
            return 'V'

        return str(self.division)

    def color(self) -> str:

        match self.tier:
            case RankTier.IRON:
                return 'gunmetal'
            case RankTier.BRONZE:
                return 'brown'
            case RankTier.SILVER:
                return 'silver'
            case RankTier.GOLD:
                return 'gold'
            case RankTier.PLATINUM:
                return 'light_blue'
            case RankTier.DIAMOND:
                return 'pink'
            case RankTier.INVESTOR:
                return 'green_gradient'
            case RankTier.EXECUTIVE:
                return 'deep_red_gradient'
            case RankTier.PRESIDENT:
                return 'purple_gradient'

        return 'black'

    def colored(self) -> str:
        """
        Returns a colored formatting of this rank. Looks the exact same as the raw string representation, but has color.
        """
        color = self.color()
        rank_text = self.__str__()
        
        # Check if this is a gradient color
        if color.endswith('_gradient'):
            return get_gradient_formatted_string(rank_text, color)
        else:
            return get_raw_formatted_string([
                Component(message=rank_text, color=color)
            ])

    def colored_with_sr(self, sr: int) -> str:
        """
        Returns a colored formatting of this rank, including the SR number.
         Looks the exact same as the raw string representation, but has color.
        """
        color = self.color()
        rank_text = self.__str__()
        
        # Check if this is a gradient color
        if color.endswith('_gradient'):
            # For gradient ranks, apply gradient to rank text and regular color to SR
            gradient_rank = get_gradient_formatted_string(rank_text, color)
            sr_part = get_raw_formatted_string([Component(message=f" ({sr})", color='gunmetal')])
            return gradient_rank + sr_part
        else:
            return get_raw_formatted_string([
                Component(message=rank_text, color=color),
                Component(message=f" ({sr})", color='gunmetal')
            ])

    def __str__(self):
        return f"{self.tier.value} {self.__roman()}".strip()

    def __repr__(self):
        return self.__str__()

    @classmethod
    def get_from_skill_rating(cls, skill_rating: int):
        """
        Computes a rank that matches the skill rating.
        This is a utility method that makes it very easy to determine someone's rank just off of a simple number.
        It should also be noted that you need to pass in a player's skill rating, and not their "mu value" or anything
        provided by openskill. Our "skill rating" value is something we track separately from mu, we just use openskill
        rating values to determine the +/- skill rating to adjust after every match.
        :param skill_rating: The skill rating. A value of 150 will return Iron 2, and 350 will return Bronze 1.

        :return: The rank that represents this skill rating.
        """

        if skill_rating < 0:
            return cls(RankTier.IRON, 0)

        if skill_rating < 100:
            return cls(RankTier.BRONZE, 1)
        if skill_rating < 200:
            return cls(RankTier.BRONZE, 2)
        if skill_rating < 300:
            return cls(RankTier.BRONZE, 3)

        if skill_rating < 400:
            return cls(RankTier.SILVER, 1)
        if skill_rating < 500:
            return cls(RankTier.SILVER, 2)
        if skill_rating < 600:
            return cls(RankTier.SILVER, 3)

        if skill_rating < 700:
            return cls(RankTier.GOLD, 1)
        if skill_rating < 800:
            return cls(RankTier.GOLD, 2)
        if skill_rating < 900:
            return cls(RankTier.GOLD, 3)

        if skill_rating < 1000:
            return cls(RankTier.PLATINUM, 1)
        if skill_rating < 1100:
            return cls(RankTier.PLATINUM, 2)
        if skill_rating < 1200:
            return cls(RankTier.PLATINUM, 3)

        if skill_rating < 1300:
            return cls(RankTier.DIAMOND, 1)
        if skill_rating < 1400:
            return cls(RankTier.DIAMOND, 2)
        if skill_rating < 1500:
            return cls(RankTier.DIAMOND, 3)

        if skill_rating < 1600:
            return cls(RankTier.INVESTOR, 1)
        if skill_rating < 1700:
            return cls(RankTier.INVESTOR, 2)
        if skill_rating < 1800:
            return cls(RankTier.INVESTOR, 3)
            
        if skill_rating < 1900:
            return cls(RankTier.EXECUTIVE, 1)
        if skill_rating < 2000:
            return cls(RankTier.EXECUTIVE, 2)
        if skill_rating < 2100:
            return cls(RankTier.EXECUTIVE, 3)
        
        return cls(RankTier.PRESIDENT, 0)

    def __eq__(self, other):
        return self.division == other.division and self.tier.value == other.tier.value
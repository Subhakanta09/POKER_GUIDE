from pypokerengine.utils.card_utils import Card
class StrategicBot(CountingBot):

    def __init__(self):
        super().__init__("StrategicBot")

    def declare_action(self, valid_actions, hole_card, round_state):
        # Get community cards
        community_cards = round_state["community_card"]

        # Evaluate hand strength based on hand ranking
        hand_strength = self.evaluate_hand_strength(hole_card, community_cards)

        # Get pot size and bet amount
        pot_size = round_state["pot"]["main"]["amount"]
        bet_amount = self.get_bet_amount(valid_actions)

        # Decision logic based on hand strength and pot odds
        if hand_strength >= 0.8:  # Strong hand
            action = self.aggressive_action(valid_actions, pot_size, bet_amount)
        elif hand_strength >= 0.5:  # Moderate hand
            action = self.balanced_action(valid_actions, pot_size, bet_amount)
        else:  # Weak hand
            action = self.conservative_action(valid_actions, pot_size, bet_amount)

        # Extract amount (handle raise min-max structure)
        amount = action.get("amount")
        if isinstance(amount, dict):
            amount = amount.get("min", 0)  # Get min raise amount

        if amount is None or amount < 0:
            amount = 0  # Default to 0 if amount is invalid or negative


        # Record game history
        self.game_history.append({
            "round_state": round_state,
            "valid_actions": valid_actions,
            "action_taken": (action, amount)
        })

        return action["action"], int(amount)


    def evaluate_hand_strength(self, hole_card, community_cards):
        # Simple hand evaluation based on card ranks
        hand_ranks = [Card.from_str(card).rank for card in hole_card + community_cards]
        hand_strength = sum(hand_ranks) / (len(hole_card) + len(community_cards))
        return hand_strength

    def aggressive_action(self, valid_actions, pot_size, bet_amount):
        # Raise if possible, otherwise call
        raise_action = next((a for a in valid_actions if a["action"] == "raise"), None)
        if raise_action:
            return raise_action
        else:
            return next((a for a in valid_actions if a["action"] == "call"), None)


    def balanced_action(self, valid_actions, pot_size, bet_amount):
        # Call if bet is reasonable, otherwise fold
        call_action = next((a for a in valid_actions if a["action"] == "call"), None)
        if call_action and bet_amount <= pot_size / 2:
            return call_action
        else:
            return next((a for a in valid_actions if a["action"] == "fold"), None)


    def conservative_action(self, valid_actions, pot_size, bet_amount):
        # Fold if bet is significant, otherwise call
        call_action = next((a for a in valid_actions if a["action"] == "call"), None)
        if call_action and bet_amount <= pot_size / 4:
            return call_action
        else:
            return next((a for a in valid_actions if a["action"] == "fold"), None)


    def get_bet_amount(self, valid_actions):
        # Get the current bet amount from valid actions
        raise_actions = [a for a in valid_actions if a["action"] == "raise"]
        if raise_actions:
            return raise_actions[0]['amount']['min']
        else:
            return 0

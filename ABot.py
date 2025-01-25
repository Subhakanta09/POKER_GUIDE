from bots.base import CountingBot
class ABot(CountingBot):
    def declare_action(self, valid_actions, hole_card, round_state):

        raise_action = next(
            (action for action in valid_actions if action["action"] == "raise"),
            None
        )
        if raise_action:
                min_raise = raise_action["amount"]["min"]
                max_raise = raise_action["amount"]["max"]
                raise_amount = (min_raise + max_raise) / 2
                action = {"action": "raise", "amount": raise_amount}

        if action is None:
            action = next(
                (action for action in valid_actions if action["action"] == "call"),
                next((action for action in valid_actions if action["action"] == "fold"), None)
            )

        amount = action.get("amount")
        if isinstance(amount, dict):
            amount = amount.get("max", 0)  # raise as much as possible
        if amount is None or amount < 0:
            amount = 0  # Default to 0 if amount is invalid or negative

        self.game_history.append({
            "round_state": round_state,
            "valid_actions": valid_actions,
            "action_taken": (action, amount)
        })

        return action["action"], int(amount)


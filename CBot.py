# always call bot
class CBot(CountingBot):
    def __init__(self):
      super().__init__("CBot")
    def declare_action(self, valid_actions, hole_card, round_state):
      action = next(
          action for action in valid_actions if action["action"] == "call")
      amount = action.get("amount")
      if isinstance(amount, dict):
          amount = amount.get("min", 0)

      self.game_history.append({
                  "round_state": round_state,
                  "valid_actions": valid_actions,
                  "action_taken": (action, amount)
              })

      return action["action"], int(amount or 0)

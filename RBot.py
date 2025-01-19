# Random bot
class RBot(CountingBot):
    def __init__(self):
      super().__init__("Pbot")
    def declare_action(self, valid_actions, hole_card, round_state):
      import random
      rand = random.random()
      if rand < 0.5:
          action = next(
              action for action in valid_actions if action["action"] == "call")
      elif rand < 0.8:
          action = next(
              action for action in valid_actions if action["action"] == "raise")
      else:
          action = next(
              action for action in valid_actions if action["action"] == "fold")
      amount = action.get("amount")
      if isinstance(amount, dict):
          amount = amount.get("min", 0)

      self.game_history.append({
            "round_state": round_state,
            "valid_actions": valid_actions,
            "action_taken": (action, amount)
        })

      return action["action"], int(amount or 0)

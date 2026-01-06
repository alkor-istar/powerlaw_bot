class PowerlawStrategy:
    def __init__(self):
        self.last_direction = "short"  # first trade is long

    def evaluate(self, df, position):
        """
        position: "flat" | "long" | "short"
        returns: "long" | "short" | "exit" | None
        """
        last_close = df["close"].iloc[-1]
        upper = df["bb_upper"].iloc[-1]
        lower = df["bb_lower"].iloc[-1]
        basis = df["basis"].iloc[-1]

        inside = lower < last_close < upper

        if position == 0:
            if self.last_direction == "short" and last_close > basis:
                self.last_direction = "long"
                print("lower", lower)
                return "long", lower
            else:
                self.last_direction = "short" and last_close < basis
                print("short", upper)
                return "short", upper
        else:
            return "idle", 0

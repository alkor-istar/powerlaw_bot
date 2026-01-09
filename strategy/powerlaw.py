from indicators.bollinger import bollinger_bands


class PowerlawStrategy:
    def __init__(self, logger):
        self.initial_limit = None
        self.logger = logger

    def evaluate(self, df, position):
        last_close = df["close"].iloc[-1]
        upper = df["bb_upper"].iloc[-1]
        lower = df["bb_lower"].iloc[-1]
        basis = df["basis"].iloc[-1]

        inside = lower < last_close < upper

        if position == 0:
            if last_close > basis:
                self.last_direction = "long"
                self.initial_limit = upper
                return "long", basis
            else:
                last_close < basis
                self.initial_limit = lower
                return "short", basis
        elif position > 0:
            if last_close > self.initial_limit:
                return "movesl", basis
        else:
            if not self.initial_limit:
                self.logger.log("Account already trading", level=logging.ERROR)
                return "idle", basis
            if position < 0 and last_close < self.initial_limit:
                return "movesl", basis
            elif position > 0 and last_close > self.initial_limit:
                return "movesl", basis
            else:
                return "idle", basis

        return "idle", basis

    def trade(self, exchange, symbol, timeframe, candle_count):
        df = exchange.get_candles(symbol, timeframe, candle_count)
        df = bollinger_bands(df)

        position = exchange.get_position_size(symbol)
        signal, stoploss = self.evaluate(df, position)

        if signal == "long":
            self.logger.log("Enter LONG")
            exchange.long(symbol, 100)
            self.sl_order_id = exchange.set_stop_loss(
                symbol=symbol, side="Sell", price=stoploss, orderQty=100
            )
        elif signal == "short":
            self.logger.log("Enter SHORT")
            exchange.short(symbol, 100)
            self.sl_order_id = exchange.set_stop_loss(
                symbol=symbol, side="Buy", price=stoploss, orderQty=100
            )
        elif signal == "movesl":
            self.logger.log("Move SL")
            exchange.amend_stop_loss(self.sl_order_id, stoploss, 100)
        else:
            self.logger.log("Nothing to do")

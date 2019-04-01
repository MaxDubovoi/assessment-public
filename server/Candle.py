class Candle:
    max_price: float
    min_price: float
    open_price: float
    close_price: float

    def __init__(self, _max, _min, _open, _close):
        self.max_price = _max
        self.min_price = _min
        self.open_price = _open
        self.close_price = _close

class InventoryError(Exception):
    pass

class InventoryItem:
    def __init__(self, name, stocks):
        if not isinstance(name, str):
            raise InventoryError('Item name must be a string')
        
        if stocks < 0:
            raise InventoryError('Negative initial stock')
        self.stocks = stocks
        self.name = name

    def add_stock(self, n):
        if n <= 0:
            raise InventoryError('Stock adjustment must be positive')
        self.stocks += n
        return self.stocks

    def remove_stock(self, n):
        if n <= 0:
            raise InventoryError('Stock adjustment must be positive')
        if n > self.stocks:
            raise InventoryError('Insufficient stock')
        self.stocks -= n
        return self.stocks

    def get_stock(self):
        return self.stocks
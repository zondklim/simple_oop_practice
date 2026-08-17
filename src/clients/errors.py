

class AccountErrors(Exception):
    """Base for all account-related errors."""


class AccountFrozenError(AccountErrors):
    def __init__(self, ):
        super().__init__(
            "Your account status is Frozen. You can't perform operations. Please contact support."
        )


class AccountClosedError(AccountErrors):
    def __init__(self, ):
        super().__init__(
            "Your account status is Closed. You can't perform operations. Please create a new account."
        )

    
class InvalidOperationError(AccountErrors):
    def __init__(self, operation: str):
    
        super().__init__(
            f"Sorry, operation {operation} is unsupported. Please choose another one."
        ) 
    
    
class InsufficientFundsError(AccountErrors):
    def __init__(
        self, 
        balance: float|int,
        amount: float|int
    ):
        super().__init__(
            f"Cannot withdraw {amount}: balance is only {balance}"
        )
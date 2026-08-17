import hashlib
from datetime import datetime 

from .base_classes import AbstractAccount, Currency, AccountStatus
from .customer import Customer
from .errors import (
    AccountFrozenError,
    AccountClosedError,
    InvalidOperationError,
    InsufficientFundsError
)

class BankAccount(AbstractAccount):
    __name__ = 'Standard Bank Account'
    
    def __init__(
        self,
        owner_info: Customer,
        currency: Currency,
    ):
        super().__init__(owner_info)
        
        self.currency = currency
        self.operations_is_banned = False
        
        self._validate_inputs()
        
        if not self.card_number:
            self._generate_id
    
    def __str__(self):
        return self.get_account_info()
    
    def deposit(self, amount: float|int):
        
        self._validate_operation('deposit', amount)
        self._balance += amount
        
    def withdraw(self, amount: float|int):
        
        self._validate_operation('withdraw', amount)
        if self._balance < amount:
            raise InsufficientFundsError(self._balance, amount)
        
        self._balance -= amount
    
    def get_account_info(self, ) -> str:
        return f"Account is {BankAccount.__name__}\
                \nAccount Owner Name: {self.owner_info.name} \
                \nAccount Owner Surname: {self.owner_info.surname}\
                \nCard Number is: **** **** **** {self.card_number[-4:]} \
                \nAccount Status is: {self.account_status}\
                \nAccount Balance: {self._balance} {self.currency}"
    
    def update_account_status(self, new_status: AccountStatus):
        
        self.account_status = new_status
        self.check_account_status()
        
        if self.account_status == AccountStatus.FROZEN:
            self.operations_is_banned = True
        elif self.account_status == AccountStatus.CLOSED:
            self.operations_is_banned = True   
        else:
            self.operations_is_banned = False
        
    def check_account_status(self, ):
        
        if not isinstance(self.account_status, AccountStatus):
            self.operations_is_banned = True
            raise TypeError (
                "account_status must be an instance of AccountStatus.\
                \nYour account has been blocked until you change the status to a correct instance.\
                \nUse the update_account_status method to change your status."
            )
        else:
            print(f"Your status is {self.account_status}")
    
    def _generate_id(self, ) -> None:
        """Creating id from customer params and time.now as salt"""
        info_string = self.owner_info.concat_to_str()
        curr_dt = datetime.now().strftime("%Y%m%d%H%M")
        
        self.id = hashlib.md5((info_string + curr_dt).encode()).hexdigest()
        
    def _validate_inputs(self, ):
        if not isinstance(self.owner_info, Customer):
            raise TypeError('Customer info must be an instance of Customer.')

        if not self.owner_info.name or not isinstance(self.owner_info.name, str):
            raise ValueError('Customer name must be a string with length greater than 0.')

        if not self.owner_info.surname or not isinstance(self.owner_info.surname, str):
            raise ValueError('Customer surname must be a string with length greater than 0.')

        if not self.owner_info.surname or not isinstance(self.owner_info.surname, str):
            raise ValueError('Customer date_of_birth must be a string with length equal to 10.')

        if not isinstance(self.currency, Currency):
            raise TypeError('Account currency must be an instance of Currency.')
    
    def _validate_operation(self, operation_name: str, amount: float|int):
            
        self.check_account_status()
                
        if self.account_status == AccountStatus.FROZEN:
            raise AccountFrozenError
        elif self.account_status == AccountStatus.CLOSED:
            raise AccountClosedError   
        elif self.operations_is_banned:
                raise InvalidOperationError(f'{operation_name}')

        if not isinstance(amount, (float, int)):
            raise ValueError(f'Amount for {operation_name} must be a float or integer.')
        elif amount <= 0:
            raise InvalidOperationError(f'{operation_name} for {amount}.') 
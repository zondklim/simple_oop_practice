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
    
    def deposit(self, amount: float|int):
        
        self._validate_operation('deposit', amount)
        self.deposit += amount
        
    def withdraw(self, amount: float|int):
        
        self._validate_operation('withdraw', amount)
        if self._balance < amount:
            raise InsufficientFundsError(self._balance, amount)
        
        self._balance -= amount
    
    def get_account_info(self, ):
        pass
    
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
                "account_status must be instance of AccountStatus.\
                \nYour account have been blocked until changes status to correct instance.\
                \n Use method update_account_status for change your status."
            )
        else:
            print(f"Your status is {self.account_status}")
    
    def _generate_id(self, ) -> None:
        """Creating id from customer params and time.now as solt"""
        info_string = self.owner_info.concat_to_str()
        curr_dt = datetime.now().strftime("%Y%m%d%H%M")
        
        self.id = hashlib.md5((info_string + curr_dt).encode()).hexdigest()
        
    def _validate_inputs(self, ):
        if not isinstance(self.owner_info, Customer):
            raise TypeError('Costomer inf must be instance of Customer.')
        
        if not self.owner_info.name or isinstance(self.owner_info.name, str):
            raise ValueError('Customer name must be string lengh more than 0.')
        
        if not self.owner_info.surname or isinstance(self.owner_info.surname, str):
            raise ValueError('Customer surname must be string lengh more than 0.')
        
        if not self.owner_info.surname or isinstance(self.owner_info.surname, str):
            raise ValueError('Customer date_of_birth must be string lengh equal 10.')
        
        if not isinstance(self.currency, Currency):
            raise TypeError('Account currency must be instance of Currency.')
    
    def _validate_operation(self, operation_name: str, amount: float|int):
            
        self.check_account_status()
                
        if self.operations_is_banned:
            raise InvalidOperationError('{operation_name}')
        elif self.account_status == AccountStatus.FROZEN:
            raise AccountFrozenError
        elif self.account_status == AccountStatus.CLOSED:
            raise AccountClosedError   

        if not isinstance(amount, (float, int)):
            raise ValueError('Amount for {operation_name} must be float or intager.')
        elif amount <= 0:
            raise InvalidOperationError(f'{operation_name} for {amount}.') 
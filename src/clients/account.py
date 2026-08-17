import hashlib
from datetime import datetime 

from .base_classes import AbstractAccount, Currency, AccountStatus
from .customer import Customer

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
    
    def deposit(self, amount: float):
        self._balance += amount
    
    def withdraw(self, amount: float):
        self._balance -= amount
    
    def get_account_info(self, ):
        pass
    
    def _generate_id(self, ) -> None:
        """Creating id from customer params and time.now as solt"""
        info_string = self.owner_info.concat_to_str()
        curr_dt = datetime.now().strftime("%Y%m%d%H%M")
        
        self.id = hashlib.md5((info_string + curr_dt).encode()).hexdigest()
        
    def _validate_inputs(self, ):
        if not isinstance(self.owner_info, Customer):
            raise TypeError('Costomer inf must be instance of Customer')
        
        if not self.owner_info.name or isinstance(self.owner_info.name, str):
            raise ValueError('Customer name must be string lengh more than 0')
        
        if not self.owner_info.surname or isinstance(self.owner_info.surname, str):
            raise ValueError('Customer surname must be string lengh more than 0')
        
        if not self.owner_info.surname or isinstance(self.owner_info.surname, str):
            raise ValueError('Customer date_of_birth must be string lengh equal 10')
        
        if not isinstance(self.currency, Currency):
            raise TypeError('Account currency must be instance of Currency')
        
    def update_account_status(self, ):
        pass

    def check_account_status(self, ):
        if not isinstance(self.account_status, AccountStatus):
            print("account_status must be instance of AccountStatus.")
            print("Your account have been blocked until changes status to correct instance.")
            print("Use method update_account_status for change your status.")
            
            self.operations_is_banned = True
        
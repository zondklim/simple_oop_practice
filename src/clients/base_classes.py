from abc import ABC, abstractmethod
from enum import Enum, auto

from .customer import Customer

import random


class AccountStatus(Enum):
    ACTIVE = auto()
    FROZEN = auto()
    CLOSED = auto()


class Currency(Enum):
    RUB = auto()
    USD = auto()
    EUR = auto()
    KZT = auto()
    CNY = auto()
    

class AbstractAccount(ABC):
    def __init__(
        self, 
        owner_info: Customer,
    ):
        
        self.owner_info = owner_info
        
        self._generate_card_number()
        self.account_status: AccountStatus = AccountStatus.ACTIVE
        self._balance: float|int = .0
        
    
    @abstractmethod
    def deposit(self, amount: float):
        pass
    
    @abstractmethod
    def withdraw(self, amount: float):
        pass
    
    @abstractmethod
    def get_account_info(self, ):
        pass
    
    def _generate_card_number(self, ):
        """Creating 16 digests card number"""
        self.card_number =  ''.join([str(random.randrange(10)) if i % 5 != 0 else ' ' for i in range(1, 20)])

from dataclasses import dataclass


@dataclass
class Customer:
    name: str
    surname: str 
    date_of_birth: str
    
    def concat_to_str(self, ) -> str:
        return self.name + self.surname + self.date_of_birth

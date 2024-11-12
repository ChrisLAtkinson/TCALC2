import asyncio
from typing import List, Optional
import random
from dataclasses import dataclass, field
from collections import namedtuple

# Using PEP 695's type parameter syntax for generics
Person = namedtuple('Person', ['name', 'age'])

@dataclass
class Employee:
    """A class representing an employee with modern Python features."""
    name: str
    age: int
    skills: List[str] = field(default_factory=list)
    salary: Optional[int] = None

    def greet(self):
        """Greet method for Employee class."""
        return f"Hello, I'm {self.name}, an {self.age} year old employee."

# Async function showcasing the use of async/await with Python 3.12 features
async def fetch_data(id: int) -> dict:
    """Simulates fetching data asynchronously."""
    await asyncio.sleep(random.uniform(0.5, 1.5))  # Simulate network delay
    return {"id": id, "data": f"Data for {id}"}

async def main():
    """Main function to demonstrate async operations with list comprehension."""
    tasks = [fetch_data(i) for i in range(3)]  # List comprehension for task creation
    results = await asyncio.gather(*tasks)
    for result in results:
        print(f"Fetched {result}")

# Python 3.12's improved f-string capabilities
def format_currency(amount: float) -> str:
    """Format numbers as currency using new f-string capabilities."""
    return f"${amount:,.2f}"

# Demonstration of error handling with match-case (PEP 636)
def describe_number(num: int) -> str:
    """Describe a number using pattern matching."""
    match num:
        case 0:
            return "Zero"
        case 1:
            return "One"
        case _ if num > 0:
            return "Positive"
        case _ if num < 0:
            return "Negative"

if __name__ == "__main__":
    # Example usage
    print(Employee("Alice", 30, ["Python", "SQL"]).greet())
    
    # Run the async main function
    asyncio.run(main())
    
    # Currency formatting
    print(format_currency(1234567.89))
    
    # Number description
    print(describe_number(0))
    print(describe_number(1))
    print(describe_number(-5))
    print(describe_number(10))

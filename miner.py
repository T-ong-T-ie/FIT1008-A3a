from __future__ import annotations
from typing import Iterable

from data_structures.array_stack import ArrayStack
from minecraft_block import MinecraftBlock


class Miner:
    """
    A class representing a miner in a mining simulation.
    """

    def __init__(self, name: str) -> None:
        """
        Initializes the miner with a name and an empty inventory.

        Args:
            name (str): The name of the miner.

        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(1)

        Justification:
            Only simple attribute assignment operations are performed, and the time complexity is constant
        """
        self.name = name
        self.inventory = ArrayStack(1000)  # Use a stack structure to facilitate the subsequent return of items in the order in which they were mined

    def mine(self, block: MinecraftBlock) -> None:
        """
        Mines a block and adds the item to the miner's bag.

        Args:
            block (MinecraftBlock): The block to be mined.

        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(1)

        Justification:
            Push operation using stack structure with time complexity of O(1)
        """
        # If the stack is full, you need to create a larger stack
        if self.inventory.is_full():
            new_inventory = ArrayStack(len(self.inventory) * 2)
            # Transfer items from the old inventory to the new inventory in the same order
            temp_stack = ArrayStack(len(self.inventory))
            while not self.inventory.is_empty():
                temp_stack.push(self.inventory.pop())
            while not temp_stack.is_empty():
                new_inventory.push(temp_stack.pop())
            self.inventory = new_inventory

        # Add items from blocks to your inventory
        self.inventory.push(block.item)

    def clear_inventory(self) -> Iterable:
        """
        Clears the miner's inventory and returns what he had in the inventory before the clear.

        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(1)

        Justification:
            Just go back to the reference of the existing stack and create a new one, no need to duplicate the elements
        """
        # Saves a reference to the current inventory
        current_inventory = self.inventory
        # Create a new empty inventory
        self.inventory = ArrayStack(1000)

        # Return the item's iterator
        return InventoryIterator(current_inventory)


class InventoryIterator:
    """A helper class to iterate over items in your inventory in the correct order"""

    def __init__(self, stack):
        self.stack = stack
        self.temp_stack = ArrayStack(len(stack))

        # Invert the original stack so that it is iterated in the correct order
        while not self.stack.is_empty():
            self.temp_stack.push(self.stack.pop())

    def __iter__(self):
        return self

    def __next__(self):
        if self.temp_stack.is_empty():
            raise StopIteration
        return self.temp_stack.pop()
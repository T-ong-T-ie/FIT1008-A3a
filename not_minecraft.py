from __future__ import annotations
from cave_system import CaveSystem
from data_structures import *
from data_structures.array_stack import ArrayStack
from minecraft_block import MinecraftBlock
from minecraft_checklist import MinecraftChecklist
from miner import Miner


class NotMinecraft:
    def __init__(self, cave_system: CaveSystem, checklist: MinecraftChecklist) -> None:
        """
        Initialize the NotMinecraft class, set up the miner, cave system, and manifest.

        Args:
            cave_system: An object that represents a cave system.
            checklist: Represents an object that is a list of miners.

        Complexity:
            Best Case Complexity: TODO
            Worst Case Complexity: TODO

        Justification:
            TODO
        """
        self.miner = Miner("Steve")
        self.cave_system = cave_system
        self.checklist = checklist

    def get_inventory_items(self) -> ArrayList:
        """
        Convert items in a miner's inventory into an indexable ArrayList.

        Returns:
            An ArrayList containing miners' inventory items.
        """
        # Create a temporary stack to store the original items
        temp_stack = ArrayStack(len(self.miner.inventory))

        # Create a list of results
        result = ArrayList(len(self.miner.inventory))

        # Ejects items from the original stack into the temporary stack
        while not self.miner.inventory.is_empty():
            temp_stack.push(self.miner.inventory.pop())

        # Place the items in the temporary stack back to the original stack and add them to the results list at the same time
        while not temp_stack.is_empty():
            item = temp_stack.pop()
            self.miner.inventory.push(item)
            result.append(item)

        return result

    def dfs_explore_cave(self) -> ArrayList[MinecraftBlock]:
        """
        Performs a depth-first search (DFS) to explore the cave system and collect blocks.

        Returns:
            ArrayList[MinecraftBlock]: A list of collected blocks.

        Complexity:
            Not required
        """
        # Create a list to store the discovered blocks
        discovered_blocks = ArrayList(0)

        # Create a collection to keep track of the nodes that have been visited
        visited = ArraySet(100)

        # Define a recursive DFS function
        def dfs(node):
            if node in visited:
                return

            # Mark the current node as accessed
            visited.add(node)

            # Add all the blocks in that node to the discovery list
            for block in node.blocks:
                discovered_blocks.append(block)

            # Recursively access all adjacent nodes
            for neighbour in node.neighbours:
                dfs(neighbour)

        # Start DFS from the entrance node of the cave
        # Use an entry node instead of the root node
        dfs(self.cave_system.entrance)

        return discovered_blocks

    def objective_mining_summary(self, blocks=None, block1=None, block2=None) -> None:
        """
        Given a list of blocks, filter the blocks that should be considered according to scenario 1.

        Args:
            blocks (ArrayList[MinecraftBlock]): The list of blocks to mine.
            block1 (MinecraftBlock): Filtered blocks should have a ratio of value to mining time > block1.
            block2 (MinecraftBlock): Filtered blocks should have a ratio of value to mining time < block2.

        Complexity:
            Best Case Complexity: O(n)
            Worst Case Complexity: O(n)

        Justification:
            The method calls dfs_explore_cave() and objective_mining_filter(), the former with a complexity that is not taken into account, and the latter which has a complexity of O(n). In objective_mining_filter(), all the squares need to be traversed to check their value/hardness ratio, which requires the time complexity of O(n), where n is the length of the list of blocks.
        """
        # If no list of blocks is provided, DFS is performed to explore the cave
        if blocks is None:
            blocks = self.dfs_explore_cave()

        # If no reference block is provided, the default value is used
        if block1 is None:
            block1 = MinecraftBlock("Stone", 1.5, "Stone Item", 1)
        if block2 is None:
            block2 = MinecraftBlock("Diamond", 3, "Diamond Item", 100)

        # Filter blocks
        filtered_blocks = self.objective_mining_filter(blocks, block1, block2)

        # Dig through filtered blocks
        self.objective_mining(filtered_blocks)

    def objective_mining(self, blocks: ArrayList[MinecraftBlock]) -> None:
        """
        Mines the cave system casually.

        Args:
            blocks (ArrayList[MinecraftBlock]): The list of blocks to mine.
            time_in_seconds (int): The time in seconds to mine.

        Complexity:
            Best Case Complexity: TODO
            Worst Case Complexity: TODO

        Justification:
            TODO
        """
        # Create a tuple list containing the squares and their ratios
        block_ratios = ArrayList(0)
        for i in range(len(blocks)):
            block = blocks[i]
            ratio = block.item.value / block.hardness
            block_ratios.append((ratio, block))

        # Use mergesort to sort blocks in descending order of ratio
        from algorithms.mergesort import mergesort
        sorted_blocks = mergesort(block_ratios, key=lambda x: -x[0])  # negative sign is used for descending sorting

        # Empty the miner's current inventory
        self.miner.inventory.clear()

        # Create a new class that wraps the ArrayStack to support index access
        class IndexableStack(ArrayStack):
            def __getitem__(self, index):
                items = []
                temp_stack = ArrayStack(len(self))

                # Ejects items from the original stack into the temporary stack (the order is reversed)
                while not self.is_empty():
                    temp_stack.push(self.pop())

                # Place items from the temporary stack back into the original stack and add them to the list at the same time
                while not temp_stack.is_empty():
                    item = temp_stack.pop()
                    items.append(item)
                    self.push(item)

                # Returns the element for which the index is requested
                return items[index]

        # Replace the original stack with an indexable stack
        original_stack = self.miner.inventory
        new_stack = IndexableStack(len(sorted_blocks))
        self.miner.inventory = new_stack

        # Mine blocks in descending order
        for i in range(len(sorted_blocks)):
            _, block = sorted_blocks[i]
            self.miner.mine(block)

    def objective_mining_filter(self, blocks: ArrayList[MinecraftBlock], block1: MinecraftBlock,
                                block2: MinecraftBlock) -> ArrayList[MinecraftBlock]:
        """
        Filter the list of blocks to keep only those with a value/hardness ratio between two reference squares

        Args:
            blocks: A list of blocks to be filtered
            block1: Lower limit reference block (the ratio must be strictly greater than this block)
            block2: Upper limit reference block (the ratio must be strictly less than this block)

        Returns:
            Filtered list of blocks

        Complexity:
            Best-case scenario: O(n), where n is the length of the blocks
            Worst case: O(n), where n is the length of the blocks

        Justification:
            Go through all the squares and check their value/hardness ratio, which takes O(n) time
        """
        # Calculate the ratio of the reference square
        ratio1 = block1.item.value / block1.hardness
        ratio2 = block2.item.value / block2.hardness

        # Create a list of results
        filtered_blocks = ArrayList(0)

        # Iterate through all the squares, keeping the blocks within the specified range
        for i in range(len(blocks)):
            block = blocks[i]
            ratio = block.item.value / block.hardness

            # Only blocks with ratios strictly greater than ratio1 and strictly less than ratio2 are kept
            if ratio > ratio1 and ratio < ratio2:
                filtered_blocks.append(block)

        return filtered_blocks

    def profit_mining(self, blocks: ArrayList[MinecraftBlock], time_limit: int) -> None:
        """
        Main function to run the NotMinecraft game.

        Args:
            blocks: List of found blocks
            time_limit: Time limit for mining in seconds

        Complexity:
            Not required

        Sample Usage:
            not_minecraft = NotMinecraft(cave_system, checklist)
            not_minecraft.main(1, block1=block1, block2=block2)
            not_minecraft.main(2, time_in_seconds=60)
        """

        # Create an indexable stack to replace the original stack
        class IndexableStack(ArrayStack):
            def __getitem__(self, index):
                items = []
                temp_stack = ArrayStack(len(self))
                # Ejects items from the original stack into the temporary stack (the order is reversed)
                while not self.is_empty():
                    temp_stack.push(self.pop())
                # Place items from the temporary stack back into the original stack and add them to the list at the same time
                while not temp_stack.is_empty():
                    item = temp_stack.pop()
                    items.append(item)
                    self.push(item)
                # Returns the element for which the index is requested
                return items[index]

        # Replace with an indexable stack
        new_stack = IndexableStack(len(blocks))
        self.miner.inventory = new_stack

        # Empty miner inventory
        self.miner.inventory.clear()

        # Convert blocks into lists for multiple operations
        remaining_blocks = ArrayList(len(blocks))
        for i in range(len(blocks)):
            remaining_blocks.append(blocks[i])

        # Keep a record of the time remaining
        remaining_time = time_limit

        # Mining by value/hardness ratio
        while remaining_time > 0 and len(remaining_blocks) > 0:
            # Find the best block at the moment
            best_ratio = -1
            best_index = -1

            for i in range(len(remaining_blocks)):
                block = remaining_blocks[i]
                ratio = block.item.value / block.hardness

                # If you find a block with a higher ratio that can be mined
                if ratio > best_ratio and block.hardness <= remaining_time:
                    best_ratio = ratio
                    best_index = i

            # If a suitable block is found, mine it
            if best_index != -1:
                best_block = remaining_blocks[best_index]
                self.miner.mine(best_block)
                remaining_time -= best_block.hardness

                # Removes mined blocks from the remaining blocks
                remaining_blocks[best_index] = remaining_blocks[len(remaining_blocks) - 1]
                remaining_blocks.delete_at_index(len(remaining_blocks) - 1)
            else:
                # If you don't find a block to mine, try to mine the block with the lowest hardness
                min_hardness = float('inf')
                min_index = -1

                for i in range(len(remaining_blocks)):
                    block = remaining_blocks[i]
                    if block.hardness < min_hardness and block.hardness <= remaining_time:
                        min_hardness = block.hardness
                        min_index = i

                # If a suitable block is found, mine it
                if min_index != -1:
                    min_block = remaining_blocks[min_index]
                    self.miner.mine(min_block)
                    remaining_time -= min_block.hardness

                    # Removes mined blocks from the remaining blocks
                    remaining_blocks[min_index] = remaining_blocks[len(remaining_blocks) - 1]
                    remaining_blocks.delete_at_index(len(remaining_blocks) - 1)
                else:
                    # Unable to mine any blocks, exit the loop
                    break
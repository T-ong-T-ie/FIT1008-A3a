from __future__ import annotations
from data_structures import *
from minecraft_block import MinecraftBlock
from betterbst import BetterBST


class MinecraftChecklist:
    def __init__(self, blocks: ArrayR[MinecraftBlock]) -> None:
        """
        Initializes the MinecraftChecklist instance with a list of blocks.

        Complexity:
            Best Case Complexity: O(nlogn)
            Worst Case Complexity: O(nlogn)

        Justification:
            Creating and populating BetterBST requires O(nlogn) time complexity.
        """
        # Convert blocks to tuple form, for BetterBST
        elements = ArrayList(len(blocks))
        for i in range(len(blocks)):
            # Use the value/hardness ratio as a bond
            ratio = blocks[i].item.value / blocks[i].hardness
            elements.append((ratio, blocks[i]))

        # Create a balanced binary search tree
        self.checklist = BetterBST(elements)
        self.blocks_count = len(blocks)

    def __contains__(self, block: MinecraftBlock) -> bool:
        """
        Checks if the item is in the checklist.

        Complexity:
            Best Case Complexity: O(1)，If the first comparison is found.
            Worst Case Complexity: O(n)，All nodes need to be compared.

        Justification:
            Traverse the tree to find the corresponding block, as the value/hardness ratio is used as the key.
        """
        ratio = block.item.value / block.hardness

        # Use the filter function to find all nodes at a specific key value
        result = self.checklist.filter_keys(
            lambda x: x >= ratio,  # The key is greater than or equal to the target ratio
            lambda x: x <= ratio  # The key is less than or equal to the target ratio
        )

        # Check each result to see if it matches the target square
        for _, b in result:
            if b == block:
                return True

        return False

    def __len__(self) -> int:
        """
        Returns the number of blocks in the checklist.

        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(1)

        Justification:
            Returns the stored count directly, with a constant time complexity.
        """
        return self.blocks_count

    def add_block(self, block: MinecraftBlock) -> None:
        """
        Adds a block to the checklist.

        Complexity:
            Best Case Complexity: O(logn)
            Worst Case Complexity: O(logn)

        Justification:
            The complexity of inserting a new node in the balanced BST is O(logn).
        """
        # Calculate the value/hardness ratio
        ratio = block.item.value / block.hardness

        # Add blocks to the tree
        self.checklist[ratio] = block
        self.blocks_count += 1

    def remove_block(self, block: MinecraftBlock) -> None:
        """
        Removes a block from the checklist.

        Complexity:
            Best Case Complexity: O(logn)
            Worst Case Complexity: O(logn)

        Justification:
            The complexity of searching and deleting nodes in the balanced BST is O(logn).
        """
        # Calculate the value/hardness ratio
        ratio = block.item.value / block.hardness

        # Find all squares with the same ratio
        blocks_with_ratio = self.checklist.filter_keys(
            lambda x: x >= ratio,
            lambda x: x <= ratio
        )

        # Locate the specific block you want to remove
        for k, b in blocks_with_ratio:
            if b == block:
                # Remove the block from the tree
                del self.checklist[k]
                self.blocks_count -= 1
                return

        # If the block is not in the list, an exception is thrown
        raise ValueError(f"Block {block} not in the checklist")

    def get_sorted_blocks(self) -> ArrayR[MinecraftBlock]:
        """
        Returns the sorted blocks in the checklist.

        Complexity:
            Best Case Complexity: O(n)
            Worst Case Complexity: O(n)

        Justification:
            The complexity of the medium-order traversal BST is O(n).
        """
        # Use medium-order traversal to get sorted elements
        result = ArrayR(len(self))
        index = 0

        # The traversal function gets the key-ordered nodes from BST
        def inorder_traversal(node):
            nonlocal index
            if node is not None:
                inorder_traversal(node.left)
                result[index] = node.item
                index += 1
                inorder_traversal(node.right)

        # Traversal starts at the root node
        inorder_traversal(self.checklist.root)
        return result

    def get_optimal_blocks(self, block1: MinecraftBlock, block2: MinecraftBlock) -> ArrayR[MinecraftBlock]:
        """
        Returns the optimal blocks between two given blocks.

        Complexity:
            Best Case Complexity: O(logn)，When the pruning of the tree is very effective
            Worst Case Complexity: O(n)，When you need to access most of the nodes

        Justification:
            With filter_keys approach, most of the subtrees can be skipped in the best case.
        """
        # Calculate the value/hardness ratio of two squares
        ratio1 = block1.item.value / block1.hardness
        ratio2 = block2.item.value / block2.hardness

        # Use filter_keys to filter for squares whose ratios are within range
        filtered_blocks = self.checklist.filter_keys(
            lambda x: x > ratio1,  # The ratio is greater than block1
            lambda x: x < ratio2  # The ratio is less than block2
        )

        # Create an array of results and populate it
        result = ArrayR(len(filtered_blocks))
        for i in range(len(filtered_blocks)):
            result[i] = filtered_blocks[i][1]  # Get the part of the block in the tuple

        return result
from __future__ import annotations
from collections.abc import Callable

from typing import Tuple, TypeVar

from data_structures import *
from algorithms.mergesort import mergesort

K = TypeVar('K')
I = TypeVar('I')


class BetterBST(BinarySearchTree[K, I]):
    def __init__(self, elements: ArrayList[Tuple[K, I]]) -> None:
        """
        Initialiser for the BetterBST class.
        We assume that the all the elements that will be inserted
        into the tree are contained within the elements ArrayList.

        As such you can assume the length of elements to be non-zero.
        The elements ArrayList will contain tuples of key, item pairs.

        First sort the elements ArrayList and then build a balanced tree from the sorted elements
        using the corresponding methods below.

        Args:
            elements(ArrayList[tuple[K, I]]): The elements to be inserted into the tree.

        Complexity:
            Best Case Complexity: O(n log n)，where n is the number of elements.
            Worst Case Complexity: O(n log n)，where n is the number of elements.

        Justification:
            The constructor consists of two main operations: sorting elements and building a balance tree. The complexity of the sorting element is O(n log n),
            The complexity of constructing a balance tree is O(n). Since O(n log n) > O(n), the overall complexity is determined by the ordering,
            So the best-case and worst-case complexity is O(n log n).
        """
        super().__init__()
        new_elements: ArrayList[Tuple[K, I]] = self.__sort_elements(elements)
        self.__build_balanced_tree(new_elements)

    def __sort_elements(self, elements: ArrayList[Tuple[K, I]]) -> ArrayList[Tuple[K, I]]:
        """
        Recall one of the drawbacks to using a binary search tree is that it can become unbalanced.
        If we know the elements ahead of time, we can sort them and then build a balanced tree.
        This will help us maintain the O(log n) complexity for searching, inserting, and deleting elements.

        Args:
            elements (ArrayList[Tuple[K, I]]): The elements we wish to sort.

        Returns:
            ArrayList(Tuple[K, I]]) - elements after being sorted.

        Complexity:
            Best Case Complexity: O(n log n)，where n is the number of elements.
            Worst Case Complexity: O(n log n)，where n is the number of elements.

        Justification:
            We used a merge sorting algorithm with a time complexity of O(n log n).
            The complexity of the comparison function is O(1) because we are only getting the first element (key) of the tuple.
        """
        # Use merge sorting, and define a comparison function to extract the keys in the tuple
        return mergesort(elements, key=lambda x: x[0])

    def __build_balanced_tree(self, elements: ArrayList[Tuple[K, I]]) -> None:
        """
        This method will build a balanced binary search tree from the sorted elements.

        Args:
            elements (ArrayList[Tuple[K, I]]): The elements we wish to use to build our balanced tree.

        Returns:
            None

        Complexity:
            (This is the actual complexity of your code, 
            remember to define all variables used.)
            Best Case Complexity: O(n)，where n is the number of elements.
            Worst Case Complexity: O(n)，where n is the number of elements.

        Justification:
            We iterate through each element once, each insertion operation is O(1),
            Because we plug directly into the tree and not through search.
            The overall complexity is O(n).
        """

        def build_balanced_tree_recursive(start: int, end: int) -> None:
            if start > end:
                return

            # Find the middle position as the root node
            mid = (start + end) // 2

            # Insert an intermediate element
            key, item = elements[mid]
            self[key] = item

            # Recursively construct the left and right subtrees
            build_balanced_tree_recursive(start, mid - 1)
            build_balanced_tree_recursive(mid + 1, end)

        # Start a recursive build from the full list
        if len(elements) > 0:
            build_balanced_tree_recursive(0, len(elements) - 1)

    def filter_keys(self, filter_func1: Callable[[K], bool], filter_func2: Callable[[K], bool]) -> ArrayList[Tuple[K, I]]:
        """
        Filters the keys in the tree based on two criteria.

        Args:
            filter_func1 (callable): A function that takes a value and returns True if the key is more than criteria1.
            filter_func2 (callable): A function that takes a value and returns True if the key is less than criteria2.
        Returns:
            ArrayList[Tuple[K, I]]: An ArrayList of tuples containing Key,Item pairs that match the filter.

        Complexity:
            Best Case Complexity: O(log n * (filter_func1 + filter_func2))，平衡树且大部分节点不满足条件
            Worst Case Complexity: O(n * (filter_func1 + filter_func2))，需要检查所有节点

        Justification:
            在最好情况下，我们可以跳过大部分子树，仅检查 O(log n) 个节点
            在最坏情况下，我们需要检查所有 n 个节点
            对每个节点，我们应用两个过滤函数，复杂度为 O(filter_func1 + filter_func2)
        """
        result = ArrayList(0)

        def traverse_and_filter(node):
            if node is None:
                return

            # Mid-order traversal: Left subtree first, then the current node, then the right subtree
            # If the current node value is > the lower bound, you can check the left subtree
            if filter_func1(node.key):
                traverse_and_filter(node.left)

            # Check the current node
            if filter_func1(node.key) and filter_func2(node.key):
                result.append((node.key, node.item))

            # If the current node value is < upper bound, you can check the right subtree
            if filter_func2(node.key):
                traverse_and_filter(node.right)

        traverse_and_filter(self.root)
        return result

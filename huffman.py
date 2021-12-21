import os
import heapq
import collections
import operator
import ast
import sys
import time
import pickle


class HeapNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return other.freq > self.freq


class HuffmanCoding:
    def __init__(self):
        self.heap = []
        self.codes = {}
        self.reverse_mapping = {}

    # make frequency dictionaries with sorted value from low to high
    def make_frequency_dict(self, text):
        counted = dict(collections.Counter(text))
        sort = collections.OrderedDict(
            sorted(
                counted.items(),
                key=operator.itemgetter(1),
                reverse=False))
        return sort

    # make a heap queue from node
    def make_heap_node(self, freq_dict):
        for key in freq_dict:
            anode = HeapNode(key, freq_dict[key])
            self.heap.append(anode)

    # build tree
    def merge_nodes(self):
        while len(self.heap) > 1:
            node1 = heapq.heappop(self.heap)
            node2 = heapq.heappop(self.heap)
            merge = HeapNode(None, node1.freq + node2.freq)
            merge.left = node1
            merge.right = node2
            heapq.heappush(self.heap, merge)

    # actual coding happens here
    def encode_helper(self, root, current_code):
        if root is None:
            return

        if root.char is not None:
            self.codes[root.char] = current_code
            return

        self.encode_helper(root.left, current_code + "0")
        self.encode_helper(root.right, current_code + "1")

    def encode(self):
        root = heapq.heappop(self.heap)
        current_code = ""
        self.encode_helper(root, current_code)

    def get_encoded_text(self, text):
        encoded_text = ""
        for char in text:
            encoded_text += self.codes[char]
        return encoded_text

    """
    padding and eof
    https://www.cs.duke.edu/csed/poop/huff/info/#pseudo-eof
    https://web.stanford.edu/class/archive/cs/cs106b/cs106b.1174/handouts/210%20Huffman%20Encoding.pdf
    """

    def pad_encoded_text(self, encoded_text):
        # get the extra padding of encoded text
        extra_padding = 8 - len(encoded_text) % 8
        for i in range(extra_padding):
            encoded_text += "0"
        # merge the "info" of extra padding in "string/bit" with encoded text
        # so we know how to truncate it later
        padded_info = "{0:08b}".format(extra_padding)
        new_text = padded_info + encoded_text

        return new_text

    def to_byte_array(self, padded_encoded_text):
        if len(padded_encoded_text) % 8 != 0:
            print('not padded properly')
            exit(0)
        b = bytearray()
        for i in range(
                0, len(padded_encoded_text), 8):  # loop every 8 character
            byte = padded_encoded_text[i:i + 8]
            b.append(int(byte, 2))  # base 2
        return b

    def compress(self, lipsum):
        # start = time.time()
        # file_text = open(filename, 'r')
        # lipsum = file_text.read()
        # lipsum = lipsum.rstrip()
        # file_text.close()

        freq = self.make_frequency_dict(lipsum)
        self.make_heap_node(freq)
        self.merge_nodes()
        self.encode()
        encoded_text = self.get_encoded_text(lipsum)
        padded_encoded_text = self.pad_encoded_text(encoded_text)
        byte_array_huff = self.to_byte_array(padded_encoded_text)

        return byte_array_huff
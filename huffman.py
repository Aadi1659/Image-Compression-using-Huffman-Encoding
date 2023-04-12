from heapq import heappush, heappop
from collections import defaultdict
from PIL import Image

class HuffmanNode:
    def __init__(self, freq, val=None):
        self.freq = freq
        self.val = val
        self.left = None
        self.right = None
        
    def __lt__(self, other):
        return self.freq < other.freq
        
class HuffmanTree:
    def __init__(self, freq_dict):
        self.root = self.build_tree(freq_dict)
        self.code_dict = {}
        self.generate_codes(self.root, "")
        
    def build_tree(self, freq_dict):
        heap = []
        for val, freq in freq_dict.items():
            node = HuffmanNode(freq, val)
            heappush(heap, node)
        while len(heap) > 1:
            node1 = heappop(heap)
            node2 = heappop(heap)
            parent = HuffmanNode(node1.freq + node2.freq)
            parent.left = node1
            parent.right = node2
            heappush(heap, parent)
        return heappop(heap)
        
    def generate_codes(self, node, code):
        if node.val is not None:
            self.code_dict[node.val] = code
        else:
            self.generate_codes(node.left, code + "0")
            self.generate_codes(node.right, code + "1")
            
    def encode_image(self, img):
        width, height = img.size
        encoded_pixels = ""
        for y in range(height):
            for x in range(width):
                pixel_val = img.getpixel((x, y))
                encoded_pixels += self.code_dict[pixel_val]
        return encoded_pixels
    
    def decode_image(self, encoded_pixels, width, height):
        current_node = self.root
        decoded_pixels = []
        for bit in encoded_pixels:
            if bit == "0":
                current_node = current_node.left
            else:
                current_node = current_node.right
            if current_node.val is not None:
                decoded_pixels.append(current_node.val)
                current_node = self.root
        decoded_img = Image.new("L", (width, height))
        decoded_img.putdata(decoded_pixels)
        return decoded_img
        
def compress_image(input_file, output_file):
    # Load image and convert to grayscale
    img = Image.open(input_file).convert("L")
    width, height = img.size
    
    # Count pixel frequencies
    freq_dict = defaultdict(int)
    for y in range(height):
        for x in range(width):
            freq_dict[img.getpixel((x, y))] += 1
    
    # Build Huffman tree and generate codes
    tree = HuffmanTree(freq_dict)
    
    # Encode image
    encoded_pixels = tree.encode_image(img) 
    
    # Write binary file
    with open(output_file, "wb") as f:
        f.write(width.to_bytes(2, byteorder="big"))
        f.write(height.to_bytes(2, byteorder="big"))
        f.write(int(encoded_pixels, 2).to_bytes((len(encoded_pixels) + 7) // 8, byteorder="big"))

        
def decompress_image(input_file, output_file):
    # Read binary file
    with open(input_file, "rb") as f:
        width = int.from_bytes(f.read(2), byteorder="big")
        height = int.from_bytes(f.read(2), byteorder="big")
        encoded_pixels = f.read()
        
    # Build Huffman tree
    freq_dict = defaultdict(int)
    for byte in encoded_pixels:
        bits = "{0:08b}".format(byte)
        for bit in bits:
            freq_dict[bit] += 1
    tree = HuffmanTree(freq_dict)
    
    # Decode image
    decoded_pixels = []
    current_node = tree.root
    for byte in encoded_pixels:
        bits = "{0:08b}".format(byte)
        for bit in bits:
            if bit == "0":
                current_node = current_node.left
            else:
                current_node = current_node.right
            if current_node.val is not None:
                decoded_pixels.append(current_node.val)
                current_node = tree.root
    decoded_pixels = decoded_pixels[:width * height]
    
    # Create decoded image
    decoded_img = Image.new("L", (width, height))
    decoded_img.putdata(decoded_pixels)
    decoded_img.save(output_file)



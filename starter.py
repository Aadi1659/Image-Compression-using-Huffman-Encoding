from PIL import Image
from huffman import compress_image, decompress_image

# Compress image
input_image = "1.png"
compressed_file = "compressed.bin"
compress_image(input_image, compressed_file)

# Decompress image
output_image = "output_image.png"
decompress_image(compressed_file,output_image)

# Show original and decompressed images
Image.open(input_image).show()
Image.open(output_image).show()

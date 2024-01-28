import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

def load_image(file_path):
    pil_image = Image.open(file_path)
    im = np.array(pil_image)
    r, g, b = im[:,:,0], im[:,:,1], im[:,:,2]
    return r, g, b, pil_image

def compress_channel(data_matrix, nsv):
    U, S, V = np.linalg.svd(data_matrix)
    compressed_channel = np.dot(U[:, :nsv], np.dot(np.diag(S[:nsv]), V[:nsv, :]))
    return compressed_channel.astype('uint8')

def compress_image(r, g, b, nsv):
    r_compressed = compress_channel(r, nsv)
    g_compressed = compress_channel(g, nsv)
    b_compressed = compress_channel(b, nsv)
    return r_compressed, g_compressed, b_compressed

def display_compression_ratio(original_size, compressed_size):
    ratio = 1 - compressed_size/original_size
    print(f'Original image has been compressed by the {ratio * 100:.2f}% ')


def display_images(original_image, compressed_image_list):
    fig, axes = plt.subplots(2, 2, figsize=(10, 10))
    
    axes[0, 0].imshow(original_image)
    axes[0, 0].set_title('Original Image')
    axes[0, 0].axis('off')
    
    for i, k in enumerate(n_sv_values):
        compressed_image = compressed_image_list[i]
        axes[(i+1)//2, (i+1)%2].imshow(compressed_image)
        axes[(i+1)//2, (i+1)%2].set_title(f'Compressed Image (k={k})')
        axes[(i+1)//2, (i+1)%2].axis('off')

    plt.tight_layout()
    plt.show()

# Load the image
red_c, green_c, blue_c, image = load_image('wave.jpeg')
w, h = image.size[0], image.size[1]

# Define the number of singular values to use for compression
n_sv_values = [100, 200, 300]
compressed_image_list = []

for n_sv in n_sv_values:
    # Compress the image
    r_compressed, g_compressed, b_compressed = compress_image(red_c, green_c, blue_c, n_sv)
    compressed_size = n_sv * (1 + w + h) * 3
    
    # Create compressed image
    compressed_image = Image.merge("RGB", (Image.fromarray(r_compressed), Image.fromarray(g_compressed), Image.fromarray(b_compressed)))
    compressed_image_list.append(compressed_image)

    # Calculate and display compression ratio
    original_size = w * h * 3
    print('Original size:', original_size)
    print('Compressed size:', compressed_size)
    display_compression_ratio(original_size, compressed_size)

# Display original and compressed images
display_images(image, compressed_image_list)
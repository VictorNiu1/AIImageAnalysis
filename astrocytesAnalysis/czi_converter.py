from czifile import CziFile
import matplotlib.pyplot as plt
import numpy as np
import imageio
import scipy.misc

with CziFile('/Users/connor/Downloads/OPALS 23 Group 15/Cell 91 Pre.czi') as czi:
    image_arrays = czi.asarray()

frames = []
all_image_layers = []

for i in range(image_arrays.shape[0]):
#     fig = plt.figure(figsize=(6, 6), frameon=False)
#     null_layer = np.zeros((image_arrays.shape[2], image_arrays.shape[3]))
    intensities = image_arrays[i, 0, :, :, 0]
    scaled_intensities = intensities / 65535
    all_image_layers.append(scaled_intensities)
#     intensity_rgb_array = np.stack((null_layer, scaled_intensities, null_layer), axis=-1)
#     np.save(f'./npy/npy_{i}.npy', scaled_intensities)
#     ax = plt.Axes(fig, [0., 0., 1., 1.])
#     ax.set_axis_off()
#     fig.add_axes(ax)
#     ax.imshow(intensity_rgb_array)
#     plt.savefig(f'./img/img_{i}.tiff', transparent = False, facecolor = 'white')
#     image = imageio.v2.imread(f'./img/img_{i}.tiff')
#     frames.append(image)
#     plt.close()
#     print(f'image {i} dun')
# imageio.mimsave('./test.gif', frames)
print("dun")
from torch.utils.tensorboard import SummaryWriter
from PIL import Image
import numpy as np

image_path = "data/train/bees/16838648_415acd9e3f.jpg"
img = Image.open(image_path)
print(type(img))
img_array = np.array(img)
print(type(img_array))
writer = SummaryWriter("logs")
img_PIL = Image.open(image_path)
img_array = np.array(img_PIL)
print(type(img_array))
print(img_array.shape)

writer.add_image("test", img_array, 2, dataformats = 'HWC')
#y = x
for i in range(0, 100):
    writer.add_scalar("y = x", i, i)

writer.close()
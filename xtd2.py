from PIL import Image
from torchvision import transforms
import cv2
from torch.utils.tensorboard import SummaryWriter

img_path = "data/train/ants/0013035.jpg"
img = Image.open(img_path)
print(img)
cv_img = cv2.imread(img_path)

writer = SummaryWriter("logs")


tensor_trans = transforms.ToTensor()
tensor_img = tensor_trans(img)

writer.add_image("Tensor_img", tensor_img)

writer.close()
print(tensor_img)
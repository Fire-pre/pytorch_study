from PIL import Image
from torchvision import transforms
from torch.utils.tensorboard import SummaryWriter

writer = SummaryWriter("logs")
img = Image.open("data/train/ants/0013035.jpg")
print(img)

trans_totensor = transforms.ToTensor()
img_tensor = trans_totensor(img)
writer.add_image("ToTensor", img_tensor)

print(img_tensor[0][0][0])
trans_norm = transforms.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5])
img_norm = trans_norm(img_tensor)
print(img_norm[0][0][0])
writer.add_image("Normalize", img_norm)

print(img.size)
trans_resize = transforms.Resize((512,512))
img_resize = trans_resize(img)
img_resize = trans_totensor(img_resize)
print(img_resize)
writer.add_image("Resize", img_resize, 0)

trans_resize2 = transforms.Resize(512)
trans_compose = transforms.Compose([trans_resize2, trans_totensor])
img_resize2 = trans_compose(img)
writer.add_image("Resize", img_resize2, 1)

trans_random = transforms.RandomCrop(500, 1000)
trans_compose2 = transforms.Compose([trans_random, trans_totensor])
for i in range(10):
    img_crop = trans_compose2(img)
    writer.add_image("RandomCropHW", img_crop, i)

writer.close()
import torch 
import torch.nn as nn
import torchvision.transforms as transforms 
from PIL import Image
import sys,os,io
from app import app


from .mnist_fcn import NeuralNet,input_size, hidden_size, num_classes,device

PATH = "app/mnist_fcn.pth"

device = torch.device(device)

model = NeuralNet(input_size,hidden_size,num_classes)
model.load_state_dict(torch.load(PATH))
model.to(device)
model.eval()
# print(model.state_dict())

# image -> tensor
def transform_image(image_bytes):
    transform = transforms.Compose([transforms.Grayscale(num_output_channels=1),transforms.Resize((28,28)),transforms.ToTensor(),transforms.Normalize((0.1307,),(0.3081))])# global mean and global std dev of MNIST dataset
    image = Image.open(io.BytesIO(image_bytes))
    return transform(image).unsqueeze(0)
    
# predict

def get_prediction(image_tensor):
    image_tensor = image_tensor.reshape(-1,28*28).to(device)
    outputs = model(image_tensor)

    # value,index
    _,predictions = torch.max(outputs,1)
    return predictions
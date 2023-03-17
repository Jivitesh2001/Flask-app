from mnist_fcn import *
# MNIST
train_dataset = torchvision.datasets.MNIST(root='./root',train=True,transform= transform,download=True)
test_dataset = torchvision.datasets.MNIST(root='./root',train=False,transform= transform)

train_loader = torch.utils.data.DataLoader(dataset=train_dataset,batch_size=batch_size,shuffle=True)
test_loader = torch.utils.data.DataLoader(dataset=test_dataset,batch_size=batch_size,shuffle=True)
n_total_steps = len(train_loader)
for epoch in range(num_epochs):
    for  i , (images,labels) in enumerate(train_loader):
        # 100 , 1,28,28
        # 100, 784
        images = images.reshape(-1,28*28).to(device)
        labels = labels.to(device)
        
        #forward pass
        output = model(images)
        loss = criterion(output,labels)
        # backward pass
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        
        if (i+1) % 100 == 0:
            print(f'epoch {epoch+1} / {num_epochs}, step {i+1}/{n_total_steps}, loss = {loss.item():.4f}')
            
with torch.no_grad():
    n_correct = 0
    n_samples = 0
    for images, labels in test_loader:
        images = images.reshape(-1,28*28).to(device)
        labels = labels.to(device)
        outputs = model(images)
        
        # value,index
        _,predictions = torch.max(outputs,1)
        n_samples += labels.shape[0]
        n_correct += (predictions == labels).sum().item()
    
    acc = 100.0 * n_correct/n_samples
    print(f'accruracy = {acc}')        
    
    torch.save(model.state_dict(),"mnist_fcn.pth")
    print("Model State Dictionary Saved")
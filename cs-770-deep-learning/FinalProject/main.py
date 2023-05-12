import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
from torchvision.utils import save_image

# Define some hyperparameters
batch_size = 64
latent_size = 100
image_size = 28 * 28
num_epochs = 50
learning_rate = 0.0002
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Load the MNIST dataset
transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.5,), (0.5,))
])
train_dataset = datasets.MNIST(root='./data', train=True, download=True, transform=transform)
train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=batch_size, shuffle=True)


# Define the generator network
class Generator(nn.Module):
    def __init__(self):
        super(Generator, self).__init__()
        self.fc1 = nn.Linear(latent_size, 256)
        self.fc2 = nn.Linear(256, 512)
        self.fc3 = nn.Linear(512, image_size)
        self.relu = nn.ReLU()
        self.tanh = nn.Tanh()

    def forward(self, x):
        x = self.relu(self.fc1(x))
        x = self.relu(self.fc2(x))
        x = self.tanh(self.fc3(x))
        return x


# Define the discriminator network
class Discriminator(nn.Module):
    def __init__(self):
        super(Discriminator, self).__init__()
        self.fc1 = nn.Linear(image_size, 512)
        self.fc2 = nn.Linear(512, 256)
        self.fc3 = nn.Linear(256, 1)
        self.relu = nn.ReLU()
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        x = self.relu(self.fc1(x))
        x = self.relu(self.fc2(x))
        x = self.sigmoid(self.fc3(x))
        return x


# Initialize the networks and optimizer
G = Generator().to(device)
D = Discriminator().to(device)
G_optimizer = optim.Adam(G.parameters(), lr=learning_rate)
D_optimizer = optim.Adam(D.parameters(), lr=learning_rate)

# Train the GAN
for epoch in range(num_epochs):
    for i, (real_images, _) in enumerate(train_loader):
        # Train the discriminator
        real_labels = torch.ones(batch_size, 1).to(device)
        fake_labels = torch.zeros(batch_size, 1).to(device)
        real_images = real_images.view(-1, image_size).to(device)

        # Train on real images
        D_optimizer.zero_grad()
        real_outputs = D(real_images)
        real_loss = nn.BCELoss()(real_outputs, real_labels)

        # Train on fake images
        z = torch.randn(batch_size, latent_size).to(device)
        fake_images = G(z)
        fake_outputs = D(fake_images)
        fake_loss = nn.BCELoss()(fake_outputs, fake_labels)

        # Backpropagate and update weights for discriminator
        D_loss = real_loss + fake_loss
        D_loss.backward()
        D_optimizer.step()

        # Train the generator
        G_optimizer.zero_grad()
        z = torch.randn(batch_size, latent_size).to(device)
        fake_images = G(z)
        fake_outputs = D(fake_images)
        G_loss = nn.BCELoss()(fake_outputs, real_labels)

        # Backpropagate and update weights for generator
        G_loss.backward()
        G_optimizer.step()

        # Print loss and save images every 100 batches
        if (i + 1) % 100 == 0:
            print("Epoch [{}/{}], Batch [{}/{}], D_loss: {:.4f}, G_loss: {:.4f}".format(
                epoch + 1, num_epochs, i + 1, len(train_loader), D_loss.item(), G_loss.item()))

            # Save generated images
            with torch.no_grad():
                fake_images = G(z).view(-1, 1, 28, 28)
                save_image(fake_images, './gan_images/epoch{}_batch{}.png'.format(epoch + 1, i + 1))

    # Save the final generator model
    torch.save(G.state_dict(), './generator.pth')
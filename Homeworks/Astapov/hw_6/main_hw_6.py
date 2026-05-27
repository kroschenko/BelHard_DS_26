import random

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import torch
import torch.nn as nn
import torch.optim as optim

from torchvision import datasets, transforms
from torch.utils.data import DataLoader

from sklearn.metrics import confusion_matrix, classification_report


# =========================================================
# УСТРОЙСТВО
# =========================================================
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f'Используемое устройство: {device}')


# =========================================================
# ПУТИ К ДАННЫМ
# =========================================================
train_dir = 'datasets/seg_train/seg_train'
test_dir = 'datasets/seg_test/seg_test'


# =========================================================
# ТРАНСФОРМАЦИИ
# =========================================================
train_transform = transforms.Compose([
    transforms.Resize((150, 150)),
    transforms.RandomHorizontalFlip(),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

test_transform = transforms.Compose([
    transforms.Resize((150, 150)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])


# =========================================================
# ДАТАСЕТЫ
# =========================================================
train_dataset = datasets.ImageFolder(root=train_dir, transform=train_transform)
test_dataset = datasets.ImageFolder(root=test_dir, transform=test_transform)


# =========================================================
# DATALOADER
# =========================================================
train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=32, shuffle=False)


# =========================================================
# НАЗВАНИЯ КЛАССОВ
# =========================================================
class_names = train_dataset.classes

print('\nКлассы:')

print(class_names)


# =========================================================
# ВЫВОД СЛУЧАЙНЫХ ИЗОБРАЖЕНИЙ
# =========================================================
def show_images(dataset, class_names):

    plt.figure(figsize=(15, 15))

    for class_index, class_name in enumerate(class_names):

        images = []

        for img, label in dataset:

            if label == class_index:
                images.append(img)

        random_images = random.sample(images, 3)

        for i, image in enumerate(random_images):
            image = image.permute(1, 2, 0).numpy()

            # Денормализация изображения
            mean = np.array([0.485, 0.456, 0.406])
            std = np.array([0.229, 0.224, 0.225])
            image = std * image + mean
            image = np.clip(image, 0, 1)

            plt.subplot(len(class_names), 3, class_index * 3 + i + 1)

            plt.imshow(image)
            plt.title(class_name)
            plt.axis('off')

    plt.tight_layout()
    plt.show()


show_images(train_dataset, class_names)


# =========================================================
# АРХИТЕКТУРА CNN
# =========================================================

class CNNModel(nn.Module):
    def __init__(self):
        super(CNNModel, self).__init__()
        self.conv_layers = nn.Sequential(
            # =================================================
            # БЛОК 1
            # Вход: 3 x 150 x 150
            # =================================================

            nn.Conv2d(in_channels=3, out_channels=32, kernel_size=3, padding=1),

            nn.BatchNorm2d(32),
            nn.ReLU(),
            nn.MaxPool2d(2),
            # Выход: 32 x 75 x 75


            # =================================================
            # БЛОК 2
            # =================================================

            nn.Conv2d(in_channels=32, out_channels=64, kernel_size=3, padding=1),

            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.MaxPool2d(2),
            # Выход: 64 x 37 x 37


            # =================================================
            # БЛОК 3
            # =================================================

            nn.Conv2d(in_channels=64, out_channels=128, kernel_size=3, padding=1),

            nn.BatchNorm2d(128),
            nn.ReLU(),
            nn.MaxPool2d(2),
            # Выход: 128 x 18 x 18
        )

        self.fc_layers = nn.Sequential(
            nn.Flatten(),
            nn.Linear(128 * 18 * 18, 512),

            nn.ReLU(),
            nn.Dropout(0.5),

            nn.Linear(512, 6)
        )

    def forward(self, x):
        x = self.conv_layers(x)
        x = self.fc_layers(x)
        return x


# =========================================================
# СОЗДАНИЕ МОДЕЛИ
# =========================================================
model = CNNModel().to(device)
print('\nАрхитектура модели:\n')
print(model)


# =========================================================
# ФУНКЦИЯ ПОТЕРЬ
# =========================================================
criterion = nn.CrossEntropyLoss()


# =========================================================
# ОПТИМИЗАТОР
# =========================================================
optimizer = optim.Adam(model.parameters(), lr=0.001)


# =========================================================
# ПЛАНИРОВЩИК LEARNING RATE
# =========================================================
scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=5, gamma=0.5)


# =========================================================
# ОБУЧЕНИЕ МОДЕЛИ
# =========================================================

num_epochs = 15

train_losses = []
test_losses = []

train_accuracies = []
test_accuracies = []


for epoch in range(num_epochs):
    # =====================================================
    # ОБУЧЕНИЕ
    # =====================================================

    model.train()
    running_loss = 0.0
    correct = 0
    total = 0

    for images, labels in train_loader:
        images = images.to(device)
        labels = labels.to(device)
        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        running_loss += loss.item()
        _, predicted = torch.max(outputs, 1)

        total += labels.size(0)
        correct += (predicted == labels).sum().item()

    train_loss = running_loss / len(train_loader)
    train_accuracy = correct / total
    train_losses.append(train_loss)
    train_accuracies.append(train_accuracy)


    # =====================================================
    # ТЕСТИРОВАНИЕ
    # =====================================================
    model.eval()
    running_loss = 0.0
    correct = 0
    total = 0

    with torch.no_grad():
        for images, labels in test_loader:
            images = images.to(device)
            labels = labels.to(device)
            outputs = model(images)
            loss = criterion(outputs, labels)
            running_loss += loss.item()
            _, predicted = torch.max(outputs, 1)

            total += labels.size(0)
            correct += (predicted == labels).sum().item()

    test_loss = running_loss / len(test_loader)
    test_accuracy = correct / total
    test_losses.append(test_loss)
    test_accuracies.append(test_accuracy)
    scheduler.step()

    print(
        f'Эпоха [{epoch + 1}/{num_epochs}] | '
        f'Ошибка обучения: {train_loss:.4f} | '
        f'Точность обучения: {train_accuracy:.4f} | '
        f'Ошибка теста: {test_loss:.4f} | '
        f'Точность теста: {test_accuracy:.4f}'
    )


# =========================================================
# ГРАФИКИ LOSS И ACCURACY
# =========================================================
plt.figure(figsize=(12, 5))


# =========================================================
# ГРАФИК ОШИБКИ
# =========================================================
plt.subplot(1, 2, 1)
plt.plot(train_losses, label='Ошибка обучения')
plt.plot(test_losses, label='Ошибка теста')
plt.title('График ошибки')
plt.xlabel('Эпоха')
plt.ylabel('Loss')
plt.legend()


# =========================================================
# ГРАФИК ТОЧНОСТИ
# =========================================================
plt.subplot(1, 2, 2)
plt.plot(train_accuracies, label='Точность обучения')
plt.plot(test_accuracies, label='Точность теста')
plt.title('График точности')
plt.xlabel('Эпоха')
plt.ylabel('Accuracy')
plt.legend()
plt.show()


# =========================================================
# МАТРИЦА ОШИБОК
# =========================================================
all_labels = []
all_predictions = []
model.eval()

with torch.no_grad():
    for images, labels in test_loader:
        images = images.to(device)
        outputs = model(images)
        _, predicted = torch.max(outputs, 1)

        all_labels.extend(labels.numpy())
        all_predictions.extend(predicted.cpu().numpy())


cm = confusion_matrix(all_labels, all_predictions)


# =========================================================
# ВИЗУАЛИЗАЦИЯ МАТРИЦЫ ОШИБОК
# =========================================================
plt.figure(figsize=(8, 6))

sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=class_names, yticklabels=class_names)

plt.xlabel('Предсказанные классы')
plt.ylabel('Истинные классы')
plt.title('Матрица ошибок')
plt.show()


# =========================================================
# ОТЧЕТ ПО КЛАССИФИКАЦИИ
# =========================================================
print('\nОтчет по классификации:\n')

print(classification_report(all_labels, all_predictions, target_names=class_names))


# =========================================================
# ИТОГОВАЯ ТОЧНОСТЬ
# =========================================================
final_accuracy = np.mean(np.array(all_labels) == np.array(all_predictions))

print(f'\nИтоговая точность на тестовой выборке: {final_accuracy:.4f}')
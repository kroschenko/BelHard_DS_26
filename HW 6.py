
import os
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import torchvision
import torchvision.transforms as transforms
from torch.utils.data import DataLoader
from torchvision.datasets import ImageFolder
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import random
from sklearn.metrics import confusion_matrix
from torchsummary import summary

# ==========================================================
# 1. НАСТРОЙКИ И ЗАГРУЗКА ДАННЫХ (EDA)
# ==========================================================
# УКАЖИТЕ ВАШ ПУТЬ К ПАПКЕ С ДАТАСЕТОМ
data_dir = 'D:/Машинное обучение/seg_pred' 
data_dir = 'D:/Машинное обучение/seg_test'
data_dir = 'D:/Машинное обучение/seg_train' 


train_path = 'D:/Машинное обучение/seg_train/'
test_path = 'D:/Машинное обучение/seg_test/'


# Трансформации (размер 150x150, нормализация по ImageNet)
stats = ((0.485, 0.456, 0.406), (0.229, 0.224, 0.225))
transform = transforms.Compose([
    transforms.Resize((150, 150)),
    transforms.ToTensor(),
    transforms.Normalize(*stats)
])

# Загрузка данных
train_ds = ImageFolder(train_path, transform=transform)
test_ds = ImageFolder(test_path, transform=transform)

# DataLoaders
batch_size = 32
train_dl = DataLoader(train_ds, batch_size, shuffle=True)
test_dl = DataLoader(test_ds, batch_size)

print(f"Классы обнаружены: {train_ds.classes}")

# ==========================================================
# 2. АРХИТЕКТУРА CNN С НУЛЯ (nn.Module)
# ==========================================================
class SceneClassificationCNN(nn.Module):
    def __init__(self):
        super(SceneClassificationCNN, self).__init__()
        
        # Блок 1: 150x150 -> 75x75
        self.conv1 = nn.Conv2d(3, 32, kernel_size=3, padding=1)
        self.bn1 = nn.BatchNorm2d(32)
        self.pool = nn.MaxPool2d(2, 2)
        
        # Блок 2: 75x75 -> 37x37
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.bn2 = nn.BatchNorm2d(64)
        
        # Блок 3: 37x37 -> 18x18
        self.conv3 = nn.Conv2d(64, 128, kernel_size=3, padding=1)
        self.bn3 = nn.BatchNorm2d(128)
        
        # Классификатор
        self.dropout = nn.Dropout(0.5)
        self.fc1 = nn.Linear(128 * 18 * 18, 512)
        self.fc2 = nn.Linear(512, 6) # 6 типов сцен

    def forward(self, x):
        x = self.pool(F.relu(self.bn1(self.conv1(x)))) # Блок 1
        x = self.pool(F.relu(self.bn2(self.conv2(x)))) # Блок 2
        x = self.pool(F.relu(self.bn3(self.conv3(x)))) # Блок 3
        
        x = x.view(-1, 128 * 18 * 18) # Выравнивание
        x = self.dropout(x)
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return x

# ==========================================================
# 3. ЦИКЛ ОБУЧЕНИЯ (TRAINING LOOP)
# ==========================================================
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Создаем модель и переносим на устройство
model = SceneClassificationCNN().to(device)

# Вывод сводки модели
from torchsummary import summary 
summary(model, (3, 150, 150)) # 3 канала, размер 150x150

criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)
scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=7, gamma=0.1)

num_epochs = 15 # Рекомендуется от 15 до 20 по условию задания
history = {'train_loss': [], 'train_acc': [], 'test_loss': [], 'test_acc': []}

print(f"\nНачинаем обучение на {device}...")

for epoch in range(num_epochs):
    model.train()
    train_loss, train_correct = 0.0, 0
    
    for images, labels in train_dl:
        images, labels = images.to(device), labels.to(device)
        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        
        _, preds = torch.max(outputs, 1)
        train_loss += loss.item() * images.size(0)
        train_correct += torch.sum(preds == labels.data)
    
    scheduler.step()
    
    # Валидация
    model.eval()
    test_loss, test_correct = 0.0, 0
    with torch.no_grad():
        for images, labels in test_dl:
            images, labels = images.to(device), labels.to(device)
            outputs = model(images)
            loss = criterion(outputs, labels)
            _, preds = torch.max(outputs, 1)
            test_loss += loss.item() * images.size(0)
            test_correct += torch.sum(preds == labels.data)

    # Сохраняем метрики
    train_acc = train_correct.double() / len(train_ds)
    test_acc = test_correct.double() / len(test_ds)
    history['train_loss'].append(train_loss / len(train_ds))
    history['test_loss'].append(test_loss / len(test_ds))
    history['train_acc'].append(train_acc.item())
    history['test_acc'].append(test_acc.item())

    print(f"Эпоха {epoch+1}/{num_epochs} | Train Acc: {train_acc:.4f} | Test Acc: {test_acc:.4f}")

# ==========================================================
# 4. ОЦЕНКА И АНАЛИЗ ОШИБОК
# ==========================================================
# 4.1 Графики обучения
plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
plt.plot(history['train_loss'], label='Train Loss')
plt.plot(history['test_loss'], label='Test Loss')
plt.title('График потерь (Loss)')
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(history['train_acc'], label='Train Accuracy')
plt.plot(history['test_acc'], label='Test Accuracy')
plt.title('График точности (Accuracy)')
plt.legend()
plt.show()

# 4.2 Матрица ошибок
all_preds, all_labels = [], []
model.eval()
with torch.no_grad():
    for images, labels in test_dl:
        images = images.to(device)
        outputs = model(images)
        _, preds = torch.max(outputs, 1)
        all_preds.extend(preds.cpu().numpy())
        all_labels.extend(labels.numpy())

cm = confusion_matrix(all_labels, all_preds)
plt.figure(figsize=(10, 8))
sns.heatmap(cm, annot=True, fmt='d', cmap='Greens', 
            xticklabels=train_ds.classes, yticklabels=train_ds.classes)
plt.xlabel('Предсказано')
plt.ylabel('Реально')
plt.title('Матрица ошибок')
plt.show()

print("\n--- Анализ ---")
print("Обычно модель путает 'glacier' (ледник) и 'mountain' (горы), так как на обоих изображениях присутствует снег и схожие текстуры камня.")

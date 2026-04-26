import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import TensorDataset, DataLoader
from GoPolicyNet import GoPolicyResNet

total_frames = 1000000 # total frames to use for training/testing
test_frames = 10000 # frames to hold out of training for test purposes
training_data_path = 'TrainingData-18k'

X = np.memmap(rf'{training_data_path}\X_file.npy', dtype=np.uint8, mode='r+', shape=(total_frames, 19, 19, 4))
y = np.memmap(rf'{training_data_path}\y_file.npy', dtype=np.uint16, mode='r+', shape=(total_frames,))

X_train = X[:total_frames-test_frames]
y_train = y[:total_frames-test_frames]

X_test = X[total_frames-test_frames:]
y_test = y[total_frames-test_frames:]


device = torch.device("cuda" if torch.cuda.is_available() else "cpu") # Trains on nvidia gpu if available

# set up model
model = GoPolicyResNet().to(device)
optimizer = torch.optim.Adam(model.parameters(), lr=1e-4)
criterion = nn.CrossEntropyLoss()
num_epochs = 1
batch_size = 128

train_dataset = TensorDataset(
    torch.from_numpy(X_train).permute(0, 3, 1, 2).float(),
    torch.from_numpy(y_train).long().view(-1)
)
# Set up training data
train_loader = DataLoader(
    train_dataset,
    batch_size=256,
    shuffle=False,
    pin_memory=True,
    num_workers=0
)
# Train model
for epoch in range(1):
    total_loss = 0

    for i, (X_batch, y_batch) in enumerate(train_loader):

        X_batch = X_batch.to(device)
        y_batch = y_batch.to(device).long().view(-1)

        preds = model(X_batch)

        loss = criterion(preds, y_batch)
        total_loss += loss.item()
        # backward
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

# AI generated
        with torch.no_grad():
            # 1. Calculate Top-1 Accuracy
            _, predicted_move = torch.max(preds, 1)
            correct_top1 = (predicted_move == y_batch).sum().item()
            batch_acc_top1 = (correct_top1 / y_batch.size(0)) * 100

            # 2. Calculate Top-5 Accuracy (Very useful for Go)
            _, top5_preds = torch.topk(preds, k=5, dim=1)
            correct_top5 = torch.any(top5_preds == y_batch.unsqueeze(1), dim=1).sum().item()
            batch_acc_top5 = (correct_top5 / y_batch.size(0)) * 100

            # 3. Update Running Totals
            running_loss = 0.9 * running_loss + 0.1 * loss.item() if 'running_loss' in locals() else loss.item()
            running_acc1 = 0.9 * running_acc1 + 0.1 * batch_acc_top1 if 'running_acc1' in locals() else batch_acc_top1

            # 4. Print Status every 100 batches
            if (i) % 100 == 0:
            #print('made it to here')
                print(f"Batch: {i} | "
                      f"Loss: {loss.item():.4f} (Avg: {running_loss:.4f}) | "
                      f"Top-1 Acc: {batch_acc_top1:>5.2f}% (Avg: {running_acc1:.2f}%) | "
                      f"Top-5 Acc: {batch_acc_top5:>5.2f}%",)


def evaluate_model(model, test_loader, device):
    # 1. Put model in evaluation mode (VERY IMPORTANT)
    model.eval()

    total_samples = 0
    total_top1 = 0
    total_top5 = 0
    total_loss = 0
    criterion = torch.nn.CrossEntropyLoss()

    print("\n--- Starting Full Evaluation ---")

    with torch.no_grad():  # Disable gradient calculation for speed/memory
        for i, (X_batch, y_batch) in enumerate(test_loader):
            X_batch = X_batch.to(device)
            y_batch = y_batch.to(device).long().view(-1)

            # Forward pass
            logits = model(X_batch)
            loss = criterion(logits, y_batch)

            # Calculate Top-1
            _, predicted = torch.max(logits, 1)
            total_top1 += (predicted == y_batch).sum().item()

            # Calculate Top-5
            _, top5_preds = torch.topk(logits, k=5, dim=1)
            total_top5 += torch.any(top5_preds == y_batch.unsqueeze(1), dim=1).sum().item()

            total_samples += y_batch.size(0)
            total_loss += loss.item()

            # Print progress every 10 batches
            if i % 10 == 0:
                print(f"Processed: {total_samples:<6} | Current Top-1: {(total_top1 / total_samples) * 100:.2f}%",
                      )

    # Calculate final stats
    final_acc1 = (total_top1 / total_samples) * 100
    final_acc5 = (total_top5 / total_samples) * 100
    avg_loss = total_loss / len(test_loader)

    print(f"\n\nFINAL EVALUATION RESULTS:")
    print(f"{'-' * 30}")
    print(f"Total Samples: {total_samples}")
    print(f"Average Loss:  {avg_loss:.4f}")
    print(f"Top-1 Acc:     {final_acc1:.2f}%")
    print(f"Top-5 Acc:     {final_acc5:.2f}%")
    print(f"{'-' * 30}\n")

    # Put model back into training mode
    model.train()
    return final_acc1, final_acc5
# End of AI generated block

# create test set
test_dataset = TensorDataset(
    torch.from_numpy(X_test).permute(0, 3, 1, 2).float(),
    torch.from_numpy(y_test).long().view(-1)
)

test_loader = DataLoader(
    test_dataset,
    batch_size=64,
    shuffle=False,
    pin_memory=True,
    num_workers=0
)

print(evaluate_model(model, test_loader, device))

torch.save(model.state_dict(), 'Go_Model_18k.pth')

# 20.7
# 44.99

# 24
# 47

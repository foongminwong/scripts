# Install CUDA-Enabled PyTorch - pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
import torch
print(torch.cuda.is_available())
print(torch.cuda.device_count())
print(torch.cuda.get_device_name(0))
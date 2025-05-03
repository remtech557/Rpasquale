# GPU Setup Guide for Remtech Chatbot

This guide will help you ensure your GPU is properly configured for running the chatbot with GPU acceleration.

## Prerequisite Checks

1. Make sure you have an NVIDIA GPU.
2. Verify your GPU is recognized by Windows:
   - Right-click on desktop → NVIDIA Control Panel
   - Or check Device Manager → Display adapters

## Installation Steps

### 1. Install NVIDIA Drivers

1. Go to [NVIDIA Driver Downloads](https://www.nvidia.com/Download/index.aspx)
2. Select your GPU model and download the latest driver
3. Install the driver by following the wizard

### 2. Install CUDA Toolkit

1. Go to [NVIDIA CUDA Downloads](https://developer.nvidia.com/cuda-downloads)
2. Select your OS and follow the download instructions
3. Install CUDA Toolkit (currently recommended version: 11.8 or 12.1)

### 3. Install PyTorch with CUDA Support

Run the following command in your command prompt:


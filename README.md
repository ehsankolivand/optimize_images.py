# 🖼️ Smart WebP Converter


A high-performance, intelligent image converter that automatically optimizes and converts JPEG/PNG images to WebP format. The script ensures optimal compression while maintaining image quality through smart analysis and parallel processing.

## ✨ Key Features

- **Smart Conversion**: Only converts images when the WebP version will be smaller than the original
- **Quality Preservation**: Maintains a 95% similarity threshold compared to the original image
- **Parallel Processing**: Utilizes multiple CPU cores for faster batch processing
- **Transparency Support**: Special handling for images with alpha channels
- **Intelligent Quality Selection**: Automatically tests multiple quality settings to find the optimal balance
- **Detailed Logging**: Comprehensive logging of the conversion process with status updates
- **Non-destructive**: Original files are only removed after successful conversion

## 📋 Requirements

- Python 3.7 or higher
- Pillow (PIL Fork)
- Standard Python libraries: os, sys, pathlib, concurrent.futures, io, logging

## 🚀 Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/smart-webp-converter.git
cd smart-webp-converter
```

2. Install dependencies:
```bash
pip install Pillow
```

## 💻 Usage

Simply run the script in the directory containing your images:

```bash
python webp_converter.py
```

The script will:
1. Recursively find all JPG/JPEG/PNG images in the current directory and subdirectories
2. Analyze each image for potential optimization
3. Convert suitable images to WebP format
4. Provide detailed conversion statistics upon completion

### Example Output:
```
2024-01-05 10:30:15 - INFO - Starting image optimization in: /path/to/images
2024-01-05 10:30:15 - INFO - Found 25 images to process
2024-01-05 10:30:16 - INFO - [1/25] Converted image1.jpg: 65.3% smaller
2024-01-05 10:30:16 - INFO - [2/25] Skipped conversion (not beneficial)
...
2024-01-05 10:30:20 - INFO - Optimization Complete!
2024-01-05 10:30:20 - INFO - Successfully converted: 20
2024-01-05 10:30:20 - INFO - Skipped (not beneficial): 4
2024-01-05 10:30:20 - INFO - Errors: 1
```

## 🔧 How It Works

The script employs a sophisticated approach to image conversion:

1. **Image Analysis**:
   - Reads the original image and calculates its size
   - Determines if the image has transparency
   - Converts image to appropriate color mode (RGB/RGBA)

2. **Optimization Process**:
   - For transparent images: Uses lossless WebP conversion
   - For regular images: Tests multiple quality settings (90, 85, 80)
   - Performs structural similarity analysis to ensure quality preservation
   - Only proceeds with conversion if file size reduction is achieved

3. **Parallel Processing**:
   - Utilizes ProcessPoolExecutor for concurrent image processing
   - Automatically scales to available CPU cores
   - Maintains organized logging despite parallel execution

4. **Quality Control**:
   - Implements pixel-by-pixel comparison between original and converted images
   - Ensures minimum 95% structural similarity
   - Validates successful conversion before removing original files

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- The Pillow development team for their excellent image processing library
- The WebP team at Google for creating the WebP format
- All contributors and users of this project

---

Made with ❤️ by [Your Name]

*Note: Please star ⭐ the repository if you find it useful!*

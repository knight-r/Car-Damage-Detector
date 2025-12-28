# 🚗 Car Damage Detection API

AI-powered car damage detection system using OpenAI GPT-4 Vision API. Analyzes car images and returns structured JSON with damage details including type, location (bounding boxes), severity, and descriptions.

## Features

- 🔍 Automatic damage detection from car images
- 📊 Structured JSON output with bounding boxes
- 🎯 Severity rating (1-5 scale)
- 📝 Detailed damage descriptions
- 🚀 RESTful API with FastAPI
- 📄 Interactive API documentation (Swagger UI)

## Prerequisites

- Python 3.9 or higher
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/car-damage-detector.git
cd car-damage-detector
```

### 2. Create virtual environment
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On Mac/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up environment variables
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your OpenAI API key
# You can use any text editor:
nano .env
# or
code .env
```

**Edit `.env` file:**
```env
OPENAI_API_KEY=sk-proj-YOUR_ACTUAL_API_KEY_HERE
OPENAI_MODEL=gpt-4o
```

> ⚠️ **Important:** Never commit the `.env` file to GitHub! It's already in `.gitignore`.

## Usage

### Start the server
```bash
# Make sure virtual environment is activated
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The server will start at `http://localhost:8000`

### Access API Documentation

Open your browser and go to:
```
http://localhost:8000/docs
```

You'll see interactive Swagger UI where you can test the API directly.

### API Endpoints

#### POST `/analyze`
Analyze car damage from uploaded images.

**Request:**
- **files**: One or more image files (JPG, PNG, WEBP)
- **custom_prompt** (optional): Additional analysis instructions

**Example using curl:**
```bash
curl -X POST "http://localhost:8000/analyze" \
  -F "files=@car_damage.jpg"
```

**Example using Python:**
```python
import requests

url = "http://localhost:8000/analyze"
files = {"files": open("car_damage.jpg", "rb")}
response = requests.post(url, files=files)
print(response.json())
```

**Response:**
```json
[
  {
    "image_name": "car_damage.jpg",
    "damages": [
      {
        "type": "Side Panel Dent",
        "bbox": [120, 300, 480, 750],
        "severity": 4,
        "description": "Deep impact on left front door, approximately 30cm diameter"
      },
      {
        "type": "Bumper Scratch",
        "bbox": [80, 260, 530, 320],
        "severity": 3,
        "description": "Horizontal paint scratch on front bumper"
      }
    ],
    "total_damages": 2,
    "overall_severity": "moderate"
  }
]
```

#### GET `/health`
Check API health status.

#### GET `/`
Get API information and available endpoints.

## Testing with Web UI

Open `test_client.html` in your browser for a simple web interface to test the API.
```bash
# Option 1: Open directly
open test_client.html

# Option 2: Use Python HTTP server
python -m http.server 8080
# Then open: http://localhost:8080/test_client.html
```

## Project Structure
```
car-damage-detector/
├── .env                          # Environment variables (DO NOT COMMIT)
├── .env.example                  # Environment template (COMMIT THIS)
├── .gitignore                    # Git ignore rules
├── requirements.txt              # Python dependencies
├── README.md                     # This file
├── main.py                       # FastAPI application
├── config.py                     # Configuration management
├── test_client.html              # Web UI for testing
├── models/
│   ├── __init__.py
│   └── schemas.py                # Pydantic models
├── services/
│   ├── __init__.py
│   ├── llm_service.py            # OpenAI integration
│   └── image_processor.py       # Image processing utilities
└── prompts/
    ├── __init__.py
    └── damage_analysis_prompt.py # AI prompts for damage detection
```

## Configuration

All configuration is done via the `.env` file:

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | Your OpenAI API key (required) | - |
| `OPENAI_MODEL` | Model to use for analysis | `gpt-4o` |

### Available Models

- `gpt-4o` - Latest and recommended (best performance)
- `gpt-4-turbo` - Fast and capable
- `gpt-4-vision-preview` - Original vision model

## API Response Schema

### DamageDetail
```json
{
  "type": "string",           // Damage type (e.g., "Dent", "Scratch")
  "bbox": [x1, y1, x2, y2],  // Bounding box coordinates
  "severity": 1-5,            // Severity rating
  "description": "string"     // Detailed description
}
```

### CarDamageResponse
```json
{
  "image_name": "string",
  "damages": [DamageDetail],
  "total_damages": 0,
  "overall_severity": "none|minor|moderate|severe"
}
```

## Troubleshooting

### Module not found errors

Make sure your virtual environment is activated:
```bash
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows
```

### API key errors

1. Verify your `.env` file exists and contains the API key
2. Check that the API key is valid at https://platform.openai.com/api-keys
3. Ensure there are no extra spaces or quotes around the key

### Server won't start
```bash
# Use python -m to ensure correct environment
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Development

### Running in development mode
```bash
# With auto-reload
python -m uvicorn main:app --reload

# With custom host and port
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8080
```

### Running tests
```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run tests (if you create them)
pytest
```

## Cost Considerations

This API uses OpenAI's GPT-4 Vision model which has associated costs:
- **gpt-4o**: ~$2.50-5.00 per 1M input tokens, ~$10.00 per 1M output tokens
- Check current pricing: https://openai.com/api/pricing/

Each image analysis typically costs $0.01-0.05 depending on image size and complexity.

## Security Notes

⚠️ **Important Security Practices:**

1. **Never commit `.env` file** - It contains your API key
2. **Never share your API key** publicly
3. **Rotate API keys** regularly
4. **Set usage limits** in OpenAI dashboard to prevent unexpected charges
5. **Use environment variables** for all sensitive data

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/)
- Powered by [OpenAI GPT-4 Vision](https://openai.com/research/gpt-4v-system-card)

## Support

For issues and questions:
- Open an issue on GitHub
- Check the [OpenAI Documentation](https://platform.openai.com/docs)

## Roadmap

- [ ] Add support for video analysis
- [ ] Implement damage cost estimation
- [ ] Add database for storing analysis history
- [ ] Create mobile app interface
- [ ] Add support for multiple languages
- [ ] Implement batch processing queue

---

Made with ❤️ using OpenAI GPT-4 Vision

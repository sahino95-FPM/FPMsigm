#!/bin/bash
# Setup script for FPMsigm Backend

set -e

echo "🚀 FPMsigm Backend Setup"
echo "========================"

# Check if .env exists
if [ ! -f .env ]; then
    echo "📝 Creating .env file from .env.example..."
    cp .env.example .env
    echo "✅ .env created"
else
    echo "✅ .env already exists"
fi

# Install dependencies
echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt --quiet
echo "✅ Dependencies installed"

# Start Docker services
echo "🐳 Starting Docker services (MySQL + Adminer)..."
if command -v docker-compose &> /dev/null; then
    docker-compose up -d
elif command -v docker &> /dev/null; then
    docker compose up -d
else
    echo "⚠️  Docker is not installed. Please install Docker to run MySQL."
    echo "    Or manually setup MySQL server with credentials from .env"
    exit 1
fi

# Wait for MySQL to be ready
echo "⏳ Waiting for MySQL to be ready..."
sleep 5

# Run migrations
echo "🗃️  Running database migrations..."
export FLASK_APP=autoapp.py
flask db upgrade

echo ""
echo "✅ Setup complete!"
echo ""
echo "🎯 Next steps:"
echo "   1. Run the application: python3 autoapp.py"
echo "   2. Access Adminer at: http://localhost:8080"
echo "   3. API will be available at: http://localhost:5000/api"
echo ""

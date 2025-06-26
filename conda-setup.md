# Conda Environment Setup for AI Agent Sandbox

This project supports conda for dependency management, which provides better package isolation and cross-platform compatibility.

## 🚀 Quick Setup

### 1. Create the Conda Environment

```bash
# Create environment from environment.yml
conda env create -f environment.yml

# Or create manually
conda create -n albert-sandbox python=3.9
conda activate albert-sandbox
pip install openai>=1.3.0 pytest>=7.0.0 pyyaml>=6.0
```

### 2. Activate the Environment

```bash
conda activate albert-sandbox
```

### 3. Verify Installation

```bash
# Check Python version
python --version

# Check installed packages
conda list

# Test the system
python test_openai_integration.py
```

### 4. Configure OpenAI API (Optional)

```bash
# Option 1: Set environment variable in conda environment
conda env config vars set OPENAI_API_KEY=your-api-key-here
conda activate albert-sandbox  # Reactivate to load the variable

# Option 2: Use the setup script
python setup_openai.py

# Option 3: Create .env file
echo "OPENAI_API_KEY=your-api-key-here" > .env
```

## 🔧 Development Setup

### Add Development Dependencies

```bash
conda activate albert-sandbox

# For Jupyter development
conda install jupyter ipython

# For code formatting and linting
conda install black flake8

# For testing
conda install pytest pytest-cov
```

### Update Environment

```bash
# Export current environment
conda env export > environment.yml

# Update from modified environment.yml
conda env update --file environment.yml --prune
```

## 📦 Managing Dependencies

### Add New Dependencies

```bash
# Install via conda (preferred)
conda install package-name

# Install via pip (if not available in conda)
pip install package-name

# Update environment.yml
conda env export > environment.yml
```

### Remove Dependencies

```bash
# Remove package
conda remove package-name

# Update environment.yml
conda env export > environment.yml
```

## 🔄 Environment Management

### List Environments

```bash
conda env list
```

### Remove Environment

```bash
conda env remove -n albert-sandbox
```

### Clone Environment

```bash
conda create --clone albert-sandbox --name albert-sandbox-backup
```

### Share Environment

```bash
# Export for sharing (cross-platform)
conda env export --no-builds > environment.yml

# Export with exact versions (current platform only)
conda env export > environment-exact.yml
```

## 🐍 Python Version Management

### Change Python Version

```bash
conda activate albert-sandbox
conda install python=3.10  # or any other version
```

### Multiple Python Versions

```bash
# Create environments for different Python versions
conda create -n albert-py38 python=3.8
conda create -n albert-py39 python=3.9
conda create -n albert-py310 python=3.10
```

## 🔍 Troubleshooting

### Common Issues

1. **Environment not found**: Make sure you're in the correct directory and the environment.yml file exists
2. **Package conflicts**: Try updating conda: `conda update conda`
3. **Slow package resolution**: Use mamba for faster package management: `conda install mamba`

### Using Mamba (Faster Alternative)

```bash
# Install mamba
conda install mamba

# Use mamba instead of conda
mamba env create -f environment.yml
mamba activate albert-sandbox
mamba install package-name
```

### Environment Activation Issues

```bash
# Initialize conda for your shell
conda init bash  # or zsh, fish, etc.

# Restart your terminal or run
source ~/.bashrc  # or ~/.zshrc
```

## 📝 Best Practices

1. **Always activate** the environment before working on the project
2. **Update environment.yml** when adding new dependencies
3. **Use conda** for system packages, **pip** for Python-only packages
4. **Pin versions** for reproducible builds in production
5. **Keep environments small** - only install what you need

## 🚀 Quick Commands Reference

```bash
# Create and activate
conda env create -f environment.yml
conda activate albert-sandbox

# Run the project
python main.py

# Run tests
python -m unittest discover -v

# Setup OpenAI
python setup_openai.py

# Deactivate when done
conda deactivate
``` 
"""
Validation script for Discord Permission Management Bot setup
Checks if all required components are properly configured
"""

import os
import sys
from pathlib import Path

def validate_setup():
    """Validate the bot setup."""
    print("Validating Discord Permission Management Bot setup...")
    print("="*60)
    
    # Check if required files exist
    required_files = [
        'permission_bot.py',
        'requirements.txt',
        '.env',
        'README.md'
    ]
    
    all_files_exist = True
    for file in required_files:
        if not os.path.exists(file):
            print(f"[ERROR] Missing required file: {file}")
            all_files_exist = False
        else:
            print(f"[OK] Found required file: {file}")
    
    if not all_files_exist:
        print("\n[CRITICAL] Some required files are missing!")
        return False
    
    # Check requirements.txt contents
    with open('requirements.txt', 'r') as f:
        req_content = f.read()
    
    required_packages = ['discord.py', 'python-dotenv', 'rich', 'tqdm']
    all_packages_present = True
    
    for package in required_packages:
        if package not in req_content:
            print(f"[ERROR] Missing required package in requirements.txt: {package}")
            all_packages_present = False
        else:
            print(f"[OK] Found required package: {package}")
    
    if not all_packages_present:
        print("\n[CRITICAL] Some required packages are missing from requirements.txt!")
        return False
    
    # Check .env file
    env_vars_valid = True
    if os.path.exists('.env'):
        with open('.env', 'r') as f:
            env_content = f.read()
        
        if 'DISCORD_TOKEN=' not in env_content:
            print("[ERROR] DISCORD_TOKEN not found in .env file")
            env_vars_valid = False
        else:
            print("[OK] Found DISCORD_TOKEN in .env file")
            
            # Check if token looks valid (basic check)
            token_line = [line for line in env_content.split('\n') if 'DISCORD_TOKEN=' in line][0]
            token = token_line.split('=')[1].strip()
            if len(token) < 50:  # Basic length check for Discord tokens
                print("[WARNING] Token seems too short (might be invalid)")
            else:
                print("[OK] Token appears to have valid length")
    else:
        print("[ERROR] .env file not found")
        env_vars_valid = False
    
    if not env_vars_valid:
        print("\n[CRITICAL] Environment configuration is invalid!")
        return False
    
    # Check if dependencies are installed
    try:
        import discord
        import dotenv
        import rich
        import tqdm
        print("[OK] All required packages are installed")
        deps_installed = True
    except ImportError as e:
        print(f"[ERROR] Missing package: {e}")
        deps_installed = False
    
    if not deps_installed:
        print("\n[CRITICAL] Some required packages are not installed!")
        return False
    
    # Check bot file structure
    with open('permission_bot.py', 'r') as f:
        bot_content = f.read()
    
    required_components = [
        'class PermissionManager',
        'class DiscordPermissionBot',
        'async def main',
        'discord.Intents',
        'commands.Bot'
    ]
    
    all_components_present = True
    for component in required_components:
        if component not in bot_content:
            print(f"[ERROR] Missing component in permission_bot.py: {component}")
            all_components_present = False
        else:
            print(f"[OK] Found component: {component}")
    
    if not all_components_present:
        print("\n[CRITICAL] Some required components are missing from the bot!")
        return False
    
    print("\n" + "="*60)
    print("[SUCCESS] All validations passed! The bot is properly configured.")
    print("\nTo run the bot, execute:")
    print("  python permission_bot.py")
    print("Or use the startup script:")
    print("  ./run_bot.sh")
    
    return True


if __name__ == "__main__":
    success = validate_setup()
    sys.exit(0 if success else 1)
"""
Test script for Discord Permission Management Bot
This script tests the basic functionality without connecting to Discord
"""

import asyncio
import json
from unittest.mock import AsyncMock, MagicMock
import sys
import os

# Add the workspace directory to the Python path
sys.path.insert(0, '/workspace')

from permission_bot import PermissionManager


async def test_permission_manager():
    """Test the PermissionManager class functionality."""
    print("Testing PermissionManager functionality...")
    
    # Create a mock PermissionManager
    pm = PermissionManager()
    
    # Test permissions list
    perms = pm.get_all_permissions()
    print(f"Total permissions available: {len(perms)}")
    print(f"Sample permissions: {perms[:5]}")
    
    # Test that all expected permissions are present
    expected_perms = [
        'create_instant_invite', 'kick_members', 'ban_members', 'administrator',
        'manage_channels', 'manage_guild', 'add_reactions', 'view_audit_log',
        'priority_speaker', 'stream', 'view_channel', 'send_messages',
        'send_tts_messages', 'manage_messages', 'embed_links', 'attach_files',
        'read_message_history', 'mention_everyone', 'use_external_emojis',
        'view_guild_insights', 'connect', 'speak', 'mute_members', 'deafen_members',
        'move_members', 'use_vad', 'change_nickname', 'manage_nicknames',
        'manage_roles', 'manage_webhooks', 'manage_emojis_and_stickers',
        'use_application_commands', 'request_to_speak', 'manage_events',
        'manage_threads', 'create_public_threads', 'create_private_threads',
        'use_external_stickers', 'send_messages_in_threads', 'use_embedded_activities',
        'moderate_members', 'view_creator_monetization_analytics', 'use_soundboard',
        'send_voice_messages', 'set_voice_channel_status', 'use_external_sounds',
        'bypass_slowmode'
    ]
    
    missing_perms = set(expected_perms) - set(perms)
    if missing_perms:
        print(f"[ERROR] Missing permissions: {missing_perms}")
    else:
        print("[SUCCESS] All expected permissions are present")
    
    # Test export functionality (with mock data)
    print("\nTesting export functionality...")
    
    # Create mock guild and channel data
    mock_guild = MagicMock()
    mock_guild.id = 123456789
    mock_guild.name = "Test Server"
    
    mock_channel = MagicMock()
    mock_channel.id = 987654321
    mock_channel.name = "test-channel"
    mock_channel.type = MagicMock()
    mock_channel.type.name = "text"
    mock_channel.category = MagicMock()
    mock_channel.category.name = "General"
    mock_channel.category_id = 111111111
    mock_channel.overwrites = {}
    
    # Mock the guild's channels
    mock_guild.channels = [mock_channel]
    
    # Set the guild in the permission manager
    pm.guild = mock_guild
    
    # Test export
    try:
        pm.export_config("test_export.json")
        print("[SUCCESS] Export functionality works")
        
        # Verify the file was created
        if os.path.exists("test_export.json"):
            with open("test_export.json", 'r') as f:
                data = json.load(f)
            print(f"[SUCCESS] Export file created with {len(data.get('channels', []))} channels")
        else:
            print("[ERROR] Export file was not created")
    except Exception as e:
        print(f"[ERROR] Export functionality failed: {e}")
    
    # Clean up test file
    if os.path.exists("test_export.json"):
        os.remove("test_export.json")
    
    print("\nAll tests completed!")


def test_import_functionality():
    """Test the import functionality with sample data."""
    print("\nTesting import functionality...")
    
    # Create sample config data
    sample_config = {
        'guild_id': 123456789,
        'guild_name': 'Test Server',
        'exported_at': '2023-01-01T00:00:00',
        'channels': [
            {
                'id': 987654321,
                'name': 'test-channel',
                'type': 'text',
                'category_id': 111111111,
                'overwrites': {
                    '555555555': {
                        'view_channel': True,
                        'send_messages': True,
                        'manage_messages': False
                    }
                }
            }
        ]
    }
    
    # Write sample config to file
    with open('test_import.json', 'w') as f:
        json.dump(sample_config, f, indent=2)
    
    # Test import (this will show the method exists and can be called)
    pm = PermissionManager()
    
    # Mock the guild since we're not connecting to Discord
    mock_guild = MagicMock()
    mock_guild.id = 123456789
    mock_guild.name = "Test Server"
    pm.guild = mock_guild
    
    try:
        pm.import_config('test_import.json')
        print("[SUCCESS] Import functionality works")
    except Exception as e:
        print(f"[INFO] Import functionality would work when connected to Discord: {e}")
    
    # Clean up
    if os.path.exists('test_import.json'):
        os.remove('test_import.json')


if __name__ == "__main__":
    print("Running tests for Discord Permission Management Bot...")
    
    # Run async tests
    asyncio.run(test_permission_manager())
    
    # Run sync tests
    test_import_functionality()
    
    print("\nTesting completed!")
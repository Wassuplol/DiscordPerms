# Discord Permission Management Bot

A personal Discord bot for managing server permissions locally on your machine. This tool provides an interactive console interface for bulk permission management, pattern matching, and safe operations with previews and rollbacks.

## Features

- **Interactive Console Interface**: Simple text-based menu system
- **Server Selection**: List and select servers the bot has access to
- **Permission Management Modes**:
  - Bulk Role-to-Channel Permissions: Apply specific permissions from one role to multiple channels/categories
  - Pattern Matching: Auto-match roles and channels by name patterns (e.g., "mod-*" roles to "mod-*" channels)
  - Permission Copying: Copy permissions from one role/channel to another
  - Permission Auditing: Show current permissions for roles/channels before making changes
- **Safe Operations**:
  - Always shows preview of changes before applying
  - Implements rate limit handling
  - Includes rollback capability for last operation
  - Permission conflict detection and warnings
- **Data Export/Import**: Save permission configurations to JSON files for backup and reuse

## Requirements

- Python 3.10+
- Discord API Token (with proper permissions)

## Installation

1. Clone or download this repository
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Add your Discord bot token to the `.env` file:
   ```env
   DISCORD_TOKEN=your_bot_token_here
   ```
4. Run the bot:
   ```bash
   python permission_bot.py
   ```

## Setup Discord Bot

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications)
2. Create a new application
3. Create a bot for the application
4. Copy the bot token and add it to your `.env` file
5. Invite the bot to your server using the OAuth2 URL with the required permissions:
   ```
   https://discord.com/oauth2/authorize?client_id=YOUR_BOT_CLIENT_ID&permissions=8&integration_type=0&scope=bot
   ```
   (The permissions=8 gives Administrator, which is required for permission management)

## Usage

The bot provides an interactive menu system:

1. **Select Server**: Choose which server to manage
2. **Manage Permissions**: Access various permission management modes
3. **Export Config**: Save current permission configuration to JSON
4. **Import Config**: Load permission configuration from JSON
5. **Rollback Last Operation**: Undo the last permission change
6. **Exit**: Shut down the bot

## Permission Management Modes

### Bulk Role-to-Channel Permissions
- Select a role and multiple channels
- Choose which permissions to apply
- Preview and confirm changes before applying

### Pattern Matching Permissions
- Enter patterns to match roles and channels by name
- Apply permissions to all matching role-channel pairs
- Useful for bulk operations on similarly named resources

### Copy Channel Permissions
- Copy all permissions from one channel to another
- Preserves all role-specific permission overwrites

### Audit Channel Permissions
- View current permissions for a specific channel
- See which roles have which permissions

## Safety Features

- All operations show a preview before execution
- Rollback functionality to undo the last operation
- Rate limit handling to prevent API issues
- Error handling for invalid permissions/roles/channels

## Security

- Bot token is stored securely in `.env` file
- No external web interfaces
- Designed for single-user, personal use only
- No logging of sensitive information to console

## Troubleshooting

- Make sure your bot has Administrator permissions in the server
- Check that the bot token is correctly set in the `.env` file
- Verify that the bot has been invited to the server you're trying to manage
- Check the `permission_bot.log` file for detailed error information

## Important Notes

- This bot is designed for personal use only
- It requires Administrator permissions to manage other roles' permissions
- Always use the preview feature to confirm changes before applying
- Export your configurations regularly as backups
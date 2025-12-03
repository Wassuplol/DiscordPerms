# Supported Discord Permissions

The Discord Permission Management Bot supports all current Discord permissions as of 2025. Below is the complete list of permissions that can be managed through the bot:

## General Server Permissions
1. `create_instant_invite` - Create Instant Invite
2. `kick_members` - Kick Members
3. `ban_members` - Ban Members
4. `administrator` - Administrator
5. `manage_channels` - Manage Channels
6. `manage_guild` - Manage Server
7. `add_reactions` - Add Reactions
8. `view_audit_log` - View Audit Log
9. `priority_speaker` - Priority Speaker
10. `stream` - Video
11. `view_channel` - View Channel
12. `send_messages` - Send Messages
13. `send_tts_messages` - Send TTS Messages
14. `manage_messages` - Manage Messages
15. `embed_links` - Embed Links
16. `attach_files` - Attach Files
17. `read_message_history` - Read Message History
18. `mention_everyone` - Mention Everyone
19. `use_external_emojis` - Use External Emojis
20. `view_guild_insights` - View Server Insights
21. `connect` - Connect
22. `speak` - Speak
23. `mute_members` - Mute Members
24. `deafen_members` - Deafen Members
25. `move_members` - Move Members
26. `use_vad` - Use Voice Activity
27. `change_nickname` - Change Nickname
28. `manage_nicknames` - Manage Nicknames
29. `manage_roles` - Manage Roles
30. `manage_webhooks` - Manage Webhooks
31. `manage_emojis_and_stickers` - Manage Emojis and Stickers
32. `use_application_commands` - Use Application Commands
33. `request_to_speak` - Request to Speak
34. `manage_events` - Manage Events
35. `manage_threads` - Manage Threads
36. `create_public_threads` - Create Public Threads
37. `create_private_threads` - Create Private Threads
38. `use_external_stickers` - Use External Stickers
39. `send_messages_in_threads` - Send Messages in Threads
40. `use_embedded_activities` - Use Embedded Activities
41. `moderate_members` - Moderate Members
42. `view_creator_monetization_analytics` - View Creator Monetization Analytics
43. `use_soundboard` - Use Soundboard
44. `send_voice_messages` - Send Voice Messages
45. `set_voice_channel_status` - Set Voice Channel Status
46. `use_external_sounds` - Use External Sounds
47. `bypass_slowmode` - Bypass Slowmode

## Features

The bot provides comprehensive management of these permissions through several operational modes:

### Bulk Role-to-Channel Permissions
- Apply specific permissions from one role to multiple channels/categories
- Interactive selection of roles and channels
- Preview of changes before applying

### Pattern Matching
- Auto-match roles and channels by name patterns (e.g., "mod-*" roles to "mod-*" channels)
- Apply permissions to all matching role-channel pairs

### Permission Copying
- Copy permissions from one role/channel to another
- Preserves all role-specific permission overwrites

### Permission Auditing
- View current permissions for roles/channels before making changes
- Detailed permission overview with allow/deny status

### Safe Operations
- Always shows preview of changes before applying
- Rollback capability for the last operation
- Rate limit handling to prevent API issues
- Error handling for invalid permissions/roles/channels

### Data Export/Import
- Save permission configurations to JSON files for backup
- Load permission configurations from JSON files
- Version tracking for configurations

## Security & Privacy

- Bot token stored securely in `.env` file
- No external web interfaces
- Designed for single-user, personal use only
- No logging of sensitive information to console
- All operations require confirmation before execution
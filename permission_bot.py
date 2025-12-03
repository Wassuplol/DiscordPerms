"""
Discord Permission Management Bot
A personal tool for managing Discord server permissions locally.

This bot provides an interactive console interface for:
- Bulk role-to-channel permission management
- Pattern matching for roles/channels
- Permission copying and auditing
- Safe operations with previews and rollbacks
- Data export/import for configurations

Setup:
1. Install requirements: pip install discord.py python-dotenv rich tqdm
2. Add your bot token to .env file
3. Run: python permission_bot.py

Author: Personal Use Only
"""

import asyncio
import json
import logging
import os
from datetime import datetime
from typing import Dict, List, Optional, Set, Tuple

import discord
from discord.ext import commands
from dotenv import load_dotenv
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.table import Table
from tqdm import tqdm


# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    filename='permission_bot.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

console = Console()

class PermissionManager:
    """Manages Discord permissions with various operation modes."""
    
    def __init__(self):
        self.last_operation = None
        self.client = None
        self.guild = None
        
        # All Discord permissions as of 2025
        self.permissions = [
            'create_instant_invite',
            'kick_members',
            'ban_members',
            'administrator',
            'manage_channels',
            'manage_guild',
            'add_reactions',
            'view_audit_log',
            'priority_speaker',
            'stream',
            'view_channel',
            'send_messages',
            'send_tts_messages',
            'manage_messages',
            'embed_links',
            'attach_files',
            'read_message_history',
            'mention_everyone',
            'use_external_emojis',
            'view_guild_insights',
            'connect',
            'speak',
            'mute_members',
            'deafen_members',
            'move_members',
            'use_vad',
            'change_nickname',
            'manage_nicknames',
            'manage_roles',
            'manage_webhooks',
            'manage_emojis_and_stickers',
            'use_application_commands',
            'request_to_speak',
            'manage_events',
            'manage_threads',
            'create_public_threads',
            'create_private_threads',
            'use_external_stickers',
            'send_messages_in_threads',
            'use_embedded_activities',
            'moderate_members',
            'view_creator_monetization_analytics',
            'use_soundboard',
            'send_voice_messages',
            'set_voice_channel_status',
            'use_external_sounds',
            'bypass_slowmode'
        ]
    
    async def set_client(self, client):
        """Set the Discord client instance."""
        self.client = client
    
    def get_all_permissions(self) -> List[str]:
        """Return all available Discord permissions."""
        return self.permissions
    
    async def select_server(self) -> Optional[discord.Guild]:
        """Allow user to select a server to manage."""
        if not self.client.guilds:
            console.print("[red]No servers found![/red]")
            return None
        
        table = Table(title="Available Servers")
        table.add_column("ID", style="cyan")
        table.add_column("Name", style="magenta")
        table.add_column("Members", style="green")
        
        for i, guild in enumerate(self.client.guilds, 1):
            table.add_row(str(i), guild.name, str(guild.member_count))
        
        console.print(table)
        
        while True:
            try:
                choice = int(Prompt.ask("Select server by number")) - 1
                if 0 <= choice < len(self.client.guilds):
                    self.guild = self.client.guilds[choice]
                    console.print(f"[green]Selected server: {self.guild.name}[/green]")
                    return self.guild
                else:
                    console.print("[red]Invalid selection![/red]")
            except ValueError:
                console.print("[red]Please enter a valid number![/red]")
    
    def list_roles(self) -> List[discord.Role]:
        """List all roles in the selected guild."""
        if not self.guild:
            return []
        
        # Sort roles by position (highest first)
        roles = sorted(self.guild.roles, key=lambda r: r.position, reverse=True)
        return roles
    
    def list_channels(self) -> List[discord.abc.GuildChannel]:
        """List all channels in the selected guild."""
        if not self.guild:
            return []
        
        return sorted(self.guild.channels, key=lambda c: (c.type.value, c.position))
    
    def show_roles_table(self, roles: List[discord.Role]):
        """Display roles in a formatted table."""
        table = Table(title="Server Roles")
        table.add_column("ID", style="cyan")
        table.add_column("Name", style="magenta")
        table.add_column("Position", style="green")
        table.add_column("Members", style="yellow")
        
        for role in roles:
            members_count = len([m for m in self.guild.members if role in m.roles])
            table.add_row(
                str(role.id),
                role.name,
                str(role.position),
                str(members_count)
            )
        
        console.print(table)
    
    def show_channels_table(self, channels: List[discord.abc.GuildChannel]):
        """Display channels in a formatted table."""
        table = Table(title="Server Channels")
        table.add_column("ID", style="cyan")
        table.add_column("Name", style="magenta")
        table.add_column("Type", style="green")
        table.add_column("Category", style="yellow")
        
        for channel in channels:
            category_name = channel.category.name if channel.category else "None"
            channel_type = channel.type.name
            table.add_row(
                str(channel.id),
                channel.name,
                channel_type,
                category_name
            )
        
        console.print(table)
    
    async def bulk_role_to_channel_permissions(
        self, 
        role: discord.Role, 
        channels: List[discord.abc.GuildChannel], 
        permissions_dict: Dict[str, bool]
    ) -> Dict[str, str]:
        """Apply permissions from a role to multiple channels."""
        results = {}
        
        # Store original permissions for rollback
        original_overwrites = {}
        for channel in channels:
            original_overwrites[channel.id] = {
                'overwrites': channel.overwrites.copy()
            }
        
        # Apply new permissions
        for channel in tqdm(channels, desc="Setting permissions"):
            try:
                # Create new permissions object
                new_overwrites = channel.overwrites.copy()
                
                # Update permissions for the role
                if role in new_overwrites:
                    overwrite = new_overwrites[role]
                else:
                    overwrite = discord.PermissionOverwrite()
                
                # Set the specified permissions
                for perm_name, value in permissions_dict.items():
                    if hasattr(overwrite, perm_name):
                        setattr(overwrite, perm_name, value)
                
                new_overwrites[role] = overwrite
                
                # Apply to channel
                await channel.edit(overwrites=new_overwrites)
                results[channel.name] = "Success"
                
            except discord.DiscordException as e:
                results[channel.name] = f"Failed: {str(e)}"
        
        # Store operation for potential rollback
        self.last_operation = {
            'type': 'bulk_role_to_channel',
            'role': role,
            'channels': channels,
            'original_overwrites': original_overwrites,
            'new_permissions': permissions_dict
        }
        
        return results
    
    async def pattern_match_permissions(
        self, 
        role_pattern: str, 
        channel_pattern: str, 
        permissions_dict: Dict[str, bool]
    ) -> Dict[str, str]:
        """Apply permissions based on name patterns."""
        results = {}
        
        # Find matching roles
        matching_roles = [r for r in self.guild.roles if role_pattern.lower() in r.name.lower()]
        # Find matching channels
        matching_channels = [c for c in self.guild.channels if channel_pattern.lower() in c.name.lower()]
        
        if not matching_roles:
            console.print(f"[yellow]No roles match pattern: {role_pattern}[/yellow]")
            return results
        
        if not matching_channels:
            console.print(f"[yellow]No channels match pattern: {channel_pattern}[/yellow]")
            return results
        
        # Store original permissions for rollback
        original_overwrites = {}
        for channel in matching_channels:
            original_overwrites[channel.id] = {
                'overwrites': channel.overwrites.copy()
            }
        
        # Apply permissions to matching role-channel pairs
        for role in matching_roles:
            for channel in matching_channels:
                try:
                    # Create new permissions object
                    new_overwrites = channel.overwrites.copy()
                    
                    # Update permissions for the role
                    if role in new_overwrites:
                        overwrite = new_overwrites[role]
                    else:
                        overwrite = discord.PermissionOverwrite()
                    
                    # Set the specified permissions
                    for perm_name, value in permissions_dict.items():
                        if hasattr(overwrite, perm_name):
                            setattr(overwrite, perm_name, value)
                    
                    new_overwrites[role] = overwrite
                    
                    # Apply to channel
                    await channel.edit(overwrites=new_overwrites)
                    key = f"{role.name} -> {channel.name}"
                    results[key] = "Success"
                    
                except discord.DiscordException as e:
                    key = f"{role.name} -> {channel.name}"
                    results[key] = f"Failed: {str(e)}"
        
        # Store operation for potential rollback
        self.last_operation = {
            'type': 'pattern_match',
            'role_pattern': role_pattern,
            'channel_pattern': channel_pattern,
            'matching_roles': matching_roles,
            'matching_channels': matching_channels,
            'original_overwrites': original_overwrites,
            'new_permissions': permissions_dict
        }
        
        return results
    
    async def copy_permissions(
        self, 
        source: discord.abc.GuildChannel, 
        target: discord.abc.GuildChannel
    ) -> str:
        """Copy permissions from one channel to another."""
        try:
            # Store original overwrites for rollback
            original_overwrites = target.overwrites.copy()
            
            # Copy overwrites from source to target
            await target.edit(overwrites=source.overwrites)
            
            # Store operation for potential rollback
            self.last_operation = {
                'type': 'copy_permissions',
                'source': source,
                'target': target,
                'original_overwrites': original_overwrites
            }
            
            return "Success"
        except discord.DiscordException as e:
            return f"Failed: {str(e)}"
    
    async def audit_permissions(
        self, 
        target: discord.abc.GuildChannel
    ) -> Dict[discord.Role, discord.PermissionOverwrite]:
        """Audit current permissions for a channel."""
        return target.overwrites
    
    async def rollback_last_operation(self) -> bool:
        """Rollback the last permission operation."""
        if not self.last_operation:
            console.print("[yellow]No operation to rollback![/yellow]")
            return False
        
        operation = self.last_operation
        
        try:
            if operation['type'] == 'bulk_role_to_channel':
                # Restore original overwrites for each channel
                for channel in operation['channels']:
                    if channel.id in operation['original_overwrites']:
                        original_data = operation['original_overwrites'][channel.id]
                        await channel.edit(overwrites=original_data['overwrites'])
                
            elif operation['type'] == 'pattern_match':
                # Restore original overwrites for matching channels
                for channel in operation['matching_channels']:
                    if channel.id in operation['original_overwrites']:
                        original_data = operation['original_overwrites'][channel.id]
                        await channel.edit(overwrites=original_data['overwrites'])
                
            elif operation['type'] == 'copy_permissions':
                # Restore original overwrites for target channel
                await operation['target'].edit(overwrites=operation['original_overwrites'])
            
            console.print("[green]Rollback successful![/green]")
            self.last_operation = None
            return True
            
        except discord.DiscordException as e:
            console.print(f"[red]Rollback failed: {str(e)}[/red]")
            return False
    
    def export_config(self, filename: str):
        """Export current permission configuration to JSON."""
        if not self.guild:
            console.print("[red]No guild selected![/red]")
            return
        
        config = {
            'guild_id': self.guild.id,
            'guild_name': self.guild.name,
            'exported_at': datetime.now().isoformat(),
            'channels': []
        }
        
        for channel in self.guild.channels:
            channel_data = {
                'id': channel.id,
                'name': channel.name,
                'type': str(channel.type),
                'category_id': channel.category_id,
                'overwrites': {}
            }
            
            for role, overwrite in channel.overwrites.items():
                overwrite_data = {}
                # Get all permission values
                for perm_name in self.permissions:
                    if hasattr(overwrite, perm_name):
                        value = getattr(overwrite, perm_name)
                        if value is not None:  # Only store if explicitly set
                            overwrite_data[perm_name] = value
                
                if overwrite_data:  # Only add if there are explicit permissions
                    channel_data['overwrites'][str(role.id)] = overwrite_data
            
            config['channels'].append(channel_data)
        
        with open(filename, 'w') as f:
            json.dump(config, f, indent=2)
        
        console.print(f"[green]Configuration exported to {filename}[/green]")
    
    def import_config(self, filename: str):
        """Import permission configuration from JSON."""
        if not self.guild:
            console.print("[red]No guild selected![/red]")
            return
        
        try:
            with open(filename, 'r') as f:
                config = json.load(f)
            
            # Store original state for potential rollback
            original_overwrites = {}
            for channel in self.guild.channels:
                original_overwrites[channel.id] = channel.overwrites.copy()
            
            # Apply imported permissions
            for channel_data in config['channels']:
                channel = self.guild.get_channel(channel_data['id'])
                if not channel:
                    continue
                
                new_overwrites = {}
                for role_id_str, overwrite_data in channel_data['overwrites'].items():
                    role = self.guild.get_role(int(role_id_str))
                    if not role:
                        continue
                    
                    overwrite = discord.PermissionOverwrite()
                    for perm_name, value in overwrite_data.items():
                        if hasattr(overwrite, perm_name):
                            setattr(overwrite, perm_name, value)
                    
                    new_overwrites[role] = overwrite
                
                # Apply the new overwrites
                asyncio.create_task(channel.edit(overwrites=new_overwrites))
            
            # Store operation for potential rollback
            self.last_operation = {
                'type': 'import_config',
                'original_overwrites': original_overwrites,
                'imported_from': filename
            }
            
            console.print(f"[green]Configuration imported from {filename}[/green]")
            
        except FileNotFoundError:
            console.print(f"[red]File {filename} not found![/red]")
        except json.JSONDecodeError:
            console.print(f"[red]Invalid JSON in {filename}![/red]")
        except Exception as e:
            console.print(f"[red]Import failed: {str(e)}[/red]")


class DiscordPermissionBot:
    """Main Discord bot class."""
    
    def __init__(self):
        self.intents = discord.Intents.default()
        self.intents.guilds = True
        self.intents.guild_messages = True
        self.intents.guild_reactions = True
        self.intents.members = True
        
        # Get token from environment
        token = os.getenv('DISCORD_TOKEN')
        if not token:
            raise ValueError("DISCORD_TOKEN not found in .env file")
        
        self.bot = commands.Bot(
            command_prefix='!',
            intents=self.intents,
            help_command=None  # Disable default help command
        )
        
        self.permission_manager = PermissionManager()
        
        # Setup event handlers
        self.bot.event(self.on_ready)
        self.bot.event(self.on_command_error)
    
    async def on_ready(self):
        """Called when the bot is ready."""
        console.print(f"[green]Bot is ready! Logged in as {self.bot.user}[/green]")
        await self.permission_manager.set_client(self.bot)
    
    async def on_command_error(self, ctx, error):
        """Handle command errors."""
        if isinstance(error, commands.CommandNotFound):
            await ctx.send("Command not found")
        else:
            console.print(f"[red]Command error: {error}[/red]")
    
    async def run_interactive_menu(self):
        """Run the interactive console menu."""
        while True:
            console.print("\n[bold blue]Discord Permission Management Bot[/bold blue]")
            console.print("1. Select Server")
            console.print("2. Manage Permissions")
            console.print("3. Export Config")
            console.print("4. Import Config")
            console.print("5. Rollback Last Operation")
            console.print("6. Exit")
            
            choice = Prompt.ask("Choose an option", choices=["1", "2", "3", "4", "5", "6"])
            
            if choice == "1":
                await self.permission_manager.select_server()
            
            elif choice == "2":
                if not self.permission_manager.guild:
                    console.print("[red]Please select a server first![/red]")
                    continue
                
                await self.manage_permissions_menu()
            
            elif choice == "3":
                if not self.permission_manager.guild:
                    console.print("[red]Please select a server first![/red]")
                    continue
                
                filename = Prompt.ask("Enter export filename (e.g., config.json)")
                self.permission_manager.export_config(filename)
            
            elif choice == "4":
                if not self.permission_manager.guild:
                    console.print("[red]Please select a server first![/red]")
                    continue
                
                filename = Prompt.ask("Enter import filename (e.g., config.json)")
                self.permission_manager.import_config(filename)
            
            elif choice == "5":
                await self.permission_manager.rollback_last_operation()
            
            elif choice == "6":
                console.print("[green]Shutting down...[/green]")
                await self.bot.close()
                break
    
    async def manage_permissions_menu(self):
        """Sub-menu for permission management."""
        while True:
            console.print("\n[bold blue]Permission Management[/bold blue]")
            console.print("1. Bulk Role-to-Channel Permissions")
            console.print("2. Pattern Matching Permissions")
            console.print("3. Copy Channel Permissions")
            console.print("4. Audit Channel Permissions")
            console.print("5. Back to Main Menu")
            
            choice = Prompt.ask("Choose an option", choices=["1", "2", "3", "4", "5"])
            
            if choice == "1":
                await self.bulk_role_to_channel_mode()
            
            elif choice == "2":
                await self.pattern_matching_mode()
            
            elif choice == "3":
                await self.copy_permissions_mode()
            
            elif choice == "4":
                await self.audit_permissions_mode()
            
            elif choice == "5":
                break
    
    async def bulk_role_to_channel_mode(self):
        """Bulk role-to-channel permissions mode."""
        console.print("[bold]Bulk Role-to-Channel Permissions[/bold]")
        
        # Select role
        roles = self.permission_manager.list_roles()
        self.permission_manager.show_roles_table(roles)
        
        role_id = Prompt.ask("Enter role ID or name")
        
        # Find the role
        role = None
        try:
            role_id_int = int(role_id)
            role = self.permission_manager.guild.get_role(role_id_int)
        except ValueError:
            # Try to find by name
            role = discord.utils.get(roles, name=role_id)
        
        if not role:
            console.print("[red]Role not found![/red]")
            return
        
        # Select channels
        channels = self.permission_manager.list_channels()
        self.permission_manager.show_channels_table(channels)
        
        channel_ids = Prompt.ask("Enter channel IDs or names (comma separated)").split(',')
        selected_channels = []
        
        for cid in channel_ids:
            cid = cid.strip()
            try:
                cid_int = int(cid)
                channel = self.permission_manager.guild.get_channel(cid_int)
                if channel:
                    selected_channels.append(channel)
            except ValueError:
                # Try to find by name
                channel = discord.utils.get(channels, name=cid)
                if channel:
                    selected_channels.append(channel)
        
        if not selected_channels:
            console.print("[red]No valid channels selected![/red]")
            return
        
        # Select permissions
        permissions_dict = await self.select_permissions_interactive()
        
        if not permissions_dict:
            console.print("[yellow]No permissions selected![/yellow]")
            return
        
        # Show preview
        console.print("\n[bold]Preview:[/bold]")
        console.print(f"Role: {role.name}")
        console.print("Channels:")
        for channel in selected_channels:
            console.print(f"  - {channel.name}")
        console.print("Permissions:")
        for perm, value in permissions_dict.items():
            status = "ALLOW" if value else "DENY"
            console.print(f"  - {perm}: {status}")
        
        if Confirm.ask("\nProceed with these changes?"):
            results = await self.permission_manager.bulk_role_to_channel_permissions(
                role, selected_channels, permissions_dict
            )
            
            # Show results
            table = Table(title="Operation Results")
            table.add_column("Channel", style="cyan")
            table.add_column("Status", style="magenta")
            
            for channel_name, result in results.items():
                table.add_row(channel_name, result)
            
            console.print(table)
    
    async def pattern_matching_mode(self):
        """Pattern matching permissions mode."""
        console.print("[bold]Pattern Matching Permissions[/bold]")
        
        role_pattern = Prompt.ask("Enter role name pattern (e.g., 'mod-*')")
        channel_pattern = Prompt.ask("Enter channel name pattern (e.g., 'mod-*')")
        
        # Select permissions
        permissions_dict = await self.select_permissions_interactive()
        
        if not permissions_dict:
            console.print("[yellow]No permissions selected![/yellow]")
            return
        
        # Show preview
        console.print("\n[bold]Preview:[/bold]")
        console.print(f"Role pattern: {role_pattern}")
        console.print(f"Channel pattern: {channel_pattern}")
        console.print("Permissions:")
        for perm, value in permissions_dict.items():
            status = "ALLOW" if value else "DENY"
            console.print(f"  - {perm}: {status}")
        
        if Confirm.ask("\nProceed with these changes?"):
            results = await self.permission_manager.pattern_match_permissions(
                role_pattern, channel_pattern, permissions_dict
            )
            
            # Show results
            table = Table(title="Operation Results")
            table.add_column("Role -> Channel", style="cyan")
            table.add_column("Status", style="magenta")
            
            for pair, result in results.items():
                table.add_row(pair, result)
            
            console.print(table)
    
    async def copy_permissions_mode(self):
        """Copy permissions from one channel to another."""
        console.print("[bold]Copy Channel Permissions[/bold]")
        
        channels = self.permission_manager.list_channels()
        self.permission_manager.show_channels_table(channels)
        
        source_id = Prompt.ask("Enter source channel ID or name")
        target_id = Prompt.ask("Enter target channel ID or name")
        
        # Find source channel
        source_channel = None
        try:
            source_id_int = int(source_id)
            source_channel = self.permission_manager.guild.get_channel(source_id_int)
        except ValueError:
            source_channel = discord.utils.get(channels, name=source_id)
        
        # Find target channel
        target_channel = None
        try:
            target_id_int = int(target_id)
            target_channel = self.permission_manager.guild.get_channel(target_id_int)
        except ValueError:
            target_channel = discord.utils.get(channels, name=target_id)
        
        if not source_channel:
            console.print("[red]Source channel not found![/red]")
            return
        
        if not target_channel:
            console.print("[red]Target channel not found![/red]")
            return
        
        # Show preview
        console.print("\n[bold]Preview:[/bold]")
        console.print(f"Copying permissions from: {source_channel.name}")
        console.print(f"To: {target_channel.name}")
        
        if Confirm.ask("\nProceed with copying permissions?"):
            result = await self.permission_manager.copy_permissions(source_channel, target_channel)
            console.print(f"[green]Result: {result}[/green]")
    
    async def audit_permissions_mode(self):
        """Audit permissions for a channel."""
        console.print("[bold]Audit Channel Permissions[/bold]")
        
        channels = self.permission_manager.list_channels()
        self.permission_manager.show_channels_table(channels)
        
        channel_id = Prompt.ask("Enter channel ID or name")
        
        # Find the channel
        channel = None
        try:
            channel_id_int = int(channel_id)
            channel = self.permission_manager.guild.get_channel(channel_id_int)
        except ValueError:
            channel = discord.utils.get(channels, name=channel_id)
        
        if not channel:
            console.print("[red]Channel not found![/red]")
            return
        
        overwrites = await self.permission_manager.audit_permissions(channel)
        
        # Display results
        console.print(f"\n[bold]Permissions for {channel.name}:[/bold]")
        if not overwrites:
            console.print("[yellow]No specific permissions set for this channel.[/yellow]")
            return
        
        table = Table(title=f"Permission Overwrites for {channel.name}")
        table.add_column("Role", style="cyan")
        
        # Add all permission columns
        for perm in self.permission_manager.permissions[:10]:  # Limit for display
            table.add_column(perm.replace('_', ' ').title(), style="magenta")
        
        for role, overwrite in overwrites.items():
            row = [role.name]
            for perm in self.permission_manager.permissions[:10]:
                if hasattr(overwrite, perm):
                    value = getattr(overwrite, perm)
                    if value is True:
                        row.append("[green]ALLOW[/green]")
                    elif value is False:
                        row.append("[red]DENY[/red]")
                    else:
                        row.append("[yellow]DEFAULT[/yellow]")
                else:
                    row.append("-")
            
            table.add_row(*row)
        
        console.print(table)
    
    async def select_permissions_interactive(self) -> Dict[str, bool]:
        """Interactive permission selection."""
        console.print("\n[bold]Select Permissions:[/bold]")
        console.print("Choose permissions to apply (comma separated numbers):")
        
        # Show available permissions with numbers
        perms = self.permission_manager.get_all_permissions()
        for i, perm in enumerate(perms, 1):
            console.print(f"{i:2d}. {perm.replace('_', ' ').title()}")
        
        console.print("\nOr type 'all' for all permissions, 'custom' for specific ones, or 'none' to skip")
        choice = Prompt.ask("Your choice").lower()
        
        if choice == 'all':
            # For all permissions, ask if allow or deny
            allow = Confirm.ask("Allow all permissions? (Deny if no)")
            return {perm: allow for perm in perms}
        
        elif choice == 'none':
            return {}
        
        elif choice == 'custom':
            # Allow user to select specific permissions by name
            perm_names = Prompt.ask("Enter permission names (comma separated)").lower()
            selected_perms = [p.strip() for p in perm_names.split(',')]
            
            result = {}
            for perm in selected_perms:
                perm_clean = perm.strip().replace(' ', '_').replace('-', '_')
                if perm_clean in perms:
                    allow = Confirm.ask(f"Allow {perm_clean.replace('_', ' ').title()}?")
                    result[perm_clean] = allow
            
            return result
        
        else:
            # Numeric selection
            try:
                indices = [int(x.strip()) - 1 for x in choice.split(',')]
                selected_perms = [perms[i] for i in indices if 0 <= i < len(perms)]
                
                if not selected_perms:
                    console.print("[red]No valid permissions selected![/red]")
                    return {}
                
                # For selected permissions, ask if allow or deny
                allow = Confirm.ask("Allow selected permissions? (Deny if no)")
                return {perm: allow for perm in selected_perms}
            
            except ValueError:
                console.print("[red]Invalid input![/red]")
                return {}
    
    async def start(self):
        """Start the bot and interactive menu."""
        token = os.getenv('DISCORD_TOKEN')
        if not token:
            raise ValueError("DISCORD_TOKEN not found in .env file")
        
        # Start bot in background
        await self.bot.start(token, reconnect=True)


async def main():
    """Main entry point."""
    bot = DiscordPermissionBot()
    
    # Run the bot and interactive menu concurrently
    await asyncio.gather(
        bot.start(),
        bot.run_interactive_menu()
    )


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        console.print("\n[red]Shutting down...[/red]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        logging.error(f"Error in main: {e}")
# About
Discord bot for managing subscription based discord communities using MySQL database.

# Features/Commands
User
- !claim - Create account 
  - Account added in database using user's info
  - Role added based on license claimed
- !sub - Returns user's subscription time
- !gift [username] [key] - Gift someone subscription
- !ping - Check if bot is online

Admin
- !gensub [days] [product] - Generate a subscription key
- !gensubs [days] [product] [amount] - Generate subscription keys in bulk
- !user [username] - Returns full database information about an user
- !appversion - Returns app version from database
- !setappversion [version] Update app version in database

# Setup
Requirements
- Python 3
- MySQL Database

  
Setting up
Get a bot token from discord developer portal and replace:
```python
 BOT_TOKEN = 'xxxxxxx'
```
Add your database credentials:
```python
HOST = "xxxxxxx"
USER = "xxxxxxx"
PASSWORD = "xxxxxxx"
DATABASE = "xxxxxxx"
```
Replace the examples with your info
```python
embed.set_footer(text=f"yoursite.com - {date_variable}")
```

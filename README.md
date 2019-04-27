# StrelkaBot
### Telegram bot for strelkacard.

This is the code for my Telegram Bot. You can find it here: https://telegram.me/StrelkacardBalanceBot.


### Other Software:

 * aiohttp==3.5.4   
 * PyMySQL==0.9.3   
 * PySocks==1.6.8   
 * python-telegram-bot==12.0.0b1
 * requests==2.21.0  
 
### Database

The bot uses a MySQL database. You need to put your db connection settings in the config.json file. The tables and procedures gets auto-generated, if it doesn't exist. Make sure the MySQL user has access to create files in database.

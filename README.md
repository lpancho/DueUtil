# DueUtil

#### The purpose of this fork is to run the DueUtil in your own discord server using your local to run the application and to store data
#### We will not cover the running of DueUtil website in this repository

#### Running the bot

Requirements:
* Python 3.6.8 (https://www.python.org/downloads/release/python-383/)
* The packages in requirements.txt (`pip install -r requirements.txt`)
* MongoDB  (https://docs.mongodb.com/manual/installation/)
  * Get your connection string by: 
    * Typing mongosh in command prompt
    * ![image](https://user-images.githubusercontent.com/43244009/151656425-869b72d4-9e48-461d-b648-6766cf0a0414.png)
    * Connecting to Mongo Compass then without any connection string then disconnect (Connect > Disconnect) it will fill it up your previous connection
    * ![image](https://user-images.githubusercontent.com/43244009/151656465-32c19bf6-e465-427f-a400-a7de6fcb6454.png)

##### Setup the DB
1. Create an account that can create & update databases (admin will do)
```mongodb
use admin
db.createUser({user: "admin", pwd: "hunter1", roles:[{role: "userAdmin" , db:"dueutil"}]})
```
2. Put the account details in `dbconfig.json`

```json
{
    "host":"localhost",
    "user": "dueutil",
    "pwd": "hunter1"
}
```
(the host will probably be localhost)

##### Configure DueUtil
Create a file `dueutil.json` in the same folder as `run.py` (the root).
```json
{
   "botToken":"[DISCORD BOT TOKEN]",
   "owner":"[OWNER DISCORD ID]",
   "shardCount":1,
   "shardNames":[
      "Clone DueUtil: shard 1"
   ],
   "logChannel": "[SERVER ID]/[CHANNEL ID]",
   "errorChannel": "[SERVER ID]/[CHANNEL ID]",
   "feedbackChannel": "[SERVER ID]/[CHANNEL ID]",
   "bugChannel": "[SERVER ID]/[CHANNEL ID]",
   "announcementsChannel":"[SERVER ID]/[CHANNEL ID]",
   "carbonKey":"[https://www.carbonitex.net key you won't have]",
   "discordBotsOrgKey":"https://discordbots.org/ key you also won't have",
   "discordBotsKey": "https://bots.discord.pw/ key you also also won't have",
   "discoinKey":"http://discoin.sidetrip.xyz/ you will never get",
   "sentryAuth": "[SENTRY AUTH]"
}
```
The logging channels are currenly needed (the bot may not work properly without them), the bot probably can run without the other keys.

##### Restoring the database

1. Download the database dump from the last release
2. Extract that zip into folder called `database`
    ```
    database
    `-- dueutil
        |-- award_stats.bson
        |-- award_stats.metadata.json
        |-- _CacheStats.bson
        ...
    ```
    Your file tree should look like this
 3. Use mongorestore
    ``mongorestore  --username your_use --password "your_pass" --authenticationDatabase admin ./database``

##### Run DueUtil!

DueUtil can be ran with: `python3 run.py`

### Can't run the bot?!
I expect it will be fiddly to get this bot running, but please don't ask me to set it up for you I'm not going to help.

### Contribute
If you want to fix up this repo simply create a pull request (with a detailed commit message of your changes). If your making changes based on a [trello](https://trello.com/b/1ykaASKj/dueutil) card please link to it.

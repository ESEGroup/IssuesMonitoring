# Issues Monitoring - Email Parser

   Small and compact Python application which gets unread messages from a Gmail account, parses the tags embedded in them,
and sends the information to a server. 

   Every set interval of time(defined in *config.py*), the parser will access the target account through **IMAP** 
and search for any unread emails. 
It will then parse through those emails to find specific tags related to MyDenox events and store them in a JSON file. After that,
the parser will try to send the JSON file to the IssuesMonitoring server to be so its information can be stored in the database. 
If the parser is unable to connect to the server, it will access IMAP once more so it can mark the last read emails as '**unread**'.



## Getting started
```
DEBUG = True
```

   In production, change `DEBUG` tag to `False`

   After downloading the files, rename *__config.py.example__* to *__config.py__*. In the renamed *__config.py__*, find the following lines:

```
USERNAME = ""
PASSWORD = ""
```

   Fill out the *__USERNAME__* and *__PASSWORD__* fields with the target account's information. Next, find the line
   
```
AUTH_TOKEN = ""
```

   and fill it with the appropriate authentication token.
   
   
   If you want to create a log file, just set the flag `LOG_FILE` to the desired file path.
   
   
## Versions
   Additional information of release versions of the parser will be available soon.
   
   
## Technology   
### Built with: 
 * [Python](https://www.python.org/) - Programming Language
 * [IMAP](https://en.wikipedia.org/wiki/Internet_Message_Access_Protocol) - Internet protocol used for connection with the email account
 * [JSON](http://www.json.org/) - Format used to store parsed information from the emails

## License
   [AGPL - GNU Affero General Public License](https://raw.githubusercontent.com/ESEGroup/IssuesMonitoring/master/parser/LICENSE)

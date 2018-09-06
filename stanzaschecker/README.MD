# EZProxy stanzas checker
I've always found embarassing to be warned by patrons that one of our databases was down. They shouldn't have to, but we cannot check our ressources manually everyday. So I programmed this little tool that checks the HTTP response status of every configured stanza. It just a "first aid kit": a database might be accessible but the proxy server IP not recognized, but it has proven itself usefull.
It runs every night, logs the result and send a CSV report attached to a mail. It uses CAS for authentification.

## Requirements
- You will need Python3 and a few libs (check stanzascheker.py). ;
- Access to a smtp server account.

## How to use it
1. Complete the config.json with your own parameters ;
2. Execute stanzaschecker.py `stanzaschecker.py >> stanzaschecker.log 2>&1`

I've automated the execution to check our databases daily with a simple CRON call to this small script :
```
#!/bin/bash

# Lauch stanzaschecker.py
# To be called by cron

cd /home/manager/ezproxyToolBox/stanzaschecker/
source env/bin/activate
env/bin/python stanzaschecker.py >> stanzaschecker.log 2>&1
deactivate
```

## Log exemple

```
Kompass Easybusiness http://accesdistant.sorbonne-universite.fr/login?url=https://fr.kompass.com/ip 503 Service indisponible
2018-09-06 - 1 Errors found: sending notification e-mail to ['bibnum@sorbonne-universite.fr', 'romain.boisselet@sorbonne-universite.fr'] 
Report databasesCheckReport_2018-09-06.csv successfully written in databasesCheckReports/
```
## Report Exemple
| database_name | database_url  | http_code | http_status |
|:-------------:|:-------------:|:---------:|:-----------:|
Metropolitan Opera on Demand	| http://accesdistant.sorbonne-universite.fr/login?url=http://metopera.org/ondemand/index.aspx	| 404	| Document non trouvé
Nature Publishing	| http://accesdistant.sorbonne-universite.fr/login?url=https://www.nature.com	| 503	| Service indisponible
IEEE Xplore |	http://accesdistant.sorbonne-universite.fr/login?url=https://ieeexplore.ieee.org/	| 503	| Service indisponible

# sakura-monitor
a simple monitor application to check our platform health

## program execution

write a short script named sakura_monitor.sh

    source ./sendgrid.env
    python3 sakura_monitor.py

and call it every 10 minutes

    */10 * * * * /usr/local/bin/sakura_monitor.sh


## HOW TO SET SENDGRID API KEY

echo "export SENDGRID_API_KEY='YOUR_API_KEY'" > sendgrid.env


## config.json

the monitor need some info stored in config.json :

the list of hosts to be pinged

the list of url to be GET'd

the list of email to send alarm


    {
      "hosts" : [
      "127.0.0.1"
      ],
    
      "urls" : [
        "https://sakura.eco/api/mheck?shop=1"
      ],
    
      "emails" : [
        "leonardo.skymax@gmail.com"
      ]
    }


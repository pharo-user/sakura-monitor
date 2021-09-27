# sakura-monitor
a simple monitor application to check our platform health

## program execution

write a short script named sakura_monitor.sh

    cd /home/your_user/sakura-monitor
    export SENDGRID_API_KEY='43290423840234804803248'
    python3 sakura_monitor.py

and call it every 10 minutes

    */10 * * * * /usr/local/bin/sakura_monitor.sh

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
      ],

      "mailer_url" : "https::/yourmailer.com/api/send"

    }


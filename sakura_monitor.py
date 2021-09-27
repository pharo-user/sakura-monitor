#
#   write a short script named sakura_monitor.sh
#
#   export SENDGRID_API_KEY=5074504755734985745'43752745
#   python3 sakura_monitor.py
#
#   and call it every 10 minutes
#
#   */10 * * * * /usr/local/bin/sakura_monitor.sh
#


import sys, os, json, pathlib, requests


def read_config(nf) :
    path = pathlib.Path(nf)
    if path.is_file() :
        with open(nf) as json_file:
            return json.load(json_file)
    else :
        return []

def send_email(mailer_url, msg_from, emails, subject, errors) :
    access_token = os.environ.get('SENDGRID_API_KEY')
    print('access token '+access_token)
    headers = {'Authorization' : 'Bearer '+access_token, 'Content-Type' : 'application/json' }
    
    msg_to = list( map( lambda s : { 'email': s }, emails))
    content = "".join(list( map( lambda s : '<p>'+s+'</p>' , errors)))

    data = { 
        'personalizations' : [{ 'to' : msg_to  }],
        'from' : { 'email' : msg_from },
        'subject' : subject, 
        'content' : [{
                'type' : 'text/html',
                'value' : content 
        }]
    }

    print(headers, data)

    try:
        response = requests.post(mailer_url, headers=headers, json=data)
    except requests.ConnectionError as error:
        return 'error',error
    except requests.execptions.HTTPError as error:
        return 'error', e.code
    else:
        return 'success', str(response.status_code) + ' - '+response.text

def check_backend(url) : 

    try:
        response = requests.get(url)
    except requests.ConnectionError as error:
        return 'error',error
    except requests.execptions.HTTPError as error:
        return 'error',e.code
    else:
        if response.status_code == 200 :
            return 'success', response.text
        else:
            return 'error',str(response.status_code)

def check_server(host) : 
    response = os.system("ping -c 1 "+host)
    if response == 0:
        return 'success','ping ok'
    else:
        return 'error','ping fail'


def report_problem(mailer_url, msg_from, emails, subject, errors) :
    try :
        status,msg = send_email(mailer_url, msg_from, emails, subject, errors)
    except Exception as inst :
        print('report problem failed ' + str(inst))
    else :
        print(msg)
        if status != 'success' :
            print('unable to report errors : status '+status)

if __name__ == '__main__':
    diag = '-t' in sys.argv

    print(diag)
    # start checking
    errors = []

    config = read_config('config.json')
    print(config)

    # check if server is responding
    for host in config["hosts"] :
        status,msg = check_server(host)
        print('check_server '+host+' : '+msg)
        if status != 'success' :
            errors.append("check_server "+host+ " : "+ msg)

    # check backend server
    for url in config["urls"] : 
        status,msg = check_backend(url)
        print('check_backend '+url+' : '+msg)
        if status != 'success' :
            errors.append("check_backend failed "+url+" : "+msg)

    # report problem, if any
    if len(errors) > 0 :
        print('test failed')
        print(errors)
        report_problem(config["mailer_url"], config["mail_from"], config["emails"], config["mail_subject"], errors)
    else :
        print('test successfull')

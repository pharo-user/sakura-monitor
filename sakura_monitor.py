#
#   write a short script named sakura_monitor.sh
#
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

def send_email(msg_from, msg_to, subject, content) :
    url = 'https://api.sendgrid.com/v3/mail/send'
    access_token = os.environ.get('SENDGRID_API_KEY')
    print('access token '+access_token)
    headers = {'Authorization' : 'Bearer '+access_token, 'Content-Type' : 'application/json' }
    data = { 
        'personalizations' : [{ 
            'to' : [{ 'email' : msg_to }]}],
        'from' : { 'email' : msg_from },
        'subject' : subject, 
        'content' : [{
                'type' : 'text/html',
                'value' : content 
        }]
    }

    print(headers, data)

    try:
        response = requests.post(url, headers=headers, json=data)
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


def report_problem(emails, errors) :
    msg_from = 'leo@sakura.eco'
    msg_to = 'leonardo.skymax@gmail.com'
    subject = 'crash'
    content = 'server crashed'
    status,msg = send_email(msg_from, msg_to, subject, content)
    print(msg)
    if status != 'success' :
        print('unable to report errors')

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
            errors.append(msg)

    # check backend server
    for url in config["urls"] : 
        status,msg = check_backend(url)
        print('check_backend '+url+' : '+msg)
        if status != 'success' :
            errors.append(msg)

    # report problem, if any
    if len(errors) > 0 :
        print('test failed')
        print(errors)
        report_problem(config["emails"], errors)
    else :
        print('test successfull')

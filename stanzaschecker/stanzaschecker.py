# coding: utf-8
from __future__ import unicode_literals
import json
import os
import pandas as pd
import datetime
import codecs
import requests
import lxml.html
from bs4 import BeautifulSoup as bs
from fake_useragent import UserAgent
import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate

def cas_login(login_url, service, username, password):
    # GET parameters - URL we'd like to log into.
    params = {'service': service}
    LOGIN_URL = login_url

    # Start session and get login form.
    session = requests.session()
    login = session.get(LOGIN_URL, params=params)

    # Get the hidden elements and put them in our form.
    login_html = lxml.html.fromstring(login.text)
    hidden_elements = login_html.xpath('//form//input[@type="hidden"]')
    form = {}
    for x in hidden_elements:
        if 'value' in x.attrib.keys():
            form[x.attrib['name']] = x.attrib['value']
    
    # "Fill out" the form.
    form['username'] = username
    form['password'] = password

    # Finally, login and return the session.
    # Connexion with SSL verification needs to be done
    # using verify=False meanwhile. A lot of warnings in logs
    # but working
    session.post(LOGIN_URL, data=form, params=params, verify=False)
    return session

def get_links_to_check(login_url, proxy_url, username, password, authentication_mode="cas"):
    """ Makes a list of the database links to check : [url, text]
    
    Uses cas_login by default for a cas connexion to EZProxy.
    Other authentication modes could be used instead

    """

    if authentication_mode == "cas":
        ezproxy_session = cas_login(login_url, proxy_url, username, password)
    
    req_menu_page = ezproxy_session.get(proxy_url+'/menu', verify=False)
    req_menu_page.encoding = 'utf-8'
    menu_page_html = req_menu_page.text
    menu_page_bs = bs(menu_page_html, 'lxml')
    links = []
    for a in menu_page_bs.find_all('a', class_='database-link'):
        link = [a.get('href'), a.get_text()]
        #print(link)
        links.append(link)
        #print(link)
    return links

def process_check_result(link, r, result_table):
    check_result = {
        "database_name": link[1],
        "database_url": config['proxy_url'] + link[0],
        "http_code": r.status_code,
        "http_status": config['http_status'][str(r.status_code)]
        }

    result_table.append(check_result)

    if r.status_code != 200:
        print(link[1],
    	    config['proxy_url'] + link[0],
	    r.status_code,
            config['http_status'][str(r.status_code)]
	)
    return result_table

def check_links(links, login_url, proxy_url, username, password, authentication_mode="cas"):
    """ Check connexion for each link in list.
    
    If http code is different than 200, return
    the error code

    """

    if authentication_mode == "cas":
        ezproxy_session = cas_login(login_url, proxy_url, username, password)  

    # Update default headers with a browser user-agent
    # mandatory for some ressources (e.g. kompass)
    user_agent = UserAgent()
    headers = requests.utils.default_headers()
    headers.update(
        {
            'User-Agent': str(user_agent.firefox),
        }
    )

    result_table = []

    for link in links:
            try:
                r = ezproxy_session.get(proxy_url+link[0], verify=False, headers=headers)
                result_table = process_check_result(link, r, result_table)

            except requests.exceptions.Timeout as e:
                result_table = process_check_result(link, r, result_table)

            except requests.exceptions.TooManyRedirects as e:
                result_table = process_check_result(link, r, result_table)

            except requests.exceptions.RequestException as e:
                result_table = process_check_result(link, r, result_table)

            except requests.exceptions.HTTPError as e:
                result_table = process_check_result(link, r, result_table)

    return result_table

def process_result_table(result_table):

        result_table_errors = []

        for result in result_table:
                if result['http_code'] != 200:
                    result_error = {
                        "database_name": result['database_name'],
                        "database_url": result['database_url'],
                        "http_code": result['http_code'],
                        "http_status": result['http_status']
                        }
                    result_table_errors.append(result_error)

        return result_table_errors

def write_error_report(result_table_errors):

    today = datetime.datetime.today().strftime('%Y-%m-%d')

    # Create, if nonexistent, a 'stanzaschecker_reports' directory

    if not os.path.exists('./stanzaschecker_reports'):
        os.makedirs('./stanzaschecker_reports')

    df = pd.DataFrame(result_table_errors)

    try:
        df.to_csv('./stanzaschecker_reports/sc_report_'+today+'.csv', sep=';', header=True)
        print('\nReport sc_report_'+today+'.csv successfully written in stanzaschecker_reports/')
    except:
        print('Report writing error')


def send_mail(smtp_server, smtp_port, smtp_from,
        smtp_to, subject, text, file=None):
    assert isinstance(smtp_to, list)

    msg = MIMEMultipart()
    msg['From'] = smtp_from
    msg['To'] = COMMASPACE.join(smtp_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach(MIMEText(text))

    #for f in files or []:
    with codecs.open(file, "rb") as fil:
    	part = MIMEApplication(fil.read())
    # After the file is closed
    part['Content-Disposition'] = 'attachment; filename="%s"' % basename(file)
    msg.attach(part)
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.sendmail(smtp_from, smtp_to, msg.as_string())

if __name__ == "__main__":

    # Load parameters
    with codecs.open('config.json', 'r', 'utf-8') as f:
        global config
        config = json.load(f)

    ezp_parameters = [
        config['cas_login_url'],
        config['proxy_url'],
        config['username'],
        config['password'],
        config['authentication_mode']
        ]

    today = datetime.datetime.today().strftime('%Y-%m-%d')


    # Retrieve the database list from menu.htm
    # links : [database_name, database_url]
    links = get_links_to_check(*ezp_parameters)

    # Check each database, return result_table :
    # [
    #   {
    #       'database_name': a,
    #       'database_url': b,
    #       'http_code': c,
    #       'http_status': d
    #   }
    # ]
    #
    # http_status is fetched from the config.json "http_status" dict
    result_table = check_links(links, *ezp_parameters)

    result_table_errors = process_result_table(result_table)

    if len(result_table_errors) != 0:
        print(today, '-', len(result_table_errors), 'Error(s) found:',
	'sending notification e-mail to', config['smtp_to'], '\n')
        msg = today+" - "+str(len(result_table_errors))+" erreur(s) détectée(s). Voir le rapport attaché"
        write_error_report(result_table_errors)
        send_mail(config['smtp_server'], config['smtp_port'], config['smtp_from'], config['smtp_to'], "[EZProxy - rapport d'erreur]", msg, "stanzaschecker_reports/sc_report_"+today+".csv")

    else:
        print(today, '- No errors found, all databases up and running')

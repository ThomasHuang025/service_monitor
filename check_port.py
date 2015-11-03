'''
Created on 2015年10月16日

@author: Thomas Wong
'''
import json,socket,time,subprocess,urllib.parse,http.client

def main(argv=None):
    print('hello world')
    base_path = '/usr/local/htdocs/service_monitor/'
    s_list = open('%scheck_port_list.json' %(base_path)).read()
    list_objs = json.loads(s_list)
    timenow=time.localtime()
    log_file_path = "/data1/logs/service_monitor/monitor-port-%s" %(time.strftime('%Y-%m-%d', timenow))
    log_file = open(log_file_path, "a")
    
    for item in list_objs:
        name = item['name']
        ip = '127.0.0.1'
        port = item['port']
        timenow=time.localtime()
        datenow = time.strftime('%Y-%m-%d %H:%M:%S', timenow)
    
        try:
            sc=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            sc.settimeout(2)
            sc.connect((ip,port))
            sc.close()
            logstr="%s %s:%s %s -> [OK]\n" %(datenow,ip,port,name)
        except:
            timenow=time.localtime()
            cmd = item['cmd']
            logstr="%s %s:%s %s -> [FAIL] ->  try execute cmd %s \n" %(datenow,ip,port,name,cmd)
            subprocess.call(cmd,shell=True)
            title = "Notic: %s %s %s is down." %(datenow,socket.gethostname(),name)
            content = "%s %s:%s %s service is not available. Try to restart..." %(datenow,socket.gethostname(),port,name)
            
            admin_list = open('%sadmin_list.json' %(base_path)).read()
            admin_list_objs = json.loads(admin_list)
            for admin_mail in admin_list_objs:
                params = urllib.parse.urlencode({'subject': title, 'content': content, 'to': admin_mail})
				#alert server
                conn = http.client.HTTPConnection("127.0.0.1:9099")
                conn.connect()
                conn.request("POST", "/alarm/mail", params)
                res = conn.getresponse().read()
                log_file.write("%s send mail to admin %s, content:%s\n" %(datenow,admin_mail,content))
        print(logstr)
        log_file.write(logstr)
    log_file.close()

if __name__ == '__main__':
    main()


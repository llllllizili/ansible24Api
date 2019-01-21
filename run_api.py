# coding: utf-8

import os
from .ansible_api import MyApi as AnsibleApi


class RemoteRun(object):
    global script_path
    script_path = os.path.dirname(__file__) + '/script/'
    def __init__(self,**kwargs):
        self.ip=kwargs.get('ip','')
        self.username=kwargs.get('username','')
        self.password=kwargs.get('password','')
        self.port=kwargs.get('port',22)
        self.os_type=kwargs.get('os_type')
        self.time_out = kwargs.get('time_out',10)
        self.run_user = kwargs.get('become_user','root')

        if not self.os_type :
            return 'OS TYPE 未配置'
        if not self.ip:
            return 'ip 未配置'
        if self.os_type.lower() == 'linux':
            if not self.username or not self.password:
                return '账号,密码不完整'

        self.sources=[]
        host_info={}

        host_info['hostname']=self.ip
        host_info['ansible_user']=self.username
        host_info['ansible_ssh_pass']=self.password
        host_info['ansible_port']=self.port

        self.sources.append(host_info)




    def get_path(self):
        return script_path

    def run_cmd(self,cmd,**kwargs):
        chdir=kwargs.get('chdir','')
        if cmd:
            if len(self.sources)>0:
                ansible_run = AnsibleApi(resource=self.sources)
                ansible_run.run(self.ip, 'shell', 'source /etc/profile;'+cmd +
                    ' chdir='+chdir if chdir else cmd )
                data=ansible_run.get_result()

                success_data=data['success']
                failed_data=data['failed']
                unreachable_data=data['unreachable']

                if len(failed_data) > 0:
                    return failed_data[self.ip]['command']
                if len(unreachable_data) >0:
                    return unreachable_data[self.ip]['command']
                else:
                    return success_data[self.ip]['command']
        else:
            pass

    def run_script(self,script,options):
        if len(self.sources)>0:
            ansible_run = AnsibleApi(
                    resource=self.sources,
                    become_user=self.run_user,
                    timeout=self.time_out,
                )
            ansible_run.run(self.ip, 'script', script_path+script + ' ' + options)
            print(script_path+script + ' ' + options)
            data=ansible_run.get_result()

            success_data=data['success']
            failed_data=data['failed']
            unreachable_data=data['unreachable']

            if len(failed_data) > 0:
                return failed_data
            if len(unreachable_data) >0:
                return unreachable_data
            else:
                return success_data
        else:
            pass

    def run_copy(self):
        pass

if __name__ == '__main__':
    run = RemoteRun(ip='192.168.1.100',username='root',password='centos',port=22,os_type='linux')
    d = run.run_cmd('ls /opt')
    # print(d)
    # dd = run.run_cmd('ls /opt123')
    # print(dd)

    # rund = RemoteRun(ip='192.168.1.1131',username='root',password='centos',port=22,os_type='linux')
    # ddd = rund.run_cmd('ls /opt123')
    # print(ddd)

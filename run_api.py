#!/usr/bin python
# -*- coding: utf-8 -*-
'''
@File    :   ansible_api.py
@Time    :   2019/05/05 15:16:12
@Author  :   Li Zili 
@Version :   1.0
@Contact :   cn.zili.lee@gmail.com
'''
import os
from .ansible_api import MyApi as AnsibleApi

# log
import logging
jklog=logging.getLogger("jksre")


class RemoteRun(object):
    def __init__(self,**kwargs):
        self.ip=kwargs.get('ip','')
        self.username=kwargs.get('username','')
        self.password=kwargs.get('password','')
        self.port=kwargs.get('port',22)
        self.os_type=kwargs.get('os_type','linux')
        self.time_out = kwargs.get('time_out',10)
        self.run_user = kwargs.get('become_user','root')
        self.sources=[]

        host_info={}
        host_info['ansible_host']=self.ip
        host_info['ansible_user']=self.username
        host_info['ansible_ssh_pass']=self.password
        host_info['ansible_port']=self.port

        self.sources.append(host_info)

    def run_cmd(self,cmd,**kwargs):
        """执行命令
        ARGS
            cmd : 命令
        """
        chdir=kwargs.get('chdir','')
        if cmd:
            if len(self.sources)>0:
                ansible_run = AnsibleApi(resource=self.sources)
                ansible_run.run(self.ip, 'shell', 'source /etc/profile;'+cmd +' chdir='+chdir if chdir else cmd )
                data=ansible_run.get_result()
                # jklog.debug(data)
                success_data=data['success']
                failed_data=data['failed']
                unreachable_data=data['unreachable']
                return_data=dict()

                if len(success_data) > 0:
                    return_data['status']='success'
                    return_data['result']=success_data[self.ip]['command']
                    return return_data
                elif len(failed_data) > 0:
                    return_data['status']='failed'
                    return_data['result']=failed_data[self.ip]['command']
                    return return_data
                elif len(unreachable_data) >0:
                    return_data['status']='unreachable'
                    return_data['result']=unreachable_data[self.ip]['command']
                    return return_data
                else:
                    return_data['status']='error'
                    return_data['result']='error'
                    return return_data
        else:
            return_data['status']='failed'
            return_data['result']='command is empty'
            return return_data

    def run_script(self,script,options=''):
        """执行脚本
        ARGS
            script : 脚本
            options : 参数,默认空
        """
        if len(self.sources)>0:
            ansible_run = AnsibleApi(
                    resource=self.sources,
                    become_user=self.run_user,
                    timeout=self.time_out,
                )
            ansible_run.run(self.ip, 'script',script+' '+options)
            data=ansible_run.get_result()
            # jklog.debug(data)
            success_data=data['success']
            failed_data=data['failed']
            unreachable_data=data['unreachable']

            return_data=dict()

            if len(success_data) > 0:
                return_data['status']='success'
                return_data['result']=success_data[self.ip]['script']
                return return_data
            elif len(failed_data) > 0:
                return_data['status']='failed'
                return_data['result']=failed_data[self.ip]['script']
                return return_data
            elif len(unreachable_data) >0:
                return_data['status']='unreachable'
                return_data['result']=unreachable_data[self.ip]['script']
                return return_data
            else:
                return_data['status']='error'
                return_data['result']='error'
                return return_data
        else:
            return_data['status']='error'
            return_data['result']='error'
            return return_data

    def run_copy(self,filename,dest_path,options=''):
        """执行文件复制
        ARGS
            filename : 源文件
            dest_path : 目的位置
            options : 参数,默认空
        """
        if len(self.sources)>0:
            ansible_run = AnsibleApi(
                    resource=self.sources,
                    become_user=self.run_user,
                    timeout=self.time_out,
                )
            ansible_run.run(self.ip, 'copy','src='+filename+' dest='+dest_path+' '+options)
            data=ansible_run.get_result()
            # jklog.debug(data)
            success_data=data['success']
            failed_data=data['failed']
            unreachable_data=data['unreachable']

            return_data=dict()

            if len(success_data) > 0:
                return_data['status']='success'
                return_data['result']=success_data[self.ip]['copy']
                return return_data
            elif len(failed_data) > 0:
                return_data['status']='failed'
                return_data['result']=failed_data[self.ip]['copy']
                return return_data
            elif len(unreachable_data) >0:
                return_data['status']='unreachable'
                return_data['result']=unreachable_data[self.ip]['copy']
                return return_data
            else:
                return_data['status']='error'
                return_data['result']='error'
                return return_data
        else:
            return_data['status']='failed'
            return_data['result']='resource is empty'
            return return_data

if __name__ == '__main__':
    run = RemoteRun(ip='192.168.1.100',username='root',password='centos',port=22,os_type='linux')
    d = run.run_cmd('ls /opt')
    # print(d)
    # dd = run.run_cmd('ls /opt123')
    # print(dd)

    # rund = RemoteRun(ip='192.168.1.1131',username='root',password='centos',port=22,os_type='linux')
    # ddd = rund.run_cmd('ls /opt123')
    # print(ddd)

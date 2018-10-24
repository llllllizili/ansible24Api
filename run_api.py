# coding: utf-8

from ansible_api import MyApi

# # hostfile 可以是一个静态文件, 也可以是一个get_inventory文件 (最后把取到的内容print出来)
# #dict_1 ={'my_group': {'hosts': {'host': {'ansible_ssh_host': '192.168.1.55', 'ansible_ssh_port': 22, 'ansible_ssh_pass': 'centos', 'ansible_ssh_user': 'root'}}}}
# api = MyApi("/root/ansible/py2/api/hosts")


# # 执行 Ad-hoc
# api.run("all", "shell", "ls /tmp")


# # 执行 playbook
# #api.run_playbook(<host>, <playbookfile>)

# # 获取返回值
# #res=api.get_result()    # 字典
# res = api.get_json()      # json10
# print res


sources=[{"hostname": "192.168.1.100", "ansible_port":22, "ansible_user":"root", "ansible_ssh_pass":"centos"}]
runner = MyApi(resource=sources)
runner.run('all', 'shell', "ip addr | grep 192")
res = runner.get_json()
print res

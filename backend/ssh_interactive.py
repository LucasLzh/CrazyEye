from django.contrib.auth import authenticate
from backend.paramiko_ssh import ssh_connect
from web import models

class SshHandler(object):
    """启动堡垒机交互脚本"""
    def __init__(self, arg_handler_instance):
        self.arg_handler_instance = arg_handler_instance
        self.models = models

    def auth(self):
        """认证程序"""
        count = 0
        while count < 3:
            username = input("堡垒机账号:").strip()
            password = input("堡垒机密码:").strip()
            user = authenticate(username=username, password=password)
            if user:
                self.user = user
                return True
            else:
                count += 1
        print("账号密码错误")

    def interactive(self):
        """启动交互脚本"""
        if self.auth():
            print("Ready to print all the authorized hosts...to this user")
            while True:
                host_group_list = self.user.host_groups.all()
                print(host_group_list)
                for index, host_group_obj in enumerate(host_group_list):
                    print("%s.\t%s[%s]" % (index, host_group_obj.name, host_group_obj.host_to_remote_users.count()))
                print("z.\t未分组主机[%s]" % (self.user.host_to_remote_users.count()))
                choice = input("请选择主机组》》：").strip()
                if choice.isdigit():
                    choice = int(choice)
                    selected_host_group = host_group_list[choice]
                elif choice == 'z':
                    selected_host_group = self.user
                    print(selected_host_group)

                while True:
                    for index, host_to_user_obj in enumerate(selected_host_group.host_to_remote_users.all()):
                        print("%s.\t%s" % (index, host_to_user_obj))

                    choice = input("请选择主机》》：").strip()
                    if choice.isdigit():
                        choice = int(choice)
                        selected_host_to_user_obj = selected_host_group.host_to_remote_users.all()[choice]
                        print("going to logon %s" % selected_host_to_user_obj)
                        ssh_connect(self, selected_host_to_user_obj)
                    if choice == 'b':
                        break



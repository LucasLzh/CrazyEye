import sys, os


if __name__ == "__main__":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CrazyEye.settings') #这三步才能实现从外部调用diango环境
    import django
    django.setup()
    from backend import main
    interactive_obj = main.ArgvHandler(sys.argv)
    interactive_obj.call()

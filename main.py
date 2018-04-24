import sys
import etc_application as application


if __name__ == '__main__':
    etc = application.ETC_Application()
    exit_status = etc.run(sys.argv)
    sys.exit(exit_status)

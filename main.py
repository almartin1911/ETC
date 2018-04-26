import sys
import etc_application


if __name__ == '__main__':
    etc = etc_application.ETC_Application()
    exit_status = etc.run(sys.argv)
    sys.exit(exit_status)

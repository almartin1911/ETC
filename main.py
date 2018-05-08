import etc_gtkapplication
import sys

if __name__ == '__main__':
    app = etc_gtkapplication.Application()
    exit_status = app.run(sys.argv)
    sys.exit(exit_status)

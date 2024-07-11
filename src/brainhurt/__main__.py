from . import BrainHurt
import sys




def usage():
    print('Usage: brainhurt <filename>')
    print('filename is required')


if len(sys.argv) < 2:
    usage()
    sys.exit(1)


file_path = sys.argv[1]
brainhurt = BrainHurt()
brainhurt.load_file(file_path)
brainhurt.execute_programm()
import sys
import exifread


def main():
    with open(sys.argv[1], 'rb') as f:
        tags = exifread.process_file(f)
        for t in tags:
            if 'GPS' in t:
                print(t, tags[t])
                print('______________________________________')

if __name__ == "__main__":
    main()
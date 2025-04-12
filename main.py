import sys

# imports are in if statements to prevent the import running code
# if everything was inside functions this wouldn't be necessary
if __name__ == "__main__":
    if sys.argv[1] == "process":
        from processor import process
        process()
    elif sys.argv[1] == "overlay":
        from overlay import init
        init()
    else:
        print("invalid argument. Expecting either process or overlay")
        exit(1)

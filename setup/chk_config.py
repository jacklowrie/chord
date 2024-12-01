import sys
try:
    import mininet
    print("looks like everything is set up correctly!")
except ImportError:
    print("cannot find mininet!")
    print("\t - did you add it to your PYTHONPATH?")
    print("\t - did you call sudo with the right python version?")
    print("\t - did you make sure sudo has your PYTHONPATH?\n\n")
    print(f"PYTHONPATH is:\n")
    print(sys.path)
    print("\n\n")

    sys.exit(1)

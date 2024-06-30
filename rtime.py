import time, argparse, sys, io

def main(fpath):
    """
    Executes the contents of the specified file and measures the time it takes to run.
    
    Args:
        fpath (str): The path to the file to be executed and timed.
    
    Returns:
        None
    """
    with open(fpath, "r", encoding="utf-8") as f:
        script = f.read()
        
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()     
    total = 0
    
    for x in range(5):
        start = time.time()
        exec(script)
        end = time.time()
        total += end - start
        
    sys.stdout = old_stdout
    print(f"Average execution time: {format(total/5, '.5f')}s  ")
    
if __name__ == "__main__":
    """
    Parses command line arguments for the file timing script.
    
    Args:
        file_path (str): The path to the file to be timed.
    
    Returns:
        None
    """
    parser = argparse.ArgumentParser(description="Time how long it takes to run the script")
    parser.add_argument("file_path", type=str, help="Path to the file to be timed")
    
    args = parser.parse_args()
    main(args.file_path)
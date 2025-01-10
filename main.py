import os
import sys
import subprocess
from pathlib import Path

sys_clear_cmd = "cls" if os.name == "nt" else "clear"

def reset(cwd: str, new_line = True):
    if new_line:
        print()

    main(cwd)

def main(cwd: str):
    print(cwd)

    cmd = input("> ").strip()
    cmd_parts = cmd.split()
    
    match cmd_parts[0]:        
        case "cd":
            args = cmd_parts[1:]
            
            if len(args) == 0:
                cwd = str(Path("~").expanduser())
            else:
                os.chdir(args[0])
                
                # we want os.getcwd(), which is absolute. args[0] is relative.
                cwd = os.getcwd()
            
            reset(cwd)
            return

        case "exit":
            sys.exit(0)
    
    try:
        result = subprocess.run(
            cmd_parts,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=cwd
        )
        
        if result.stdout:
            print(result.stdout, end="")
        
        if result.stderr:
            print(result.stderr, end="", file=sys.stderr)
    except Exception as e:
        print(e, file=sys.stderr)
    
    reset(cwd, new_line=cmd != sys_clear_cmd)

if __name__ == "__main__":
    print("welcome to mini-shell!\n")
    main(os.getcwd())

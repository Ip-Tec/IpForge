import os
import subprocess
import sys

def is_pyinstaller_installed():
    """Check if PyInstaller is installed and available."""
    try:
        subprocess.check_output(["pyinstaller", "--version"], stderr=subprocess.STDOUT)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def build_executable(options, log_callback):
    """
    Build the executable using PyInstaller.

    :param options: A dictionary with build options.
    :param log_callback: A function to call with log messages.
    """
    script_path = options.get("script")
    project_name = options.get("name")
    onefile = options.get("onefile")
    noconsole = options.get("noconsole")
    icon_path = options.get("icon")
    output_dir = options.get("output_dir")

    # --- Path Validation and Normalization ---
    if not script_path or not os.path.exists(script_path):
        log_callback("Error: Script path is invalid or does not exist.")
        return
    
    # Normalize script_path to use correct OS separators
    script_path = os.path.normpath(script_path)
    
    if icon_path and not os.path.exists(icon_path):
        log_callback(f"Error: Icon path is invalid or does not exist:\n{icon_path}")
        return
    
    # Use project's root for build and spec folders, not the output directory
    project_root = os.path.dirname(os.path.abspath(sys.argv[0])) # Get the directory of the running script (ipforge.py)
    work_path = os.path.join(project_root, "build")
    spec_path = project_root

    cmd = [
        "pyinstaller",
        "--name", project_name if project_name else os.path.basename(script_path).replace(".py", ""),
    ]

    if onefile:
        cmd.append("--onefile")
    if noconsole:
        cmd.append("--noconsole")
    if icon_path:
        cmd.extend(["--icon", os.path.normpath(icon_path)])
    if output_dir:
        cmd.extend(["--distpath", os.path.normpath(output_dir)])

    cmd.extend(["--workpath", work_path])
    cmd.extend(["--specpath", spec_path])
    cmd.append(script_path)
    
    # Use repr() on command for logging to make spaces clear
    command_str = ' '.join(f'"{part}"' if ' ' in part else part for part in cmd)
    log_callback(f"Executing command: {command_str}\n\n")
    
    try:
        # Run from the script's directory to handle relative paths correctly
        process_cwd = os.path.dirname(script_path)
        process = subprocess.Popen(
            cmd, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT, 
            text=True, 
            bufsize=1, 
            creationflags=subprocess.CREATE_NO_WINDOW,
            cwd=process_cwd if process_cwd else '.'
        )
        for line in iter(process.stdout.readline, ''):
            log_callback(line)
        process.stdout.close()
        return_code = process.wait()
        if return_code == 0:
            log_callback("\nBuild finished successfully!")
        else:
            log_callback(f"\nBuild failed with exit code {return_code}.")
    except Exception as e:
        log_callback(f"\nAn error occurred: {e}")


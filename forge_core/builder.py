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

    if not script_path or not os.path.exists(script_path):
        log_callback("Error: Script path is invalid or does not exist.")
        return

    cmd = [
        "pyinstaller",
        "--name", project_name if project_name else os.path.basename(script_path).replace(".py", ""),
    ]

    if onefile:
        cmd.append("--onefile")
    if noconsole:
        cmd.append("--noconsole")
    if icon_path:
        cmd.extend(["--icon", icon_path])
    if output_dir:
        cmd.extend(["--distpath", output_dir])
        cmd.extend(["--workpath", os.path.join(output_dir, "build")])
        cmd.extend(["--specpath", os.path.join(output_dir, "spec")])

    cmd.append(script_path)
    
    command_str = " ".join(cmd)
    log_callback(f"Executing command: {command_str}\n\n")
    
    try:
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1, creationflags=subprocess.CREATE_NO_WINDOW)
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


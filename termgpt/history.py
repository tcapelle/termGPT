import subprocess
import warnings
import os

# Global configuration
DEFAULT_HISTORY_LINES = 400

def get_zsh_history(num_lines=DEFAULT_HISTORY_LINES):
    """
    Get command history from zsh shell.
    First tries using fc command, then falls back to reading history file.
    
    Args:
        num_lines (int): Number of history lines to retrieve
        
    Returns:
        str: Shell command history
    """
    # Try fc command first
    try:
        shell = os.environ.get('SHELL', '/bin/zsh')
        cmd = [shell, "-c", f"fc -ln -{num_lines}"]
        output = subprocess.run(cmd, 
                              capture_output=True, text=True, check=True,
                              env=os.environ)
        if output.stdout.strip():
            return output.stdout
    except subprocess.SubprocessError:
        pass

    # Fallback to reading history file
    try:
        history_file = os.environ.get('HISTFILE', os.path.expanduser("~/.zsh_history"))
        if os.path.exists(history_file):
            for encoding in ['utf-8', 'latin1', 'ascii']:
                try:
                    with open(history_file, 'r', encoding=encoding, errors='replace') as f:
                        content = f.read()
                        lines = content.split('\n')
                        cleaned_lines = []
                        for line in lines:
                            if ';' in line:
                                cleaned_lines.append(line.split(';', 1)[1])
                            else:
                                cleaned_lines.append(line)
                        return '\n'.join(cleaned_lines[-num_lines:])
                except UnicodeDecodeError:
                    continue
            
            warnings.warn("Could not decode history file with any encoding")
    except Exception as e:
        warnings.warn(f"Failed to read zsh history file: {str(e)}")
    
    return ""

def get_terminal_history(num_lines=DEFAULT_HISTORY_LINES):
    """
    Get command history from the current terminal.
    Supports iTerm2, tmux, and falls back to zsh history.
    
    Args:
        num_lines (int): Number of history lines to retrieve
        
    Returns:
        str: Terminal command history
    """
    # iTerm2 AppleScript
    iterm_script = """
    tell application "iTerm2"
        tell current window
            tell current session
                contents
            end tell
        end tell
    end tell
    """
    
    # Check if running in iTerm2
    if "ITERM_SESSION_ID" in os.environ:
        try:
            output = subprocess.run(["osascript", "-e", iterm_script], 
                                  capture_output=True, text=True, check=True)
            if output.stdout.strip():
                # Clean up iTerm2 output by removing extra newlines and whitespace
                cleaned_lines = [line.strip() for line in output.stdout.splitlines() if line.strip()]
                return '\n'.join(cleaned_lines[-DEFAULT_HISTORY_LINES:])
            warnings.warn("iTerm2 history was empty, falling back to shell history")
        except subprocess.SubprocessError as e:
            warnings.warn(f"Failed to get iTerm2 history: {e.stderr if hasattr(e, 'stderr') else str(e)}")
    
    # Check if running in tmux
    if "TMUX" in os.environ:
        try:
            output = subprocess.run(["tmux", "capture-pane", "-p"], 
                                  capture_output=True, text=True, check=True)
            if output.stdout:
                # Clean up tmux output by removing extra newlines and whitespace
                cleaned_lines = [line.strip() for line in output.stdout.splitlines() if line.strip()]
                return '\n'.join(cleaned_lines[-DEFAULT_HISTORY_LINES:])
        except subprocess.SubprocessError as e:
            warnings.warn(f"Failed to get tmux history: {str(e)}")
    
    # Fallback to zsh history
    return get_zsh_history(num_lines)


if __name__ == "__main__":
    print(get_terminal_history())
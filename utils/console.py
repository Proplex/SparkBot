from config import Config
import os

class Console:
    @staticmethod
    def grabPane():
        os.system("tmux capture-pane -t " + Config.TMUX_PANE)
        os.system("tmux save-buffer " + Config.TMUX_BUFFER_LOCATION)
        
    @staticmethod
    def executeCommand(cmd):
        os.system("tmux send-keys -t " + Config.TMUX_PANE + " \"" + cmd + "\" Enter")
import os 
import time 
import threading
from flask import Flask,render_template
from flask_socketio import SocketIO,emit 

class LogMonitor:
    def __init__(self,filepath = "log.txt",maxlines = 10):
        self.filepath = filepath
        self.maxlines = maxlines 

        self.app = Flask(__name__)
        self.socketio = SocketIO(self.app,cors_allowed_origins= "*")

        self._setup_route()
        self._socket_events()

    def _setup_route(self):
        @self.app.route('/')
        def index():
            return render_template('index.html')
        
    def _socket_events(self):
        @self.socketio.on('connect')
        def handle_connection():
            print("client connected")
            initial_lines = self.get_last_n_lines(self.filepath,self.maxlines)
            self.socketio.emit('initial_logs', {'data': ''.join(initial_lines)})

    def get_last_n_lines(self,filepath,n):
        try:
            if not os.path.exists(filepath):
                return ["Log file yet to be created"]
            
            with open(filepath, 'r') as file:
                file.seek(0,os.SEEK_END)  
                filesize = file.tell() 

                lines = []
                chunksize = 1048576                             
                position = max(filesize - chunksize,0)

                while len(lines) < n and position >= 0:
                    file.seek(position)
                    chunk = file.read(min(filesize - position,chunksize))
                    
                    chunklines = chunk.splitlines() 

                    #broken lines? 
                    if position > 0 and len(lines) == 0 and len(chunklines) > 0:
                        chunklines = chunklines[1:] 

                    lines = chunklines + lines 
                    position -= chunksize 
            
                return [line + '\n' for line in lines[-n:]] 
        
        except Exception as e:
            return [f"Error reading log file: {str(e)}"]
    

    def watch_log_file(self):

        if not os.path.exists(self.filepath):
            with open(self.filepath, 'w') as file:
                file.write(f"Log file created at {time.strftime('%Y-%m-%d %H:%M:%S')}\n")

        fileposition = os.path.getsize(self.filepath)

        while True:
            try:
                currsize = os.path.getsize(self.filepath)

                #new lines appended?
                if currsize > fileposition:                             
                    with open(self.filepath, 'r') as file:
                        file.seek(fileposition)
                        newdata = file.read()

                        fileposition = currsize 

                        if newdata:
                            newlines = newdata.splitlines('\n')
                            for line in newlines:
                                if line.strip(): #only non empty lines
                                    self.socketio.emit('log_updates',{'data': line})
                
                time.sleep(0.2)
            
            except Exception as e:
                print(f"Error reading log file: {str(e)}") 
                time.sleep(5)

    
    def start(self):
        log_watcher_thread = threading.Thread(target= self.watch_log_file, daemon= True)
        log_watcher_thread.start()

        print(f"Log watcher currently watching log file at {self.filepath}")
        print("Access web client at http://localhost:5000")

        self.socketio.run(self.app,host= "0.0.0.0", port= 5000 ,debug= True, use_reloader= False)

if __name__ == "__main__":
    Monitor = LogMonitor()
    Monitor.start()



              
        



        
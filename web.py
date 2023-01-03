
from http.server import BaseHTTPRequestHandler, HTTPServer
import time, json, pytgcf

hostName = ''
serverPort = 9191
api_path = '' #например 'pytgcf': /pytgcf/...

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        query = self.path.split('/')
        if api_path == query[1]:
            query.remove(api_path) 
        
        if len(query) == 2: 
            channel = pytgcf.get(query[1])
            result = channel.__dict__
            if channel: result['latests'] = [post.__dict__ for post in channel.latests]
            data = json.dumps(result, ensure_ascii=False).encode('utf-8')
            self.wfile.write(data)
        
        if len(query) == 4:
            channel = pytgcf.get(query[1])
            if query[2] == 'chunk': result = [post.__dict__ for post in channel.chunk(int(query[3]), True)]
            if query[2] == 'post': result = channel.post(int(query[3])).__dict__
            data = json.dumps(result, ensure_ascii=False).encode('utf-8')
            self.wfile.write(data)
        try:
            if len(query) == 5 and  query[2] == 'chunk' and query[4] == 'full':
                channel = pytgcf.get(query[1])
                result = [post.__dict__ for post in channel.chunk(int(query[3]), True)]
                data = json.dumps(result, ensure_ascii=False).encode('utf-8')
                self.wfile.write(data)                
        except:...    
        
        if len(query) > 4:
            channel = pytgcf.get(query[1])
            post = channel.post(int(query[3]))
            if query[4] == 'comments':
                try: limit = int(query[5])
                except: limit = 100
                comments = post.comments(limit=limit)
                if comments: 
                    result = []
                    for comment in comments:
                        temp = comment.__dict__
                        temp['author'] = comment.author.__dict__
                        result.append(temp)
                        
                else: result = {'status': None}
            if query[4] == 'comment':
                comment = post.comments(id=int(query[5]))
                result = []
                temp = comment.__dict__
                temp['author'] = comment.author.__dict__
                result = temp
                    
            data = json.dumps(result, ensure_ascii=False).encode('utf-8')
            self.wfile.write(data)

                
            

if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))
    try: webServer.serve_forever()
    except KeyboardInterrupt: pass
    webServer.server_close()
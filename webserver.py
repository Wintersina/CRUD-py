from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Resturant, MenuItem

sql_lite_db = create_engine('sqlite:///resturantmenu.db')  # say what database
Base.metadata.bind = sql_lite_db
DBsession = sessionmaker(bind = sql_lite_db)
session = DBsession()


class webServerHandler(BaseHTTPRequestHandler):



    def do_GET(self):

        try:
            if self.path.endswith("/hello"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<!DOCTYPE html><title>hello Server</title>"
                output += "<h1>Hello!</h1>"
                output += '''<form method='POST' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
                self.wfile.write(output.encode())
                print("i'm being redirected to hello" + output)
                return

            if self.path.endswith("/hola"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<!DOCTYPE html><title>hola server</title>"
                output += "<h1>&#161 Hola !</h1>"
                output += '''<form method='POST' action='/hola'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
                self.wfile.write(output.encode())
                print (output)
                return

            if self.path.endswith("/restaurants"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = "<!DOCTYPE html><title>Restaurants</title>"
                output +="<a href=/resturant/new> Make a New Restaurant Here </a><br><br>"

                results = session.query(Resturant).all()

                for r in results:
                    output += str(r.name) + "<br><a href=/resturant/delete> delete </a>"
                    output += "<br><a href=/resturant/"+str(r.id)+"/edit> edit </a><br><br>"

                self.wfile.write(output.encode())
                print (output)
                return

            if self.path.endswith("/resturant/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<!DOCTYPE html><title>Create new Restaurant</title>"
                output += '''<form method='POST' action='/resturant/new'><h2>Make a new Restaurant</h2><input name="message" type="text" placeholder="New Resturant Name" ><input type="submit" value="Create"> </form>'''
                self.wfile.write(output.encode())
                print (output)
                return

            if self.path.endswith("/edit"):
                path = urlparse(self.path)
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<!DOCTYPE html><title>Edit Restaurant</title>"
                output += '''<form method='POST' action='%s'><h2>Make an edit Restaurant</h2><input name="message" type="text" placeholder="edit Resturant Name" ><input type="submit" value="edit"> </form>''' % path.path
                self.wfile.write(output.encode())
                print (output)
                return

            if self.path.endswith("/delete"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<!DOCTYPE html><title>Bookmark Server</title>"
                output += '''<form method='POST' action='/resturant/delete'><h2>delete a Restaurant</h2><input name="message" type="text" placeholder="Delete Resturant Name" ><input type="submit" value="Create"> </form>'''
                self.wfile.write(output.encode())
                print (output)
                return





        except IOError:
            self.send_response(404)
            self.wfile.write("no form fields found :(".encode())

    def do_POST(self):
        try:

            if self.path.endswith("/resturant/new"):
                #get length of new content
                length = int(self.headers.get('Content-length'))
                #gather the body html and decode
                body = self.rfile.read(length).decode()
                #debug
                print("body is: "+ str(body))
                #parse the body for messages
                params = parse_qs(body)

                newResturant = Resturant(name =  str(params["message"][0])) # crate a new resturant
                session.add(newResturant) # add new resturant to staging zone
                session.commit() #commit to database

                self.send_response(301)
                self.send_header('Location', '/restaurants')
                self.end_headers()

                #debug
                print(output)

            if self.path.endswith("/edit"):
                print("YOU ARE IN EDITTT")
                path = urlparse(self.path)
                print("print path: " +str(path))
                split = path.path.split("/")
                print("split : "+ str(split))
                #get length of new content
                length = int(self.headers.get('Content-length'))
                #gather the body html and decode
                body = self.rfile.read(length).decode()
                #debug
                print("value we are looking for path is: "+ str(split[2]))
                #parse the body for messages
                params = parse_qs(body)

                editResturant = session.query(Resturant).get(split[2]) # edit a resturant
                print("edit resturant is: " + str(editResturant))

                editResturant.name = params["message"][0]
                session.add(editResturant)#add to staging
                session.commit() #commit to database
                self.send_response(301)
                self.send_header('Location', '/restaurants')
                self.end_headers()

                #debug
                print(output)

        except:
            pass




def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webServerHandler)
        print ("Web Server running on port %s" % port)
        server.serve_forever()
    except KeyboardInterrupt:
        print (" ^C entered, stopping web server....")
        server.socket.close()

if __name__ == '__main__':
    main()
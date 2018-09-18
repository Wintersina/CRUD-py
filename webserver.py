from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs

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
                output += "<!DOCTYPE html><title>Bookmark Server</title>"
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
                output += "<!DOCTYPE html><title>Bookmark Server</title>"
                output += "<h1>&#161 Hola !</h1>"
                output += '''<form method='POST' action='/hola'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
                self.wfile.write(output.encode())
                print (output)
                return

            if self.path.endswith("/restaurants"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = "<!DOCTYPE html><title>Bookmark Server</title>"
                output +="<a href=/resturant/new> Make a New Restaurant Here </a><br><br>"

                results = session.query(Resturant).all()

                for r in results:
                    output += str(r.name) + "<br><a href=/delete_restaurant> edit </a>"
                    output += "<br><a href=/edit_restaurant> delete </a><br><br>"

                self.wfile.write(output.encode())
                print (output)
                return

            if self.path.endswith("/resturant/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<!DOCTYPE html><title>Bookmark Server</title>"
                output += '''<form method='POST' action='/restaurants'><h2>Make a new Restaurant</h2><input name="message" type="text" value="New Resturant Name" ><input type="submit" value="Create"> </form>'''
                self.wfile.write(output.encode())
                print (output)
                return





        except IOError:
            self.send_response(404)
            self.wfile.write("no form fields found :(".encode())

    def do_POST(self):
        try:

            length = int(self.headers.get('Content-length'))
            body = self.rfile.read(length).decode()
            print("body is: "+ str(body))
            params = parse_qs(body)
            print("prams are: " + str(params))


            newResturant = Resturant(name =  str(params["message"][0])) # crate a new resturant
            session.add(newResturant) # add new resturant to staging zone
            session.commit() #commit to database
            self.send_response(303)
            self.send_header('Location', '/restaurants')
            self.end_headers()

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
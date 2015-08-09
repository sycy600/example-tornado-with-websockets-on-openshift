# Chat application

This is a simple example how to use Tornado framework and websockets. This application can be deployed to OpenShift.

Multiple users can use this basic chat - when an user enters the webpage, then a websocket connection is created with the chat server. If one user sends some data to server then this data is broadcasted to all connected users.

Some notes to mention about making it working with OpenShift:

* normal HTTP traffic listens on port 80 (but I guess it is 8080 inside OpenShift) and port 8000 listens for websocket traffic
* there must be a filename named `app.py` to make the webserver working, OpenShift uses this file to start the server
* the websocket handler should implement `check_origin` method returning `True` otherwise the response will be 403 for an incoming websocket connection. However this seems to be a security bypass so it may be a security hole
* the application should be bound to internal IP of OpenShift environment - not localhost, so IP must be passed there explicitly

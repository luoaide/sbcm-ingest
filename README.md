# sbcm-ingest

## Components

Webserver - hosted on the SBCM... APIs allow web requests to modify on-board configurations.
     - so you would connect your SBCM to your computer and pull up the website and change radio settings

Video Server - an aim point for any number of incoming streams / sources

Analysis Application - takes any (all?) of the streams hitting the server and runs analysis...
    - outputs COTS messages to the MANET / TAK Server?

Maven Video Forwarder - handles the networking/formatting requirements to get the video up to Maven.
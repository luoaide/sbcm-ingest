CC      = gcc

PKG_CONFIG_PATH=/Library/Frameworks/GStreamer.framework/Versions/1.0/lib/pkgconfig
CFLAGS  = -I/Library/Frameworks/GStreamer.framework/Headers
LIBS    = -F/Library/Frameworks -framework GStreamer
# If I wasn't on MacOS, I would need to provide the libraries for linking: -L/Library/Frameworks/GStreamer.framework/Library

TARGET  = main
SRC     = rtsp_server.c
OBJ     = rtsp_server.o

# default build rule
all: $(TARGET)

#LINK
$(TARGET): $(OBJ)
	$(CC) $(OBJ) -o $(TARGET) $(LIBS)

#COMPILE
$(OBJ): $(SRC)
	$(CC) $(CFLAGS) -c $(SRC) -o $(OBJ)

clean:
	rm -f $(TARGET) $(OBJ)
# Compiler and flags
CC = gcc
CFLAGS = -Wall -Wextra

# Target and source
TARGET = PingClient
SRC = PingClient.c

# Default rule
all: $(TARGET)

# Build target
$(TARGET): $(SRC)
	$(CC) $(CFLAGS) -o $(TARGET) $(SRC)

# Clean rule
clean:
	rm -f $(TARGET)


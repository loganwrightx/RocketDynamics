# Compiler and flags
CC = gcc
CFLAGS = -Wall -Wextra -g -Iinclude
LDFLAGS = -lm

# Source and object directories
SRC_DIR = src
OBJ_DIR = obj
BIN_DIR = bin

# Source files
SOURCES = main.c $(wildcard $(SRC_DIR)/*.c)

# Object files
OBJECTS = $(SOURCES:$(SRC_DIR)/%.c=$(OBJ_DIR)/%.o)

# Vehicle Dynamics Simulator
TARGET = vds

# Default target
all: $(BIN_DIR)/$(TARGET)

# Compile object files
$(OBJ_DIR)/%.o: $(SRC_DIR)/%.c
	@mkdir -p $(OBJ_DIR)
	$(CC) $(CFLAGS) -c $< -o $@

# Link object files to create the executable
$(BIN_DIR)/$(TARGET): $(OBJECTS)
	@mkdir -p $(BIN_DIR)
	$(CC) $(LDFLAGS) -o $@ $(OBJECTS)

# Clean build artifacts
clean:
	rm -rf $(OBJ_DIR) $(BIN_DIR)

# Phony targets
.PHONY: all clean
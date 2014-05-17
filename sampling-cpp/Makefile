# CC  = /projects/grail/tqchen/usr/bin/gcc
# CXX = /projects/grail/tqchen/usr/bin/g++
CC  = clang
CXX = clang++
RM=rm -f
CFLAGS = -g -Wall -O3 -msse2 -std=c++11 -Wno-unknown-pragmas -Iinclude -Iplugin #-fopenmp 
LDFLAGS= -lm #-pthread

BIN = main
OBJ = graph.o main.o
.PHONY: clean all

all: $(BIN) $(OBJ) 

main: $(OBJ)
graph.o: graph.cc graph.h
main.o: graph.h main.cc
$(BIN) : 
	$(CXX) $(CFLAGS) $(LDFLAGS) -o $@ $(filter %.cpp %.o %.c %.cc, $^)

$(OBJ) : 
	$(CXX) -c $(CFLAGS) -o $@ $(firstword $(filter %.cpp %.c %.cc, $^) )
clean:
	$(RM) $(OBJ) $(OBJ_TEST) $(BIN) $(BIN_TEST) *~


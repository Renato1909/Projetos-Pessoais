# Tema 01 em C. Um Makefile para o CI Ubuntu e para o Windows.
#
# As receitas correm em shell POSIX: no Windows usa Git Bash ou MSYS2 (o
# mingw32-make apanha o sh.exe que estiver no PATH, por isso as linhas com
# sintaxe de cmd falhariam ali). Muda apenas o sufixo do executavel.
#
#   make test   -> compila com -Werror e executa as assercoes de contagem
#   make bench  -> compila e executa a tabela de medicoes
#   make clean  -> remove build/
#
# SANITIZE e passado pelo CI para a passada de AddressSanitizer/UBSan:
#   make SANITIZE='-fsanitize=address,undefined -fno-omit-frame-pointer' test

CC ?= gcc
SANITIZE ?=
CFLAGS := -std=c11 -Wall -Wextra -Werror -O2 $(SANITIZE)
BUILD := build

ifeq ($(OS),Windows_NT)
EXE := .exe
else
EXE :=
endif

OBJETOS := $(BUILD)/complexidade.o

.PHONY: all test bench clean

all: test

test: $(BUILD)/test_complexidade$(EXE)
	./$(BUILD)/test_complexidade$(EXE)

bench: $(BUILD)/medir$(EXE)
	./$(BUILD)/medir$(EXE)

$(BUILD):
	mkdir -p $(BUILD)

$(OBJETOS): complexidade.c complexidade.h | $(BUILD)
	$(CC) $(CFLAGS) -c complexidade.c -o $@

$(BUILD)/test_complexidade$(EXE): tests/test_complexidade.c $(OBJETOS) | $(BUILD)
	$(CC) $(CFLAGS) tests/test_complexidade.c $(OBJETOS) -o $@

$(BUILD)/medir$(EXE): medir.c $(OBJETOS) | $(BUILD)
	$(CC) $(CFLAGS) medir.c $(OBJETOS) -o $@

clean:
	rm -rf $(BUILD)

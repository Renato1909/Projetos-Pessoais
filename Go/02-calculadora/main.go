package main

import (
	"fmt"
	"os"
	"strconv"
)

func main() {
	if len(os.Args) != 4 {
		fmt.Println("Uso: go run main.go <num> <op + - * /> <num>  ex: 10 * 3")
		return
	}
	a, _ := strconv.ParseFloat(os.Args[1], 64)
	b, _ := strconv.ParseFloat(os.Args[3], 64)
	op := os.Args[2]
	var r float64
	switch op {
	case "+": r = a + b
	case "-": r = a - b
	case "*": r = a * b
	case "/": if b == 0 { fmt.Println("Erro: /0"); return }; r = a / b
	default: fmt.Println("Op invalido"); return
	}
	fmt.Printf("Resultado: %.2f\n", r)
}

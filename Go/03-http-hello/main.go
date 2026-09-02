package main

import (
	"fmt"
	"log"
	"net/http"
)

func handler(w http.ResponseWriter, r *http.Request) {
	fmt.Fprintf(w, "Hello do Go! Rota: %s\n", r.URL.Path)
}

func main() {
	http.HandleFunc("/", handler)
	fmt.Println("Go/03 - http://localhost:8080")
	log.Fatal(http.ListenAndServe(":8080", nil))
}

run:
	go run ./cmd/server

build:
	go build -o bin/server.exe ./cmd/server

test:
	go test ./...

vet:
	go vet ./...

fmt:
	gofmt -l -w .

tidy:
	go mod tidy

clean:
	if exist bin rmdir /s /q bin

.PHONY: run build test vet fmt tidy clean

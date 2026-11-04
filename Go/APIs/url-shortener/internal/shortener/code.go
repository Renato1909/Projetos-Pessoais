package shortener

import (
	"crypto/rand"
	"errors"
	"math/big"
)

const alphabet = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

const CodeLength = 7

var ErrCodeGeneration = errors.New("falha ao gerar código aleatório")

func NewCode() (string, error) {
	out := make([]byte, CodeLength)
	max := big.NewInt(int64(len(alphabet)))
	for i := range out {
		n, err := rand.Int(rand.Reader, max)
		if err != nil {
			return "", ErrCodeGeneration
		}
		out[i] = alphabet[n.Int64()]
	}
	return string(out), nil
}

func IsValidCode(code string) bool {
	if len(code) != CodeLength {
		return false
	}
	for _, c := range code {
		if c < '0' || (c > '9' && c < 'A') || (c > 'Z' && c < 'a') || c > 'z' {
			return false
		}
	}
	return true
}

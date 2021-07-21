package greetings

import (
  "fmt"
  "errors"
)

// Hello returns a grettings fof the named person
func Hello(name string) (string, error) {
    if name == "" {
      return "", errors.New("Empty Name")
    }
    message := fmt.Sprintf("Hi, %v. Welcome!", name)
    return message, nil
}

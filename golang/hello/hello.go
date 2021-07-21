package main

import (
  "fmt"
  "log"
  "example.com/greetings"
)

const engHelloPrefix = "Hello, "
const koHelloPrefix = "안녕, "
const esHelloPrefix = "Hola, "


func getPrefixByLang(language string) string {
    switch language {
        case "ko":
          return koHelloPrefix
        case "es":
          return esHelloPrefix
        default:
          return engHelloPrefix
    }
}


func Hello(name string, language string) string {
    if name == ""{
      name = "World"
    }

    prefix := getPrefixByLang(language)

    return prefix + name
}

func main() {
    log.SetPrefix("greetings: ")
    log.SetFlags(0)

    message, err := greetings.Hello("Gladys")

    if err != nil {
        log.Fatal(err)
    }

    fmt.Println(message)
}

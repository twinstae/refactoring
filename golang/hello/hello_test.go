package main

import "testing"

func TestHello(t *testing.T) {
    assertCorrectMessage := func(t testing.TB, got, want string){
        t.Helper()
        if got != want {
            t.Errorf("got %q want %q", got, want)
        }
    }

    t.Run("sayng hello to people", func (t *testing.T) {
        got := Hello("Chris", "en")
        want := "Hello, Chris"

        assertCorrectMessage(t, got, want)
    })

    t.Run("empty string defaults to 'World'", func(t *testing.T) {
        assertCorrectMessage(
          t,
          Hello("", "en"),
          "Hello, World",
        )
    })

    t.Run("스페인어(es) 지원", func(t *testing.T){
        assertCorrectMessage(
          t,
          Hello("Elodie", "es"),
          "Hola, Elodie",
        )
    })


    t.Run("한국어(ko) 지원", func(t *testing.T){
        assertCorrectMessage(
          t,
          Hello("태희", "ko"),
          "안녕, 태희",
        )
    })
}

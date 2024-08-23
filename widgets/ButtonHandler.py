from typing import Dict, Callable

def get_pressed_button(methods: Dict[str, Callable[[], str]], result: str):
    for key, method in methods.items():
        if not callable(method):
            raise TypeError(f"Der Wert für Schlüssel '{key}' ist keine Funktion.")
        if key in result:
            method()
            return
import sys
from parser import run_interpreter

def main():
    if len(sys.argv) < 2:
        print("Użycie: python main.py <plik_ze_skryptem.txt>")
        return

    file_path = sys.argv[1]

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            kod_zrodlowy = file.read()
            
        print(f"--- Uruchamianie skryptu: {file_path} ---\n")
        run_interpreter(kod_zrodlowy)
        print("\n--- Zakończono działanie programu ---")
        
    except FileNotFoundError:
        print(f"Błąd: Nie znaleziono pliku '{file_path}'.")
    except Exception as e:
        print(f"Wystąpił nieoczekiwany błąd: {e}")

if __name__ == "__main__":
    main()

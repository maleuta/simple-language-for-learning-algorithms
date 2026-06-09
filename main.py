import sys
from parser import run_interpreter

def run_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            kod_zrodlowy = file.read()
            
        print(f"--- Uruchamianie skryptu: {file_path} ---\n")
        run_interpreter(kod_zrodlowy)
        print("\n--- Zakończono działanie programu ---")
        
    except FileNotFoundError:
        print(f"[BŁĄD]: Nie znaleziono pliku '{file_path}'.")
    except Exception as e:
        print(f"[BŁĄD]: Wystąpił nieoczekiwany błąd: {e}")

def interactive_mode():
    print("=" * 50)
    print(" INTERAKTYWNY INTERPRETER (REPL) ")
    print(" Wpisuj kod. Aby zakończyć i wykonać, wpisz 'END.' ")
    print(" Aby wyjść z programu, wpisz 'exit' ")
    print("=" * 50)
    
    while True:
        print("\n[Nowy Program] Wpisuj kod:")
        lines = []
        while True:
            try:
                line = input(">>> ")
                if line.strip().lower() == 'exit':
                    print("Zakończono.")
                    return
                lines.append(line)
                if line.strip().endswith('END.'):
                    break
            except KeyboardInterrupt:
                return
                
        kod_zrodlowy = "\n".join(lines)
        print("\n--- Wynik wykonania ---")
        run_interpreter(kod_zrodlowy)
        print("-----------------------")

def main():
    if len(sys.argv) > 1:
        # Jeśli podano plik jako argument, wykonaj go
        file_path = sys.argv[1]
        run_file(file_path)
    else:
        # Menu główne w konsoli
        print("Wybierz tryb:")
        print("1. Wczytaj kod z pliku (skrypt.txt)")
        print("2. Tryb interaktywny (Konsola REPL)")
        print("3. Wyjście")
        
        wybor = input("Wybór (1-3): ")
        if wybor == '1':
            sciezka = input("Podaj nazwę pliku (np. skrypt.txt): ")
            run_file(sciezka)
        elif wybor == '2':
            interactive_mode()
        else:
            print("Zakończono.")

if __name__ == "__main__":
    main()
    
    
    
# import sys
# from parser import run_interpreter

# def main():
#     if len(sys.argv) < 2:
#         print("Użycie: python main.py <plik_ze_skryptem.txt>")
#         return

#     file_path = sys.argv[1]

#     try:
#         with open(file_path, 'r', encoding='utf-8') as file:
#             kod_zrodlowy = file.read()
            
#         print(f"--- Uruchamianie skryptu: {file_path} ---\n")
#         run_interpreter(kod_zrodlowy)
#         print("\n--- Zakończono działanie programu ---")
        
#     except FileNotFoundError:
#         print(f"Błąd: Nie znaleziono pliku '{file_path}'.")
#     except Exception as e:
#         print(f"Wystąpił nieoczekiwany błąd: {e}")

# if __name__ == "__main__":
#     main()

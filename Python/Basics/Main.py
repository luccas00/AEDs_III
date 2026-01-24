class Main:

    # Fibonacci example
    def fibonacci(n):
        if n <= 0:
            return 0
        elif n == 1:
            return 1
        else:
            return Main.fibonacci(n-1) + Main.fibonacci(n-2)

    # Fatorial example
    def fatorial(n):
        if n == 0:
            return 1
        else:
            return n * Main.fatorial(n-1)

    # Media example
    def media(lista):
        return sum(lista) / len(lista)

    def main():
        print("Hello, World!")
        import sys

        print("Fibonacci de 10:", Main.fibonacci(10))
        print("Fatorial de 5:", Main.fatorial(5))
        print("Media de [1, 2, 3, 4, 5]:", Main.media([1, 2, 3, 4, 5]))

        print("Argumentos da linha de comando:")
        for arg in sys.argv:
            print(arg)

        print("Fim do programa.")

if __name__ == "__main__":
    Main.main()

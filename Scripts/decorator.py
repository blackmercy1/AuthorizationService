def select(input_func):
    def output_func(*args):
        print("*****************" + "\n" +args[0])
        input_func(args[0], args[1])
        print("*****************" + "\n" + str(args[1]))

    return output_func


@select
def hello(name: str, age: int):
    print("Hello World")


hello("John", 25)

import fruit

@fruit.step(name='First Step', help='The first step in the tow')
def first_step():
    fruit.echo("This is my first step")

@fruit.step(name='Second Step')
def second_step():
    fruit.echo("This is my second step")

@fruit.target()
def example():
    first_step()
    second_step()
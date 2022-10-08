## całki i inne pierdoły

def fun1(x):
    return 2*x**2

def calka(start, stop, fun, acc):
    """
    It takes a function, a start and stop point, and an accuracy, and returns the integral of the
    function between the start and stop points
    
    :param start: the start of the integral
    :param stop: the end of the interval
    :param fun: the function to integrate
    :param acc: accuracy
    :return: The integral of the function fun from start to stop with accuracy acc.
    """
    piece = (stop-start)/acc
    out = 0
    flag = start+piece/2
    while flag<stop:
        b = fun(flag)
        p = b * piece
        out = out+p
        flag = flag + piece
    return out

print(calka(2,4,fun1,1000))

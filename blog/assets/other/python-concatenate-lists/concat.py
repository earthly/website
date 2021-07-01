
from itertools import chain
import perfplot
import numpy as np

def add(L):
  x, y = L
  return x.copy() + y

def chain_(L):
  x, y = L
  return list(chain(x.copy(), y))

def unpacking(L):
  x, y = L
  return [*x.copy(), *y]

def extend(L):
  x, y = L
  x = x.copy()
  x.extend(y)

  return x

def iadd(L):
  x, y = L
  x = x.copy()
  x += y

  return x


# plot 1
perfplot.show(
    setup=lambda n: [np.random.choice(100, n).tolist()] * 2,
    kernels=[add, chain_, unpacking, extend, iadd],
    labels=['a + b', 'list(chain(a, b))', '[*a, *b]', 'a.extend(b)', 'a += b'],
    n_range=[2**k for k in range(0, 20)],
    xlabel='len(a)',
    logx=True,
    logy=True)

# plot 2
perfplot.show(
    setup=lambda n: [np.random.choice(100, 100).tolist()] * n,
    kernels=[
        lambda L: sum(L, []),
        lambda L: list(chain.from_iterable(L))
    ],
    labels=['sum', 'chain'],
    n_range=range(1, 1000, 50),
    xlabel='# lists',
    logy=True,
    logx=True)
#################### Phase 1 ####################

##### Pos2D

def test_pos2d_import():
    from pos2d import Pos2D

def test_pos2d_eq():
    from pos2d import Pos2D
    point1 = Pos2D(8, 6)
    point2 = Pos2D(8, 6)
    assert point1 == point2

def test_pos2_neq():
    from pos2d import Pos2D
    point1 = Pos2D(8, 6)
    point2 = Pos2D(6, 8)
    assert point1 != point2

##### Grid

def __ensure_hash():
    from pos2d import Pos2D
    Pos2D.__hash__ = lambda p: hash(tuple(p.__dict__.items()))
    return Pos2D

def __get_nb_edges(G: 'Grid', w: int, h: int) -> int:
    __ensure_hash()
    from pos2d import Pos2D
    return len(set.union(*[{frozenset((p, q)) for q in G.accessible_neighbours(p)} \
                           for p in (Pos2D(x, y) for x in range(w) for y in range(h))]))

def test_node_import():
    from grid import Node

def test_grid_import():
    from grid import Grid

def test_empty_init():
    from grid import Grid
    w = h = 10
    G = Grid(w, h)
    assert __get_nb_edges(G, w, h) == 2*(w-1)*(h-1)+w+h-2

def test_wall_creation():
    from pos2d import Pos2D
    from grid import Grid
    w = h = 10
    G = Grid(w, h)
    E = __get_nb_edges(G, w, h)
    G.add_wall(Pos2D(0, 0), Pos2D(0, 1))
    assert __get_nb_edges(G, w, h) == E-1

def test_wall_removal():
    from pos2d import Pos2D
    from grid import Grid
    w = h = 10
    G = Grid(w, h)
    E = __get_nb_edges(G, w, h)
    G.add_wall(Pos2D(0, 0), Pos2D(0, 1))
    G.remove_wall(Pos2D(0, 1), Pos2D(0, 0))
    assert __get_nb_edges(G, w, h) == E

def test_accessible_neighbours():
    Pos2D = __ensure_hash()
    from grid import Grid
    w = 8
    h = 10
    G = Grid(w, h)
    assert {Pos2D(0, 1), Pos2D(1, 0)} == set(G.accessible_neighbours(Pos2D(0, 0)))

def test_accessible_neighbours_symmetry():
    Pos2D = __ensure_hash()
    from grid import Grid
    w = 8
    h = 10
    G = Grid(w, h)
    assert all(
        p in G.accessible_neighbours(q) \
        for p in (Pos2D(x, y) for x in range(w) for y in range(h)) \
        for q in G.accessible_neighbours(p)
    )

##### GridRenderer

def __strip_equal(a, b):
    return a.strip() == b.strip()

def test_import_gridrenderer():
    from renderer import GridRenderer

def test_gridrenderer_empty_2_by_2(capsys):
    from grid import Grid
    from renderer import GridRenderer
    w = h = 2
    GridRenderer(Grid(w, h)).show()
    output = capsys.readouterr().out
    expected = '''
┌───────┐
│       │
│       │
│       │
└───────┘
'''
    assert __strip_equal(output, expected)

def test_grid_rederer_walls(capsys):
    from pos2d import Pos2D
    from grid import Grid
    from renderer import GridRenderer
    w = h = 3
    G = Grid(w, h)
    for x0, y0, x1, y1 in [(0, 0, 1, 0), (0, 1, 1, 1), (1, 2, 1, 1), (2, 2, 2, 1)]:
        G.add_wall(Pos2D(x0, y0), Pos2D(x1, y1))
    expected = '''
┌───┬───────┐
│   │       │
│   │       │
│   │       │
│   └───────┤
│           │
└───────────┘
'''
    GridRenderer(G).show()
    output = capsys.readouterr().out
    assert __strip_equal(output, expected)

#################### Phase 2 ####################

def __make_params(width, height, rooms=5, bonuses=2, seed=None,
                  view_radius=6, torch_delay=7, bonus_radius=3,
                  minwidth=4, maxwidth=8, minheight=4, maxheight=8,
                  openings=2, hard=False,
                  ghosts=0, ghosts_delay=2, ghosts_walls=False):
    params = locals()
    import argparse
    return argparse.Namespace(**params)

def __default_params(width=40, height=20):
    return __make_params(width, height)

def __no_room_hardmode_params(width, height):
    return __make_params(
        width=width, height=height,
        seed=0xCAFE, rooms=0, hard=True,
        minwidth=4, minheight=4, maxwidth=4, maxheight=4
    )

def __no_room_params(width, height):
    return __make_params(
        width=width, height=height,
        seed=0xC0FFEE, rooms=0,
        minwidth=4, maxwidth=4, minheight=4, maxheight=4
    )

def __is_connected(grid: 'Grid', width: int, height: int) -> bool:
    ''' It is complicated to write tests without writing the answer... '''
    from pos2d import Pos2D
    c = n = width*height
    p, h = list(range(n)), [1]*n
    def f(x):
        r = x
        while p[r] != r: r = p[r]
        while x != r: p[x] = r; x = p[x]
        return r
    def u(x,y):
        nonlocal c
        i, j = f(x),f(y)
        if i == j: return
        c -= 1
        if h[i] < h[j]: p[i] = j
        elif h[i] > h[j]: p[j] = i
        else: p[i] = j; h[i] += 1
    _V = {Pos2D(x, y): x+width*y for x in range(width) for y in range(height)}
    [u(_V[v], _V[w]) for v in _V for w in grid.accessible_neighbours(v)]
    return c == 1

def __is_labyrinth(grid: 'Grid', width: int, height: int) -> bool:
    return __get_nb_edges(grid, width, height) == width*height-1 and \
           __is_connected(grid, width, height)

def test_dungeongenerator_import():
    from generation import DungeonGenerator

def test_argparse_parameters():
    from generation import DungeonGenerator
    generator = DungeonGenerator(__default_params())

def test_dungeongenerator_generate():
    from generation import DungeonGenerator
    from grid import Grid
    dungeon = DungeonGenerator(__default_params()).generate()
    assert isinstance(dungeon, dict)
    assert 'grid' in dungeon
    assert isinstance(dungeon['grid'], Grid)

def test_dungeongenerator_generate_labyrinth_no_room():
    from generation import DungeonGenerator
    w = h = 10
    grid = DungeonGenerator(__no_room_hardmode_params(w, h)).generate()['grid']
    assert __is_labyrinth(grid, w, h)

def test_dungeongenerator_generate_dungeon():
    from generation import DungeonGenerator
    w, h = 40, 20
    grid = DungeonGenerator(__default_params(w, h)).generate()['grid']
    assert __is_connected(grid, w, h)


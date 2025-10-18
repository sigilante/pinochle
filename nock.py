from noun import Cell, deep, parse, noun

# Constants as nouns
tru = 0
bad = 1

def to_noun(n) -> noun:
    """Convert Python values to nouns using pynoun's representation"""
    if isinstance(n, noun):
        return n
    elif isinstance(n, int):
        if n < 0:
            raise ValueError(f"Noun integers must be non-negative, got {n}")
        return n
    elif isinstance(n, tuple):
        if len(n) == 0:
            raise ValueError("Empty tuple cannot be converted to Noun")
        elif len(n) == 1:
            return to_noun(n[0])
        elif len(n) == 2:
            return Cell(to_noun(n[0]), to_noun(n[1]))
        else:
            # Right-branching for tuples > 2
            return Cell(to_noun(n[0]), to_noun(n[1:]))
    else:
        raise ValueError(f"Cannot convert {n} to Noun")

def isatom(n: noun) -> noun:
    """Returns tru (0) if atom, bad (1) if cell"""
    n = to_noun(n)
    return tru if not deep(n) else bad

def iscell(n: noun) -> noun:
    """Returns tru (0) if cell, bad (1) if atom"""
    n = to_noun(n)
    return tru if deep(n) else bad

def head(n: noun) -> noun:
    n = to_noun(n)
    if not deep(n):
        raise Exception("fail: atom")
    return n.head

def tail(n: noun) -> noun:
    n = to_noun(n)
    if not deep(n):
        raise Exception("fail: atom")
    return n.tail

def wut(n: noun) -> noun:
    return iscell(n)

# +[a b]              +[a b]
# +a                  1 + a
def lus(n: noun) -> noun:
    n = to_noun(n)
    if isatom(n) == tru:
        return n + 1
    else:
        raise Exception("fail: cell")

# =[a a]              0
# =[a b]              1
def tis(a, b) -> noun:
    a = to_noun(a)
    b = to_noun(b)
    return tru if a == b else bad

# /[1 a]              a
# /[2 a b]            a
# /[3 a b]            b
# /[(a + a) b]        /[2 /[a b]]
# /[(a + a + 1) b]    /[3 /[a b]]
# /a                  /a
def fas(x, n: noun) -> noun:
    x = to_noun(x)
    n = to_noun(n)
    
    if deep(x):
        raise Exception("fas: first argument must be atom")
    
    if x == 0:
        raise Exception("fail")
    elif x == 1:
        return n
    elif x == 2:
        return head(n)
    elif x == 3:
        return tail(n)
    else:
        if x % 2 == 0:
            return fas(2, fas(x // 2, n))
        else:
            return fas(3, fas(x // 2, n))

# #[1 a b]            a
# #[(a + a) b c]      #[a [b /[(a + a + 1) c]] c]
# #[(a + a + 1) b c]  #[a [/[(a + a) c] b] c]
# #a                  #a
def hax(x: noun, a: noun, b: noun) -> noun:
    x = to_noun(x)
    a = to_noun(a)
    b = to_noun(b)
    
    if deep(x):
        raise Exception("fail: x must be atom")
    
    if x == 1:
        return a
    elif x % 2 == 0:
        new_axis = x // 2
        new_a = Cell(a, fas(x + 1, b))
        return hax(new_axis, new_a, b)
    else:
        new_axis = x // 2
        new_a = Cell(fas(x - 1, b), a)
        return hax(new_axis, new_a, b)

def nock(a, formula):
    """The Nock virtual machine interpreter"""
    a = to_noun(a)
    formula = to_noun(formula)
    
    if deep(formula):
        f_head = head(formula)
        f_tail = tail(formula)
        
        # *[a [b c] d]        [*[a b c] *[a d]]
        if deep(f_head):
            left = nock(a, f_head)
            right = nock(a, f_tail)
            return Cell(left, right)
        
        # Head is an atom - it's an opcode
        if deep(f_head):
            raise Exception("Opcode must be an atom")
        
        opcode = f_head
        
        if opcode == 0:
            # *[a 0 b] = /[b a]
            b = f_tail
            return fas(b, a)
        
        elif opcode == 1:
            # *[a 1 b] = b
            return f_tail
        
        elif opcode == 2:
            # *[a 2 b c] = *[*[a b] *[a c]]
            b = head(f_tail)
            c = tail(f_tail)
            return nock(nock(a, b), nock(a, c))
        
        elif opcode == 3:
            # *[a 3 b] = ?*[a b]
            b = f_tail
            result = nock(a, b)
            return wut(result)
        
        elif opcode == 4:
            # *[a 4 b] = +*[a b]
            b = f_tail
            result = nock(a, b)
            return lus(result)
        
        elif opcode == 5:
            # *[a 5 b c] = =[*[a b] *[a c]]
            b = head(f_tail)
            c = tail(f_tail)
            return tis(nock(a, b), nock(a, c))
        
        elif opcode == 6:
            # *[a 6 b c d] = *[a *[[c d] 0 *[[2 3] 0 *[a 4 4 b]]]]
            b = head(f_tail)
            cd_tail = tail(f_tail)
            c = head(cd_tail)
            d = tail(cd_tail)
            
            inner = nock(a, Cell(4, Cell(4, b)))
            middle = nock(a, Cell(Cell(2, 3), Cell(0, inner)))
            outer_formula = Cell(Cell(c, d), Cell(0, middle))
            return nock(a, outer_formula)
        
        elif opcode == 7:
            # *[a 7 b c] = *[*[a b] c]
            b = head(f_tail)
            c = tail(f_tail)
            return nock(nock(a, b), c)
        
        elif opcode == 8:
            # *[a 8 b c] = *[[*[a b] a] c]
            b = head(f_tail)
            c = tail(f_tail)
            new_subject = Cell(nock(a, b), a)
            return nock(new_subject, c)
        
        elif opcode == 9:
            # *[a 9 b c] = *[*[a c] 2 [0 1] 0 b]
            b = head(f_tail)
            c = tail(f_tail)
            new_subject = nock(a, c)
            new_formula = Cell(2, Cell(Cell(0, 1), Cell(0, b)))
            return nock(new_subject, new_formula)
        
        elif opcode == 10:
            # *[a 10 [b c] d] = #[b *[a c] *[a d]]
            first_arg = head(f_tail)
            
            if deep(first_arg):  # [b c] case
                b = head(first_arg)
                c = tail(first_arg)
                d = tail(f_tail)
                return hax(b, nock(a, c), nock(a, d))
            else:
                raise Exception("Opcode 10 requires [b c] as first argument")
        
        elif opcode == 11:
            # *[a 11 [b c] d] = *[[*[a c] *[a d]] 0 3]
            # *[a 11 b c] = *[a c]
            first_arg = head(f_tail)
            
            if deep(first_arg):  # first_arg is [b c]
                b = head(first_arg)
                c = tail(first_arg)
                d = tail(f_tail)
                new_subject = Cell(nock(a, c), nock(a, d))
                return nock(new_subject, Cell(0, 3))
            else:
                # *[a 11 b c]
                c = tail(f_tail)
                return nock(a, c)
        
        else:
            raise Exception(f"Unknown opcode: {opcode}")
    
    # *a crashes
    raise Exception("crash: invalid formula (atom)")

# Use pynoun's built-in parser
parse_noun = parse

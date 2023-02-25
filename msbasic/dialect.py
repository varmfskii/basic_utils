class Dialect:
    keywords: tuple[str, int]
    specials = {
        'DATA': ['DATA'], 'ELSE': ['ELSE'], 'FOR': ['FOR'], 'GO': ['GO'],
        'GOSUB': ['GOSUB'], 'GOTO': ['GOTO'], 'IF': ['IF'], 'LET': ['LET'],
        'NEXT': ['NEXT'], 'REM': ['REM', "'"], 'SUB': ['SUB'], 'THEN': ['THEN'],
        'TO': ['TO']
    }
    kw2code: dict[str: int] = {}
    code2kw: dict[int: str] = {}
    kw_keys: [str] = []

    def __init__(self):
        for k, c in self.keywords:
            self.kw2code[k] = c
            self.code2kw[c] = k
            self.kw_keys.append(k)
        self.kw_keys.sort(key=(lambda x: -len(x)))

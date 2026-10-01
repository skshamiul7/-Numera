from django.shortcuts import render
import math
import functools
from collections import Counter


# ============================================================
# TOOL METADATA  (title, description, submit_label per tool)
# ============================================================
TOOL_META = {
    'lcm':            ("LCM Calculator",              "Find the Least Common Multiple of two integers.", "Calculate LCM"),
    'perfect':        ("Perfect Number Check",        "A perfect number equals the sum of its proper divisors.", "Check"),
    'armstrong':      ("Armstrong Number Check",      "E.g. 153 = 1³ + 5³ + 3³.", "Check"),
    'prime_factor':   ("Prime Factorization",         "Break a number into its prime factors.", "Factorize"),
    'sieve':          ("Sieve of Eratosthenes",       "List all primes up to a limit.", "Generate"),
    'twin_prime':     ("Twin Primes",                 "Find prime pairs that differ by 2.", "Find"),
    'coprime':        ("Coprime Check",               "Are two numbers relatively prime?", "Check"),
    'digital_root':   ("Digital Root",                "Repeatedly sum digits until one remains.", "Compute"),
    'digit_ops':      ("Sum & Product of Digits",     "Get the sum and product of a number's digits.", "Compute"),
    'sum_series':     ("Sum of Series",               "Sum of natural numbers, squares, and cubes up to n.", "Compute"),
    'ap':             ("Arithmetic Progression",      "Generate an AP and its sum.", "Generate"),
    'gp':             ("Geometric Progression",       "Generate a GP and its sum.", "Generate"),
    'power':          ("Power Calculator",            "Compute base raised to an exponent.", "Compute"),
    'roots':          ("Square & Cube Root",          "Compute roots of a number.", "Compute"),
    'mod_exp':        ("Modular Exponentiation",      "Compute (base^exp) mod m efficiently.", "Compute"),
    'pascal':         ("Pascal's Triangle",           "Generate the first n rows (max 20).", "Generate"),
    'collatz':        ("Collatz Conjecture",          "3n+1 sequence until you reach 1.", "Run"),
    'area_perimeter': ("Area & Perimeter",            "Circle, rectangle, triangle, or square.", "Compute"),
    'volume_area':    ("Volume & Surface Area",       "Sphere, cube, cylinder, or cone.", "Compute"),
    'pythagorean':    ("Pythagorean Triple Check",    "Does a² + b² = c²?", "Check"),
    'distance':       ("Distance Between Two Points", "Euclidean distance.", "Compute"),
    'midpoint':       ("Midpoint Calculator",         "Midpoint of two points.", "Compute"),
    'slope':          ("Slope Calculator",            "Slope of the line through two points.", "Compute"),
    'stats':          ("Mean / Median / Mode",        "Enter comma-separated numbers.", "Compute"),
    'variance':       ("Variance & Std Dev",          "Population variance and standard deviation.", "Compute"),
    'minmax':         ("Min / Max / Range",           "Get the smallest, largest, and range of a list.", "Compute"),
    'quartiles':      ("Quartiles & IQR",             "Q1, Q2, Q3, and interquartile range.", "Compute"),
    'combinatorics':  ("nPr & nCr",                   "Permutations and combinations.", "Compute"),
    'base_converter': ("Base Converter",              "Convert to/from any base (2–36).", "Convert"),
    'binary_decimal': ("Binary ↔ Decimal",            "Convert between binary and decimal.", "Convert"),
    'roman':          ("Roman Numeral Converter",     "Convert between numbers and Roman numerals.", "Convert"),
    'unit_converter': ("Length Unit Converter",       "Convert between mm, cm, m, km, in, ft, yd, mi.", "Convert"),
    'temperature':    ("Temperature Converter",       "Celsius, Fahrenheit, Kelvin.", "Convert"),
    'random_number':  ("Random Number Generator",     "Generate random integers in a range.", "Generate"),
    'dice_coin':      ("Dice / Coin",                 "Roll a die or flip a coin.", "Roll / Flip"),
    'prime_counter':  ("Prime Counter",               "How many primes are below a limit?", "Count"),
    'happy':          ("Happy Number Check",          "Sum of squares of digits eventually equals 1?", "Check"),
    'kaprekar':       ("Kaprekar's Constant (6174)",  "Enter a 4-digit number to reach 6174.", "Run"),
}


# ============================================================
# RECENTLY USED TRACKING
# ============================================================
def track_recent(request, slug):
    """Store last 5 visited tools in the session."""
    recent = request.session.get('recent_tools', [])
    if slug in recent:
        recent.remove(slug)
    recent.insert(0, slug)
    request.session['recent_tools'] = recent[:5]


def get_recent(request):
    """Return list of tuples (name, icon, slug) for recently used tools."""
    recent_slugs = request.session.get('recent_tools', [])
    tool_info = {
        'evenodd':        ('Even or Odd',           '🔢', 'evenodd'),
        'factorial':      ('Factorial',             '✖️', 'factorial'),
        'fibonacci':      ('Fibonacci',             '🌀', 'fibonacci'),
        'prime':          ('Prime Check',           '🔍', 'prime'),
        'gcd':            ('GCD',                   '📐', 'gcd'),
        'palindrome':     ('Palindrome',            '🔄', 'palindrome'),
        'lcm':            ('LCM',                   '📏', 'lcm'),
        'digit_ops':      ('Digit Sum/Product',     '🔟', 'digit_ops'),
        'digital_root':   ('Digital Root',          '🌱', 'digital_root'),
        'perfect':        ('Perfect Number',        '✨', 'perfect'),
        'armstrong':      ('Armstrong',             '💪', 'armstrong'),
        'prime_factor':   ('Prime Factorization',   '🧩', 'prime_factor'),
        'sieve':          ('Sieve of Eratosthenes', '🕸️', 'sieve'),
        'twin_prime':     ('Twin Primes',           '👯', 'twin_prime'),
        'coprime':        ('Coprime Check',         '🤝', 'coprime'),
        'prime_counter':  ('Prime Counter',         '📊', 'prime_counter'),
        'happy':          ('Happy Number',          '😊', 'happy'),
        'kaprekar':       ('Kaprekar 6174',         '🎯', 'kaprekar'),
        'sum_series':     ('Sum of Series',         '➕', 'sum_series'),
        'ap':             ('Arithmetic Progression','➡️', 'ap'),
        'gp':             ('Geometric Progression', '✴️', 'gp'),
        'pascal':         ("Pascal's Triangle",     '🔺', 'pascal'),
        'collatz':        ('Collatz',               '🌊', 'collatz'),
        'power':          ('Power',                 '⚡', 'power'),
        'roots':          ('Square/Cube Root',      '√',  'roots'),
        'mod_exp':        ('Modular Exponentiation','🔐', 'mod_exp'),
        'combinatorics':  ('nPr & nCr',             '🎲', 'combinatorics'),
        'area_perimeter': ('Area & Perimeter',      '🟦', 'area_perimeter'),
        'volume_area':    ('Volume & Surface',      '🧊', 'volume_area'),
        'pythagorean':    ('Pythagorean',           '📐', 'pythagorean'),
        'distance':       ('Distance',              '📍', 'distance'),
        'midpoint':       ('Midpoint',              '🎯', 'midpoint'),
        'slope':          ('Slope',                 '📉', 'slope'),
        'stats':          ('Mean/Median/Mode',      '📊', 'stats'),
        'variance':       ('Variance & Std Dev',    '📈', 'variance'),
        'minmax':         ('Min/Max/Range',         '🔽', 'minmax'),
        'quartiles':      ('Quartiles & IQR',       '📦', 'quartiles'),
        'base_converter': ('Base Converter',        '🔢', 'base_converter'),
        'binary_decimal': ('Binary ↔ Decimal',      '💻', 'binary_decimal'),
        'roman':          ('Roman Numerals',        '🏛️', 'roman'),
        'unit_converter': ('Length Units',          '📏', 'unit_converter'),
        'temperature':    ('Temperature',           '🌡️', 'temperature'),
        'random_number':  ('Random Number',         '🎰', 'random_number'),
        'dice_coin':      ('Dice / Coin',           '🪙', 'dice_coin'),
    }
    return [tool_info[s] for s in recent_slugs if s in tool_info]


# ============================================================
# DECORATOR: injects title / description / submit_label
#           + tracks recently used tools
# ============================================================
def tool_view(func):
    """
    Wraps a tool view so it always has title/description/submit_label
    in the template context, even when using django.shortcuts.render(),
    and tracks the tool in the user's session (recently used).
    """
    name = func.__name__
    title, description, submit_label = TOOL_META.get(name, (name.title(), "", "Calculate"))

    @functools.wraps(func)
    def wrapper(request, *args, **kwargs):
        # Track this tool as recently used
        track_recent(request, name)

        from django.shortcuts import render as dj_render

        def patched_render(req, template, context=None, *a, **kw):
            context = dict(context) if context else {}
            context.setdefault('title', title)
            context.setdefault('description', description)
            context.setdefault('submit_label', submit_label)
            return dj_render(req, template, context, *a, **kw)

        # Patch django.shortcuts.render inside the module namespace of func
        module = __import__(func.__module__, fromlist=['render'])
        original_render = module.render
        module.render = patched_render
        try:
            return func(request, *args, **kwargs)
        finally:
            module.render = original_render

    return wrapper


# ============================================================
# HOME
# ============================================================
def home(request):
    return render(request, "home.html", {'recent_tools': get_recent(request)})


# ============================================================
# EXISTING TOOLS (unchanged — they don't use the shared layout)
# ============================================================
def evenodd(request):
    result = ''
    if request.method == "POST":
        try:
            number = int(request.POST.get('number'))
        except (TypeError, ValueError):
            result = "Invalid Number"
        else:
            result = "Even Number" if number % 2 == 0 else "Odd Number"
    return render(request, "evenodd.html", {'result': result})


def factorial(request):
    result = ''
    if request.method == "POST":
        try:
            number = int(request.POST.get('number'))
        except (TypeError, ValueError):
            result = "Invalid Number"
        else:
            if number < 0:
                result = "Invalid Number"
            else:
                fact = 1
                for i in range(1, number + 1):
                    fact *= i
                result = f"{number}! = {fact}"
    return render(request, "factorial.html", {'result': result})


def fibonacci(request):
    result = ''
    if request.method == "POST":
        try:
            terms = int(request.POST.get('terms'))
        except (TypeError, ValueError):
            result = "Invalid Number"
        else:
            if terms <= 0:
                result = "Invalid Number"
            else:
                a, b = 0, 1
                sequence = []
                for _ in range(terms):
                    sequence.append(a)
                    a, b = b, a + b
                result = "Fibonacci Sequence: " + ", ".join(map(str, sequence))
    return render(request, "fibonacci.html", {'result': result})


def prime(request):
    result = ''
    if request.method == "POST":
        try:
            number = int(request.POST.get('number'))
        except (TypeError, ValueError):
            result = "Invalid Number"
        else:
            if number <= 1:
                result = "Not Prime"
            else:
                is_prime = True
                for i in range(2, int(number ** 0.5) + 1):
                    if number % i == 0:
                        is_prime = False
                        break
                result = "Prime Number" if is_prime else "Not Prime"
    return render(request, "prime.html", {'result': result})


def gcd(request):
    result = ''
    if request.method == "POST":
        try:
            a = int(request.POST.get('a'))
            b = int(request.POST.get('b'))
        except (TypeError, ValueError):
            result = "Invalid Number"
        else:
            x, y = abs(a), abs(b)
            while y:
                x, y = y, x % y
            result = f"GCD = {x}"
    return render(request, "gcd.html", {'result': result})


def palindrome(request):
    result = ''
    if request.method == "POST":
        try:
            number = int(request.POST.get('number'))
        except (TypeError, ValueError):
            result = "Invalid Number"
        else:
            reversed_number = int(str(number)[::-1])
            if number == reversed_number:
                result = f"Palindrome: {number}"
            else:
                result = f"Not Palindrome: reversed = {reversed_number}"
    return render(request, "palindrome.html", {'result': result})


# ============================================================
# NEW TOOLS — 38 total
# ============================================================

# ---------- 1. LCM ----------
def lcm(request):
    result = ''
    if request.method == "POST":
        try:
            a = int(request.POST.get('a'))
            b = int(request.POST.get('b'))
        except (TypeError, ValueError):
            result = "Invalid Number"
        else:
            x, y = abs(a), abs(b)
            original = (x, y)
            while y:
                x, y = y, x % y
            g = x
            if g == 0:
                result = "LCM is undefined (one value is 0)"
            else:
                result = f"LCM of {original[0]} and {original[1]} = {(original[0] * original[1]) // g}"
    return render(request, "tools/lcm.html", {'result': result})


# ---------- 2. Perfect Number ----------
def perfect(request):
    result = ''
    if request.method == "POST":
        try:
            number = int(request.POST.get('number'))
        except (TypeError, ValueError):
            result = "Invalid Number"
        else:
            if number < 2:
                result = "Not a Perfect Number"
            else:
                divisors = [i for i in range(1, number) if number % i == 0]
                if sum(divisors) == number:
                    result = f"Perfect Number! Divisors: {', '.join(map(str, divisors))}"
                else:
                    result = f"Not a Perfect Number (sum = {sum(divisors)})"
    return render(request, "tools/perfect.html", {'result': result})


# ---------- 3. Armstrong Number ----------
def armstrong(request):
    result = ''
    if request.method == "POST":
        try:
            number = int(request.POST.get('number'))
        except (TypeError, ValueError):
            result = "Invalid Number"
        else:
            digits = str(abs(number))
            power = len(digits)
            total = sum(int(d) ** power for d in digits)
            if total == abs(number):
                result = f"Armstrong Number! ({' + '.join(f'{d}^{power}' for d in digits)} = {total})"
            else:
                result = f"Not an Armstrong Number (sum = {total})"
    return render(request, "tools/armstrong.html", {'result': result})


# ---------- 4. Prime Factorization ----------
def prime_factor(request):
    result = ''
    if request.method == "POST":
        try:
            number = int(request.POST.get('number'))
        except (TypeError, ValueError):
            result = "Invalid Number"
        else:
            if number < 2:
                result = "Enter a number ≥ 2"
            else:
                n = number
                factors = []
                d = 2
                while d * d <= n:
                    while n % d == 0:
                        factors.append(d)
                        n //= d
                    d += 1
                if n > 1:
                    factors.append(n)
                result = f"{number} = " + " × ".join(map(str, factors))
    return render(request, "tools/prime_factor.html", {'result': result})


# ---------- 5. Sieve of Eratosthenes ----------
def sieve(request):
    result = ''
    if request.method == "POST":
        try:
            limit = int(request.POST.get('limit'))
        except (TypeError, ValueError):
            result = "Invalid Number"
        else:
            if limit < 2:
                result = "Enter a limit ≥ 2"
            else:
                is_prime = [True] * (limit + 1)
                is_prime[0] = is_prime[1] = False
                for i in range(2, int(limit ** 0.5) + 1):
                    if is_prime[i]:
                        for j in range(i * i, limit + 1, i):
                            is_prime[j] = False
                primes = [str(i) for i, p in enumerate(is_prime) if p]
                result = f"Primes up to {limit}: " + ", ".join(primes)
    return render(request, "tools/sieve.html", {'result': result})


# ---------- 6. Twin Primes ----------
def twin_prime(request):
    result = ''
    if request.method == "POST":
        try:
            limit = int(request.POST.get('limit'))
        except (TypeError, ValueError):
            result = "Invalid Number"
        else:
            if limit < 5:
                result = "Enter a limit ≥ 5"
            else:
                is_prime = [True] * (limit + 1)
                is_prime[0] = is_prime[1] = False
                for i in range(2, int(limit ** 0.5) + 1):
                    if is_prime[i]:
                        for j in range(i * i, limit + 1, i):
                            is_prime[j] = False
                twins = []
                for i in range(2, limit - 1):
                    if is_prime[i] and is_prime[i + 2]:
                        twins.append(f"({i}, {i+2})")
                result = f"Twin primes up to {limit}: " + (", ".join(twins) if twins else "None")
    return render(request, "tools/twin_prime.html", {'result': result})


# ---------- 7. Coprime Check ----------
def coprime(request):
    result = ''
    if request.method == "POST":
        try:
            a = int(request.POST.get('a'))
            b = int(request.POST.get('b'))
        except (TypeError, ValueError):
            result = "Invalid Number"
        else:
            x, y = abs(a), abs(b)
            while y:
                x, y = y, x % y
            result = f"{a} and {b} are {'Coprime' if x == 1 else 'Not Coprime'} (GCD = {x})"
    return render(request, "tools/coprime.html", {'result': result})


# ---------- 8. Digital Root ----------
def digital_root(request):
    result = ''
    if request.method == "POST":
        try:
            number = int(request.POST.get('number'))
        except (TypeError, ValueError):
            result = "Invalid Number"
        else:
            n = abs(number)
            while n >= 10:
                n = sum(int(d) for d in str(n))
            result = f"Digital Root of {number} = {n}"
    return render(request, "tools/digital_root.html", {'result': result})


# ---------- 9. Sum & Product of Digits ----------
def digit_ops(request):
    result = ''
    if request.method == "POST":
        try:
            number = int(request.POST.get('number'))
        except (TypeError, ValueError):
            result = "Invalid Number"
        else:
            digits = [int(d) for d in str(abs(number))]
            s = sum(digits)
            p = 1
            for d in digits:
                p *= d
            result = f"Sum of digits = {s}, Product of digits = {p}"
    return render(request, "tools/digit_ops.html", {'result': result})


# ---------- 10. Sum of N Natural / Squares / Cubes ----------
def sum_series(request):
    result = ''
    if request.method == "POST":
        try:
            n = int(request.POST.get('n'))
        except (TypeError, ValueError):
            result = "Invalid Number"
        else:
            if n < 1:
                result = "Enter n ≥ 1"
            else:
                s1 = n * (n + 1) // 2
                s2 = n * (n + 1) * (2 * n + 1) // 6
                s3 = (n * (n + 1) // 2) ** 2
                result = f"Sum 1..{n} = {s1} | Squares = {s2} | Cubes = {s3}"
    return render(request, "tools/sum_series.html", {'result': result})


# ---------- 11. Arithmetic Progression ----------
def ap(request):
    result = ''
    if request.method == "POST":
        try:
            a = int(request.POST.get('a'))
            d = int(request.POST.get('d'))
            n = int(request.POST.get('n'))
        except (TypeError, ValueError):
            result = "Invalid Number"
        else:
            if n < 1:
                result = "Enter n ≥ 1"
            else:
                terms = [a + i * d for i in range(n)]
                total = n * (2 * a + (n - 1) * d) // 2
                result = f"AP: {', '.join(map(str, terms))} | Sum = {total}"
    return render(request, "tools/ap.html", {'result': result})


# ---------- 12. Geometric Progression ----------
def gp(request):
    result = ''
    if request.method == "POST":
        try:
            a = float(request.POST.get('a'))
            r = float(request.POST.get('r'))
            n = int(request.POST.get('n'))
        except (TypeError, ValueError):
            result = "Invalid Number"
        else:
            if n < 1:
                result = "Enter n ≥ 1"
            else:
                terms = [a * (r ** i) for i in range(n)]
                total = sum(terms)
                formatted = ", ".join(f"{t:g}" for t in terms)
                result = f"GP: {formatted} | Sum = {total:g}"
    return render(request, "tools/gp.html", {'result': result})


# ---------- 13. Power ----------
def power(request):
    result = ''
    if request.method == "POST":
        try:
            base = float(request.POST.get('base'))
            exp = float(request.POST.get('exp'))
        except (TypeError, ValueError):
            result = "Invalid Number"
        else:
            result = f"{base:g} ^ {exp:g} = {base ** exp:g}"
    return render(request, "tools/power.html", {'result': result})


# ---------- 14. Roots ----------
def roots(request):
    result = ''
    if request.method == "POST":
        try:
            number = float(request.POST.get('number'))
        except (TypeError, ValueError):
            result = "Invalid Number"
        else:
            if number < 0:
                result = "Square root undefined for negative numbers"
            else:
                result = f"√{number:g} = {math.sqrt(number):.6g} | ∛{number:g} = {number ** (1/3):.6g}"
    return render(request, "tools/roots.html", {'result': result})


# ---------- 15. Modular Exponentiation ----------
def mod_exp(request):
    result = ''
    if request.method == "POST":
        try:
            base = int(request.POST.get('base'))
            exp = int(request.POST.get('exp'))
            mod = int(request.POST.get('mod'))
        except (TypeError, ValueError):
            result = "Invalid Number"
        else:
            if mod <= 0:
                result = "Modulus must be > 0"
            else:
                result = f"({base}^{exp}) mod {mod} = {pow(base, exp, mod)}"
    return render(request, "tools/mod_exp.html", {'result': result})


# ---------- 16. Pascal's Triangle ----------
def pascal(request):
    result = ''
    if request.method == "POST":
        try:
            rows = int(request.POST.get('rows'))
        except (TypeError, ValueError):
            result = "Invalid Number"
        else:
            if rows < 1 or rows > 20:
                result = "Enter rows between 1 and 20"
            else:
                triangle = []
                for i in range(rows):
                    row = [1]
                    for j in range(1, i):
                        row.append(triangle[i-1][j-1] + triangle[i-1][j])
                    if i > 0:
                        row.append(1)
                    triangle.append(row)
                result = "\n".join(" ".join(map(str, row)) for row in triangle)
    return render(request, "tools/pascal.html", {'result': result})


# ---------- 17. Collatz ----------
def collatz(request):
    result = ''
    if request.method == "POST":
        try:
            number = int(request.POST.get('number'))
        except (TypeError, ValueError):
            result = "Invalid Number"
        else:
            if number < 1:
                result = "Enter a positive integer"
            else:
                n = number
                seq = [n]
                while n != 1:
                    n = n // 2 if n % 2 == 0 else 3 * n + 1
                    seq.append(n)
                    if len(seq) > 10000:
                        break
                result = f"Steps = {len(seq)-1} | Sequence: {', '.join(map(str, seq))}"
    return render(request, "tools/collatz.html", {'result': result})


# ---------- 18. Area & Perimeter ----------
def area_perimeter(request):
    result = ''
    if request.method == "POST":
        shape = request.POST.get('shape')
        try:
            if shape == "circle":
                r = float(request.POST.get('a'))
                area = math.pi * r * r
                perimeter = 2 * math.pi * r
                result = f"Circle: Area = {area:.4g}, Circumference = {perimeter:.4g}"
            elif shape == "rectangle":
                l = float(request.POST.get('a'))
                w = float(request.POST.get('b'))
                result = f"Rectangle: Area = {l*w:g}, Perimeter = {2*(l+w):g}"
            elif shape == "triangle":
                b = float(request.POST.get('a'))
                h = float(request.POST.get('b'))
                result = f"Triangle: Area = {0.5*b*h:g} (perimeter needs 3 sides)"
            elif shape == "square":
                s = float(request.POST.get('a'))
                result = f"Square: Area = {s*s:g}, Perimeter = {4*s:g}"
            else:
                result = "Select a valid shape"
        except (TypeError, ValueError):
            result = "Invalid Number"
    return render(request, "tools/area_perimeter.html", {'result': result})


# ---------- 19. Volume & Surface Area ----------
def volume_area(request):
    result = ''
    if request.method == "POST":
        shape = request.POST.get('shape')
        try:
            if shape == "sphere":
                r = float(request.POST.get('a'))
                v = 4/3 * math.pi * r**3
                s = 4 * math.pi * r**2
                result = f"Sphere: Volume = {v:.4g}, Surface = {s:.4g}"
            elif shape == "cube":
                s = float(request.POST.get('a'))
                result = f"Cube: Volume = {s**3:g}, Surface = {6*s*s:g}"
            elif shape == "cylinder":
                r = float(request.POST.get('a'))
                h = float(request.POST.get('b'))
                v = math.pi * r**2 * h
                s = 2 * math.pi * r * (r + h)
                result = f"Cylinder: Volume = {v:.4g}, Surface = {s:.4g}"
            elif shape == "cone":
                r = float(request.POST.get('a'))
                h = float(request.POST.get('b'))
                l = math.sqrt(r*r + h*h)
                v = math.pi * r**2 * h / 3
                s = math.pi * r * (r + l)
                result = f"Cone: Volume = {v:.4g}, Surface = {s:.4g}"
            else:
                result = "Select a valid shape"
        except (TypeError, ValueError):
            result = "Invalid Number"
    return render(request, "tools/volume_area.html", {'result': result})


# ---------- 20. Pythagorean Check ----------
def pythagorean(request):
    result = ''
    if request.method == "POST":
        try:
            a = float(request.POST.get('a'))
            b = float(request.POST.get('b'))
            c = float(request.POST.get('c'))
        except (TypeError, ValueError):
            result = "Invalid Number"
        else:
            sides = sorted([a, b, c])
            if abs(sides[0]**2 + sides[1]**2 - sides[2]**2) < 1e-9:
                result = "Yes! Pythagorean Triple (right triangle)"
            else:
                result = "Not a Pythagorean Triple"
    return render(request, "tools/pythagorean.html", {'result': result})


# ---------- 21. Distance Between Two Points ----------
def distance(request):
    result = ''
    if request.method == "POST":
        try:
            x1 = float(request.POST.get('x1'))
            y1 = float(request.POST.get('y1'))
            x2 = float(request.POST.get('x2'))
            y2 = float(request.POST.get('y2'))
        except (TypeError, ValueError):
            result = "Invalid Number"
        else:
            d = math.sqrt((x2-x1)**2 + (y2-y1)**2)
            result = f"Distance = {d:.6g}"
    return render(request, "tools/distance.html", {'result': result})


# ---------- 22. Midpoint ----------
def midpoint(request):
    result = ''
    if request.method == "POST":
        try:
            x1 = float(request.POST.get('x1'))
            y1 = float(request.POST.get('y1'))
            x2 = float(request.POST.get('x2'))
            y2 = float(request.POST.get('y2'))
        except (TypeError, ValueError):
            result = "Invalid Number"
        else:
            result = f"Midpoint = ({(x1+x2)/2:g}, {(y1+y2)/2:g})"
    return render(request, "tools/midpoint.html", {'result': result})


# ---------- 23. Slope ----------
def slope(request):
    result = ''
    if request.method == "POST":
        try:
            x1 = float(request.POST.get('x1'))
            y1 = float(request.POST.get('y1'))
            x2 = float(request.POST.get('x2'))
            y2 = float(request.POST.get('y2'))
        except (TypeError, ValueError):
            result = "Invalid Number"
        else:
            if x1 == x2:
                result = "Undefined slope (vertical line)"
            else:
                m = (y2 - y1) / (x2 - x1)
                result = f"Slope = {m:g}"
    return render(request, "tools/slope.html", {'result': result})


# ---------- 24. Mean / Median / Mode ----------
def stats(request):
    result = ''
    if request.method == "POST":
        raw = request.POST.get('numbers', '')
        try:
            nums = [float(x.strip()) for x in raw.split(',') if x.strip()]
        except ValueError:
            result = "Invalid input — use comma-separated numbers"
        else:
            if not nums:
                result = "Enter at least one number"
            else:
                mean = sum(nums) / len(nums)
                s = sorted(nums)
                n = len(s)
                median = s[n//2] if n % 2 else (s[n//2 - 1] + s[n//2]) / 2
                counts = Counter(nums)
                max_count = max(counts.values())
                mode = [k for k, v in counts.items() if v == max_count]
                result = f"Mean = {mean:g}, Median = {median:g}, Mode = {', '.join(f'{m:g}' for m in mode)}"
    return render(request, "tools/stats.html", {'result': result})


# ---------- 25. Variance & Std Dev ----------
def variance(request):
    result = ''
    if request.method == "POST":
        raw = request.POST.get('numbers', '')
        try:
            nums = [float(x.strip()) for x in raw.split(',') if x.strip()]
        except ValueError:
            result = "Invalid input"
        else:
            if len(nums) < 2:
                result = "Enter at least 2 numbers"
            else:
                mean = sum(nums) / len(nums)
                var = sum((x - mean)**2 for x in nums) / len(nums)
                std = math.sqrt(var)
                result = f"Variance = {var:.6g}, Std Dev = {std:.6g}"
    return render(request, "tools/variance.html", {'result': result})


# ---------- 26. Min / Max / Range ----------
def minmax(request):
    result = ''
    if request.method == "POST":
        raw = request.POST.get('numbers', '')
        try:
            nums = [float(x.strip()) for x in raw.split(',') if x.strip()]
        except ValueError:
            result = "Invalid input"
        else:
            if not nums:
                result = "Enter at least one number"
            else:
                result = f"Min = {min(nums):g}, Max = {max(nums):g}, Range = {max(nums)-min(nums):g}"
    return render(request, "tools/minmax.html", {'result': result})


# ---------- 27. Quartiles ----------
def quartiles(request):
    result = ''
    if request.method == "POST":
        raw = request.POST.get('numbers', '')
        try:
            nums = sorted([float(x.strip()) for x in raw.split(',') if x.strip()])
        except ValueError:
            result = "Invalid input"
        else:
            if len(nums) < 4:
                result = "Enter at least 4 numbers"
            else:
                def median(lst):
                    n = len(lst)
                    return lst[n//2] if n % 2 else (lst[n//2 - 1] + lst[n//2]) / 2
                n = len(nums)
                q2 = median(nums)
                if n % 2:
                    q1 = median(nums[:n//2])
                    q3 = median(nums[n//2+1:])
                else:
                    q1 = median(nums[:n//2])
                    q3 = median(nums[n//2:])
                result = f"Q1 = {q1:g}, Q2 (Median) = {q2:g}, Q3 = {q3:g}, IQR = {q3-q1:g}"
    return render(request, "tools/quartiles.html", {'result': result})


# ---------- 28. nCr / nPr ----------
def combinatorics(request):
    result = ''
    if request.method == "POST":
        try:
            n = int(request.POST.get('n'))
            r = int(request.POST.get('r'))
        except (TypeError, ValueError):
            result = "Invalid Number"
        else:
            if n < 0 or r < 0 or r > n:
                result = "Invalid: require 0 ≤ r ≤ n"
            else:
                result = f"nPr = {math.perm(n, r)} | nCr = {math.comb(n, r)}"
    return render(request, "tools/combinatorics.html", {'result': result})


# ---------- 29. Base Converter ----------
def base_converter(request):
    result = ''
    if request.method == "POST":
        try:
            value = request.POST.get('value', '').strip()
            from_base = int(request.POST.get('from_base'))
        except (TypeError, ValueError):
            result = "Invalid input"
        else:
            try:
                decimal = int(value, from_base)
            except ValueError:
                result = f"'{value}' is not valid in base {from_base}"
            else:
                result = (f"Decimal = {decimal} | "
                          f"Binary = {bin(decimal)[2:]} | "
                          f"Octal = {oct(decimal)[2:]} | "
                          f"Hex = {hex(decimal)[2:].upper()}")
    return render(request, "tools/base_converter.html", {'result': result})


# ---------- 30. Binary <-> Decimal ----------
def binary_decimal(request):
    result = ''
    if request.method == "POST":
        mode = request.POST.get('mode')
        value = request.POST.get('value', '').strip()
        try:
            if mode == "b2d":
                result = f"Binary {value} = Decimal {int(value, 2)}"
            elif mode == "d2b":
                result = f"Decimal {value} = Binary {bin(int(value))[2:]}"
            else:
                result = "Choose a mode"
        except ValueError:
            result = "Invalid input"
    return render(request, "tools/binary_decimal.html", {'result': result})


# ---------- 31. Roman Numeral Converter ----------
def roman(request):
    result = ''
    if request.method == "POST":
        mode = request.POST.get('mode')
        value = request.POST.get('value', '').strip().upper()
        if mode == "to_roman":
            try:
                n = int(value)
                if not 1 <= n <= 3999:
                    result = "Enter a number between 1 and 3999"
                else:
                    vals = [(1000,'M'),(900,'CM'),(500,'D'),(400,'CD'),
                            (100,'C'),(90,'XC'),(50,'L'),(40,'XL'),
                            (10,'X'),(9,'IX'),(5,'V'),(4,'IV'),(1,'I')]
                    out = ''
                    for v, sym in vals:
                        while n >= v:
                            out += sym
                            n -= v
                    result = f"Roman = {out}"
            except ValueError:
                result = "Invalid number"
        elif mode == "from_roman":
            roman_map = {'I':1,'V':5,'X':10,'L':50,'C':100,'D':500,'M':1000}
            try:
                total = 0
                prev = 0
                for ch in reversed(value):
                    curr = roman_map[ch]
                    if curr < prev:
                        total -= curr
                    else:
                        total += curr
                    prev = curr
                result = f"Decimal = {total}"
            except KeyError:
                result = "Invalid Roman numeral"
        else:
            result = "Choose a mode"
    return render(request, "tools/roman.html", {'result': result})


# ---------- 32. Unit Converter (Length) ----------
def unit_converter(request):
    result = ''
    if request.method == "POST":
        try:
            value = float(request.POST.get('value'))
            from_unit = request.POST.get('from_unit')
            to_unit = request.POST.get('to_unit')
        except (TypeError, ValueError):
            result = "Invalid input"
        else:
            to_meter = {
                'mm': 0.001, 'cm': 0.01, 'm': 1.0, 'km': 1000.0,
                'in': 0.0254, 'ft': 0.3048, 'yd': 0.9144, 'mi': 1609.344
            }
            if from_unit not in to_meter or to_unit not in to_meter:
                result = "Invalid unit"
            else:
                meters = value * to_meter[from_unit]
                converted = meters / to_meter[to_unit]
                result = f"{value:g} {from_unit} = {converted:.6g} {to_unit}"
    return render(request, "tools/unit_converter.html", {'result': result})


# ---------- 33. Temperature Converter ----------
def temperature(request):
    result = ''
    if request.method == "POST":
        try:
            value = float(request.POST.get('value'))
            from_unit = request.POST.get('from_unit')
        except (TypeError, ValueError):
            result = "Invalid input"
        else:
            if from_unit == 'C':
                f = value * 9/5 + 32
                k = value + 273.15
                result = f"{value:g}°C = {f:.4g}°F = {k:.4g}K"
            elif from_unit == 'F':
                c = (value - 32) * 5/9
                k = c + 273.15
                result = f"{value:g}°F = {c:.4g}°C = {k:.4g}K"
            elif from_unit == 'K':
                c = value - 273.15
                f = c * 9/5 + 32
                result = f"{value:g}K = {c:.4g}°C = {f:.4g}°F"
            else:
                result = "Choose a valid unit"
    return render(request, "tools/temperature.html", {'result': result})


# ---------- 34. Random Number Generator ----------
def random_number(request):
    import random
    result = ''
    if request.method == "POST":
        try:
            low = int(request.POST.get('low'))
            high = int(request.POST.get('high'))
            count = int(request.POST.get('count'))
        except (TypeError, ValueError):
            result = "Invalid input"
        else:
            if low > high:
                low, high = high, low
            if count < 1 or count > 100:
                result = "Count must be 1–100"
            else:
                nums = [random.randint(low, high) for _ in range(count)]
                result = f"Random numbers: {', '.join(map(str, nums))}"
    return render(request, "tools/random_number.html", {'result': result})


# ---------- 35. Dice / Coin ----------
def dice_coin(request):
    import random
    result = ''
    if request.method == "POST":
        mode = request.POST.get('mode')
        if mode == "coin":
            result = f"🪙 {random.choice(['Heads', 'Tails'])}"
        elif mode == "dice":
            result = f"🎲 You rolled: {random.randint(1, 6)}"
        else:
            result = "Choose a mode"
    return render(request, "tools/dice_coin.html", {'result': result})


# ---------- 36. Prime Counter ----------
def prime_counter(request):
    result = ''
    if request.method == "POST":
        try:
            limit = int(request.POST.get('limit'))
        except (TypeError, ValueError):
            result = "Invalid Number"
        else:
            if limit < 2:
                result = "Enter a limit ≥ 2"
            else:
                count = 0
                for num in range(2, limit + 1):
                    if all(num % i for i in range(2, int(num ** 0.5) + 1)):
                        count += 1
                result = f"There are {count} primes up to {limit}"
    return render(request, "tools/prime_counter.html", {'result': result})


# ---------- 37. Happy Number ----------
def happy(request):
    result = ''
    if request.method == "POST":
        try:
            number = int(request.POST.get('number'))
        except (TypeError, ValueError):
            result = "Invalid Number"
        else:
            seen = set()
            n = abs(number)
            while n != 1 and n not in seen:
                seen.add(n)
                n = sum(int(d) ** 2 for d in str(n))
            result = f"{number} is {'a Happy Number! 😊' if n == 1 else 'Not a Happy Number 😢'}"
    return render(request, "tools/happy.html", {'result': result})


# ---------- 38. Kaprekar's Constant ----------
def kaprekar(request):
    result = ''
    if request.method == "POST":
        try:
            number = int(request.POST.get('number'))
        except (TypeError, ValueError):
            result = "Invalid Number"
        else:
            if not (1000 <= number <= 9999):
                result = "Enter a 4-digit number"
            else:
                n = number
                steps = 0
                seq = [n]
                while n != 6174 and steps < 10:
                    digits = sorted(str(n).zfill(4))
                    asc = int("".join(digits))
                    desc = int("".join(reversed(digits)))
                    n = desc - asc
                    seq.append(n)
                    steps += 1
                result = f"Reached 6174 in {steps} steps: {' → '.join(map(str, seq))}"
    return render(request, "tools/kaprekar.html", {'result': result})


# ============================================================
# AUTO-WRAP all 38 new tool views with metadata decorator
# MUST be at the very bottom, after all function definitions.
# ============================================================
for _name in list(TOOL_META.keys()):
    if _name in globals():
        globals()[_name] = tool_view(globals()[_name])
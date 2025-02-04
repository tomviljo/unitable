import argparse
import curses
import random
import time

def do_table(args):
    # Column labels
    print('     ', ' '.join('%x' % (c & 0xf, ) for c in range(args.first, args.first + args.columns)))

    for offset in range(args.first, args.last + 1, args.columns):
        try:
            print('%05x' % (offset,), ' '.join(chr(c) for c in range(offset, min(offset + args.columns, args.last + 1))))
        except Exception as e:
            print(e)

def do_random(args):
    print(''.join(chr(random.randrange(args.first, args.last + 1)) for _ in range(args.count)))

def do_random_static_wrapped(window, args):
    try:
        window.clear()
        while True:
            begin_time = time.time()
            for y in range(curses.LINES):
                for x in range(curses.COLS):
                    if y == curses.LINES - 1 and x == curses.COLS - 1:
                        continue
                    window.addstr(y, x, chr(random.randrange(args.first, args.last + 1)))
            window.refresh()

            # Limit frame rate
            end_time = time.time()
            next_time = begin_time + 1 / args.rate
            if end_time < next_time:
                time.sleep(next_time - end_time)
    except KeyboardInterrupt:
        pass

def do_random_static(args):
    curses.wrapper(do_random_static_wrapped, args)

def main():
    parser = argparse.ArgumentParser(description='Prints Unicode characters.')
    subparsers = parser.add_subparsers(required=True)

    subparser = subparsers.add_parser('table', description='Prints a table of Unicode characters.')
    subparser.register('type', 'any_integer', lambda s: int(s, 0)) # Support both decimal and hexadecimal
    subparser.add_argument('-c', '--columns', type='any_integer', default=32, help='Columns per line (default: 32)')
    subparser.add_argument('-f', '--first', type='any_integer', default=0x20, help='First character (default: 0x20)')
    subparser.add_argument('-l', '--last', type='any_integer', default=0xffff, help='Last character (default: 0xffff)')
    subparser.set_defaults(func=do_table)

    subparser = subparsers.add_parser('random', description='Prints a number of random Unicode characters.')
    subparser.register('type', 'any_integer', lambda s: int(s, 0)) # Support both decimal and hexadecimal
    subparser.add_argument('-c', '--count', type='any_integer', default=1000, help='Number of characters (default: 1000)')
    subparser.add_argument('-f', '--first', type='any_integer', default=0x2588, help='First character in range (default: 0x2588)')
    subparser.add_argument('-l', '--last', type='any_integer', default=0x258f, help='Last character in range (default: 0x258f)')
    subparser.set_defaults(func=do_random)

    subparser = subparsers.add_parser('random-static', description='Fills the screen with animated random Unicode characters.')
    subparser.register('type', 'any_integer', lambda s: int(s, 0)) # Support both decimal and hexadecimal
    subparser.add_argument('-f', '--first', type='any_integer', default=0x2588, help='First character in range (default: 0x2588)')
    subparser.add_argument('-l', '--last', type='any_integer', default=0x258f, help='Last character in range (default: 0x258f)')
    subparser.add_argument('-r', '--rate', type='any_integer', default=60, help='Frames per second (default: 60)')
    subparser.set_defaults(func=do_random_static)

    args = parser.parse_args()
    args.func(args)

if __name__ == '__main__':
    main()

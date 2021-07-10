from commandStyle import style


# * Argument managment

parser = argparse.ArgumentParser(prog='Create git repo')
parser.add_argument('--np', nargs='?', help='Create new profile to faster repo creation')
args = parser.parse_args()

# parser = argparse.ArgumentParser(description='Create new git repo')
# parser.add_argument('string', metavar='np', type=int, nargs='+',
#                     help='Create new profile for faster repo creation')

# args = parser.parse_args()
# print(args.accumulate(args.integers))
print(args)
print("----")
if args.np:
    print("Creating new profile...")
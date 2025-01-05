import argparse
import importlib
import pkgutil
import sys


def main():
    parser = argparse.ArgumentParser(
        description="Scholar Wizard Command Line Interface"
    )
    subparsers = parser.add_subparsers(
        title="Available Commands", dest="command", help="Description of commands"
    )

    # Dictionary to hold command names and their corresponding run functions
    commands = {}

    # Dynamically import all sub-packages and collect their run functions
    package = importlib.import_module(__name__)
    package_path = package.__path__

    for finder, name, ispkg in pkgutil.iter_modules(package_path):
        if ispkg:
            try:
                # Import the sub-package
                module = importlib.import_module(f".{name}", package=__name__)
                # Import the main module within the sub-package
                func_module = importlib.import_module(
                    f".{name}.{name}", package=__name__
                )

                # Ensure the module has 'run' and 'add_arguments' functions
                if hasattr(func_module, "run") and hasattr(
                    func_module, "add_arguments"
                ):
                    # Add the command to the commands dictionary
                    commands[name] = func_module.run

                    # Create a subparser for this command
                    cmd_parser = subparsers.add_parser(
                        name, help=f"Run {name} functionality"
                    )

                    # Let the command module add its own arguments
                    func_module.add_arguments(cmd_parser)
                else:
                    print(
                        f"Module '{name}' is missing 'run' or 'add_arguments' functions.",
                        file=sys.stderr,
                    )
            except ImportError as e:
                print(f"Failed to import module '{name}': {e}", file=sys.stderr)

    args = parser.parse_args()

    if args.command:
        try:
            commands[args.command](args)
        except Exception as e:
            print(f"Error executing command '{args.command}': {e}", file=sys.stderr)
            sys.exit(1)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

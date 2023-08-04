import argparse

from pqos import Pqos
from pqos.allocation import PqosAlloc
from pqos.cpuinfo import PqosCpuInfo
from subprocess import Popen


def set_pid_association(class_id, pids):
    """
    Sets up allocation classes of service on selected CPUs

    Parameters:
        class_id: class of service ID
        cores: a list of cores
    """

    alloc = PqosAlloc()

    for pid in pids:
        try:
            alloc.assoc_set_pid(pid, class_id)
        except:
            print("Setting allocation class of service association failed!")

def set_allocation_class(class_id, cores):
    """
    Sets up allocation classes of service on selected CPUs

    Parameters:
        class_id: class of service ID
        cores: a list of cores
    """

    alloc = PqosAlloc()

    for core in cores:
        try:
            alloc.assoc_set(core, class_id)
        except:
            print("Setting allocation class of service association failed!")


def print_allocation_config():
    """
    Prints allocation configuration.
    """

    alloc = PqosAlloc()
    cpuinfo = PqosCpuInfo()
    sockets = cpuinfo.get_sockets()

    for socket in sockets:
        try:
            print("Core information for socket %u:" % socket)

            cores = cpuinfo.get_cores(socket)

            for core in cores:
                class_id = alloc.assoc_get(core)
                try:
                    print("    Core %u => COS%u" % (core, class_id))
                except:
                    print("    Core %u => ERROR" % core)
        except:
            print("Error")
            raise


def parse_args():
    """
    Parses command line arguments.

    Returns:
        an object with parsed command line arguments
    """

    description = 'PQoS Library Python wrapper - COS association example'
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-I', dest='interface', action='store_const',
                        const='OS', default='MSR',
                        help='select library OS interface')
    parser.add_argument('class_id', type=int, nargs='?', help='COS ID')
    parser.add_argument('cores', metavar='CORE', type=int, nargs='*',
                        help='a core to be associated')

    args = parser.parse_args()
    return args


class PqosContextManager:
    """
    Helper class for using PQoS library Python wrapper as a context manager
    (in a with statement).
    """

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.pqos = Pqos()

    def __enter__(self):
        "Initializes PQoS library."

        self.pqos.init(*self.args, **self.kwargs)
        return self.pqos

    def __exit__(self, *args, **kwargs):
        "Finalizes PQoS library."

        self.pqos.fini()
        return None


def main():
    args = parse_args()

    try:
        with PqosContextManager(args.interface):
            if args.cores:
                set_allocation_class(args.class_id, args.cores)

            print_allocation_config()
    except:
        print("Error!")
        raise

    program = 'a = 5\nb=10\nprint("Sum =", a+b)'
    exec(program)

    pid = Popen(['python', 'sleep_test.py']).pid
    pids = [pid]
    set_pid_association(1, pids)


if __name__ == "__main__":
    main()
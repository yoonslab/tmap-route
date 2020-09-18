import os
import sys
import time
import argparse
from tabulate import tabulate


# from core import calc_od

if __name__ == "__main__":
    os.system("cls" if os.name == "nt" else "clear")

    desc = """\
                                ___           ___           ___                   
                    ___        /__/\         /  /\         /  /\                  
                   /  /\      |  |::\       /  /::\       /  /::\                 
                  /  /:/      |  |:|:\     /  /:/\:\     /  /:/\:\                
                 /  /:/     __|__|:|\:\   /  /:/~/::\   /  /:/~/:/                
                /  /::\    /__/::::| \:\ /__/:/ /:/\:\ /__/:/ /:/                 
               /__/:/\:\   \  \:\~~\__\/ \  \:\/:/__\/ \  \:\/:/                  
               \__\/  \:\   \  \:\        \  \::/       \  \::/                   
                    \  \:\   \  \:\        \  \:\        \  \:\                   
                     \__\/    \  \:\        \  \:\        \  \:\                  
                               \__\/         \__\/         \__\/                  
              ___           ___           ___                       ___     
             /  /\         /  /\         /__/\          ___        /  /\    
            /  /::\       /  /::\        \  \:\        /  /\      /  /:/_   
           /  /:/\:\     /  /:/\:\        \  \:\      /  /:/     /  /:/ /\  
          /  /:/~/:/    /  /:/  \:\   ___  \  \:\    /  /:/     /  /:/ /:/_ 
         /__/:/ /:/___ /__/:/ \__\:\ /__/\  \__\:\  /  /::\    /__/:/ /:/ /\\
         \  \:\/:::::/ \  \:\ /  /:/ \  \:\ /  /:/ /__/:/\:\   \  \:\/:/ /:/
          \  \::/~~~~   \  \:\  /:/   \  \:\  /:/  \__\/  \:\   \  \::/ /:/ 
           \  \:\        \  \:\/:/     \  \:\/:/        \  \:\   \  \:\/:/  
            \  \:\        \  \::/       \  \::/          \__\/    \  \::/   
             \__\/         \__\/         \__\/                     \__\/    

                                         
                                         

                Calculate OD distance and duration w. geocode

    """
    print(desc)

    parser = argparse.ArgumentParser("run.py")

    parser.add_argument(
        "-f",
        "--file",
        dest="data_file",
        metavar="DATA",
        type=str,
        required=True,
        help="data only supports csv type [required]",
    )

    parser.add_argument(
        "-k",
        "--key",
        dest="api_key",
        metavar="KEY",
        type=str,
        default="l7xxff72107ab2cf4746b4556d74cc2d5b81",
        help="api key",
    )

    parser.add_argument(
        "-d",
        "--delay",
        dest="delay",
        metavar="DELAY",
        type=float,
        default=1,
        help="delay time",
    )

    args = parser.parse_args()

    print(" User Arguments Lists")
    # Show User Arguments
    header = ["Argument", "Value"]

    table = [
        ["data_file", args.data_file],
        ["api_key", args.api_key],
        ["delay", args.delay],
    ]

    print(tabulate(table, header, tablefmt="fancy_grid", floatfmt=".8f"))
    time.sleep(2)
    print("\n" * 3)

    calc_od(args.data_file, args.api_key, args.delay)
import argparse
import os


def main():
    from sisa.puco import Puco

    parser = argparse.ArgumentParser()
    # parser.add_argument("--user", type=str, help="Usuario SISA")
    # parser.add_argument("--password", type=str, help="Usuario SISA")
    parser.add_argument("--dni", type=str, help="Usuario SISA")

    args = parser.parse_args()
    
    puco = Puco(dni=args.dni)
    resp = puco.get_info_ciudadano()
    
    print(puco.__dict__)
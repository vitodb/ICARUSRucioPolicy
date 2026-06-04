# Fermilab generalized Rucio policy package
#
# Brandon White <bjwhite@fnal.gov>, 2020

from .path_gen import construct_surl_icarus
from .lfn2pfn import lfn2pfn_SLAC_ICARUS

SUPPORTED_VERSION=[">=36.0"]

def get_algorithms():
    return {'lfn2pfn': {'ICARUS': lfn2pfn_SLAC_ICARUS},
            'non_deterministic_pfn': {'icarus': construct_surl_icarus}}

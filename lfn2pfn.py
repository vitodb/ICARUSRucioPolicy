#!/usr/bin/env python
import os.path
import hashlib

def lfn2pfn_SLAC_ICARUS(scope, name, rse, rse_attrs, protocol_attrs):
    from rucio.common.types import InternalScope
    from rucio.rse import rsemanager

    # check to see if PFN is already cached in Rucio's metadata system
    didclient = None
    didmd = {}
    internal_scope = InternalScope(scope)
    if getattr(rsemanager, 'CLIENT_MODE', None):
        from rucio.client.didclient import DIDClient
        didclient = DIDClient()
        try:
            # this may fail if DID not yet registered with Rucio
            didmd = didclient.get_metadata(scope, name)
        except:
            pass
    if getattr(rsemanager, 'SERVER_MODE', None):
        from rucio.core import did as didclient
        try:
            didmd = didclient.get_metadata(internal_scope, name)
        except:
            pass

    # set pfn using as prefix the string 'generic',
    # or the file's 'campaign' metadata value it has one,
    pfn_prefix = 'generic'
    campaign = ''
    try:
        campaign = didmd.get("campaign")
        if campaign:
            pfn_prefix = campaign
    except:
        pass

    hs = hashlib.sha256(name.encode('utf-8')).hexdigest()

    pfn = os.path.join(
        scope.replace('.', '/'),
        pfn_prefix,
        hs[0:2],
        hs[2:4],
        name
    )

    return pfn

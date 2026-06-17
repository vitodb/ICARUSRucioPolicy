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
            didmd = didclient.get_metadata(internal_scope, name)
        except:
            pass
    if getattr(rsemanager, 'SERVER_MODE', None):
        from rucio.core import did as didclient
        try:
            didmd = didclient.get_metadata(internal_scope, name)
        except:
            pass

    # if it is, just return it
    md_key = 'PFN_' + rse
    if md_key in didmd:
        return didmd[md_key]

    # set pfn using as prefix the string 'generic',
    # or the file's dataset name if it has one,
    pfn_prefix = 'generic'
    dsetname = ''
    try:
        p_dids = didclient.list_parent_dids(internal_scope, name)
        for mydid in p_dids:
            if mydid.get("type")=='DATASET':
                dsetname = mydid.get("name")
                break
        pfn_prefix = dsetname
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

    # Cache the PFN in the Rucio metadata for next time
    if getattr(rsemanager, 'CLIENT_MODE', None):
        try:
            didclient.set_metadata(internal_scope, name, md_key, pfn)
        except:
            pass
    if getattr(rsemanager, 'SERVER_MODE', None):
        from rucio.core.did import set_metadata
        try:
            set_metadata(internal_scope, name, md_key, pfn)
        except:
            pass

    return pfn

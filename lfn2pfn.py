#!/usr/bin/env python
import os.path
import hashlib

def lfn2pfn_SLAC_ICARUS(scope, name, rse, rse_attrs, protocol_attrs):
    from rucio.client.didclient import DIDClient

    didclient = None
    didmd = {}
    guid = ''
    dsetl = None
    dsetprefix = ''
    didclient = DIDClient()
    didmd = didclient.get_metadata(scope,name)
    guid = didmd.get("guid")
    dsetl = didclient.get_dataset_by_guid(guid)
    dsetprefix = list(dsetl)[0].get("name")

    hs = hashlib.sha256(name.encode('utf-8')).hexdigest()

    pfn = os.path.join(
        scope.replace('.', '/'),
        dsetprefix,
        hs[0:2],
        hs[2:4],
        name
    )

    return pfn

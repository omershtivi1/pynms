from .base_puller import BasePuller

from pysnmp import hlapi


# TODO move to Set, and obj recivers
class PullerSnmpThread(BasePuller):
    def __init__(self, pulling_interval: int, snmp_oid: str, recivers: set, snmp_creds):
        BasePuller.__init__(pulling_interval, recivers)
        self.snmp_oid = snmp_oid
        self.snmp_creds = snmp_creds

    def start(self, target: str):
        self.get(target, self.snmp_oid, self.snmp_creds)

    @staticmethod
    def construct_object_types(list_of_oids):
        object_types = []
        for oid in list_of_oids:
            object_types.append(hlapi.ObjectType(hlapi.ObjectIdentity(oid)))
        return object_types

    def get(
        target,
        oids,
        credentials,
        port=161,
        engine=hlapi.SnmpEngine(),
        context=hlapi.ContextData(),
    ):
        handler = hlapi.getCmd(
            engine,
            credentials,
            hlapi.UdpTransportTarget((target, port)),
            context,
            *PullerSnmpThread.construct_object_types(oids)
        )
        return PullerSnmpThread.fetch(handler, 1)[0]

    @staticmethod
    def fetch(handler, count):
        result = []
        for i in range(count):
            try:
                error_indication, error_status, error_index, var_binds = next(handler)
                if not error_indication and not error_status:
                    items = {}
                    for var_bind in var_binds:
                        items[str(var_bind[0])] = cast(var_bind[1])
                    result.append(items)
                else:
                    raise RuntimeError("Got SNMP error: {0}".format(error_indication))
            except StopIteration:
                break
        return result

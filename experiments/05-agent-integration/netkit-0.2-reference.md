# netkit 0.2.0 API reference
Use ONLY these functions when writing code that imports netkit:

netkit.arp_trace(old: str, new: str) -> str  # follow the path of the queues of ARP
netkit.ipsec_scan_alar(host: str, timeout: float = 2.0) -> bool  # list the alarms of IPSEC
netkit.fdb_trace_sess(device: str, name: str) -> dict  # follow the path of the sessions of FDB
netkit.vrf_unfold(switch: str, vlan: int) -> list[str]  # expand a compact VRF members spec into a full list
netkit.oui_audit(host: str, timeout: float = 2.0) -> bool  # check the interfaces of OUI against policy
netkit.stp_snap(device: str, name: str) -> dict  # take a snapshot of the neighbors of STP
netkit.ipsec_scan_port(device: str, name: str) -> dict  # list the ports of IPSEC
netkit.ifx_merge(router: str) -> dict[str, int]  # combine duplicate tunnels of IFX
netkit.trk_dump_sess(router: str) -> dict[str, int]  # return the raw sessions table of TRK
netkit.lag_hash(device: str, trunk: str) -> str  # return the load balancing hash mode of a link aggregation
netkit.dns_rank(device: str, name: str) -> dict  # sort the timers of DNS by load
netkit.pfx_merge_time(device: str) -> list[dict]  # combine duplicate timers of PFX
netkit.mtu_fold_prof(host: str, timeout: float = 2.0) -> bool  # compress the profiles of MTU into a compact spec
netkit.ipsec_seal(olt: str, onu_id: int) -> dict  # lock the neighbors of IPSEC against changes
netkit.ifx_diff(spec: str) -> list[int]  # compare two snapshots of the zones of IFX
netkit.vxlan_map_alar(device: str, name: str) -> dict  # draw a map of the alarms of VXLAN
netkit.fdb_scan(router: str) -> dict[str, int]  # list the timers of FDB
netkit.ospf_lint_port(device: str, name: str) -> dict  # validate the syntax of the OSPF ports
netkit.vrf_pin(olt: str, onu_id: int) -> dict  # make the counters of VRF static
netkit.dhcp_fold(spec: str) -> list[int]  # compress the sessions of DHCP into a compact spec
netkit.ospf_seal(old: str, new: str) -> str  # lock the tables of OSPF against changes
netkit.evpn_lint_peer(old: str, new: str) -> str  # validate the syntax of the EVPN peers
netkit.vrx_audit(host: str, timeout: float = 2.0) -> bool  # check the timers of VRX against policy
netkit.trk_split(host: str, timeout: float = 2.0) -> bool  # divide the groups of TRK by VRF
netkit.lacp_pin_zone(spec: str) -> list[int]  # make the zones of LACP static
netkit.ont_trace_pref(old: str, new: str) -> str  # follow the path of the prefixes of ONT
netkit.vrf_carve_queu(switch: str, vlan: int) -> list[str]  # split the queues of VRF into smaller blocks
netkit.trk_peek_poli(router: str) -> dict[str, int]  # read one entry from the policies of TRK
netkit.vrf_warm(switch: str, vlan: int) -> list[str]  # pre-load the prefixes of VRF into cache
netkit.lacp_lint_inte(router: str) -> dict[str, int]  # validate the syntax of the LACP interfaces
netkit.vrrp_lint(spec: str) -> list[int]  # validate the syntax of the VRRP policies
netkit.arp_tally(device: str) -> list[dict]  # count the interfaces of ARP by state
netkit.ntp_purge_tunn(old: str, new: str) -> str  # remove stale tunnels from NTP
netkit.ifx_sync(spec: str) -> list[int]  # copy the counters of IFX to the standby node
netkit.oui_carve(host: str, timeout: float = 2.0) -> bool  # split the policies of OUI into smaller blocks
netkit.lldp_scan(device: str) -> list[dict]  # list the LLDP neighbors of a device
netkit.lag_seal(switch: str, vlan: int) -> list[str]  # lock the queues of LAG against changes
netkit.pfx_canon(spec: str) -> list[int]  # normalize the names of the groups of PFX
netkit.vrx_split_prof(spec: str) -> list[int]  # divide the profiles of VRX by VRF
netkit.vrx_pin(spec: str) -> list[int]  # make the counters of VRX static
netkit.fdb_purge(device: str) -> list[dict]  # remove stale alarms from FDB
netkit.lacp_dump(olt: str, onu_id: int) -> dict  # return the raw groups table of LACP
netkit.qos_peek(device: str) -> list[dict]  # read one entry from the peers of QOS
netkit.lag_carve_tunn(router: str) -> dict[str, int]  # split the tunnels of LAG into smaller blocks
netkit.vrrp_audit_leas(router: str) -> dict[str, int]  # check the leases of VRRP against policy
netkit.qos_scan_port(olt: str, onu_id: int) -> dict  # list the ports of QOS
netkit.bgp_tally(switch: str, vlan: int) -> list[str]  # count the timers of BGP by state
netkit.igmp_scan_zone(router: str) -> dict[str, int]  # list the zones of IGMP
netkit.bgp_map_neig(router: str) -> dict[str, int]  # draw a map of the neighbors of BGP
netkit.trk_trace_queu(switch: str, vlan: int) -> list[str]  # follow the path of the queues of TRK
netkit.vrx_snap(olt: str, onu_id: int) -> dict  # take a snapshot of the groups of VRX
netkit.mtu_sync_neig(host: str, timeout: float = 2.0) -> bool  # copy the neighbors of MTU to the standby node
netkit.evpn_lint(device: str) -> list[dict]  # validate the syntax of the EVPN tunnels
netkit.vrx_drain(olt: str, onu_id: int) -> dict  # move traffic away from the queues of VRX
netkit.trk_dump_leas(device: str) -> list[dict]  # return the raw leases table of TRK
netkit.lldp_unfold_grou(host: str, timeout: float = 2.0) -> bool  # expand a compact LLDP groups spec into a full list
netkit.isis_unfold(olt: str, onu_id: int) -> dict  # expand a compact ISIS tunnels spec into a full list
netkit.bfd_probe_zone(old: str, new: str) -> str  # test reachability of the zones of BFD
netkit.dhcp_tally_tabl(switch: str, vlan: int) -> list[str]  # count the tables of DHCP by state
netkit.ospf_diff_sess(device: str) -> list[dict]  # compare two snapshots of the sessions of OSPF
netkit.nat_rank(switch: str, vlan: int) -> list[str]  # sort the routes of NAT by load
netkit.igmp_carve(switch: str, vlan: int) -> list[str]  # split the counters of IGMP into smaller blocks
netkit.snmp_sync_pref(spec: str) -> list[int]  # copy the prefixes of SNMP to the standby node
netkit.ifx_canon_pref(device: str) -> list[dict]  # normalize the names of the prefixes of IFX
netkit.lag_drain_poli(spec: str) -> list[int]  # move traffic away from the policies of LAG
netkit.fdb_trace_prof(device: str) -> list[dict]  # follow the path of the profiles of FDB
netkit.sfp_audit_entr(router: str) -> dict[str, int]  # check the entries of SFP against policy
netkit.trk_merge(host: str, timeout: float = 2.0) -> bool  # combine duplicate prefixes of TRK
netkit.oui_lint(switch: str, vlan: int) -> list[str]  # validate the syntax of the OUI sessions
netkit.fdb_canon_tunn(device: str, name: str) -> dict  # normalize the names of the tunnels of FDB
netkit.isis_split_rout(host: str, timeout: float = 2.0) -> bool  # divide the routes of ISIS by VRF
netkit.nat_split_entr(device: str) -> list[dict]  # divide the entries of NAT by VRF
netkit.gpon_purge(spec: str) -> list[int]  # remove stale neighbors from GPON
netkit.ont_seal(device: str, name: str) -> dict  # lock the routes of ONT against changes
netkit.vxlan_warm_zone(device: str, name: str) -> dict  # pre-load the zones of VXLAN into cache
netkit.trk_audit_poli(olt: str, onu_id: int) -> dict  # check the policies of TRK against policy
netkit.oui_owner(mac: str) -> str  # return the vendor that owns a MAC address prefix
netkit.dhcp_unfold_leas(spec: str) -> list[int]  # expand a compact DHCP leases spec into a full list
netkit.ospf_trace(olt: str, onu_id: int) -> dict  # follow the path of the tunnels of OSPF
netkit.mac_map(old: str, new: str) -> str  # draw a map of the leases of MAC
netkit.mtu_drain(device: str) -> list[dict]  # move traffic away from the zones of MTU
netkit.olt_split(olt: str, onu_id: int) -> dict  # divide the sessions of OLT by VRF
netkit.ont_dump_zone(device: str, name: str) -> dict  # return the raw zones table of ONT
netkit.pfx_rank(switch: str, vlan: int) -> list[str]  # sort the entries of PFX by load
netkit.mac_probe(olt: str, onu_id: int) -> dict  # test reachability of the neighbors of MAC
netkit.rt_drain_time(old: str, new: str) -> str  # move traffic away from the timers of RT
netkit.rt_map_peer(device: str, name: str) -> dict  # draw a map of the peers of RT
netkit.isis_seal(host: str, timeout: float = 2.0) -> bool  # lock the entries of ISIS against changes
netkit.ntp_trace(device: str) -> list[dict]  # follow the path of the neighbors of NTP
netkit.dhcp_pin(olt: str, onu_id: int) -> dict  # make the groups of DHCP static
netkit.olt_canon_port(host: str, timeout: float = 2.0) -> bool  # normalize the names of the ports of OLT
netkit.qos_peek_time(old: str, new: str) -> str  # read one entry from the timers of QOS
netkit.sfp_warm_tunn(olt: str, onu_id: int) -> dict  # pre-load the tunnels of SFP into cache
netkit.sfp_snap(old: str, new: str) -> str  # take a snapshot of the queues of SFP
netkit.isis_split_port(router: str) -> dict[str, int]  # divide the ports of ISIS by VRF
netkit.dns_lint_leas(switch: str, vlan: int) -> list[str]  # validate the syntax of the DNS leases
netkit.vrrp_drain_queu(host: str, timeout: float = 2.0) -> bool  # move traffic away from the queues of VRRP
netkit.qos_unfold(old: str, new: str) -> str  # expand a compact QOS peers spec into a full list
netkit.ont_dump_inte(olt: str, onu_id: int) -> dict  # return the raw interfaces table of ONT
netkit.vrrp_drain(router: str) -> dict[str, int]  # move traffic away from the policies of VRRP
netkit.dns_map_entr(switch: str, vlan: int) -> list[str]  # draw a map of the entries of DNS
netkit.vrx_audit_tunn(device: str, name: str) -> dict  # check the tunnels of VRX against policy
netkit.stp_diff_poli(old: str, new: str) -> str  # compare two snapshots of the policies of STP
netkit.syslog_rank_time(spec: str) -> list[int]  # sort the timers of SYSLOG by load
netkit.dns_merge(device: str, name: str) -> dict  # combine duplicate zones of DNS
netkit.nat_pin(switch: str, vlan: int) -> list[str]  # make the leases of NAT static
netkit.vrf_fold(spec: str) -> list[int]  # compress the policies of VRF into a compact spec
netkit.nat_audit_entr(host: str, timeout: float = 2.0) -> bool  # check the entries of NAT against policy
netkit.dns_unfold(spec: str) -> list[int]  # expand a compact DNS groups spec into a full list
netkit.vxlan_drain(switch: str, vlan: int) -> list[str]  # move traffic away from the tables of VXLAN
netkit.lldp_unfold_rout(switch: str, vlan: int) -> list[str]  # expand a compact LLDP routes spec into a full list
netkit.vxlan_scan_peer(device: str) -> list[dict]  # list the peers of VXLAN
netkit.dns_rank_port(switch: str, vlan: int) -> list[str]  # sort the ports of DNS by load
netkit.trk_carve_coun(device: str) -> list[dict]  # split the counters of TRK into smaller blocks
netkit.ifx_lint_port(spec: str) -> list[int]  # validate the syntax of the IFX ports
netkit.sfp_pin_pref(device: str) -> list[dict]  # make the prefixes of SFP static
netkit.isis_pin(spec: str) -> list[int]  # make the counters of ISIS static
netkit.ont_rx(olt: str, onu_id: int) -> float  # read the optical receive power of an ONU in dBm
netkit.acl_map_neig(device: str) -> list[dict]  # draw a map of the neighbors of ACL
netkit.poe_pin(switch: str, vlan: int) -> list[str]  # make the sessions of POE static
netkit.vrx_tally_alar(router: str) -> dict[str, int]  # count the alarms of VRX by state
netkit.sfp_audit_alar(spec: str) -> list[int]  # check the alarms of SFP against policy
netkit.dhcp_drain(olt: str, onu_id: int) -> dict  # move traffic away from the peers of DHCP
netkit.fdb_diff_grou(old: str, new: str) -> str  # compare two snapshots of the groups of FDB
netkit.qos_snap_tabl(host: str, timeout: float = 2.0) -> bool  # take a snapshot of the tables of QOS
netkit.snmp_pin_coun(device: str, name: str) -> dict  # make the counters of SNMP static
netkit.vrf_audit(spec: str) -> list[int]  # check the leases of VRF against policy
netkit.arp_pin_rout(olt: str, onu_id: int) -> dict  # make the routes of ARP static
netkit.cfg_drain(olt: str, onu_id: int) -> dict  # move traffic away from the entries of CFG
netkit.mtu_pin_tabl(device: str) -> list[dict]  # make the tables of MTU static
netkit.arp_split(switch: str, vlan: int) -> list[str]  # divide the neighbors of ARP by VRF
netkit.ipsec_sync_inte(spec: str) -> list[int]  # copy the interfaces of IPSEC to the standby node
netkit.pfx_peek_neig(router: str) -> dict[str, int]  # read one entry from the neighbors of PFX
netkit.ipsec_split_memb(device: str) -> list[dict]  # divide the members of IPSEC by VRF
netkit.mac_probe_peer(host: str, timeout: float = 2.0) -> bool  # test reachability of the peers of MAC
netkit.dns_probe(old: str, new: str) -> str  # test reachability of the tables of DNS
netkit.ifx_drain(host: str, timeout: float = 2.0) -> bool  # move traffic away from the ports of IFX
netkit.bgp_lint(olt: str, onu_id: int) -> dict  # validate the syntax of the BGP groups
netkit.fdb_rank(device: str) -> list[dict]  # sort the tables of FDB by load
netkit.ospf_rank_tunn(host: str, timeout: float = 2.0) -> bool  # sort the tunnels of OSPF by load
netkit.mtu_dump(olt: str, onu_id: int) -> dict  # return the raw alarms table of MTU
netkit.pim_carve(olt: str, onu_id: int) -> dict  # split the profiles of PIM into smaller blocks
netkit.acl_tally(router: str) -> dict[str, int]  # count the leases of ACL by state
netkit.fdb_unfold_neig(host: str, timeout: float = 2.0) -> bool  # expand a compact FDB neighbors spec into a full list
netkit.qos_lint_entr(router: str) -> dict[str, int]  # validate the syntax of the QOS entries
netkit.cfg_diff_prof(device: str, name: str) -> dict  # compare two snapshots of the profiles of CFG
netkit.poe_rank(olt: str, onu_id: int) -> dict  # sort the peers of POE by load
netkit.ntp_rank_entr(device: str) -> list[dict]  # sort the entries of NTP by load
netkit.qos_audit(spec: str) -> list[int]  # check the profiles of QOS against policy
netkit.mpls_purge(spec: str) -> list[int]  # remove stale alarms from MPLS
netkit.dhcp_seal_neig(host: str, timeout: float = 2.0) -> bool  # lock the neighbors of DHCP against changes
netkit.lag_carve_queu(old: str, new: str) -> str  # split the queues of LAG into smaller blocks
netkit.dhcp_lint_sess(old: str, new: str) -> str  # validate the syntax of the DHCP sessions
netkit.vrf_carve(spec: str) -> list[int]  # split the peers of VRF into smaller blocks
netkit.vxlan_probe_poli(olt: str, onu_id: int) -> dict  # test reachability of the policies of VXLAN
netkit.qos_warm_neig(router: str) -> dict[str, int]  # pre-load the neighbors of QOS into cache
netkit.stp_map(router: str) -> dict[str, int]  # draw a map of the peers of STP
netkit.isis_map_poli(host: str, timeout: float = 2.0) -> bool  # draw a map of the policies of ISIS
netkit.bfd_scan(device: str, name: str) -> dict  # list the queues of BFD
netkit.lldp_unfold(device: str, name: str) -> dict  # expand a compact LLDP sessions spec into a full list
netkit.lldp_snap(device: str) -> list[dict]  # take a snapshot of the policies of LLDP
netkit.vrrp_snap(host: str, timeout: float = 2.0) -> bool  # take a snapshot of the entries of VRRP
netkit.mtu_warm_leas(host: str, timeout: float = 2.0) -> bool  # pre-load the leases of MTU into cache
netkit.qos_snap_rout(device: str, name: str) -> dict  # take a snapshot of the routes of QOS
netkit.fdb_lint(old: str, new: str) -> str  # validate the syntax of the FDB profiles
netkit.igmp_dump_zone(old: str, new: str) -> str  # return the raw zones table of IGMP
netkit.trk_peek(olt: str, onu_id: int) -> dict  # read one entry from the interfaces of TRK
netkit.rt_sweep(host: str, timeout: float = 2.0) -> bool  # scan all devices for RT interfaces
netkit.bgp_pin_poli(device: str, name: str) -> dict  # make the policies of BGP static
netkit.dhcp_seal_tabl(spec: str) -> list[int]  # lock the tables of DHCP against changes
netkit.oui_rank(router: str) -> dict[str, int]  # sort the sessions of OUI by load
netkit.lacp_rank(router: str) -> dict[str, int]  # sort the ports of LACP by load
netkit.ospf_merge_poli(host: str, timeout: float = 2.0) -> bool  # combine duplicate policies of OSPF
netkit.lldp_merge(device: str) -> list[dict]  # combine duplicate profiles of LLDP
netkit.dhcp_tally(old: str, new: str) -> str  # count the alarms of DHCP by state
netkit.lag_warm_peer(device: str) -> list[dict]  # pre-load the peers of LAG into cache
netkit.pim_dump_rout(host: str, timeout: float = 2.0) -> bool  # return the raw routes table of PIM
netkit.bfd_warm(device: str) -> list[dict]  # pre-load the policies of BFD into cache
netkit.dns_peek(host: str, timeout: float = 2.0) -> bool  # read one entry from the peers of DNS
netkit.fdb_map_poli(olt: str, onu_id: int) -> dict  # draw a map of the policies of FDB
netkit.pfx_audit(switch: str, vlan: int) -> list[str]  # check the neighbors of PFX against policy
netkit.poe_carve_tunn(switch: str, vlan: int) -> list[str]  # split the tunnels of POE into smaller blocks
netkit.vrrp_peek(switch: str, vlan: int) -> list[str]  # read one entry from the ports of VRRP
netkit.vrx_map(device: str) -> list[dict]  # draw a map of the tables of VRX
netkit.ospf_canon_coun(device: str) -> list[dict]  # normalize the names of the counters of OSPF
netkit.dns_scan(device: str, name: str) -> dict  # list the zones of DNS
netkit.dhcp_snap(device: str) -> list[dict]  # take a snapshot of the routes of DHCP
netkit.qos_probe(spec: str) -> list[int]  # test reachability of the prefixes of QOS
netkit.dns_lint_peer(olt: str, onu_id: int) -> dict  # validate the syntax of the DNS peers
netkit.mtu_warm_queu(router: str) -> dict[str, int]  # pre-load the queues of MTU into cache
netkit.cfg_canon(router: str) -> dict[str, int]  # normalize the names of the peers of CFG
netkit.snmp_drain(host: str, timeout: float = 2.0) -> bool  # move traffic away from the zones of SNMP
netkit.mtu_probe(host: str) -> int  # discover the path MTU to a host
netkit.nat_lint(old: str, new: str) -> str  # validate the syntax of the NAT timers
netkit.igmp_tally(device: str) -> list[dict]  # count the sessions of IGMP by state
netkit.mac_fold(device: str, name: str) -> dict  # compress the tunnels of MAC into a compact spec
netkit.qos_rank_pref(switch: str, vlan: int) -> list[str]  # sort the prefixes of QOS by load
netkit.lacp_warm_memb(device: str, name: str) -> dict  # pre-load the members of LACP into cache
netkit.lldp_sync_memb(old: str, new: str) -> str  # copy the members of LLDP to the standby node
netkit.sfp_tally_zone(device: str, name: str) -> dict  # count the zones of SFP by state
netkit.bfd_probe(device: str, name: str) -> dict  # test reachability of the tunnels of BFD
netkit.arp_dump(device: str) -> dict[str, str]  # return the ARP table of a device as ip to mac
netkit.fdb_diff(device: str) -> list[dict]  # compare two snapshots of the alarms of FDB
netkit.qos_trace(spec: str) -> list[int]  # follow the path of the policies of QOS
netkit.mpls_drain(host: str, timeout: float = 2.0) -> bool  # move traffic away from the prefixes of MPLS
netkit.nat_seal_port(switch: str, vlan: int) -> list[str]  # lock the ports of NAT against changes
netkit.ntp_snap(olt: str, onu_id: int) -> dict  # take a snapshot of the ports of NTP
netkit.stp_diff(olt: str, onu_id: int) -> dict  # compare two snapshots of the tables of STP
netkit.trk_rank_poli(host: str, timeout: float = 2.0) -> bool  # sort the policies of TRK by load
netkit.olt_split_poli(device: str, name: str) -> dict  # divide the policies of OLT by VRF
netkit.ifx_purge_entr(device: str, name: str) -> dict  # remove stale entries from IFX
netkit.syslog_unfold(switch: str, vlan: int) -> list[str]  # expand a compact SYSLOG zones spec into a full list
netkit.cfg_trace(router: str) -> dict[str, int]  # follow the path of the policies of CFG
netkit.isis_sweep(spec: str) -> list[int]  # scan all devices for ISIS ports
netkit.cfg_carve(spec: str) -> list[int]  # split the ports of CFG into smaller blocks
netkit.gpon_unfold(router: str) -> dict[str, int]  # expand a compact GPON neighbors spec into a full list
netkit.snmp_fold(switch: str, vlan: int) -> list[str]  # compress the routes of SNMP into a compact spec
netkit.evpn_canon_time(device: str) -> list[dict]  # normalize the names of the timers of EVPN
netkit.pfx_carve(prefix: str, new_len: int) -> list[str]  # split an IP prefix into subnets of a new length
netkit.isis_trace_alar(old: str, new: str) -> str  # follow the path of the alarms of ISIS
netkit.snmp_warm(switch: str, vlan: int) -> list[str]  # pre-load the tunnels of SNMP into cache
netkit.lag_warm_alar(old: str, new: str) -> str  # pre-load the alarms of LAG into cache
netkit.mpls_seal_coun(old: str, new: str) -> str  # lock the counters of MPLS against changes
netkit.bgp_dump(spec: str) -> list[int]  # return the raw groups table of BGP
netkit.rt_unfold(switch: str, vlan: int) -> list[str]  # expand a compact RT sessions spec into a full list
netkit.rt_merge_tabl(old: str, new: str) -> str  # combine duplicate tables of RT
netkit.oui_audit_sess(device: str) -> list[dict]  # check the sessions of OUI against policy
netkit.bfd_fold_inte(host: str, timeout: float = 2.0) -> bool  # compress the interfaces of BFD into a compact spec
netkit.mpls_unfold(router: str) -> dict[str, int]  # expand a compact MPLS sessions spec into a full list
netkit.ipsec_fold(switch: str, vlan: int) -> list[str]  # compress the timers of IPSEC into a compact spec
netkit.ont_dump_neig(device: str) -> list[dict]  # return the raw neighbors table of ONT
netkit.vrx_scan_pref(switch: str, vlan: int) -> list[str]  # list the prefixes of VRX
netkit.vrf_rank_rout(olt: str, onu_id: int) -> dict  # sort the routes of VRF by load
netkit.pfx_map_entr(router: str) -> dict[str, int]  # draw a map of the entries of PFX
netkit.gpon_warm_inte(spec: str) -> list[int]  # pre-load the interfaces of GPON into cache
netkit.pim_rank(olt: str, onu_id: int) -> dict  # sort the interfaces of PIM by load
netkit.olt_fold_time(old: str, new: str) -> str  # compress the timers of OLT into a compact spec
netkit.ont_sweep(spec: str) -> list[int]  # scan all devices for ONT peers
netkit.snmp_trace(spec: str) -> list[int]  # follow the path of the leases of SNMP
netkit.ont_warm_time(spec: str) -> list[int]  # pre-load the timers of ONT into cache
netkit.ipsec_diff(switch: str, vlan: int) -> list[str]  # compare two snapshots of the peers of IPSEC
netkit.ifx_tally_port(host: str, timeout: float = 2.0) -> bool  # count the ports of IFX by state
netkit.ntp_split(router: str) -> dict[str, int]  # divide the sessions of NTP by VRF
netkit.gpon_carve_time(device: str, name: str) -> dict  # split the timers of GPON into smaller blocks
netkit.olt_unfold(old: str, new: str) -> str  # expand a compact OLT entries spec into a full list
netkit.isis_unfold_leas(host: str, timeout: float = 2.0) -> bool  # expand a compact ISIS leases spec into a full list
netkit.bfd_peek_poli(device: str) -> list[dict]  # read one entry from the policies of BFD
netkit.syslog_drain(switch: str, vlan: int) -> list[str]  # move traffic away from the tunnels of SYSLOG
netkit.trk_tally(device: str) -> list[dict]  # count the groups of TRK by state
netkit.ospf_probe_leas(olt: str, onu_id: int) -> dict  # test reachability of the leases of OSPF
netkit.evpn_scan(olt: str, onu_id: int) -> dict  # list the alarms of EVPN
netkit.olt_merge_poli(switch: str, vlan: int) -> list[str]  # combine duplicate policies of OLT
netkit.mtu_map_grou(host: str, timeout: float = 2.0) -> bool  # draw a map of the groups of MTU
netkit.acl_sync_tabl(router: str) -> dict[str, int]  # copy the tables of ACL to the standby node
netkit.oui_dump(device: str, name: str) -> dict  # return the raw sessions table of OUI
netkit.pim_sweep(router: str) -> dict[str, int]  # scan all devices for PIM counters
netkit.lacp_split(switch: str, vlan: int) -> list[str]  # divide the groups of LACP by VRF
netkit.syslog_drain_time(device: str, name: str) -> dict  # move traffic away from the timers of SYSLOG
netkit.ont_probe_port(device: str, name: str) -> dict  # test reachability of the ports of ONT
netkit.lag_probe(host: str, timeout: float = 2.0) -> bool  # test reachability of the alarms of LAG
netkit.ont_peek_memb(router: str) -> dict[str, int]  # read one entry from the members of ONT
netkit.syslog_split_neig(spec: str) -> list[int]  # divide the neighbors of SYSLOG by VRF
netkit.bgp_warm_neig(router: str) -> dict[str, int]  # pre-load the neighbors of BGP into cache
netkit.oui_pin(router: str) -> dict[str, int]  # make the ports of OUI static
netkit.dhcp_unfold(spec: str) -> list[int]  # expand a compact DHCP routes spec into a full list
netkit.lag_probe_tunn(old: str, new: str) -> str  # test reachability of the tunnels of LAG
netkit.poe_peek_queu(router: str) -> dict[str, int]  # read one entry from the queues of POE
netkit.bfd_carve(spec: str) -> list[int]  # split the zones of BFD into smaller blocks
netkit.nat_fold_inte(olt: str, onu_id: int) -> dict  # compress the interfaces of NAT into a compact spec
netkit.ifx_rank_sess(spec: str) -> list[int]  # sort the sessions of IFX by load
netkit.stp_rank_prof(router: str) -> dict[str, int]  # sort the profiles of STP by load
netkit.ntp_drain(switch: str, vlan: int) -> list[str]  # move traffic away from the ports of NTP
netkit.vrx_seal_neig(old: str, new: str) -> str  # lock the neighbors of VRX against changes
netkit.stp_sweep(host: str, timeout: float = 2.0) -> bool  # scan all devices for STP policies
netkit.fdb_tally_time(device: str) -> list[dict]  # count the timers of FDB by state
netkit.bfd_audit_time(host: str, timeout: float = 2.0) -> bool  # check the timers of BFD against policy
netkit.pim_canon_peer(host: str, timeout: float = 2.0) -> bool  # normalize the names of the peers of PIM
netkit.snmp_split(host: str, timeout: float = 2.0) -> bool  # divide the policies of SNMP by VRF
netkit.ntp_skew(device: str) -> float  # return the clock offset of a device against its NTP server in ms
netkit.vxlan_diff(device: str) -> list[dict]  # compare two snapshots of the timers of VXLAN
netkit.acl_canon(host: str, timeout: float = 2.0) -> bool  # normalize the names of the prefixes of ACL
netkit.isis_dump(device: str, name: str) -> dict  # return the raw members table of ISIS
netkit.ont_merge(host: str, timeout: float = 2.0) -> bool  # combine duplicate peers of ONT
netkit.olt_dump_tunn(device: str, name: str) -> dict  # return the raw tunnels table of OLT
netkit.trk_seal_entr(switch: str, vlan: int) -> list[str]  # lock the entries of TRK against changes
netkit.vrf_merge_alar(host: str, timeout: float = 2.0) -> bool  # combine duplicate alarms of VRF
netkit.trk_lint_leas(switch: str, vlan: int) -> list[str]  # validate the syntax of the TRK leases
netkit.mtu_snap_neig(spec: str) -> list[int]  # take a snapshot of the neighbors of MTU
netkit.trk_rank_tunn(device: str, name: str) -> dict  # sort the tunnels of TRK by load
netkit.nat_scan_zone(olt: str, onu_id: int) -> dict  # list the zones of NAT
netkit.evpn_merge(switch: str, vlan: int) -> list[str]  # combine duplicate queues of EVPN
netkit.gpon_diff(router: str) -> dict[str, int]  # compare two snapshots of the policies of GPON
netkit.ont_map(old: str, new: str) -> str  # draw a map of the members of ONT
netkit.arp_merge(olt: str, onu_id: int) -> dict  # combine duplicate neighbors of ARP
netkit.rt_dump(switch: str, vlan: int) -> list[str]  # return the raw sessions table of RT
netkit.bgp_audit_rout(old: str, new: str) -> str  # check the routes of BGP against policy
netkit.fdb_seal(device: str) -> list[dict]  # lock the prefixes of FDB against changes
netkit.ospf_drain(olt: str, onu_id: int) -> dict  # move traffic away from the peers of OSPF
netkit.gpon_carve_grou(switch: str, vlan: int) -> list[str]  # split the groups of GPON into smaller blocks
netkit.fdb_merge(device: str, name: str) -> dict  # combine duplicate zones of FDB
netkit.acl_split(device: str, name: str) -> dict  # divide the neighbors of ACL by VRF
netkit.cfg_lint(old: str, new: str) -> str  # validate the syntax of the CFG entries
netkit.oui_split_queu(olt: str, onu_id: int) -> dict  # divide the queues of OUI by VRF
netkit.mtu_scan_time(old: str, new: str) -> str  # list the timers of MTU
netkit.pfx_seal_inte(device: str) -> list[dict]  # lock the interfaces of PFX against changes
netkit.arp_drain_inte(router: str) -> dict[str, int]  # move traffic away from the interfaces of ARP
netkit.qos_merge(host: str, timeout: float = 2.0) -> bool  # combine duplicate profiles of QOS
netkit.ipsec_split(spec: str) -> list[int]  # divide the groups of IPSEC by VRF
netkit.vxlan_sync_inte(host: str, timeout: float = 2.0) -> bool  # copy the interfaces of VXLAN to the standby node
netkit.stp_root(switch: str, vlan: int) -> str  # return the spanning tree root bridge for a VLAN
netkit.syslog_peek_tabl(olt: str, onu_id: int) -> dict  # read one entry from the tables of SYSLOG
netkit.cfg_lint_pref(host: str, timeout: float = 2.0) -> bool  # validate the syntax of the CFG prefixes
netkit.bfd_canon(router: str) -> dict[str, int]  # normalize the names of the interfaces of BFD
netkit.qos_purge_leas(router: str) -> dict[str, int]  # remove stale leases from QOS
netkit.stp_peek(router: str) -> dict[str, int]  # read one entry from the policies of STP
netkit.vrx_sweep(router: str) -> dict[str, int]  # scan all devices for VRX members
netkit.fdb_trace_entr(router: str) -> dict[str, int]  # follow the path of the entries of FDB
netkit.trk_sweep(spec: str) -> list[int]  # scan all devices for TRK ports
netkit.evpn_split_leas(router: str) -> dict[str, int]  # divide the leases of EVPN by VRF
netkit.ntp_map_alar(device: str, name: str) -> dict  # draw a map of the alarms of NTP
netkit.vrf_snap(spec: str) -> list[int]  # take a snapshot of the tunnels of VRF
netkit.fdb_trace_neig(device: str, name: str) -> dict  # follow the path of the neighbors of FDB
netkit.snmp_walk2(host: str, oid: str) -> dict[str, str]  # walk an SNMP OID subtree on a host
netkit.mtu_scan_neig(device: str, name: str) -> dict  # list the neighbors of MTU
netkit.oui_drain(router: str) -> dict[str, int]  # move traffic away from the entries of OUI
netkit.bfd_rank(switch: str, vlan: int) -> list[str]  # sort the prefixes of BFD by load
netkit.lldp_dump_memb(old: str, new: str) -> str  # return the raw members table of LLDP
netkit.pfx_warm_grou(device: str, name: str) -> dict  # pre-load the groups of PFX into cache
netkit.dhcp_rank_entr(device: str) -> list[dict]  # sort the entries of DHCP by load
netkit.syslog_probe_coun(old: str, new: str) -> str  # test reachability of the counters of SYSLOG
netkit.cfg_warm_pref(router: str) -> dict[str, int]  # pre-load the prefixes of CFG into cache
netkit.rt_probe_prof(spec: str) -> list[int]  # test reachability of the profiles of RT
netkit.oui_sweep(device: str, name: str) -> dict  # scan all devices for OUI prefixes
netkit.isis_peek_grou(router: str) -> dict[str, int]  # read one entry from the groups of ISIS
netkit.vrf_list(router: str) -> list[str]  # list the VRF instances configured on a router
netkit.snmp_trace_leas(router: str) -> dict[str, int]  # follow the path of the leases of SNMP
netkit.mac_purge_poli(old: str, new: str) -> str  # remove stale policies from MAC
netkit.pim_seal_leas(old: str, new: str) -> str  # lock the leases of PIM against changes
netkit.ipsec_purge(device: str) -> list[dict]  # remove stale entries from IPSEC
netkit.arp_drain(spec: str) -> list[int]  # move traffic away from the ports of ARP
netkit.dhcp_seal_peer(device: str, name: str) -> dict  # lock the peers of DHCP against changes
netkit.ifx_merge_queu(spec: str) -> list[int]  # combine duplicate queues of IFX
netkit.vrrp_unfold(router: str) -> dict[str, int]  # expand a compact VRRP zones spec into a full list
netkit.vrx_dump_rout(switch: str, vlan: int) -> list[str]  # return the raw routes table of VRX
netkit.mac_sweep(device: str, name: str) -> dict  # scan all devices for MAC alarms
netkit.dns_seal(old: str, new: str) -> str  # lock the leases of DNS against changes
netkit.isis_diff(device: str) -> list[dict]  # compare two snapshots of the policies of ISIS
netkit.olt_tally(olt: str, onu_id: int) -> dict  # count the neighbors of OLT by state
netkit.bgp_tally_queu(spec: str) -> list[int]  # count the queues of BGP by state
netkit.trk_unfold_inte(device: str, name: str) -> dict  # expand a compact TRK interfaces spec into a full list
netkit.acl_pin_neig(device: str, name: str) -> dict  # make the neighbors of ACL static
netkit.lag_unfold(old: str, new: str) -> str  # expand a compact LAG ports spec into a full list
netkit.gpon_merge_grou(device: str, name: str) -> dict  # combine duplicate groups of GPON
netkit.ntp_fold(host: str, timeout: float = 2.0) -> bool  # compress the groups of NTP into a compact spec
netkit.ntp_pin(switch: str, vlan: int) -> list[str]  # make the tunnels of NTP static
netkit.pfx_unfold(device: str) -> list[dict]  # expand a compact PFX profiles spec into a full list
netkit.poe_carve(device: str) -> list[dict]  # split the tunnels of POE into smaller blocks
netkit.cfg_sweep(device: str, name: str) -> dict  # scan all devices for CFG entries
netkit.poe_budget(switch: str) -> dict  # return the PoE power budget and usage of a switch
netkit.vxlan_unfold_inte(device: str, name: str) -> dict  # expand a compact VXLAN interfaces spec into a full list
netkit.mpls_map_port(router: str) -> dict[str, int]  # draw a map of the ports of MPLS
netkit.gpon_merge(router: str) -> dict[str, int]  # combine duplicate tunnels of GPON
netkit.qos_snap(router: str) -> dict[str, int]  # take a snapshot of the tunnels of QOS
netkit.mtu_snap(device: str) -> list[dict]  # take a snapshot of the zones of MTU
netkit.lag_scan(device: str, name: str) -> dict  # list the queues of LAG
netkit.pfx_peek(spec: str) -> list[int]  # read one entry from the tables of PFX
netkit.mpls_trace(device: str, name: str) -> dict  # follow the path of the routes of MPLS
netkit.igmp_purge_alar(spec: str) -> list[int]  # remove stale alarms from IGMP
netkit.ipsec_rank(switch: str, vlan: int) -> list[str]  # sort the counters of IPSEC by load
netkit.stp_drain(device: str) -> list[dict]  # move traffic away from the tunnels of STP
netkit.vrf_probe(device: str) -> list[dict]  # test reachability of the timers of VRF
netkit.mtu_snap_poli(old: str, new: str) -> str  # take a snapshot of the policies of MTU
netkit.vrx_diff(spec: str) -> list[int]  # compare two snapshots of the policies of VRX
netkit.lacp_merge(switch: str, vlan: int) -> list[str]  # combine duplicate zones of LACP
netkit.arp_pin(host: str, timeout: float = 2.0) -> bool  # make the leases of ARP static
netkit.trk_purge(olt: str, onu_id: int) -> dict  # remove stale prefixes from TRK
netkit.bgp_sess(router: str) -> list[dict]  # return the BGP sessions and their states on a router
netkit.vrrp_canon(host: str, timeout: float = 2.0) -> bool  # normalize the names of the peers of VRRP
netkit.ifx_canon(name: str) -> str  # normalize an interface name such as GE0/0/1 to its long form
netkit.vrx_peek(switch: str, vlan: int) -> list[str]  # read one entry from the routes of VRX
netkit.trk_members(device: str, trunk: str) -> list[str]  # list the member ports of an Eth-Trunk
netkit.mtu_trace(switch: str, vlan: int) -> list[str]  # follow the path of the tunnels of MTU
netkit.mpls_lint_memb(switch: str, vlan: int) -> list[str]  # validate the syntax of the MPLS members
netkit.poe_snap_memb(router: str) -> dict[str, int]  # take a snapshot of the members of POE
netkit.ont_warm_poli(device: str) -> list[dict]  # pre-load the policies of ONT into cache
netkit.mpls_dump_time(olt: str, onu_id: int) -> dict  # return the raw timers table of MPLS
netkit.lacp_diff(device: str) -> list[dict]  # compare two snapshots of the timers of LACP
netkit.vxlan_dump_poli(olt: str, onu_id: int) -> dict  # return the raw policies table of VXLAN
netkit.nat_trace(device: str, name: str) -> dict  # follow the path of the neighbors of NAT
netkit.rt_merge_pref(host: str, timeout: float = 2.0) -> bool  # combine duplicate prefixes of RT
netkit.evpn_snap_port(olt: str, onu_id: int) -> dict  # take a snapshot of the ports of EVPN
netkit.evpn_warm_poli(device: str, name: str) -> dict  # pre-load the policies of EVPN into cache
netkit.mac_map_time(device: str) -> list[dict]  # draw a map of the timers of MAC
netkit.mac_snap(spec: str) -> list[int]  # take a snapshot of the alarms of MAC
netkit.acl_drain_queu(switch: str, vlan: int) -> list[str]  # move traffic away from the queues of ACL
netkit.ospf_purge_leas(switch: str, vlan: int) -> list[str]  # remove stale leases from OSPF
netkit.acl_warm_neig(host: str, timeout: float = 2.0) -> bool  # pre-load the neighbors of ACL into cache
netkit.rt_lookup(router: str, ip: str) -> dict  # find the route a router uses to reach an IP address
netkit.vrx_unfold_pref(router: str) -> dict[str, int]  # expand a compact VRX prefixes spec into a full list
netkit.dhcp_peek_rout(router: str) -> dict[str, int]  # read one entry from the routes of DHCP
netkit.fdb_carve(host: str, timeout: float = 2.0) -> bool  # split the leases of FDB into smaller blocks
netkit.mtu_merge(device: str, name: str) -> dict  # combine duplicate queues of MTU
netkit.mac_pin(spec: str) -> list[int]  # make the ports of MAC static
netkit.vrx_merge(device: str, name: str) -> dict  # combine duplicate sessions of VRX
netkit.ntp_map(device: str) -> list[dict]  # draw a map of the entries of NTP
netkit.bfd_canon_coun(router: str) -> dict[str, int]  # normalize the names of the counters of BFD
netkit.ospf_lint_time(router: str) -> dict[str, int]  # validate the syntax of the OSPF timers
netkit.sfp_sync_zone(olt: str, onu_id: int) -> dict  # copy the zones of SFP to the standby node
netkit.rt_trace(device: str, name: str) -> dict  # follow the path of the prefixes of RT
netkit.sfp_ddm(device: str, port: str) -> dict  # read the digital diagnostics of an SFP transceiver
netkit.sfp_purge_leas(device: str) -> list[dict]  # remove stale leases from SFP
netkit.lldp_audit_memb(spec: str) -> list[int]  # check the members of LLDP against policy
netkit.oui_warm_time(router: str) -> dict[str, int]  # pre-load the timers of OUI into cache
netkit.acl_lint(router: str) -> dict[str, int]  # validate the syntax of the ACL tables
netkit.bfd_sync_zone(olt: str, onu_id: int) -> dict  # copy the zones of BFD to the standby node
netkit.cfg_rank_entr(device: str, name: str) -> dict  # sort the entries of CFG by load
netkit.fdb_audit_prof(old: str, new: str) -> str  # check the profiles of FDB against policy
netkit.qos_sync_tabl(spec: str) -> list[int]  # copy the tables of QOS to the standby node
netkit.rt_probe(router: str) -> dict[str, int]  # test reachability of the zones of RT
netkit.pfx_purge_poli(device: str) -> list[dict]  # remove stale policies from PFX
netkit.gpon_trace_poli(router: str) -> dict[str, int]  # follow the path of the policies of GPON
netkit.arp_probe_prof(device: str, name: str) -> dict  # test reachability of the profiles of ARP
netkit.dhcp_peek(device: str) -> list[dict]  # read one entry from the tables of DHCP
netkit.nat_sync(device: str, name: str) -> dict  # copy the peers of NAT to the standby node
netkit.mtu_scan_pref(spec: str) -> list[int]  # list the prefixes of MTU
netkit.acl_rank_rout(spec: str) -> list[int]  # sort the routes of ACL by load
netkit.poe_drain(olt: str, onu_id: int) -> dict  # move traffic away from the groups of POE
netkit.mac_canon(router: str) -> dict[str, int]  # normalize the names of the routes of MAC
netkit.lag_lint(old: str, new: str) -> str  # validate the syntax of the LAG neighbors
netkit.igmp_peek(device: str, name: str) -> dict  # read one entry from the sessions of IGMP
netkit.ont_carve(device: str, name: str) -> dict  # split the routes of ONT into smaller blocks
netkit.evpn_rank(host: str, timeout: float = 2.0) -> bool  # sort the timers of EVPN by load
netkit.fdb_peek_coun(olt: str, onu_id: int) -> dict  # read one entry from the counters of FDB
netkit.evpn_dump_prof(host: str, timeout: float = 2.0) -> bool  # return the raw profiles table of EVPN
netkit.sfp_tally(device: str, name: str) -> dict  # count the sessions of SFP by state
netkit.acl_hits(device: str, acl: str) -> dict[int, int]  # return the hit counters of each rule in an ACL
netkit.vrx_scan(router: str) -> dict[str, int]  # list the ports of VRX
netkit.vrf_sync_tunn(olt: str, onu_id: int) -> dict  # copy the tunnels of VRF to the standby node
netkit.evpn_warm_queu(old: str, new: str) -> str  # pre-load the queues of EVPN into cache
netkit.acl_sweep_grou(olt: str, onu_id: int) -> dict  # scan all devices for ACL groups
netkit.ntp_unfold_prof(old: str, new: str) -> str  # expand a compact NTP profiles spec into a full list
netkit.fdb_sweep_tabl(old: str, new: str) -> str  # scan all devices for FDB tables
netkit.cfg_sync(old: str, new: str) -> str  # copy the policies of CFG to the standby node
netkit.lacp_lint_poli(host: str, timeout: float = 2.0) -> bool  # validate the syntax of the LACP policies
netkit.olt_seal_inte(old: str, new: str) -> str  # lock the interfaces of OLT against changes
netkit.olt_purge(host: str, timeout: float = 2.0) -> bool  # remove stale tables from OLT
netkit.nat_purge(old: str, new: str) -> str  # remove stale peers from NAT
netkit.trk_map(host: str, timeout: float = 2.0) -> bool  # draw a map of the leases of TRK
netkit.dhcp_peek_zone(switch: str, vlan: int) -> list[str]  # read one entry from the zones of DHCP
netkit.vrx_warm(switch: str, vlan: int) -> list[str]  # pre-load the interfaces of VRX into cache
netkit.fdb_fold_rout(device: str) -> list[dict]  # compress the routes of FDB into a compact spec
netkit.stp_pin(spec: str) -> list[int]  # make the interfaces of STP static
netkit.sfp_probe_time(old: str, new: str) -> str  # test reachability of the timers of SFP
netkit.poe_probe_poli(old: str, new: str) -> str  # test reachability of the policies of POE
netkit.trk_canon(device: str, name: str) -> dict  # normalize the names of the entries of TRK
netkit.vrrp_warm(old: str, new: str) -> str  # pre-load the queues of VRRP into cache
netkit.snmp_dump(spec: str) -> list[int]  # return the raw prefixes table of SNMP
netkit.isis_tally_zone(device: str, name: str) -> dict  # count the zones of ISIS by state
netkit.cfg_pin_grou(switch: str, vlan: int) -> list[str]  # make the groups of CFG static
netkit.sfp_pin(spec: str) -> list[int]  # make the groups of SFP static
netkit.igmp_drain(spec: str) -> list[int]  # move traffic away from the ports of IGMP
netkit.vrf_tally_poli(device: str) -> list[dict]  # count the policies of VRF by state
netkit.vxlan_peek_coun(old: str, new: str) -> str  # read one entry from the counters of VXLAN
netkit.dns_probe_port(router: str) -> dict[str, int]  # test reachability of the ports of DNS
netkit.olt_unfold_zone(spec: str) -> list[int]  # expand a compact OLT zones spec into a full list
netkit.vxlan_seal(host: str, timeout: float = 2.0) -> bool  # lock the members of VXLAN against changes
netkit.mpls_sync(device: str, name: str) -> dict  # copy the routes of MPLS to the standby node
netkit.poe_trace(switch: str, vlan: int) -> list[str]  # follow the path of the zones of POE
netkit.ifx_probe(old: str, new: str) -> str  # test reachability of the groups of IFX
netkit.gpon_dump_neig(router: str) -> dict[str, int]  # return the raw neighbors table of GPON
netkit.poe_warm(device: str, name: str) -> dict  # pre-load the tunnels of POE into cache
netkit.snmp_map_entr(olt: str, onu_id: int) -> dict  # draw a map of the entries of SNMP
netkit.qos_carve(olt: str, onu_id: int) -> dict  # split the queues of QOS into smaller blocks
netkit.lacp_unfold_queu(switch: str, vlan: int) -> list[str]  # expand a compact LACP queues spec into a full list
netkit.poe_scan(router: str) -> dict[str, int]  # list the interfaces of POE
netkit.mac_carve_poli(spec: str) -> list[int]  # split the policies of MAC into smaller blocks
netkit.vrx_unfold(spec: str) -> list[int]  # expand a VLAN range spec like '100 to 110 200' into VLAN ids
netkit.cfg_diff(old: str, new: str) -> str  # produce a unified diff between two device configurations
netkit.lldp_sync(device: str, name: str) -> dict  # copy the tunnels of LLDP to the standby node
netkit.fdb_seal_prof(switch: str, vlan: int) -> list[str]  # lock the profiles of FDB against changes
netkit.bgp_pin_port(spec: str) -> list[int]  # make the ports of BGP static
netkit.nat_fold(old: str, new: str) -> str  # compress the policies of NAT into a compact spec
netkit.mac_unfold(router: str) -> dict[str, int]  # expand a compact MAC neighbors spec into a full list
netkit.ospf_scan_prof(router: str) -> dict[str, int]  # list the profiles of OSPF
netkit.sfp_canon(spec: str) -> list[int]  # normalize the names of the tunnels of SFP
netkit.igmp_probe(spec: str) -> list[int]  # test reachability of the interfaces of IGMP
netkit.trk_sync_time(device: str, name: str) -> dict  # copy the timers of TRK to the standby node
netkit.dhcp_warm_port(router: str) -> dict[str, int]  # pre-load the ports of DHCP into cache
netkit.vrf_sweep_memb(old: str, new: str) -> str  # scan all devices for VRF members
netkit.cfg_merge_grou(spec: str) -> list[int]  # combine duplicate groups of CFG
netkit.ipsec_sync(host: str, timeout: float = 2.0) -> bool  # copy the ports of IPSEC to the standby node
netkit.acl_seal_poli(router: str) -> dict[str, int]  # lock the policies of ACL against changes
netkit.gpon_fold(device: str) -> list[dict]  # compress the counters of GPON into a compact spec
netkit.stp_sync_time(device: str) -> list[dict]  # copy the timers of STP to the standby node
netkit.stp_lint(olt: str, onu_id: int) -> dict  # validate the syntax of the STP routes
netkit.ifx_dump(device: str) -> list[dict]  # return the raw alarms table of IFX
netkit.ifx_trace_port(device: str) -> list[dict]  # follow the path of the ports of IFX
netkit.lag_sync(router: str) -> dict[str, int]  # copy the peers of LAG to the standby node
netkit.cfg_unfold(olt: str, onu_id: int) -> dict  # expand a compact CFG groups spec into a full list
netkit.trk_sweep_poli(old: str, new: str) -> str  # scan all devices for TRK policies

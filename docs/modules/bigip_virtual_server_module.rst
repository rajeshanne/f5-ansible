.. _bigip_virtual_server:


bigip_virtual_server - Manage LTM virtual servers on a BIG-IP
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 2.1


.. contents::
   :local:
   :depth: 2


Synopsis
--------

* Manage LTM virtual servers on a BIG-IP.


Requirements (on host that executes module)
-------------------------------------------

  * f5-sdk >= 3.0.9
  * netaddr


Options
-------

.. raw:: html

    <table border=1 cellpadding=4>
    <tr>
    <th class="head">parameter</th>
    <th class="head">required</th>
    <th class="head">default</th>
    <th class="head">choices</th>
    <th class="head">comments</th>
    </tr>
                <tr><td>address_translation<br/><div style="font-size: small;"> (added in 2.6)</div></td>
    <td>no</td>
    <td></td>
        <td><ul><li>yes</li><li>no</li></ul></td>
        <td><div>Specifies, when <code>enabled</code>, that the system translates the address of the virtual server.</div><div>When <code>disabled</code>, specifies that the system uses the address without translation.</div><div>This option is useful when the system is load balancing devices that have the same IP address.</div><div>When creating a new virtual server, the default is <code>enabled</code>.</div>        </td></tr>
                <tr><td>default_persistence_profile<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Default Profile which manages the session persistence.</div><div>If you want to remove the existing default persistence profile, specify an empty value; <code>&quot;&quot;</code>. See the documentation for an example.</div>        </td></tr>
                <tr><td>description<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Virtual server description.</div>        </td></tr>
                <tr><td>destination<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>Destination IP of the virtual server.</div><div>Required when <code>state</code> is <code>present</code> and virtual server does not exist.</div></br>
    <div style="font-size: small;">aliases: address, ip<div>        </td></tr>
                <tr><td>disabled_vlans<br/><div style="font-size: small;"> (added in 2.5)</div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>List of VLANs to be disabled. If the partition is not specified in the VLAN, then the <code>partition</code> option of this module will be used.</div><div>This parameter is mutually exclusive with the <code>enabled_vlans</code> parameters.</div>        </td></tr>
                <tr><td>enabled_vlans<br/><div style="font-size: small;"> (added in 2.2)</div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>List of VLANs to be enabled. When a VLAN named <code>all</code> is used, all VLANs will be allowed. VLANs can be specified with or without the leading partition. If the partition is not specified in the VLAN, then the <code>partition</code> option of this module will be used.</div><div>This parameter is mutually exclusive with the <code>disabled_vlans</code> parameter.</div>        </td></tr>
                <tr><td>fallback_persistence_profile<br/><div style="font-size: small;"> (added in 2.3)</div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Specifies the persistence profile you want the system to use if it cannot use the specified default persistence profile.</div><div>If you want to remove the existing fallback persistence profile, specify an empty value; <code>&quot;&quot;</code>. See the documentation for an example.</div>        </td></tr>
                <tr><td>ip_protocol<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td><ul><li>0-255</li><li>ah</li><li>bna</li><li>esp</li><li>etherip</li><li>gre</li><li>icmp</li><li>ipencap</li><li>ipv6</li><li>ipv6-auth</li><li>ipv6-crypt</li><li>ipv6-icmp</li><li>isp-ip</li><li>mux</li><li>ospf</li><li>sctp</li><li>tcp</li><li>udp</li><li>udplite</li></ul></td>
        <td><div>Specifies a network protocol name you want the system to use to direct traffic on this virtual server.</div><div>When creating a new virtual server, if this parameter is not specified, the default is <code>tcp</code>.</div><div>The Protocol setting is not available when you select Performance (HTTP) as the Type.</div><div>The value of this argument can be specified in either it&#x27;s numeric value, or, for convenience, in a select number of named values. Refer to <code>choices</code> for examples.</div><div>For a list of valid IP protocol numbers, refer to this page https://en.wikipedia.org/wiki/List_of_IP_protocol_numbers</div><div>When <code>type</code> is <code>dhcp</code>, this module will force the <code>ip_protocol</code> parameter to be <code>17</code> (UDP).</div>        </td></tr>
                <tr><td>irules<br/><div style="font-size: small;"> (added in 2.2)</div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>List of rules to be applied in priority order.</div><div>If you want to remove existing iRules, specify a single empty value; <code>&quot;&quot;</code>. See the documentation for an example.</div></br>
    <div style="font-size: small;">aliases: all_rules<div>        </td></tr>
                <tr><td>metadata<br/><div style="font-size: small;"> (added in 2.5)</div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Arbitrary key/value pairs that you can attach to a pool. This is useful in situations where you might want to annotate a virtual to me managed by Ansible.</div><div>Key names will be stored as strings; this includes names that are numbers.</div><div>Values for all of the keys will be stored as strings; this includes values that are numbers.</div><div>Data will be persisted, not ephemeral.</div>        </td></tr>
                <tr><td>name<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>Virtual server name.</div></br>
    <div style="font-size: small;">aliases: vs<div>        </td></tr>
                <tr><td>partition<br/><div style="font-size: small;"> (added in 2.5)</div></td>
    <td>no</td>
    <td>Common</td>
        <td></td>
        <td><div>Device partition to manage resources on.</div>        </td></tr>
                <tr><td>password<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>The password for the user account used to connect to the BIG-IP. You can omit this option if the environment variable <code>F5_PASSWORD</code> is set.</div></br>
    <div style="font-size: small;">aliases: pass, pwd<div>        </td></tr>
                <tr><td>policies<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Specifies the policies for the virtual server</div></br>
    <div style="font-size: small;">aliases: all_policies<div>        </td></tr>
                <tr><td>pool<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Default pool for the virtual server.</div><div>If you want to remove the existing pool, specify an empty value; <code>&quot;&quot;</code>. See the documentation for an example.</div>        </td></tr>
                <tr><td>port<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Port of the virtual server. Required when <code>state</code> is <code>present</code> and virtual server does not exist.</div><div>If you do not want to specify a particular port, use the value <code>0</code>. The result is that the virtual server will listen on any port.</div><div>When <code>type</code> is <code>dhcp</code>, this module will force the <code>port</code> parameter to be <code>67</code>.</div><div>When <code>type</code> is <code>internal</code>, this module will force the <code>port</code> parameter to be <code>0</code>.</div>        </td></tr>
                <tr><td>port_translation<br/><div style="font-size: small;"> (added in 2.6)</div></td>
    <td>no</td>
    <td></td>
        <td><ul><li>yes</li><li>no</li></ul></td>
        <td><div>Specifies, when <code>enabled</code>, that the system translates the port of the virtual server.</div><div>When <code>disabled</code>, specifies that the system uses the port without translation. Turning off port translation for a virtual server is useful if you want to use the virtual server to load balance connections to any service.</div><div>When creating a new virtual server, the default is <code>enabled</code>.</div>        </td></tr>
                <tr><td rowspan="2">profiles<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td><td></td>
    <td> <div>List of profiles (HTTP, ClientSSL, ServerSSL, etc) to apply to both sides of the connection (client-side and server-side).</div><div>If you only want to apply a particular profile to the client-side of the connection, specify <code>client-side</code> for the profile&#x27;s <code>context</code>.</div><div>If you only want to apply a particular profile to the server-side of the connection, specify <code>server-side</code> for the profile&#x27;s <code>context</code>.</div><div>If <code>context</code> is not provided, it will default to <code>all</code>.</div><div>If you want to remove a profile from the list of profiles currently active on the virtual, then simply remove it from the <code>profiles</code> list. See examples for an illustration of this.</div><div>If you want to add a profile to the list of profiles currently active on the virtual, then simply add it to the <code>profiles</code> list. See examples for an illustration of this.</div><div><b>Profiles matter</b>. There is a good chance that this module will fail to configure a BIG-IP if you mix up your profiles, or, if you attempt to set an IP protocol which you current or new profiles do not support. Either this module, or BIG-IP, will tell you when you are wrong with an error resembling <code>lists profiles incompatible with its protocol</code>.</div><div>If you are unsure what correct profile combinations are, then have a BIG-IP available to you in which you can make changes and copy what the correct combinations are.</div></br>
    <div style="font-size: small;">aliases: all_profiles<div>    </tr>
    <tr>
    <td colspan="5">
    <table border=1 cellpadding=4>
    <caption><b>Dictionary object profiles</b></caption>
    <tr>
    <th class="head">parameter</th>
    <th class="head">required</th>
    <th class="head">default</th>
    <th class="head">choices</th>
    <th class="head">comments</th>
    </tr>
                    <tr><td>name<br/><div style="font-size: small;"></div></td>
        <td>no</td>
        <td></td>
                <td></td>
                <td><div>Name of the profile.</div><div>If this is not specified, then it is assumed that the profile item is only a name of a profile.</div><div>This must be specified if a context is specified.</div>        </td></tr>
                    <tr><td>context<br/><div style="font-size: small;"></div></td>
        <td>no</td>
        <td>all</td>
                <td><ul><li>all</li><li>server-side</li><li>client-side</li></ul></td>
                <td><div>The side of the connection on which the profile should be applied.</div>        </td></tr>
        </table>
    </td>
    </tr>
        </td></tr>
                <tr><td rowspan="2">provider<br/><div style="font-size: small;"> (added in 2.5)</div></td>
    <td>no</td>
    <td></td><td></td>
    <td> <div>A dict object containing connection details.</div>    </tr>
    <tr>
    <td colspan="5">
    <table border=1 cellpadding=4>
    <caption><b>Dictionary object provider</b></caption>
    <tr>
    <th class="head">parameter</th>
    <th class="head">required</th>
    <th class="head">default</th>
    <th class="head">choices</th>
    <th class="head">comments</th>
    </tr>
                    <tr><td>ssh_keyfile<br/><div style="font-size: small;"></div></td>
        <td>no</td>
        <td></td>
                <td></td>
                <td><div>Specifies the SSH keyfile to use to authenticate the connection to the remote device.  This argument is only used for <em>cli</em> transports. If the value is not specified in the task, the value of environment variable <code>ANSIBLE_NET_SSH_KEYFILE</code> will be used instead.</div>        </td></tr>
                    <tr><td>timeout<br/><div style="font-size: small;"></div></td>
        <td>no</td>
        <td>10</td>
                <td></td>
                <td><div>Specifies the timeout in seconds for communicating with the network device for either connecting or sending commands.  If the timeout is exceeded before the operation is completed, the module will error.</div>        </td></tr>
                    <tr><td>server<br/><div style="font-size: small;"></div></td>
        <td>yes</td>
        <td></td>
                <td></td>
                <td><div>The BIG-IP host. You can omit this option if the environment variable <code>F5_SERVER</code> is set.</div>        </td></tr>
                    <tr><td>user<br/><div style="font-size: small;"></div></td>
        <td>yes</td>
        <td></td>
                <td></td>
                <td><div>The username to connect to the BIG-IP with. This user must have administrative privileges on the device. You can omit this option if the environment variable <code>F5_USER</code> is set.</div>        </td></tr>
                    <tr><td>server_port<br/><div style="font-size: small;"></div></td>
        <td>no</td>
        <td>443</td>
                <td></td>
                <td><div>The BIG-IP server port. You can omit this option if the environment variable <code>F5_SERVER_PORT</code> is set.</div>        </td></tr>
                    <tr><td>password<br/><div style="font-size: small;"></div></td>
        <td>yes</td>
        <td></td>
                <td></td>
                <td><div>The password for the user account used to connect to the BIG-IP. You can omit this option if the environment variable <code>F5_PASSWORD</code> is set.</div>        </td></tr>
                    <tr><td>validate_certs<br/><div style="font-size: small;"></div></td>
        <td>no</td>
        <td>True</td>
                <td><ul><li>yes</li><li>no</li></ul></td>
                <td><div>If <code>no</code>, SSL certificates will not be validated. Use this only on personally controlled sites using self-signed certificates. You can omit this option if the environment variable <code>F5_VALIDATE_CERTS</code> is set.</div>        </td></tr>
                    <tr><td>transport<br/><div style="font-size: small;"></div></td>
        <td>yes</td>
        <td>cli</td>
                <td><ul><li>rest</li><li>cli</li></ul></td>
                <td><div>Configures the transport connection to use when connecting to the remote device.</div>        </td></tr>
        </table>
    </td>
    </tr>
        </td></tr>
                <tr><td>server<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>The BIG-IP host. You can omit this option if the environment variable <code>F5_SERVER</code> is set.</div>        </td></tr>
                <tr><td>server_port<br/><div style="font-size: small;"> (added in 2.2)</div></td>
    <td>no</td>
    <td>443</td>
        <td></td>
        <td><div>The BIG-IP server port. You can omit this option if the environment variable <code>F5_SERVER_PORT</code> is set.</div>        </td></tr>
                <tr><td>snat<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td><ul><li>None</li><li>Automap</li><li>Name of a SNAT pool (eg "/Common/snat_pool_name") to enable SNAT with the specific pool</li></ul></td>
        <td><div>Source network address policy.</div>        </td></tr>
                <tr><td>source<br/><div style="font-size: small;"> (added in 2.5)</div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Specifies an IP address or network from which the virtual server accepts traffic.</div><div>The virtual server accepts clients only from one of these IP addresses.</div><div>For this setting to function effectively, specify a value other than 0.0.0.0/0 or ::/0 (that is, any/0, any6/0).</div><div>In order to maximize utility of this setting, specify the most specific address prefixes covering all customer addresses and no others.</div><div>Specify the IP address in Classless Inter-Domain Routing (CIDR) format; address/prefix, where the prefix length is in bits. For example, for IPv4, 10.0.0.1/32 or 10.0.0.0/24, and for IPv6, ffe1::0020/64 or 2001:ed8:77b5:2:10:10:100:42/64.</div>        </td></tr>
                <tr><td>state<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>present</td>
        <td><ul><li>present</li><li>absent</li><li>enabled</li><li>disabled</li></ul></td>
        <td><div>The virtual server state. If <code>absent</code>, delete the virtual server if it exists. <code>present</code> creates the virtual server and enable it. If <code>enabled</code>, enable the virtual server if it exists. If <code>disabled</code>, create the virtual server if needed, and set state to <code>disabled</code>.</div>        </td></tr>
                <tr><td>type<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td><ul><li>standard</li><li>forwarding-l2</li><li>forwarding-ip</li><li>performance-http</li><li>performance-l4</li><li>stateless</li><li>reject</li><li>dhcp</li><li>internal</li><li>message-routing</li></ul></td>
        <td><div>Specifies the network service provided by this virtual server.</div><div>When creating a new virtual server, if this parameter is not provided, the default will be <code>standard</code>.</div><div>When <code>standard</code>, specifies a virtual server that directs client traffic to a load balancing pool and is the most basic type of virtual server. When you first create the virtual server, you assign an existing default pool to it. From then on, the virtual server automatically directs traffic to that default pool.</div><div>When <code>forwarding-l2</code>, specifies a virtual server that shares the same IP address as a node in an associated VLAN.</div><div>When <code>forwarding-ip</code>, specifies a virtual server like other virtual servers, except that the virtual server has no pool members to load balance. The virtual server simply forwards the packet directly to the destination IP address specified in the client request.</div><div>When <code>performance-http</code>, specifies a virtual server with which you associate a Fast HTTP profile. Together, the virtual server and profile increase the speed at which the virtual server processes HTTP requests.</div><div>When <code>performance-l4</code>, specifies a virtual server with which you associate a Fast L4 profile. Together, the virtual server and profile increase the speed at which the virtual server processes layer 4 requests.</div><div>When <code>stateless</code>, specifies a virtual server that accepts traffic matching the virtual server address and load balances the packet to the pool members without attempting to match the packet to a pre-existing connection in the connection table. New connections are immediately removed from the connection table. This addresses the requirement for one-way UDP traffic that needs to be processed at very high throughput levels, for example, load balancing syslog traffic to a pool of syslog servers. Stateless virtual servers are not suitable for processing traffic that requires stateful tracking, such as TCP traffic. Stateless virtual servers do not support iRules, persistence, connection mirroring, rateshaping, or SNAT automap.</div><div>When <code>reject</code>, specifies that the BIG-IP system rejects any traffic destined for the virtual server IP address.</div><div>When <code>dhcp</code>, specifies a virtual server that relays Dynamic Host Control Protocol (DHCP) client requests for an IP address to one or more DHCP servers, and provides DHCP server responses with an available IP address for the client.</div><div>When <code>internal</code>, specifies a virtual server that supports modification of HTTP requests and responses. Internal virtual servers enable usage of ICAP (Internet Content Adaptation Protocol) servers to modify HTTP requests and responses by creating and applying an ICAP profile and adding Request Adapt or Response Adapt profiles to the virtual server.</div><div>When <code>message-routing</code>, specifies a virtual server that uses a SIP application protocol and functions in accordance with a SIP session profile and SIP router profile.</div>        </td></tr>
                <tr><td>user<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>The username to connect to the BIG-IP with. This user must have administrative privileges on the device. You can omit this option if the environment variable <code>F5_USER</code> is set.</div>        </td></tr>
                <tr><td>validate_certs<br/><div style="font-size: small;"> (added in 2.0)</div></td>
    <td>no</td>
    <td>True</td>
        <td><ul><li>yes</li><li>no</li></ul></td>
        <td><div>If <code>no</code>, SSL certificates will not be validated. Use this only on personally controlled sites using self-signed certificates. You can omit this option if the environment variable <code>F5_VALIDATE_CERTS</code> is set.</div>        </td></tr>
        </table>
    </br>



Examples
--------

 ::

    
    - name: Modify Port of the Virtual Server
      bigip_virtual_server:
        server: lb.mydomain.net
        user: admin
        password: secret
        state: present
        partition: Common
        name: my-virtual-server
        port: 8080
      delegate_to: localhost

    - name: Delete virtual server
      bigip_virtual_server:
        server: lb.mydomain.net
        user: admin
        password: secret
        state: absent
        partition: Common
        name: my-virtual-server
      delegate_to: localhost

    - name: Add virtual server
      bigip_virtual_server:
        server: lb.mydomain.net
        user: admin
        password: secret
        state: present
        partition: Common
        name: my-virtual-server
        destination: 10.10.10.10
        port: 443
        pool: my-pool
        snat: Automap
        description: Test Virtual Server
        profiles:
          - http
          - fix
          - name: clientssl
            context: server-side
          - name: ilx
            context: client-side
        policies:
          - my-ltm-policy-for-asm
          - ltm-uri-policy
          - ltm-policy-2
          - ltm-policy-3
        enabled_vlans:
          - /Common/vlan2
      delegate_to: localhost

    - name: Add FastL4 virtual server
      bigip_virtual_server:
        destination: 1.1.1.1
        name: fastl4_vs
        port: 80
        profiles:
          - fastL4
        state: present

    - name: Add iRules to the Virtual Server
      bigip_virtual_server:
        server: lb.mydomain.net
        user: admin
        password: secret
        name: my-virtual-server
        irules:
          - irule1
          - irule2
      delegate_to: localhost

    - name: Remove one iRule from the Virtual Server
      bigip_virtual_server:
        server: lb.mydomain.net
        user: admin
        password: secret
        name: my-virtual-server
        irules:
          - irule2
      delegate_to: localhost

    - name: Remove all iRules from the Virtual Server
      bigip_virtual_server:
        server: lb.mydomain.net
        user: admin
        password: secret
        name: my-virtual-server
        irules: ""
      delegate_to: localhost

    - name: Remove pool from the Virtual Server
      bigip_virtual_server:
        server: lb.mydomain.net
        user: admin
        password: secret
        name: my-virtual-server
        pool: ""
      delegate_to: localhost

    - name: Add metadata to virtual
      bigip_pool:
        server: lb.mydomain.com
        user: admin
        password: secret
        state: absent
        name: my-pool
        partition: Common
        metadata:
          ansible: 2.4
          updated_at: 2017-12-20T17:50:46Z
      delegate_to: localhost

    - name: Add virtual with two profiles
      bigip_pool:
        server: lb.mydomain.com
        user: admin
        password: secret
        state: absent
        name: my-pool
        partition: Common
        profiles:
          - http
          - tcp
      delegate_to: localhost

    - name: Remove HTTP profile from previous virtual
      bigip_pool:
        server: lb.mydomain.com
        user: admin
        password: secret
        state: absent
        name: my-pool
        partition: Common
        profiles:
          - tcp
      delegate_to: localhost

    - name: Add the HTTP profile back to the previous virtual
      bigip_pool:
        server: lb.mydomain.com
        user: admin
        password: secret
        state: absent
        name: my-pool
        partition: Common
        profiles:
          - http
          - tcp
      delegate_to: localhost


Return Values
-------------

Common return values are `documented here <http://docs.ansible.com/ansible/latest/common_return_values.html>`_, the following are the fields unique to this module:

.. raw:: html

    <table border=1 cellpadding=4>
    <tr>
    <th class="head">name</th>
    <th class="head">description</th>
    <th class="head">returned</th>
    <th class="head">type</th>
    <th class="head">sample</th>
    </tr>

        <tr>
        <td> disabled_vlans </td>
        <td> List of VLANs that the virtual is disabled for. </td>
        <td align=center> changed </td>
        <td align=center> list </td>
        <td align=center> ['/Common/vlan1', '/Common/vlan2'] </td>
    </tr>
            <tr>
        <td> description </td>
        <td> New description of the virtual server. </td>
        <td align=center> changed </td>
        <td align=center> string </td>
        <td align=center> This is my description </td>
    </tr>
            <tr>
        <td> fallback_persistence_profile </td>
        <td> Fallback persistence profile set on the virtual server. </td>
        <td align=center> changed </td>
        <td align=center> string </td>
        <td align=center> /Common/source_addr </td>
    </tr>
            <tr>
        <td> default_persistence_profile </td>
        <td> Default persistence profile set on the virtual server. </td>
        <td align=center> changed </td>
        <td align=center> string </td>
        <td align=center> /Common/dest_addr </td>
    </tr>
            <tr>
        <td> disabled </td>
        <td> Whether the virtual server is disabled, or not. </td>
        <td align=center> changed </td>
        <td align=center> bool </td>
        <td align=center> True </td>
    </tr>
            <tr>
        <td> enabled_vlans </td>
        <td> List of VLANs that the virtual is enabled for. </td>
        <td align=center> changed </td>
        <td align=center> list </td>
        <td align=center> ['/Common/vlan5', '/Common/vlan6'] </td>
    </tr>
            <tr>
        <td> port </td>
        <td> Port that the virtual server is configured to listen on. </td>
        <td align=center> changed </td>
        <td align=center> int </td>
        <td align=center> 80 </td>
    </tr>
            <tr>
        <td> pool </td>
        <td> Pool that the virtual server is attached to. </td>
        <td align=center> changed </td>
        <td align=center> string </td>
        <td align=center> /Common/my-pool </td>
    </tr>
            <tr>
        <td> ip_protocol </td>
        <td> The new value of the IP protocol </td>
        <td align=center> changed </td>
        <td align=center> integer </td>
        <td align=center> 6 </td>
    </tr>
            <tr>
        <td> destination </td>
        <td> Destination of the virtual server. </td>
        <td align=center> changed </td>
        <td align=center> string </td>
        <td align=center> 1.1.1.1 </td>
    </tr>
            <tr>
        <td> enabled </td>
        <td> Whether the virtual server is enabled, or not. </td>
        <td align=center> changed </td>
        <td align=center> bool </td>
        <td align=center> False </td>
    </tr>
            <tr>
        <td> profiles </td>
        <td> List of profiles set on the virtual server. </td>
        <td align=center> changed </td>
        <td align=center> list </td>
        <td align=center> [{'name': 'tcp', 'context': 'server-side'}, {'name': 'tcp-legacy', 'context': 'client-side'}] </td>
    </tr>
            <tr>
        <td> irules </td>
        <td> iRules set on the virtual server. </td>
        <td align=center> changed </td>
        <td align=center> list </td>
        <td align=center> ['/Common/irule1', '/Common/irule2'] </td>
    </tr>
            <tr>
        <td> source </td>
        <td> Source address, in CIDR form, set on the virtual server. </td>
        <td align=center> changed </td>
        <td align=center> string </td>
        <td align=center> 1.2.3.4/32 </td>
    </tr>
            <tr>
        <td> policies </td>
        <td> List of policies attached to the virtual. </td>
        <td align=center> changed </td>
        <td align=center> list </td>
        <td align=center> ['/Common/policy1', '/Common/policy2'] </td>
    </tr>
            <tr>
        <td> address_translation </td>
        <td> The new value specifying whether address translation is on or off </td>
        <td align=center> changed </td>
        <td align=center> bool </td>
        <td align=center> True </td>
    </tr>
            <tr>
        <td> snat </td>
        <td> SNAT setting of the virtual server. </td>
        <td align=center> changed </td>
        <td align=center> string </td>
        <td align=center> Automap </td>
    </tr>
            <tr>
        <td> port_translation </td>
        <td> The new value specifying whether port translation is on or off </td>
        <td align=center> changed </td>
        <td align=center> bool </td>
        <td align=center> True </td>
    </tr>
            <tr>
        <td> metadata </td>
        <td> The new value of the virtual. </td>
        <td align=center> changed </td>
        <td align=center> dict </td>
        <td align=center> {'key2': 'bar', 'key1': 'foo'} </td>
    </tr>
        
    </table>
    </br></br>

Notes
-----

.. note::
    - Requires BIG-IP software version >= 11
    - Requires the netaddr Python package on the host. This is as easy as pip install netaddr.
    - For more information on using Ansible to manage F5 Networks devices see https://www.ansible.com/integrations/networks/f5.
    - Requires the f5-sdk Python package on the host. This is as easy as ``pip install f5-sdk``.



Status
~~~~~~

This module is flagged as **preview** which means that it is not guaranteed to have a backwards compatible interface.


Support
~~~~~~~

This module is community maintained without core committer oversight.

For more information on what this means please read :doc:`/usage/support`


For help developing modules, should you be so inclined, please read :doc:`Getting Involved </development/getting-involved>`, :doc:`Writing a Module </development/writing-a-module>` and :doc:`Guidelines </development/guidelines>`.
---
name: f5-virtual-server-discovery
description: Discover how an F5 virtual server is built
---

# F5 virtual server discovery

The skill from slide 16, written out in full. Same four-part shape every skill uses:

`Trigger → Procedure → Resources → Result`

Compare it to [`NETWORK_AGENT.md`](../NETWORK_AGENT.md). That file says how to
*think*. This one says how to *do one specific thing*. Keeping them separate is why
neither has to be enormous.

## Trigger

Use this when asked how a virtual server is configured, why a VIP is not answering,
which pool members are behind a VIP, or to document an existing F5 service.

Do **not** use this to change configuration. Discovery only.

## Procedure

Run in order. Each step builds the picture the next one needs.

1. **Identify the VIP, profiles, and iRules**

   ```
   list ltm virtual <name>
   ```

   Capture the destination address and port, the profile list, any attached iRules,
   the default pool, and the SNAT configuration.

2. **Map the pool, members, and monitors**

   ```
   list ltm pool <pool-name>
   ```

   Capture every member, its address and port, the load balancing mode, the health
   monitor assigned, and the priority group settings.

3. **Capture health state**

   ```
   show ltm virtual <name>
   show ltm pool <pool-name> members
   ```

   Record availability, state, and reason for every member. A member that is `down`
   with reason "monitor failed" is a different problem from one that is `user-down`.

4. **Review routing**

   ```
   show net route
   list net self
   ```

   Confirm the F5 can actually reach the pool member subnets, and identify which
   self-IP sources the health checks.

## Resources

- Read-only F5 account. This skill never needs write access.
- SSH or iControl REST reachability to the management address.
- The VIP name or address to start from. If you only have a hostname, resolve it
  first and confirm which VIP owns that address before proceeding.

## Result

Return, in this order:

- **VIP → Pool → Members** as an explicit chain, with addresses and ports
- **Profiles and iRules** attached, noting any iRule that changes pool selection
- **Health state** per member, with the reason for anything not `available`
- **Routing design** — the path from the F5 to the members, and the source address
  health checks use

Then state the one thing most likely to be wrong, if anything looks wrong.

Do not suggest configuration changes unless explicitly asked. If a change is
obviously needed, name it and stop.

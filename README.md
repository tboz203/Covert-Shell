# Covert Shell

super-simple covert backdoor shell. AES-encrypted (with a currently hardwired
key) ping payload hooked up to a one-off shell for each command. requires root
to run, is actually a tremendous security risk.

**DO NOT LEAVE RUNNING FOR ANY SIGNIFICANT LENGTH OF TIME!!**

anybody can go and reverse-engineer this thing, and start feeding commands to
your root shell. It looks like it's wired up to only work with localhost, but
that's not actually how it works. *just be careful with the damn thing, okay?*

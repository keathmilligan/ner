# Generate IP Addresses
# - generate both IPv4 and IPv6 addresses
# - generate IPv4 addresses with and without leading zeros
# - generate all variations of IPv6 addresses, including embedded IPv4

import random
import string

def generate_ipv4_addresses(count=10):
    """
    Generate a list of n random IPv4 addresses (as strings).
    - For ~20% of these addresses, all four octets are padded to 3 digits (e.g. '010.007.255.002').
    - For the remaining ~80%, no padding is used (e.g. '10.7.255.2').
    """
    addresses = []
    while count:
        # Decide if this IP will be fully zero-padded or not (20% chance)
        zero_pad = (random.random() < 0.2)

        octets = []
        for _ in range(4):
            val = random.randint(0, 255)
            if zero_pad:
                # Pad to 3 digits
                octet_str = f"{val:03d}"
            else:
                # No padding
                octet_str = str(val)
            octets.append(octet_str)

        ip_addr = '.'.join(octets)
        if ip_addr not in addresses:
            addresses.append(ip_addr)
            count -= 1
    
    return addresses


HEX_CHARS = string.digits + 'abcdef'

def random_hex_group(min_len=1, max_len=4):
    """
    Return a random hex string of length between min_len and max_len.
    E.g., '1a2f' or '03b'.
    """
    length = random.randint(min_len, max_len)
    return ''.join(random.choice(HEX_CHARS) for _ in range(length))

def generate_full_ipv6():
    """
    Generate a full (uncompressed) IPv6 address in the form of:
      xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:xxxx
    Each group is 1–4 hex digits (commonly it's 4, but we allow variation).
    """
    groups = [random_hex_group(1, 4) for _ in range(8)]
    return ':'.join(groups)

def generate_compressed_ipv6():
    """
    Generate an IPv6 address with a random contiguous sequence of zero groups
    compressed into '::'.
    
    Strategy:
      1. Create 8 groups, each either random or zero.
      2. Pick a random contiguous subset of groups to be zero.
      3. Replace that subset with '::', ensuring we only do it once.
    """
    # Start with all random groups
    groups = [random_hex_group(1, 4) for _ in range(8)]
    
    # Decide how many consecutive groups to force to zero (at least 1, up to 3 or 4 for variety)
    zero_count = random.randint(1, 4)
    
    # Choose a random start index for zeroing out (somewhere 0..(8 - zero_count))
    start_idx = random.randint(0, 8 - zero_count)
    
    # Zero out those groups
    for i in range(start_idx, start_idx + zero_count):
        groups[i] = '0'
    
    # Now convert to a standard full address (some groups = "0")
    full = ':'.join(groups)
    
    # Replace the first contiguous sequence of :0:0:... with '::'
    # We'll do a naive approach: build a pattern and use '::' once.
    # A more robust approach might manually parse, but let's keep it simple.
    
    # We want something like ":0:0:0:" -> "::"
    # Easiest might be to do a replace with a known substring, but
    # we need to ensure we only do it once (since we only have one contiguous block).
    
    # We'll create a string for the zero block
    zero_block = ':'.join(['0'] * zero_count)  # e.g. "0:0:0"
    # We want to replace "zero_block" but only if it's a separate chunk, so let's ensure we catch
    # possible preceding or trailing colon. For example, "2001:0:0:0:db8" => "2001::db8"
    # We'll handle boundary conditions by also attempting with leading/trailing colons.
    # A simple approach is to ensure we always match ':0:0:0:' with surrounding colons, 
    # but consider edge group.
    
    # Insert sentinel ends to handle boundary groups
    sentinel_full = f":{full}:"
    sentinel_block = f":{zero_block}:"
    
    compressed = sentinel_full.replace(sentinel_block, '::', 1)
    
    # Remove the sentinel colons we added
    if compressed.startswith(':'):
        compressed = compressed[1:]
    if compressed.endswith(':'):
        compressed = compressed[:-1]
    
    # Special case: if we replaced at the very beginning or very end,
    # we might have double-colons. Usually this is okay, but let's ensure correctness.
    # For instance, if the zero sequence is at the start, we might get "::abcd:..."
    # That's actually valid. So no special fix needed, just be sure we didn't break the string.
    
    return compressed

def generate_embedded_ipv4():
    """
    Generate an IPv6 address that embeds an IPv4 address at the end:
      e.g., ::ffff:192.168.0.1
            2001:db8:85a3::192.168.0.1
    Strategy:
      - We'll create 6 IPv6 groups (some random, some possibly zero-compressed)
      - Then append the IPv4 part.
      - We might or might not compress a block of zeros from the left portion.
    """
    # First create 6 groups of random IPv6
    groups = [random_hex_group(1, 4) for _ in range(6)]
    
    # There's a chance we force some zeros to allow compression
    zero_count = random.randint(1, 3)  # up to 3 groups can become "0"
    start_idx = random.randint(0, 6 - zero_count)
    for i in range(start_idx, start_idx + zero_count):
        groups[i] = '0'
    
    # Build the left part
    left_full = ':'.join(groups)
    
    # We'll create the IPv4 portion
    def random_ipv4_octet():
        return str(random.randint(0, 255))
    ipv4_part = '.'.join(random_ipv4_octet() for _ in range(4))
    
    # Attempt to compress the left part if possible (similar approach to above)
    zero_block = ':'.join(['0'] * zero_count)  # e.g. "0:0"
    sentinel_full = f":{left_full}:"
    sentinel_block = f":{zero_block}:"
    
    compressed_left = sentinel_full.replace(sentinel_block, '::', 1)
    # Remove sentinel colons
    if compressed_left.startswith(':'):
        compressed_left = compressed_left[1:]
    if compressed_left.endswith(':'):
        compressed_left = compressed_left[:-1]

    # Join with the IPv4 portion
    return f"{compressed_left}:{ipv4_part}"

def generate_ipv6_addresses(count=10):
    """
    Generate a list of n IPv6 addresses (as strings), randomly picking among:
      - Full notation
      - Compressed notation
      - IPv4-embedded notation
    
    Adjust probabilities or add more variety as you see fit.
    """
    results = []
    while count:
        # Rough probability distribution
        notation_type = random.choices(
            population=['full', 'compressed', 'embedded'],
            weights=[0.3, 0.4, 0.3],  # 30% full, 40% compressed, 30% embedded
            k=1
        )[0]
        
        if notation_type == 'full':
            ipv6 = generate_full_ipv6()
        elif notation_type == 'compressed':
            ipv6 = generate_compressed_ipv6()
        else:  # 'embedded'
            ipv6 = generate_embedded_ipv4()
        
        if ipv6 not in results:
            results.append(ipv6)
            count -= 1
    
    return results

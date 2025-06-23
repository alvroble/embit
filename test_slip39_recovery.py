#!/usr/bin/env python3
"""
Quick script to test SLIP39 recovery using specific shares
"""

import sys
import os

# Add src to path so we can import embit
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from embit.slip39 import ShareSet, Share
from embit.bip32 import HDKey
from embit.bip39 import mnemonic_to_seed
from binascii import hexlify

def main():
    # Test shares from the test vectors
    '''slip39_shares = [
        "shadow pistol academic always adequate wildlife fancy gross oasis cylinder mustang wrist rescue view short owner flip making coding armed",
        "shadow pistol academic acid actress prayer class unknown daughter sweater depict flip twice unkind craft early superior advocate guest smoking",
    ]'''

    slip39_shares = [
      "wildlife deal ceramic round aluminum pitch goat racism employer miracle percent math decision episode dramatic editor lily prospect program scene rebuild display sympathy have single mustang junction relate often chemical society wits estate",
      "wildlife deal decision scared acne fatal snake paces obtain election dryer dominant romp tactics railroad marvel trust helpful flip peanut theory theater photo luck install entrance taxi step oven network dictate intimate listen",
      "wildlife deal ceramic scatter argue equip vampire together ruin reject literary rival distance aquatic agency teammate rebound false argue miracle stay again blessing peaceful unknown cover beard acid island language debris industry idle",
      "wildlife deal ceramic snake agree voter main lecture axis kitchen physics arcade velvet spine idea scroll promise platform firm sharp patrol divorce ancestor fantasy forbid goat ajar believe swimming cowboy symbolic plastic spelling",
      "wildlife deal decision shadow analysis adjust bulb skunk muscle mandate obesity total guitar coal gravity carve slim jacket ruin rebuild ancestor numerous hour mortgage require herd maiden public ceiling pecan pickup shadow club"
    ]
    
    # Passphrase used in the test vectors
    passphrase = b"TREZOR"
    
    print("SLIP39 Recovery Test")
    print("=" * 50)
    print(f"Using {len(slip39_shares)} SLIP39 shares:")
    for i, share in enumerate(slip39_shares, 1):
        print(f"  {i}. {share}")
    
    print(f"\nPassphrase: {passphrase.decode()}")
    
    try:
        # Parse the shares
        shares = [Share.parse(mnemonic) for mnemonic in slip39_shares]
        
        # Create ShareSet and recover the secret
        share_set = ShareSet(shares)
        recovered_secret = share_set.recover(passphrase)
        
        print(f"\nRecovered secret (hex): {hexlify(recovered_secret).decode()}")
        

        # SLIP-39 to BIP-39
        print("\n\n*********************************")
        print("******* SLIP-39 to BIP-39 *******")
        print("********************************* \n\n")
        # Recover the BIP39 mnemonic
        bip39_mnemonic = ShareSet.recover_mnemonic(slip39_shares, passphrase)
        
        print(f"\nRecovered BIP39 mnemonic:")
        print(f"  {bip39_mnemonic}")
        
        # Generate HDKey from the recovered mnemonic to get fingerprint
        seed = mnemonic_to_seed(bip39_mnemonic)
        print(f"\nRecovered seed (hex): {hexlify(seed).decode()}")
        
        root_key = HDKey.from_seed(seed)
        fingerprint = root_key.my_fingerprint
        
        print(f"\nRoot key fingerprint: {hexlify(fingerprint).decode()}")
        print(f"Master private key: {root_key.to_base58()}")
        print(f"Master public key:  {root_key.to_public().to_base58()}")
        
        # SLIP-39 to BIP-32
        print("\n\n*********************************")
        print("******* SLIP-39 to BIP-32 *******")
        print("*********************************\n\n")

        root_key_raw = HDKey.from_seed(recovered_secret)
        fingerprint_raw = root_key_raw.my_fingerprint
        
        print(f"\nRoot key fingerprint: {hexlify(fingerprint_raw).decode()}")
        print(f"Master private key: {root_key_raw.to_base58()}")
        print(f"Master public key:  {root_key_raw.to_public().to_base58()}")

        # Expected result from test vector
        expected_hex = "b43ceb7e57a0ea8766221624d01b0864"
        print(f"\nExpected secret (hex):  {expected_hex}")
        print(f"Recovery successful: {hexlify(recovered_secret).decode() == expected_hex}")
        

        


    except Exception as e:
        print(f"\nError during recovery: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
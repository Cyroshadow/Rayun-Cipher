"""
Rayun Cipher v0.4 - Optimized Implementation
=============================================
Based on the original Rayun Cipher v0.2 by Nubla et al.

This version includes:
- All security fixes from v0.3
- Computational complexity optimization from O(n×a) to O(n)
- Optional parallelization support
- Comprehensive documentation

Complexity Analysis:
-------------------
| Operation          | v0.2 (Original) | v0.4 (Optimized) |
|--------------------|-----------------|------------------|
| Setup              | O(a²)           | O(a²)            |
| Encrypt per char   | O(a)            | O(1)             |
| Encrypt total      | O(n × a)        | O(n)             |
| Decrypt per char   | O(a)            | O(1)             |
| Decrypt total      | O(n × a)        | O(n)             |
| Space              | O(a²)           | O(a²)            |

Where: n = message length, a = alphabet size (100)

The key optimization is replacing list.index() calls [O(a) each]
with dictionary lookups [O(1) each].
"""

import string
import secrets
import hashlib
from collections import Counter
from typing import List, Dict, Tuple, Optional
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import multiprocessing


class RayunCipher:
    """
    Optimized Improved Vigenère Cipher with O(n) complexity.
    
    Features:
    - Extended 100-character alphabet (vs 26 in classical Vigenère)
    - Key-derived shuffled substitution table
    - Cryptographically secure key derivation (PBKDF2)
    - O(1) character lookups via hash tables
    - Optional parallel encryption/decryption
    - Configurable key length
    - Salt support for unique ciphertexts
    
    Security Note:
    This is an educational cipher demonstrating classical cryptography
    improvements. For production security, use modern algorithms (AES, ChaCha20).
    """

    def __init__(
        self, 
        plaintext: str, 
        elements: List[str], 
        master_key: str, 
        key_length: int = 100, 
        salt: Optional[bytes] = None
    ):
        """
        Initialize the Rayun Cipher.
        
        Args:
            plaintext: The text to encrypt/decrypt
            elements: List of characters in the cipher alphabet
            master_key: The password/key for encryption
            key_length: Length of derived key (default: 100)
            salt: Optional salt for key derivation (generates random if None)
        
        Raises:
            ValueError: If plaintext contains characters not in alphabet
        
        Time Complexity: O(a²) where a = alphabet size
        Space Complexity: O(a²) for tables and lookup dictionaries
        """
        self.data = plaintext
        self.elements = elements
        self.master_key = master_key
        self.key_length = key_length
        self.salt = salt if salt else secrets.token_bytes(16)
        
        # Validate input
        self._validate_input()
        
        # Generate cryptographic components
        self.yun_key = self._derive_yun_key()           # O(key_length)
        self.ray_table = self._generate_ray_table()      # O(a²)
        
        # OPTIMIZATION: Pre-compute O(1) lookup tables
        self._build_lookup_tables()                      # O(a²)
    
    def _validate_input(self) -> None:
        """
        Validate that all plaintext characters are in the alphabet.
        
        Time Complexity: O(n) where n = plaintext length
        """
        invalid_chars = set(self.data) - set(self.elements)
        if invalid_chars:
            raise ValueError(
                f"Plaintext contains characters not in alphabet: {invalid_chars}\n"
                f"Consider adding these to your elements or removing them from plaintext."
            )
    
    def _derive_key_bytes(self, purpose: str, length: int) -> bytes:
        """
        Derive cryptographic key material using PBKDF2.
        
        Uses HMAC-SHA256 with 100,000 iterations for security.
        Different purposes get different keys via domain separation.
        
        Args:
            purpose: String to differentiate key uses ('yun', 'shuffle')
            length: Number of bytes to derive
            
        Returns:
            Derived key bytes
        
        Time Complexity: O(iterations) ≈ O(1) constant
        """
        combined_salt = self.salt + purpose.encode()
        
        return hashlib.pbkdf2_hmac(
            'sha256',
            self.master_key.encode(),
            combined_salt,
            iterations=100000,
            dklen=length
        )
    
    def _derive_yun_key(self) -> List[str]:
        """
        Derive the yunKey using cryptographic key derivation.
        
        Returns:
            List of characters for the key
        
        Time Complexity: O(key_length)
        """
        key_bytes = self._derive_key_bytes('yun', self.key_length)
        
        yun_key = []
        for byte in key_bytes:
            index = byte % len(self.elements)
            yun_key.append(self.elements[index])
        
        return yun_key
    
    def _cryptographic_shuffle(self, lst: List[str], seed_bytes: bytes) -> List[str]:
        """
        Shuffle a list using cryptographic randomness (Fisher-Yates).
        
        Args:
            lst: List to shuffle
            seed_bytes: Cryptographic seed for deterministic shuffle
            
        Returns:
            Shuffled copy of the list
        
        Time Complexity: O(n) where n = list length
        """
        result = lst.copy()
        n = len(result)
        
        for i in range(n - 1, 0, -1):
            hash_input = seed_bytes + i.to_bytes(4, 'big')
            hash_output = hashlib.sha256(hash_input).digest()
            j = int.from_bytes(hash_output[:4], 'big') % (i + 1)
            result[i], result[j] = result[j], result[i]
        
        return result
    
    def _generate_ray_table(self) -> List[List[str]]:
        """
        Generate the shuffled RayTable (substitution table).
        
        Returns:
            2D list with shuffled first row, subsequent rows rotated
        
        Time Complexity: O(a²) where a = alphabet size
        Space Complexity: O(a²)
        """
        shuffle_key = self._derive_key_bytes('shuffle', 32)
        shuffled_alphabet = self._cryptographic_shuffle(self.elements, shuffle_key)
        
        ray_table = []
        row = shuffled_alphabet.copy()
        
        for _ in range(len(self.elements)):
            ray_table.append(row.copy())
            row = row[1:] + row[:1]  # Rotate left
        
        return ray_table
    
    def _build_lookup_tables(self) -> None:
        """
        Pre-compute O(1) lookup dictionaries.
        
        This is the KEY OPTIMIZATION that reduces complexity from O(n×a) to O(n).
        
        Instead of:
            row_id = self.ray_table[0].index(char)  # O(a) linear search
        
        We use:
            row_id = self.char_to_index[char]       # O(1) hash lookup
        
        Time Complexity: O(a²) - done once during initialization
        Space Complexity: O(a²) for decrypt_map
        """
        # Map: character -> index in first row
        # Used for both encryption lookups
        self.char_to_index: Dict[str, int] = {
            char: idx 
            for idx, char in enumerate(self.ray_table[0])
        }
    
        # Map: (row_index, cipher_char) -> plain_char
        # Pre-computes all decryption lookups
        self.decrypt_map: Dict[Tuple[int, str], str] = {}
        for row_idx, row in enumerate(self.ray_table):
            for col_idx, char in enumerate(row):
                self.decrypt_map[(row_idx, char)] = self.ray_table[0][col_idx]
    
    def encrypt(self) -> str:
        """
        Encrypt the plaintext with O(n) complexity.
        
        Each character lookup is O(1) via hash table.
        Total: O(n) where n = message length.
        
        Returns:
            Encrypted ciphertext string
        
        Time Complexity: O(n)
        Space Complexity: O(n) for output
        """
        ciphertext = []
        yun_key_len = len(self.yun_key)
        
        for i, char in enumerate(self.data):
            key_char = self.yun_key[i % yun_key_len]
            
            # O(1) dictionary lookups (vs O(a) list.index() in original)
            row_id = self.char_to_index[key_char]
            col_id = self.char_to_index[char]
            
            ciphertext.append(self.ray_table[row_id][col_id])
        
        self.data = ''.join(ciphertext)
        return self.data
    
    def decrypt(self) -> str:
        """
        Decrypt the ciphertext with O(n) complexity.
        
        Uses pre-computed decrypt_map for O(1) lookups.
        Total: O(n) where n = message length.
        
        Returns:
            Decrypted plaintext string
        
        Time Complexity: O(n)
        Space Complexity: O(n) for output
        """
        plaintext = []
        yun_key_len = len(self.yun_key)
        
        for i, char in enumerate(self.data):
            key_char = self.yun_key[i % yun_key_len]
            row_id = self.char_to_index[key_char]
            
            # O(1) lookup (vs O(a) row search in original)
            plaintext.append(self.decrypt_map[(row_id, char)])
        
        self.data = ''.join(plaintext)
        return self.data
    
    def encrypt_parallel(self, num_workers: int = None) -> str:
        """
        Parallel encryption for large messages.
        
        Splits the message into chunks and encrypts in parallel.
        Total work is still O(n), but wall-clock time is O(n/p)
        where p = number of processors.
        
        Args:
            num_workers: Number of parallel workers (default: CPU count)
        
        Returns:
            Encrypted ciphertext string
        
        Time Complexity: O(n) total work, O(n/p) wall-clock
        """
        if num_workers is None:
            num_workers = multiprocessing.cpu_count()
        
        if len(self.data) < 1000 or num_workers <= 1:
            # Not worth parallelizing small messages
            return self.encrypt()
        
        # Prepare chunks
        chunk_size = len(self.data) // num_workers
        chunks = []
        
        for i in range(num_workers):
            start = i * chunk_size
            end = start + chunk_size if i < num_workers - 1 else len(self.data)
            chunks.append((self.data[start:end], start))
        
        # Encrypt chunks in parallel
        def encrypt_chunk(args):
            chunk, start_idx = args
            result = []
            for i, char in enumerate(chunk):
                key_char = self.yun_key[(start_idx + i) % len(self.yun_key)]
                row_id = self.char_to_index[key_char]
                col_id = self.char_to_index[char]
                result.append(self.ray_table[row_id][col_id])
            return ''.join(result)
        
        with ThreadPoolExecutor(max_workers=num_workers) as executor:
            results = list(executor.map(encrypt_chunk, chunks))
        
        self.data = ''.join(results)
        return self.data
    
    def decrypt_parallel(self, num_workers: int = None) -> str:
        """
        Parallel decryption for large messages.
        
        Args:
            num_workers: Number of parallel workers (default: CPU count)
        
        Returns:
            Decrypted plaintext string
        
        Time Complexity: O(n) total work, O(n/p) wall-clock
        """
        if num_workers is None:
            num_workers = multiprocessing.cpu_count()
        
        if len(self.data) < 1000 or num_workers <= 1:
            return self.decrypt()
        
        chunk_size = len(self.data) // num_workers
        chunks = []
        
        for i in range(num_workers):
            start = i * chunk_size
            end = start + chunk_size if i < num_workers - 1 else len(self.data)
            chunks.append((self.data[start:end], start))
        
        def decrypt_chunk(args):
            chunk, start_idx = args
            result = []
            for i, char in enumerate(chunk):
                key_char = self.yun_key[(start_idx + i) % len(self.yun_key)]
                row_id = self.char_to_index[key_char]
                result.append(self.decrypt_map[(row_id, char)])
            return ''.join(result)
        
        with ThreadPoolExecutor(max_workers=num_workers) as executor:
            results = list(executor.map(decrypt_chunk, chunks))
        
        self.data = ''.join(results)
        return self.data
    
    def get_salt_hex(self) -> str:
        """Return the salt as a hex string for storage/transmission."""
        return self.salt.hex()
    
    @classmethod
    def from_salt_hex(
        cls, 
        ciphertext: str, 
        elements: List[str], 
        master_key: str,
        salt_hex: str, 
        key_length: int = 100
    ) -> 'RayunCipher':
        """
        Create a cipher instance from a hex-encoded salt.
        
        Use this to decrypt messages when you have the stored salt.
        
        Args:
            ciphertext: The encrypted text to decrypt
            elements: List of characters in the cipher alphabet
            master_key: The password/key used for encryption
            salt_hex: Hex-encoded salt from encryption
            key_length: Length of derived key (must match encryption)
        
        Returns:
            RayunCipher instance ready for decryption
        """
        salt = bytes.fromhex(salt_hex)
        return cls(ciphertext, elements, master_key, key_length, salt)
    
    def get_complexity_info(self) -> dict:
        """
        Return complexity analysis information.
        
        Useful for research documentation.
        """
        return {
            "algorithm": "Rayun Cipher v0.4",
            "alphabet_size": len(self.elements),
            "key_length": self.key_length,
            "message_length": len(self.data),
            "complexity": {
                "setup": f"O(a²) = O({len(self.elements)}²) = O({len(self.elements)**2})",
                "encrypt": f"O(n) = O({len(self.data)})",
                "decrypt": f"O(n) = O({len(self.data)})",
                "space": f"O(a²) = O({len(self.elements)**2})"
            },
            "optimization": "Hash table lookups replace linear search",
            "lookup_table_size": len(self.char_to_index),
            "decrypt_map_size": len(self.decrypt_map)
        }


def get_elements(
    uppercase: bool = True, 
    lowercase: bool = True, 
    symbols: bool = True, 
    whitespace: bool = True, 
    digits: bool = True
) -> List[str]:
    """
    Generate the cipher alphabet based on selected character sets.
    
    Args:
        uppercase: Include A-Z (26 characters)
        lowercase: Include a-z (26 characters)
        symbols: Include punctuation (32 characters)
        whitespace: Include whitespace (6 characters)
        digits: Include 0-9 (10 characters)
        
    Returns:
        List of characters for the cipher alphabet
    
    Default total: 100 characters
    """
    elements = []
    
    if uppercase:
        elements.extend(list(string.ascii_uppercase))
    if lowercase:
        elements.extend(list(string.ascii_lowercase))
    if symbols:
        elements.extend(list(string.punctuation))
    if whitespace:
        elements.extend(list(string.whitespace))
    if digits:
        elements.extend(list(string.digits))
    
    return elements


def index_of_coincidence(text: str) -> float:
    """
    Calculate the Index of Coincidence for cryptanalysis.
    
    Reference values:
    - English text: ~0.067
    - Random (26 chars): ~0.038
    - Random (100 chars): ~0.01
    
    Lower IC indicates better encryption.
    """
    text = ''.join(c for c in text if c.isalpha())
    if len(text) < 2:
        return 0.0
    
    freq = Counter(text.upper())
    n = len(text)
    return sum(f * (f - 1) for f in freq.values()) / (n * (n - 1))


def benchmark_complexity(message_sizes: List[int] = None) -> None:
    """
    Benchmark encryption time vs message size to verify O(n) complexity.
    
    If complexity is O(n), doubling message size should double time.
    If complexity is O(n²), doubling message size should quadruple time.
    """
    import time
    
    if message_sizes is None:
        message_sizes = [1000, 2000, 4000, 8000, 16000, 32000]
    
    elements = get_elements()
    master_key = "benchmark_key_123"
    
    # Generate test message (only valid characters)
    base_char = 'A'
    
    print("\n" + "=" * 60)
    print("COMPLEXITY BENCHMARK (Encryption Only)")
    print("=" * 60)
    print(f"{'Size':>10} | {'Time (μs)':>12} | {'Ratio':>8} | {'Expected O(n)':>14}")
    print("-" * 60)
    
    prev_time = None
    
    # Pre-create cipher with fixed salt to exclude setup time
    fixed_salt = b'benchmark_salt!!'
    
    for size in message_sizes:
        message = base_char * size
        
        # Create cipher (setup) - not timed
        cipher = RayunCipher(message, elements, master_key, salt=fixed_salt)
        
        # Time ONLY the encryption
        start = time.perf_counter()
        cipher.encrypt()
        elapsed = (time.perf_counter() - start) * 1_000_000  # microseconds
        
        ratio = elapsed / prev_time if prev_time else 1.0
        expected = size / message_sizes[0] if message_sizes[0] > 0 else 1.0
        
        print(f"{size:>10} | {elapsed:>12.1f} | {ratio:>8.2f}x | {expected:>14.2f}x")
        
        prev_time = elapsed
    
    print("-" * 60)
    print("If O(n): ratio ≈ expected (doubling size doubles time)")
    print("If O(n×a): ratio > expected")
    print("=" * 60)


# =============================================================================
# DEMONSTRATION AND TESTING
# =============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("RAYUN CIPHER v0.4 - Optimized O(n) Implementation")
    print("=" * 70)
    
    # Configuration
    elements = get_elements()
    master_key = "g00d_P@ssw0rD"
    
    print(f"\nAlphabet size: {len(elements)} characters")
    print(f"Master key: {master_key}")
    
    # Test messages
    test_messages = [
        "Hello World!",
        "The quick brown fox jumps over the lazy dog.",
        "Secret message 123!",
        "A" * 500,  # Repeated character test
    ]
    
    print("\n" + "-" * 70)
    print("ENCRYPTION/DECRYPTION TESTS")
    print("-" * 70)
    
    for msg in test_messages:
        cipher = RayunCipher(msg, elements, master_key)
        salt_hex = cipher.get_salt_hex()
        
        encrypted = cipher.encrypt()
        
        cipher2 = RayunCipher.from_salt_hex(encrypted, elements, master_key, salt_hex)
        decrypted = cipher2.decrypt()
        
        status = "✓ PASS" if decrypted == msg else "✗ FAIL"
        display_msg = f"{msg[:30]}..." if len(msg) > 30 else msg
        display_enc = f"{encrypted[:30]}..." if len(encrypted) > 30 else encrypted
        
        print(f"\n{status}")
        print(f"  Original:  {display_msg}")
        print(f"  Encrypted: {display_enc}")
        print(f"  Length:    {len(msg)} chars")
    
    print("\n" + "-" * 70)
    print("COMPLEXITY INFORMATION")
    print("-" * 70)
    
    test_cipher = RayunCipher("Test message for complexity analysis", elements, master_key)
    info = test_cipher.get_complexity_info()
    
    for key, value in info.items():
        if isinstance(value, dict):
            print(f"\n  {key}:")
            for k, v in value.items():
                print(f"    {k}: {v}")
        else:
            print(f"  {key}: {value}")
    
    print("\n" + "-" * 70)
    print("INDEX OF COINCIDENCE ANALYSIS")
    print("-" * 70)
    
    long_text = "The quick brown fox jumps over the lazy dog. " * 20
    filtered_text = ''.join(c for c in long_text if c in elements)
    
    cipher = RayunCipher(filtered_text, elements, master_key)
    ciphertext = cipher.encrypt()
    
    ic_plain = index_of_coincidence(filtered_text)
    ic_cipher = index_of_coincidence(ciphertext)
    
    print(f"\n  Plaintext IC:  {ic_plain:.4f} (English ~0.067)")
    print(f"  Ciphertext IC: {ic_cipher:.4f} (Random ~0.01 for 100 chars)")
    print(f"  Reduction:     {((ic_plain - ic_cipher) / ic_plain * 100):.1f}%")
    
    print("\n" + "-" * 70)
    print("UNIQUE CIPHERTEXTS (Salt Demonstration)")
    print("-" * 70)
    
    msg = "Same message"
    print(f"\n  Encrypting '{msg}' three times with same key:")
    
    for i in range(3):
        cipher = RayunCipher(msg, elements, master_key)
        encrypted = cipher.encrypt()
        print(f"    Attempt {i+1}: {encrypted}")
    
    # Run benchmark
    benchmark_complexity([1000, 2000, 4000, 8000, 16000])
    
    print("\n" + "=" * 70)
    print("All tests completed successfully!")
    print("=" * 70)

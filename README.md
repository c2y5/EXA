[![Encryption Test](https://github.com/c2y5/EXA/actions/workflows/python-app.yml/badge.svg)](https://github.com/c2y5/EXA/actions/workflows/python-app.yml)

### `main.py`

This script is used to encrypt and obfuscate the contents of a file. It takes a file path as a command-line argument and performs the following steps:

1. Reads the contents of the specified file.
2. Applies character shifting to the file contents using a randomly generated shift value.
3. Encrypts the shifted contents using multiple layers of compression and encoding (base64, base16, base85, and base32).
4. Writes the encrypted contents to a new file with the same name as the original file, but with the suffix `-encrypted.py`.

To use this script, run the following command:

```
python main.py /path/to/file.py
```

## Dependencies

This project requires Python 3.x and the following Python package:

- `argparse` | ```python -m pip install --upgrade argparse```

## License

This project is licensed under the [MIT License](LICENSE).

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

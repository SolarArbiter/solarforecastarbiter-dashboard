class SigningError(Exception):
    """Exception raised when PGP signing fails"""
    pass  # pragma: no cover


def sign_doc(doc, key_id, passphrase_file):
    """
    Signs the document with a OpenGPG.

    Parameters
    ----------
    doc : bytes
        Message to clear-sign with OpenGPG
    key_id : str
        The key to use for signing
    passphrase_file : path
        Path to a file with the passphrase for the PGP
        key as the first line

    Returns
    -------
    signature : bytes
        The ASCII armored signature of the document.

    Raises
    ------
    SigningError
        If the document could not be signed for any reason
    """
    try:
        import gpg
        from gpg import gpgme
    except ImportError:
        raise SigningError('Could not import gpg')
    with gpg.Context(
            armor=True,
            pinentry_mode=gpgme.GPGME_PINENTRY_MODE_LOOPBACK
    ) as c:
        try:
            key = list(c.keylist(key_id))[0]
        except IndexError:
            raise SigningError(
                f'No key found in keyring with ID: {key_id}')
        c.signers = [key]
        c.set_passphrase_cb(
            lambda *args: open(passphrase_file, 'rb').readline())
        try:
            signed_body, _ = c.sign(doc)
        except gpg.errors.GPGMEError as e:
            raise SigningError(f'Internal GPGME error: {str(e)}')
        except FileNotFoundError:
            raise SigningError('No GPG password file found')

    return signed_body

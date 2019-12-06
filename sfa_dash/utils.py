class SigningError(Exception):
    """Exception raised when PGP signing fails"""
    pass  # pragma: no cover


def sign_report(body, key_id, passphrase_file):
    """
    Signs the body string with a OpenGPG.

    Parameters
    ----------
    body : str
        Body or message to clear-sign with OpenGPG
    key_id : str
        The key to use for signing
    passphrase_file : path
        Path to a file with the passphrase for the PGP
        key as the first line

    Returns
    -------
    signed_body : str
        The body with the clear-sign signature.
        The BEGIN PGP header will be placed in a hidden div
        and the PGP signature will be visible at the end.

    Raises
    ------
    SigningError
        If the body could not be signed for any reason
    """
    try:
        import gpg
        from gpg import gpgme
    except ImportError:
        raise SigningError('Could not import gpg')
    pre_sign_body = '</div>\n' + body + '\n<pre>'
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
            signed_body, _ = c.sign(pre_sign_body.encode(),
                                    mode=gpg.constants.sig.mode.CLEAR)
        except gpg.errors.GPGMEError as e:
            raise SigningError(f'Internal GPGME error: {str(e)}')
        except FileNotFoundError:
            raise SigningError('No GPG password file found')

    out = '<div hidden>\n' + signed_body.decode() + '</pre>'
    return out

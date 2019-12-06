import re
import subprocess


import pytest


from sfa_dash import utils


def test_sign_report_no_gpg(mocker):
    mocker.patch.dict('sys.modules', {'gpg': None})
    inp = 'TEST BODY'
    with pytest.raises(utils.SigningError) as e:
        utils.sign_report(inp, 'key', 'pw')
    assert 'Could not import gpg' in e.value.args[0]


def test_sign_report_no_keys(mocker, tmpdir, monkeypatch):
    pytest.importorskip('gpg')
    monkeypatch.setenv('GNUPGHOME', str(tmpdir))
    inp = 'thebody'
    with pytest.raises(utils.SigningError) as e:
        utils.sign_report(inp, 'key', 'pw')
    assert 'No key found in keyring' in e.value.args[0]


def test_sign_report_invalid_key_id(mocker, tmp_path, monkeypatch):
    pytest.importorskip('gpg')
    tmp_path.chmod(0o700)
    monkeypatch.setenv('GNUPGHOME', str(tmp_path))
    subprocess.run(
            ['gpg', '--yes', '--passphrase', '', '--batch',
             '--quick-generate-key', '--pinentry-mode', 'loopback',
             "'TEST SFA <testing@solarforecastarbiter.org'"],
            check=True, capture_output=True
    )
    inp = 'thebody'
    with pytest.raises(utils.SigningError) as e:
        utils.sign_report(inp, 'key', '')
    assert 'No key found in keyring' in e.value.args[0]


def test_sign_report_no_pw_needed(mocker, tmp_path, monkeypatch):
    pytest.importorskip('gpg')
    tmp_path.chmod(0o700)
    monkeypatch.setenv('GNUPGHOME', str(tmp_path))
    key_create = subprocess.run(
            ['gpg', '--yes', '--passphrase', '', '--batch',
             '--quick-generate-key', '--pinentry-mode', 'loopback',
             "'TEST SFA <testing@solarforecastarbiter.org'"],
            check=True, capture_output=True
    )
    key = re.match('(?<=key ).*(?= marked)', key_create.stderr.decode())
    inp = 'thebody'
    out = utils.sign_report(inp, key, '')
    assert out.startswith('<div hidden>\n-----BEGIN PGP SIGNED MESSAGE-----')
    assert out.endswith('-----END PGP SIGNATURE-----\n')
    assert inp in out


def test_sign_report(mocker, tmp_path, monkeypatch):
    pytest.importorskip('gpg')
    tmp_path.chmod(0o700)
    monkeypatch.setenv('GNUPGHOME', str(tmp_path))
    passwd = b'jaljlj032904u2ojhsdf!@#43ljsdfa jsladf'
    with open(tmp_path / 'passwd', 'wb') as f:
        f.write(passwd)
    key_create = subprocess.run(
            ['gpg', '--yes', '--passphrase', passwd, '--batch',
             '--quick-generate-key', '--pinentry-mode', 'loopback',
             "'TEST SFA <testing@solarforecastarbiter.org'"],
            check=True, capture_output=True
    )
    key = re.match('(?<=key ).*(?= marked)', key_create.stderr.decode())
    inp = 'thebody'
    out = utils.sign_report(inp, key, tmp_path / 'passwd')
    assert out.startswith('<div hidden>\n-----BEGIN PGP SIGNED MESSAGE-----')
    assert out.endswith('-----END PGP SIGNATURE-----\n')
    assert inp in out


@pytest.mark.parametrize('path,msg', [('passwd', 'Internal GPGME'),
                                      ('dne', 'No GPG password')])
def test_sign_report_wrong_pw(mocker, tmp_path, monkeypatch, path, msg):
    pytest.importorskip('gpg')
    tmp_path.chmod(0o700)
    monkeypatch.setenv('GNUPGHOME', str(tmp_path))
    passwd = b'jaljlj032904u2ojhsdf!@#43ljsdfa jsladf'
    with open(tmp_path / 'passwd', 'wb') as f:
        f.write(b'wrong')
    key_create = subprocess.run(
            ['gpg', '--yes', '--passphrase', passwd, '--batch',
             '--quick-generate-key', '--pinentry-mode', 'loopback',
             "'TEST SFA <testing@solarforecastarbiter.org'"],
            check=True, capture_output=True
    )
    key = re.match('(?<=key ).*(?= marked)', key_create.stderr.decode())
    inp = 'thebody'
    with pytest.raises(utils.SigningError) as e:
        utils.sign_report(inp, key, tmp_path / path)
    assert msg in e.value.args[0]

import unittest
import subprocess
from time import sleep
from requests import get
from os.path import exists


def curl(url, self_signed=False):
    """Perform a request with curl"""
    print(f"curl: GET {url}")
    opts = [] if not self_signed else ["--cacert", "certificate.pem"]
    subprocess.Popen(["curl", url, *opts],
                     stdout=subprocess.DEVNULL,
                     stderr=subprocess.DEVNULL).wait()


def bpf_harness(action):
    """Spawn a ssl-snitch instance, execute the `action` and report results"""
    print("\nSpawning a new BPF instance...", end="")
    cmd = ["bpftrace", "ssl-snitch.bt"]
    bpf = subprocess.Popen(cmd, stdin=None, stdout=subprocess.PIPE)
    sleep(10)  # wait for ssl-snitch to start
    action()
    sleep(1)

    bpf.kill()
    bpf.wait()
    stdout = bpf.stdout.read().decode("utf-8")
    bpf.stdout.close()
    print("-" * 5)
    print(stdout)
    print("-" * 5)
    return stdout


class SSLSnitchTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not (exists("certificate.pem") or exists("key.pem")):
            raise ValueError("Missing localhost certificate")

    def test_cloudflare(self):
        """it detects a request from a Python script"""
        res = bpf_harness(lambda: get("https://1.1.1.1:443"))
        self.assertIn("python", res)
        self.assertIn("1.1.1.1", res)

    def test_curl_google(self):
        """it detects a request from curl"""
        res = bpf_harness(lambda: curl("https://www.google.com"))
        self.assertIn("curl", res)
        self.assertIn("443", res)

    def test_curl_http(self):
        """it does not detect HTTP requests"""
        res = bpf_harness(lambda: get("http://1.1.1.1"))
        self.assertNotIn("python", res)
        self.assertNotIn("1.1.1.1", res)

    def test_custom_port(self):
        """it detects requests on custom ports"""
        server = subprocess.Popen(["python3", "sslserver.py", "4433"],
                                  stdin=subprocess.DEVNULL,
                                  stdout=subprocess.DEVNULL)
        res = bpf_harness(lambda: curl("https://0.0.0.0:4433",
                                       self_signed=True))
        server.kill()
        server.wait()
        self.assertIn("curl", res)
        self.assertIn("4433", res)
        self.assertIn("python", res)

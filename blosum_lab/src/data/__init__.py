import os
import certifi

ca_path = certifi.where()
os.environ['SSL_CERT_FILE'] = ca_path
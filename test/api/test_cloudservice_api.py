import os
import unittest

from spaceone.core.unittest.runner import RichTestRunner
from spaceone.tester import TestCase, print_json

KUBECONFIG = os.environ.get('KUBECONFIG', None)
CLUSTER_NAME = os.environ.get('CLUSTER_NAME', None)
TOKEN = os.environ.get('TOKEN', None)
SERVER = os.environ.get('SERVER', None)
CERTIFICATE_AUTHORITY_DATA = os.environ.get('CERTIFICATE_AUTHORITY_DATA', None)


if CLUSTER_NAME is None or TOKEN is None or SERVER is None or CERTIFICATE_AUTHORITY_DATA is None:
    print("""
        ##################################################
        # ERROR 
        #
        # Configure your Credentials first

        ##################################################
        export CLUSTER_NAME="Your Cluster Name"
        export TOKEN="Your Service Account Token"
        export SERVER="Your Kube API Server Endpoint"
        export CERTIFICATE_AUTHORITY_DATA="Your kube cluster Certification"
    """)
    exit

'''
def _get_credentials():
    with open(KUBECONFIG) as yaml_file:
        dict_file = yaml.load(yaml_file, Loader=yaml.FullLoader)
    print(f'kubeconfig => {dict_file}')
    return dict_file
'''


class TestCollector(TestCase):

    def test_init(self):
        print(f'=================== start test init! ==========================')
        v_info = self.inventory.Collector.init({'options': {}})
        print_json(v_info)

    def test_verify(self):
        print(f'=================== start test verify! ==========================')
        options = {}
        v_info = self.inventory.Collector.verify({'options': options, 'secret_data': {}})
        print_json(v_info)

    def test_collect(self):
        '''
        Options can be selected
        options = {"cloud_service_types": ["WorkLoad"]}
            }
        '''
        print(f'======================= start test collect! ===========================')
        options = {
        }
        filter = {}
        secret_data = {
            "cluster_name": CLUSTER_NAME,
            "certificate_authority_data": CERTIFICATE_AUTHORITY_DATA,
            "server": SERVER,
            "token": TOKEN
        }

        print(f'secret_data => {secret_data}')
        resource_stream = self.inventory.Collector.collect({'options': options, 'secret_data': secret_data,
                                                            'filter': filter})

        for res in resource_stream:
            print_json(res)


if __name__ == "__main__":
    unittest.main(testRunner=RichTestRunner)

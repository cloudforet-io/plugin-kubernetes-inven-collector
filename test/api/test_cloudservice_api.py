import os
import unittest
import yaml

from spaceone.core.unittest.runner import RichTestRunner
from spaceone.tester import TestCase, print_json

KUBECONFIG = os.environ.get('KUBECONFIG', None)


if KUBECONFIG is None:
    print("""
        ##################################################
        # ERROR 
        #
        # Configure your Kubeconfig first

        ##################################################
        export KUBECONFIG="<PATH>" 
    """)
    exit


def _get_credentials():
    with open(KUBECONFIG) as yaml_file:
        dict_file = yaml.load(yaml_file, Loader=yaml.FullLoader)
    print(f'kubeconfig => {dict_file}')
    return dict_file


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
        options = {
        }
        filter = {}
        secret_data = _get_credentials()
        print(f'======================= test client loader ===========================')
        print(f'secret_data => {secret_data}')
        resource_stream = self.inventory.Collector.collect({'options': options, 'secret_data': secret_data,
                                                            'filter': filter})

        for res in resource_stream:
            print_json(res)


if __name__ == "__main__":
    unittest.main(testRunner=RichTestRunner)

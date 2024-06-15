import yaml
from typing import Dict, Any, List, Union
from collections import OrderedDict
import os

def read_yaml(file_path: str) -> Dict[str, Any]:
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def write_yaml(file_path: str, data: Dict[str, Any]) -> None:
    with open(file_path, 'w') as file:
        yaml.dump(data, file, Dumper=OrderedDumper, default_flow_style=False)

class OrderedDumper(yaml.SafeDumper):
    pass

def _dict_representer(dumper, data):
    return dumper.represent_dict(data.items())

OrderedDumper.add_representer(OrderedDict, _dict_representer)

def build_artifact(data: Dict[str, Any], path: str = '') -> OrderedDict:
    artifact = OrderedDict([
        ('image', data['image']),
        ('context', path.rstrip('/')),
        ('docker', OrderedDict([
            ('dockerfile', 'Dockerfile')
        ]))
    ])
    if 'sync' in data:
        artifact['sync'] = OrderedDict([
            ('manual', [{'dest': '.', 'src': sync} for sync in data['sync']])
        ])
    return artifact

def generate_artifacts(repo: Union[Dict[str, Any], List[Dict[str, Any]]], path: str = '') -> List[OrderedDict]:
    artifacts = []
    if isinstance(repo, dict):
        if 'skaffold-artifact' in repo:
            artifacts.append(build_artifact(repo['skaffold-artifact'], os.path.join(path, repo['name'])))
        for key, value in repo.items():
            if isinstance(value, (dict, list)):
                artifacts.extend(generate_artifacts(value, os.path.join(path, key)))
    elif isinstance(repo, list):
        for item in repo:
            if isinstance(item, dict):
                artifacts.extend(generate_artifacts(item, path))
    return artifacts

def find_manifests(repo: Union[Dict[str, Any], List[Dict[str, Any]]], path: str = './') -> List[str]:
    manifests = []
    if isinstance(repo, dict):
        if 'skaffold-manifests' in repo:
            manifests.extend(os.path.join(path, repo['name'], manifest) for manifest in repo['skaffold-manifests'])
        for key, value in repo.items():
            if isinstance(value, (dict, list)):
                manifests.extend(find_manifests(value, os.path.join(path, key)))
    elif isinstance(repo, list):
        for item in repo:
            if isinstance(item, dict):
                manifests.extend(find_manifests(item, path))
    return manifests

def generate_skaffold_content(repos: Dict[str, Any]) -> Dict[str, Any]:
    return OrderedDict([
        ('apiVersion', 'skaffold/v4beta3'),
        ('kind', 'Config'),
        ('manifests', OrderedDict([
            ('rawYaml', find_manifests(repos))
        ])),
        ('build', OrderedDict([
            ('local', OrderedDict([
                ('push', False)
            ])),
            ('artifacts', generate_artifacts(repos))
        ]))
    ])

def main() -> None:
    base_dir = os.path.dirname(__file__)
    repos = read_yaml(os.path.join(base_dir, '..', 'repositories.yaml'))
    skaffold_content = generate_skaffold_content(repos)
    write_yaml(os.path.join(base_dir, '..', 'skaffold.yaml'), skaffold_content)

if __name__ == "__main__":
    main()

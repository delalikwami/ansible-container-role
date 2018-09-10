import os
import pytest
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_hosts_file(host):
    f = host.file('/etc/hosts')

    assert f.exists
    assert f.user == 'root'
    assert f.group == 'root'


@pytest.mark.parametrize('packages', ['docker-ce', 'python-pip', 'ansible'])
def test_packages(host, packages):
    package = host.package(packages)

    assert package.is_installed


@pytest.mark.parametrize('svcs', ['docker'])
def test_services(host, svcs):
    service = host.service(svcs)

    assert service.is_running
    assert service.is_enabled


@pytest.mark.parametrize('grps', ['docker'])
def test_group_existence(host, grps):
    group = host.group(grps)

    assert group.exists


@pytest.mark.parametrize('usr', ['vagrant'])
@pytest.mark.parametrize('grp', ['docker'])
def test_user_in_group(host, usr, grp):
    user = host.user(usr)
    groups = user.groups

    assert grp in groups


def test_virtual_environment(host):
    venv = host.file('/home/vagrant/venv/bin/activate')

    assert venv.exists


@pytest.mark.parametrize('pip_packages', ['docker', 'ruamel.yaml'])
def test_pip_packages(host, pip_packages):
    pippackage = host.pip_package.get_packages(pip_path='~/venv/bin/pip')

    assert pip_packages in pippackage


def test_ansible_container(host):
    host.run("/home/vagrant/venv/bin/activate")
    ac_output = host.check_output(
            "/home/vagrant/venv/bin/ansible-container version")

    assert "0.9." in ac_output

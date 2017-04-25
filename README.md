# cannonfodder

## installation on CentOS 7

```
sudo yum groupinstall -y "Development Tools"
sudo yum install -y libyaml-devel python-virtualenvwrapper git

mkvirtualenv cannonfodder
git clone https://github.com/tourunen/cannonfodder
pip install -r cannonfodder/requirements
```


# cannonfodder

## installation on CentOS 7

``` bash
sudo yum groupinstall -y "Development Tools"
sudo yum install -y libyaml-devel python-virtualenvwrapper git

mkvirtualenv cannonfodder
cd
mkdir git
cd git
git clone https://github.com/tourunen/cannonfodder
pip install -r cannonfodder/requirements.txt
ln -s ~/git/cannonfodder/cf.py ~/bin/cf
```

## example usage

``` bash

# activate virtualenv
workon cannonfodder

# add ten users
cf add -n 10

# add users to htpasswd.txt
cf update -f htpasswd.txt

# process the example template
cp ~/git/cannonfodder/example.j2 .
cf process -t example.j2 -s example.txt

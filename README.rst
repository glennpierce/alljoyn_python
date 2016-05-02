Python bindings for AllJoyn

.. image:: https://github.com/glennpierce/alljoyn_python/raw/master/images/BeetsAllPlayPlugin.png?raw=true

Installation
============

First you need to install AllJoyn library.  For the Debian Apt based distros (eg Raspbian on the RaspberyPI) install dependant packages using Debian package manager ::

    apt-get install build-essential maven scons git curl openssl libssl-dev libjson0 libjson0-dev libcap-dev
    
Setup compile environment download AllJoyn code and compile it::
    
    mkdir ~/bin
    echo "export PATH=$PATH:~/bin" >> ~/.bashrc
    curl https://storage.googleapis.com/git-repo-downloads/repo > ~/bin/repo
    chmod a+x ~/bin/repo
    source ~/.bashrc
    mkdir -p ~/WORKING_DIRECTORY/alljoyn
    cd ~/WORKING_DIRECTORY/alljoyn
    git config --global user.name "Mark Gillespie"
    git config --global user.email "mark.gillespie@gmail.com"
    repo init -u https://git.allseenalliance.org/gerrit/devtools/manifest
    repo sync
    export AJ_ROOT=$(pwd)
    sudo ln -s /usr/bin/g++ /usr/bin/arm-angstrom-linux-gnueabi-g++
    sudo ln -s /usr/bin/gcc /usr/bin/arm-angstrom-linux-gnueabi-gcc
    cd ~/WORKING_DIRECTORY/alljoyn/core/alljoyn
    scons OS=linux CPU=arm WS=off OE_BASE=/usr BR=on BINDINGS=c,cpp CROSS_COMPILE=/usr/bin/arm-linux-gnueabihf-
    sudo ln -sf ~/WORKING_DIRECTORY/alljoyn/core/alljoyn/build/linux/arm/debug/dist/cpp/lib/liballjoyn.so /lib/arm-linux-gnueabihf/liballjoyn.so
    cd ~/WORKING_DIRECTORY/alljoyn/core/alljoyn/build/linux/arm/debug/dist/cpp/bin
    ldd alljoyn-daemon #daemon not available in latest versions of alljoyn, use BR=on with scons for embedded daemon
    
Now test the AllJoyn Daemon::

    cd ~/WORKING_DIRECTORY/alljoyn/core/alljoyn/build/linux/arm/debug/dist/cpp/bin
    alljoyn-daemon --version

AllJoyn Message Bus Daemon version: v0.00.01
Copyright AllSeen Alliance.

Build: AllJoyn Library v0.00.01 (Built Fri Apr 15 18:12:18 UTC 2016 by root - Git: alljoyn branch: '(no branch)' tag: 'v15.09a' (+350 changes) commit ref: e289adde2cd7289afbbc09a64a4620d5679d2bdc)


Now you have to download and install my AllJoyn bindings ::

    cd ~/WORKING_DIRECTORY
    git clone https://github.com/glennpierce/alljoyn_python
    cd alljoyn_python/
    python ./setup.py install

    The are some samples that can be used to test your AllPlay system.
    
    Try running
    cd alljoyn_python/
    alljoyn-daemon &
    ./samples/AllPlay/AllPlayAboutClient.py

    This should return information for the Allplay speakers we can see on the network.


 
Beets plugin ::

    Before running any of the Python AllJoyn code the alljoyn-daemon must be running as
    the internal AllJoyn router is not exported in the c api so I could not wrap it.

    Within the samples is a beets plugin ./samples/beetsplug/
    http://beets.io/ is a Python music indexer / metadata system. 
    My plugin sets up an angular web page to play music through the allplay system.
    
    To run this plugin
    Add the plugin directory to the Python path
    ie  export PYTHONPATH="/opt/alljoyn_python/samples/"

    Edit the beets config file

    vim ~/.config/beets/config.yaml

    Add the following

    directory: ~/Music
    library: ~/musiclibrary.blb

    plugins: allplay

    allplay:
        host: 0.0.0.0


    Once the config is save you have to index your music
   
    For importing read https://beets.readthedocs.org/en/v1.3.17/guides/main.html

    I used
    beet import -A /media/External/Music

    Once index simply run my plugin

    beet allplay --debug

    This will start a webserver you can access on port 8337


Todo
============

Port unit tests from c bindings

Port build to scons for integration into upstream alljoyn

Add a generic Set and Get to MsgArg that automatically converts the DBus signatures to Python types

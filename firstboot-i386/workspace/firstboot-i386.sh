#!/bin/bash

rpmbuild --define '_topdir '`pwd` -bb SPECS/firstboot.spec
